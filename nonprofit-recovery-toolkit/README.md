# Nonprofit Post-Hack Recovery Toolkit

Reusable tooling for volunteer engagements where a nonprofit's WordPress site
was hacked and needs help recovering its Google search standing. Built for
the SEACC engagement, designed to be reused for any org by passing a
different domain/config.

Everything here runs under **your** control (you run it, you review the
report, you hand the org a finished writeup) — nothing is designed to be
self-hosted by the nonprofit.

## What's in here

- `recon_check.py` — CLI that runs the automatable parts of the pre-call
  recon checklist against a domain and produces a markdown report:
  cloaking check (Googlebot UA vs. normal UA diff), spam-term grep,
  robots.txt + sitemap fetch/analysis, optional Safe Browsing API check,
  optional PageSpeed Insights check, WordPress exposure (xmlrpc.php, user
  enumeration, exposed version), security headers
  (CSP/HSTS/X-Frame-Options/X-Content-Type-Options), SSL certificate
  issuer/validity, DNS (A/MX/NS records), and subdomain discovery via
  certificate transparency logs (flags subdomains not linked from the
  homepage and CNAMEs pointing at takeover-prone service patterns).
- `optimize_images.py` — standalone script: pass it one or more image
  URLs (e.g. ones PageSpeed flags as oversized) and it downloads +
  re-saves each as optimized JPEG and WebP, organized into
  `original/`/`jpg/`/`webp/` folders. No resizing, so output is safe to
  reuse anywhere the original was used.
- `spam_terms.txt` — default wordlist for the spam grep (edit/extend freely,
  or point `--wordlist` at your own per-engagement list).
- `templates/reconsideration_request.md` — fill-in-the-blanks Google
  reconsideration request, for use if Search Console shows a manual action.
- `templates/recovery_playbook.md` — one-page leave-behind: what happened,
  what to check, what to fix, how to prevent recurrence.

## Usage

```bash
cd nonprofit-recovery-toolkit
python3 recon_check.py seacc.org --output seacc-recon-report.md
```

With a Safe Browsing API key (optional — get one from the Google Cloud
Console, enable the "Safe Browsing API"):

```bash
cp .env.example .env    # then paste your key into .env
python3 recon_check.py seacc.org --output seacc-recon-report.md
```

`.env` is gitignored, so the key never gets committed. If you'd rather not
use a file, `export GOOGLE_SAFE_BROWSING_API_KEY=your-key-here` works too
and takes priority over `.env`.

Full walkthrough (GCP project setup, key restrictions, common 403 errors):
[`docs/safe-browsing-api-setup.md`](docs/safe-browsing-api-setup.md) — the
same setup process works for a PageSpeed Insights key
(`GOOGLE_PAGESPEED_API_KEY`), just enable "PageSpeed Insights API" instead
of "Safe Browsing API" on the same project.

**Why bother with the PageSpeed check at all:** page speed (Core Web
Vitals) is a confirmed Google ranking factor — a slow page can suppress
search rankings even once a hack is otherwise fully cleaned up, which
matters directly for the "why isn't my ranking recovering" conversation.

To optimize any images PageSpeed flags as oversized:

```bash
python3 optimize_images.py --output findings/image-optimization \
    https://their-domain.org/wp-content/uploads/big-photo.png
```

No Python dependencies beyond the standard library for `recon_check.py`;
`optimize_images.py` needs Pillow (`pip3 install --user Pillow`). MX/NS
lookups shell out to the `dig` binary (present by default on macOS/most
Linux); if it's missing, those two fields just note how to check
manually — everything else still runs fine. The subdomain check calls
crt.sh (a free, occasionally-flaky third-party service) — if it 502s/404s,
the report notes it and links the manual fallback instead of failing.

## What this does NOT automate (do these manually, they need a browser/login)

- Google Search Console → Security Issues / Manual Actions (needs org's login)
- `site:domain.com` search in an incognito window (Google blocks scripted
  queries; do this by hand, 2 minutes)
- Wayback Machine snapshot comparison around the hack date
- Free backlink checker (Ahrefs/Semrush free tier, browser-only)

The script's report includes a checklist reminder for these so nothing gets
missed before the call.

## Extending for the next engagement

1. Run `recon_check.py <their-domain>`.
2. Fill in `templates/recovery_playbook.md` and
   `templates/reconsideration_request.md` with the org's specifics.
3. If the hack left a distinctive spam pattern (e.g. pharma keywords,
   Japanese SEO spam, gambling terms), add those terms to a copy of
   `spam_terms.txt` and pass it via `--wordlist`.
