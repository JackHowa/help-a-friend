#!/usr/bin/env python3
"""
Pre-call recon checker for post-hack search recovery engagements.

Automates the parts of the recon checklist that don't require a browser
login (Search Console) or violate a search engine's scripted-query terms
(site: search). Produces a markdown report you can read before the call
and hand to the org afterward.

Zero third-party dependencies (stdlib only) so it runs anywhere with
python3, no venv/pip setup needed for a one-hour-call turnaround.

Usage:
    python3 recon_check.py seacc.org --output seacc-recon-report.md
    GOOGLE_SAFE_BROWSING_API_KEY=xxx python3 recon_check.py seacc.org
"""

import argparse
import difflib
import json
import os
import re
import socket
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

GOOGLEBOT_UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
NORMAL_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
TIMEOUT = 15
MAX_SITEMAPS = 5
MAX_SITEMAP_URLS_SHOWN = 20


def load_dotenv(path=None):
    """Minimal .env loader (stdlib-only): sets os.environ for KEY=VALUE
    lines that aren't already set in the environment. Does not override
    existing env vars, so `export FOO=bar` still wins over a .env file."""
    path = path or os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value

# Query-string keys and inline patterns that vary per-request even with no
# real content change (WP nonces, cache-busters, timestamps). Stripped
# before diffing so the cloaking check isn't drowned in noise.
DYNAMIC_PATTERNS = [
    re.compile(r"nonce=[\w-]+", re.I),
    re.compile(r"\bver=[\d.]+", re.I),
    re.compile(r"[?&]_=\d+"),
    re.compile(r"<!--.*?-->", re.S),
    re.compile(r"csrf[-_]?token=[\w-]+", re.I),
]


def fetch(url, user_agent, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.status, body.decode(charset, errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return None, str(e)


def normalize_html(html):
    out = html
    for pattern in DYNAMIC_PATTERNS:
        out = pattern.sub("", out)
    out = re.sub(r"\s+", " ", out).strip()
    return out


def load_wordlist(path):
    terms = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                terms.append(line.lower())
    return terms


def find_spam_terms(text, terms):
    lower = text.lower()
    return sorted({t for t in terms if t in lower})


def check_cloaking(domain, terms):
    url = f"https://{domain}/"
    gb_status, gb_html = fetch(url, GOOGLEBOT_UA)
    n_status, n_html = fetch(url, NORMAL_UA)

    result = {
        "url": url,
        "googlebot_status": gb_status,
        "normal_status": n_status,
    }

    if gb_status != 200 or n_status != 200:
        result["error"] = (
            f"Could not fetch cleanly (googlebot={gb_status}, normal={n_status})"
        )
        return result

    gb_terms = find_spam_terms(gb_html, terms)
    n_terms = find_spam_terms(n_html, terms)
    result["spam_terms_googlebot_only"] = sorted(set(gb_terms) - set(n_terms))
    result["spam_terms_normal_only"] = sorted(set(n_terms) - set(gb_terms))
    result["spam_terms_both"] = sorted(set(gb_terms) & set(n_terms))

    gb_norm = normalize_html(gb_html)
    n_norm = normalize_html(n_html)
    if gb_norm == n_norm:
        result["diff_ratio"] = 1.0
    else:
        matcher = difflib.SequenceMatcher(None, gb_norm, n_norm)
        result["diff_ratio"] = round(matcher.ratio(), 4)

    result["cloaking_suspected"] = bool(
        result["spam_terms_googlebot_only"] or result["diff_ratio"] < 0.85
    )
    return result


def check_robots_and_sitemaps(domain, terms):
    robots_url = f"https://{domain}/robots.txt"
    status, body = fetch(robots_url, NORMAL_UA)
    result = {"robots_url": robots_url, "status": status}
    if status != 200:
        result["error"] = f"robots.txt not reachable (status={status})"
        return result

    sitemap_urls = re.findall(r"(?im)^sitemap:\s*(\S+)", body)
    result["sitemap_urls_declared"] = sitemap_urls
    result["disallow_count"] = len(re.findall(r"(?im)^disallow:", body))

    sitemaps_checked = []
    for sm_url in sitemap_urls[:MAX_SITEMAPS]:
        sm_url = urljoin(robots_url, sm_url)
        sm_status, sm_body = fetch(sm_url, NORMAL_UA)
        entry = {"url": sm_url, "status": sm_status}
        if sm_status == 200:
            locs = re.findall(r"<loc>(.*?)</loc>", sm_body, re.S)
            entry["url_count"] = len(locs)
            flagged = []
            for loc in locs:
                path = urlparse(loc).path.lower()
                if any(t in path for t in terms):
                    flagged.append(loc)
            entry["flagged_urls"] = flagged[:MAX_SITEMAP_URLS_SHOWN]
            entry["flagged_url_count"] = len(flagged)
        sitemaps_checked.append(entry)
    result["sitemaps"] = sitemaps_checked
    return result


def check_safe_browsing(domain, api_key):
    if not api_key:
        return None
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    payload = {
        "client": {"clientId": "nonprofit-recovery-toolkit", "clientVersion": "1.0.0"},
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION",
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": f"https://{domain}/"},
                {"url": f"http://{domain}/"},
            ],
        },
    }
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {"flagged": bool(data.get("matches")), "raw": data}
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        return {"error": str(e)}


SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def check_security_headers(domain):
    url = f"https://{domain}/"
    req = urllib.request.Request(url, headers={"User-Agent": NORMAL_UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            headers = resp.headers
    except urllib.error.HTTPError as e:
        headers = e.headers
    except (urllib.error.URLError, OSError) as e:
        return {"error": str(e)}

    present = {h: headers.get(h) for h in SECURITY_HEADERS if headers.get(h)}
    missing = [h for h in SECURITY_HEADERS if not headers.get(h)]
    return {"present": present, "missing": missing}


def check_ssl_certificate(domain):
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=TIMEOUT) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
    except (ssl.SSLError, OSError, socket.timeout) as e:
        return {"error": str(e)}

    issuer = dict(x[0] for x in cert.get("issuer", []))
    return {
        "issuer": issuer.get("organizationName") or issuer.get("commonName") or "unknown",
        "not_before": cert.get("notBefore"),
        "not_after": cert.get("notAfter"),
    }


def check_dns(domain):
    result = {}
    try:
        result["a_records"] = sorted(
            {info[4][0] for info in socket.getaddrinfo(domain, None, socket.AF_INET)}
        )
    except OSError as e:
        result["a_records_error"] = str(e)

    for record_type, key in (("MX", "mx_records"), ("NS", "ns_records")):
        try:
            proc = subprocess.run(
                ["dig", "+short", record_type, domain],
                capture_output=True,
                timeout=TIMEOUT,
                text=True,
            )
            if proc.returncode == 0:
                result[key] = [line for line in proc.stdout.strip().splitlines() if line]
            else:
                result[f"{key}_error"] = proc.stderr.strip() or "dig returned a nonzero exit code"
        except FileNotFoundError:
            result[f"{key}_error"] = (
                "`dig` not found on this machine — install bind-utils/dnsutils "
                "(or run `dig MX/NS " + domain + "` manually) to enable this check"
            )
        except subprocess.TimeoutExpired:
            result[f"{key}_error"] = "dig timed out"
    return result


def check_wp_exposure(domain):
    base = f"https://{domain}"
    result = {}

    status, html = fetch(f"{base}/", NORMAL_UA)
    if status == 200:
        m = re.search(r'<meta name="generator" content="([^"]+)"', html, re.I)
        result["generator_tag"] = m.group(1) if m else None

    status, body = fetch(f"{base}/xmlrpc.php", NORMAL_UA)
    result["xmlrpc_status"] = status
    result["xmlrpc_exposed"] = status == 200 and "XML-RPC server accepts POST requests only" in body

    status, body = fetch(f"{base}/wp-json/wp/v2/users", NORMAL_UA)
    result["wp_json_users_status"] = status
    result["wp_json_users_exposed"] = False
    result["wp_json_usernames"] = []
    if status == 200:
        try:
            users = json.loads(body)
            if isinstance(users, list) and users:
                result["wp_json_users_exposed"] = True
                result["wp_json_usernames"] = [u.get("slug") for u in users][:10]
        except json.JSONDecodeError:
            pass

    status, _ = fetch(f"{base}/readme.html", NORMAL_UA)
    result["readme_html_status"] = status
    result["readme_html_exposed"] = status == 200

    return result


def render_report(domain, cloaking, robots, safe_browsing, security_headers, ssl_cert, dns, wp_exposure):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = []
    lines.append(f"# Recon report: {domain}")
    lines.append(f"_Generated {now}_\n")

    lines.append("## Cloaking check (Googlebot UA vs. normal UA)")
    if "error" in cloaking:
        lines.append(f"- ⚠️ {cloaking['error']}")
    else:
        verdict = "🚩 SUSPECTED" if cloaking["cloaking_suspected"] else "✅ clean"
        lines.append(f"- Verdict: **{verdict}**")
        lines.append(f"- Content similarity ratio: {cloaking['diff_ratio']}")
        if cloaking["spam_terms_googlebot_only"]:
            lines.append(
                f"- 🚩 Spam terms shown ONLY to Googlebot: {cloaking['spam_terms_googlebot_only']}"
            )
        if cloaking["spam_terms_normal_only"]:
            lines.append(
                f"- Spam terms shown ONLY to normal browser: {cloaking['spam_terms_normal_only']}"
            )
        if cloaking["spam_terms_both"]:
            lines.append(f"- Spam terms in both: {cloaking['spam_terms_both']}")
        if not (cloaking["spam_terms_googlebot_only"] or cloaking["spam_terms_normal_only"] or cloaking["spam_terms_both"]):
            lines.append("- No wordlist matches in either fetch.")
        lines.append(
            "- Note: this only catches UA-based cloaking. A hack that cloaks by "
            "checking the requester's IP against Google's published ranges "
            "won't show up here — that needs a fetch from a real Google IP, "
            "which this script can't do."
        )
    lines.append("")

    lines.append("## robots.txt / sitemap")
    if "error" in robots:
        lines.append(f"- ⚠️ {robots['error']}")
    else:
        lines.append(f"- Declared sitemaps: {robots['sitemap_urls_declared'] or 'none'}")
        lines.append(f"- Disallow rules: {robots['disallow_count']}")
        for sm in robots["sitemaps"]:
            if sm.get("status") != 200:
                lines.append(f"- ⚠️ {sm['url']} — unreachable (status={sm.get('status')})")
                continue
            lines.append(f"- {sm['url']}: {sm['url_count']} URLs")
            if sm["flagged_url_count"]:
                lines.append(
                    f"  - 🚩 {sm['flagged_url_count']} URL(s) matched spam wordlist, "
                    f"e.g. {sm['flagged_urls'][:5]}"
                )
    lines.append("")

    lines.append("## Safe Browsing status")
    if safe_browsing is None:
        lines.append(
            "- Not checked (no API key). Manually check: "
            f"https://transparencyreport.google.com/safe-browsing/search?url={domain}"
        )
    elif "error" in safe_browsing:
        lines.append(f"- ⚠️ API error: {safe_browsing['error']}")
    else:
        verdict = "🚩 FLAGGED" if safe_browsing["flagged"] else "✅ clean"
        lines.append(f"- Verdict: **{verdict}**")
    lines.append("")

    lines.append("## WordPress exposure")
    if "error" in wp_exposure:
        lines.append(f"- ⚠️ {wp_exposure['error']}")
    else:
        if wp_exposure.get("generator_tag"):
            lines.append(f"- WP version exposed via generator tag: `{wp_exposure['generator_tag']}`")
        else:
            lines.append("- No `generator` meta tag found (version not exposed that way)")
        flag = "🚩 exposed" if wp_exposure["xmlrpc_exposed"] else "✅ not exposed"
        lines.append(f"- xmlrpc.php: {flag} (status={wp_exposure['xmlrpc_status']})")
        flag = "🚩 exposed" if wp_exposure["wp_json_users_exposed"] else "✅ not exposed"
        lines.append(f"- wp-json user enumeration: {flag} (status={wp_exposure['wp_json_users_status']})")
        if wp_exposure["wp_json_usernames"]:
            lines.append(f"  - Usernames leaked: {wp_exposure['wp_json_usernames']}")
        flag = "🚩 reachable" if wp_exposure["readme_html_exposed"] else "✅ not reachable"
        lines.append(f"- readme.html: {flag} (status={wp_exposure['readme_html_status']})")
    lines.append("")

    lines.append("## Security headers")
    if "error" in security_headers:
        lines.append(f"- ⚠️ {security_headers['error']}")
    else:
        for header, value in security_headers["present"].items():
            lines.append(f"- ✅ {header}: `{value}`")
        for header in security_headers["missing"]:
            lines.append(f"- 🚩 missing: {header}")
    lines.append("")

    lines.append("## SSL certificate")
    if "error" in ssl_cert:
        lines.append(f"- ⚠️ {ssl_cert['error']}")
    else:
        lines.append(f"- Issuer: {ssl_cert['issuer']}")
        lines.append(f"- Valid: {ssl_cert['not_before']} → {ssl_cert['not_after']}")
        lines.append(
            "- Note: a normal renewal looks identical to a compromise-driven "
            "reissue here — cross-check the validity start date against the "
            "hack date and who currently controls the cert (org vs. host/CDN)."
        )
    lines.append("")

    lines.append("## DNS")
    if dns.get("a_records"):
        lines.append(f"- A records: {dns['a_records']}")
    elif "a_records_error" in dns:
        lines.append(f"- ⚠️ A record lookup failed: {dns['a_records_error']}")
    if "mx_records" in dns:
        lines.append(f"- MX records: {dns['mx_records'] or 'none'}")
    elif "mx_records_error" in dns:
        lines.append(f"- ⚠️ {dns['mx_records_error']}")
    if "ns_records" in dns:
        lines.append(f"- NS records: {dns['ns_records'] or 'none'}")
    elif "ns_records_error" in dns:
        lines.append(f"- ⚠️ {dns['ns_records_error']}")
    lines.append(
        "- Compare these against what the org/host expects — an unrecognized "
        "NS or MX entry can mean the hack extended to DNS/registrar level, "
        "not just the WordPress install."
    )
    lines.append("")

    lines.append("## Manual checks — do these before the call (script can't automate)")
    lines.append(f"- [ ] Incognito: `site:{domain}` — scan every indexed URL for junk terms/languages")
    lines.append(f"- [ ] Incognito: search the org's name, note where they actually rank")
    lines.append("- [ ] Google Search Console → Security Issues / Manual Actions (needs org login)")
    lines.append(f"- [ ] Wayback Machine around the hack date: https://web.archive.org/web/*/https://{domain}/")
    lines.append(f"- [ ] PageSpeed Insights: https://pagespeed.web.dev/analysis?url=https://{domain}")
    lines.append("- [ ] Free backlink checker (Ahrefs/Semrush free tier) for spammy inbound links")
    lines.append("")

    return "\n".join(lines)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("domain", help="Domain to check, e.g. seacc.org")
    parser.add_argument("--wordlist", default=os.path.join(os.path.dirname(__file__), "spam_terms.txt"))
    parser.add_argument("--output", help="Write report to this file instead of stdout")
    parser.add_argument(
        "--safe-browsing-key",
        default=os.environ.get("GOOGLE_SAFE_BROWSING_API_KEY"),
        help="Google Safe Browsing API key (or set GOOGLE_SAFE_BROWSING_API_KEY)",
    )
    args = parser.parse_args()

    domain = args.domain.replace("https://", "").replace("http://", "").strip("/")
    terms = load_wordlist(args.wordlist)

    print(f"Checking {domain} ...", file=sys.stderr)
    cloaking = check_cloaking(domain, terms)
    robots = check_robots_and_sitemaps(domain, terms)
    safe_browsing = check_safe_browsing(domain, args.safe_browsing_key)
    security_headers = check_security_headers(domain)
    ssl_cert = check_ssl_certificate(domain)
    dns = check_dns(domain)
    wp_exposure = check_wp_exposure(domain)

    report = render_report(
        domain, cloaking, robots, safe_browsing,
        security_headers, ssl_cert, dns, wp_exposure,
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
