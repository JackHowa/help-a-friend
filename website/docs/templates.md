---
sidebar_position: 5
---

# Templates

Two fill-in-the-blank markdown templates live in
`nonprofit-recovery-toolkit/templates/`. Copy them into a per-engagement
`findings/` folder (gitignored) and fill in the `{{PLACEHOLDERS}}` — don't
edit the shared templates in place.

## recovery_playbook.md

A one-page leave-behind covering:

- What happened and the current recon status
- Why search rankings dropped, and why they recover
- Action items in order: confirm manual-action status, clean up
  remnants, harden WordPress (one free plugin, no code), check
  backlinks, apply for Google Ad Grants, rebuild trust signals, cover
  other search engines, prevent recurrence via Cloudflare Project
  Galileo
- A Google Ad Grants checklist (eligibility, application steps, what
  keeps the grant active)
- A "who owns what going forward" section so access/responsibility
  doesn't fall through the cracks after you leave

## reconsideration_request.md

A draft Google reconsideration request, for use **only if** Search
Console shows an actual Manual Action under Security & Manual Actions —
skip it entirely otherwise, since an algorithmic ranking drop recovers on
its own once the site is re-crawled clean.

Includes:
- The narrative to paste into Search Console's "Request Review" form
- Placeholders for hack date, attack vector, and remediation steps taken
- Notes on being specific rather than vague (vague requests get
  rejected), and on removing/410-ing any still-indexed spam URLs
  *before* submitting

## Extending for the next engagement

1. Run [`recon_check.py`](./recon-check) against the new domain.
2. Copy both templates into that engagement's `findings/` folder and
   fill them in.
3. If the hack left a distinctive spam pattern (pharma keywords,
   Japanese SEO spam, gambling terms), add those terms to a copy of
   `spam_terms.txt` and pass it via `--wordlist`.
