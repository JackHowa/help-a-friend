# {{ORG_NAME}} — Post-Hack Search Recovery Playbook

One-page leave-behind. Fill in the {{PLACEHOLDERS}} after the call.

## What happened

- **Hack date:** {{HACK_DATE}}
- **What it did:** {{e.g. "injected spam pages / redirected visitors /
  defaced homepage"}}
- **How it was cleaned:** {{e.g. "backup restore" / "manual plugin/file
  cleanup"}}
- **Current status per this toolkit's recon check:** {{SUMMARY — see
  attached recon report}}

## Why search rankings dropped (and why they'll recover)

A hack that got indexed by Google — even briefly — can trigger a manual
action or just tank trust signals algorithmically. "Fixed in a day" often
means the visible symptom was removed while remnants (spam pages still
indexed, a lingering manual action, or degraded backlink profile) kept
suppressing rankings. Recovery is real but not instant — typically weeks to
a few months once the site is verifiably clean.

## Action items, in order

1. **Confirm the manual action status.** Search Console → Security & Manual
   Actions. If flagged, submit a reconsideration request (see
   `reconsideration_request.md`) — but only after step 2.
2. **Clean up remnants.** Any spam URLs still indexed (`site:{{DOMAIN}}` in
   an incognito window) need to be removed/410'd before requesting review.
3. **Harden WordPress.**
   - Update core, all plugins, and the theme.
   - Delete unused plugins/themes entirely (smaller attack surface).
   - Enable 2FA for all admin accounts; rotate all admin passwords.
   - Install a WAF — Wordfence (free tier) or Cloudflare (see below).
   - Audit the admin user list for anything unrecognized.
4. **Check backlinks.** Some hacks generate spammy inbound links that
   outlive the hack itself. Run a free Ahrefs/Semrush backlink check;
   disavow anything clearly spammy.
5. **Apply for Google Ad Grants** (up to $10k/month in free search ads) as
   a bridge while organic rankings recover. Apply only after steps 1-2 are
   clean — activation includes a website review that a lingering flag will
   fail. See the "Ad Grants" checklist below.
6. **Rebuild trust signals.**
   - Add Organization schema markup with a `sameAs` link to the org's
     Wikipedia/Wikidata page if one exists.
   - Pitch local press (papers, public radio) around active campaigns —
     fresh authoritative coverage and earned backlinks help rankings
     recover faster than SEO tweaks alone.
7. **Cover other search engines.** Set up Bing Webmaster Tools (has its own
   security scan) and submit via IndexNow, which also covers DuckDuckGo and
   Yahoo. Five minutes of setup, usually skipped.
8. **Prevent recurrence.** Apply for
   [Cloudflare Project Galileo](https://www.cloudflare.com/galileo/) — free
   enterprise WAF/DDoS protection for at-risk public-interest orgs;
   environmental advocacy groups qualify. Re-hacks are what actually kill a
   recovery, so this matters more than any single SEO fix.

## Google Ad Grants — application checklist

- **Eligibility:** 501(c)(3), not a government entity/hospital/school.
- **Have ready:** EIN, a Google account tied to an `@{{DOMAIN}}` address,
  HTTPS site with clear mission content (already true), a named account
  owner (ongoing maintenance rules apply).
- **Steps:** Register at google.com/nonprofits → verify charitable status
  via Goodstack (2-14 business days) → activate Ad Grants from the Google
  for Nonprofits dashboard → build first campaign (min. 2 ad groups/campaign,
  2 ads + 2 sitelinks each, conversion tracking wired to Analytics).
- **Keep it:** maintain ≥5% CTR (two consecutive months below risks
  suspension), avoid single-word/generic keywords, ads must point to the
  verified domain.

## Who owns what going forward

- **Site/hosting access:** {{WHO — org staff, or vendor "CoBuild"?}}
- **Admin access audit:** {{DONE / TODO}}
- **WAF/hardening owner:** {{WHO}}
- **Ad Grants account owner:** {{WHO}}
