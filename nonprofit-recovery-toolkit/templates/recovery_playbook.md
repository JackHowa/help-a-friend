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
3. **Harden WordPress — one free plugin, no code.** For orgs without a
   technical staffer, recommend a single all-in-one security plugin
   rather than a list of manual changes:
   1. Plugins → Add New → search **"Solid Security"** (free) → Install →
      Activate.
   2. Turn on: hide WordPress version, stop username/user-enumeration
      leaks, block repeated login attempts, and two-factor login for
      every admin account (highest-value setting of the four).
   - Also worth doing regardless of plugin choice: update core/plugins/
     theme, delete unused plugins/themes, rotate admin passwords, audit
     the admin user list for anything unrecognized.
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
8. **Prevent recurrence — free upgraded protection, simple application.**
   Most nonprofits qualify for
   [Cloudflare Project Galileo](https://www.cloudflare.com/galileo/) — free
   enterprise WAF/DDoS protection for at-risk public-interest orgs
   (environmental, human rights, journalism, and similar advocacy orgs all
   qualify). Re-hacks are what actually kill a recovery, so this matters
   more than any single SEO fix. If the org's domain already resolves to
   Cloudflare nameservers (check the recon report's DNS section), this is
   an upgrade to what they already have, not a new signup:
   1. Go to **cloudflare.com/galileo** → click **Apply**.
   2. Fill in 501(c)(3) status and mission — Cloudflare's team reviews it.
   3. No further setup needed once approved.

## Google Ad Grants — simple version to tell them, then the checklist

**Say:** "You likely qualify for up to $10,000/month in free Google search
ads, meant as a bridge while organic rankings recover. It's an
application, not a technical setup."

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
- **Sequencing:** apply only after steps 1-2 above are clean — activation
  includes a website review that a lingering hack flag will fail.

## Who owns what going forward

- **Site/hosting access:** {{WHO — org staff, or vendor "CoBuild"?}}
- **Admin access audit:** {{DONE / TODO}}
- **WAF/hardening owner:** {{WHO}}
- **Ad Grants account owner:** {{WHO}}
