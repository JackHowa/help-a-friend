---
sidebar_position: 2
---

# recon_check.py

Zero-dependency Python CLI (standard library only) that runs the
automatable parts of a pre-call recon checklist against a domain and
produces a markdown report.

## Usage

```bash
python3 recon_check.py their-domain.org --output findings/their-domain-recon-report.md
```

## Options

| Flag | Description |
|---|---|
| `domain` | Domain to check, e.g. `seacc.org` (positional, required) |
| `--wordlist PATH` | Spam-term wordlist for the cloaking/sitemap grep (defaults to `spam_terms.txt`) |
| `--output PATH` | Write the report to a file instead of stdout |
| `--safe-browsing-key KEY` | Google Safe Browsing API key (or set `GOOGLE_SAFE_BROWSING_API_KEY`) |
| `--pagespeed-key KEY` | Google PageSpeed Insights API key (or set `GOOGLE_PAGESPEED_API_KEY`) |
| `--pagespeed-strategy` | `mobile` (default) or `desktop` |

Both API keys are optional — see [API setup](./api-setup) for how to get
one, and what happens if you skip it (a manual-check link instead of a
failure).

## What it checks

- **Cloaking** — fetches the homepage as Googlebot and as a normal
  browser, diffs the content (after stripping nonces/timestamps/dynamic
  noise) and cross-checks for spam terms shown to only one user-agent.
- **robots.txt + sitemap** — fetches and scans declared sitemaps for
  injected/spammy URL patterns.
- **Safe Browsing** *(optional key)* — checks Google's malware/phishing
  blocklist directly via the API.
- **PageSpeed Insights** *(optional key)* — pulls real Lighthouse
  performance/accessibility/best-practices/SEO scores and Core Web Vitals
  metrics.
- **WordPress exposure** — `xmlrpc.php` reachability, REST API user
  enumeration (`/wp-json/wp/v2/users`), exposed version via
  `readme.html`/generator meta tag.
- **Security headers** — presence of CSP, HSTS, X-Frame-Options,
  X-Content-Type-Options.
- **SSL certificate** — issuer and validity window.
- **DNS** — A/MX/NS records (MX/NS shell out to the `dig` binary).
- **Subdomain discovery** — queries certificate transparency logs
  (crt.sh, free, no key) to find every subdomain ever issued a cert,
  flags ones not linked from the homepage and CNAMEs pointing at
  takeover-prone service patterns (GitHub Pages, Heroku, S3, etc.).

## What it does NOT automate

These need a browser or a login, so they stay manual — the report
includes a checklist reminder for each:

- Google Search Console → Security Issues / Manual Actions (needs the
  org's login)
- `site:domain.com` search in an incognito window (Google blocks
  scripted queries)
- Wayback Machine snapshot comparison around the hack date
- Free backlink checker (Ahrefs/Semrush free tier, browser-only)

## Reliability notes

- MX/NS lookups shell out to `dig` (present by default on macOS/most
  Linux). If it's missing, those two fields just note how to check
  manually — everything else still runs.
- The subdomain check calls crt.sh, a free third-party service that's
  occasionally flaky (502/404). If it fails, the report notes it and
  links the manual fallback instead of erroring out.
