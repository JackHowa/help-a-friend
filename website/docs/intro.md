---
sidebar_position: 1
---

# Nonprofit Website Security Toolkit

Reusable tooling for volunteer engagements helping nonprofits keep their
websites secure — whether that's a proactive checkup on a healthy site
or recovering one that's already been hacked (including repairing the
Google search fallout that often follows). Built during a real recovery
engagement, designed to be reused for any org by pointing it at a
different domain.

Most nonprofits are running on a volunteer-built WordPress site with
nobody actively maintaining the technical/security side. This toolkit
turns a one-hour volunteer call into a real security review, not just a
conversation — the same checks work whether you're getting ahead of a
problem or cleaning one up.

Everything here runs under **your** control as the volunteer — you run
it, you review the report, you hand the org a finished writeup. Nothing
is designed to be self-hosted by the nonprofit itself.

## What's in the toolkit

- **[`recon_check.py`](./recon-check)** — a CLI that runs a full security
  checkup against a domain and produces a markdown report. Useful for
  any nonprofit site, hacked or not: it's the same checks a security-
  minded volunteer would want run proactively (missing security headers,
  exposed WordPress internals, subdomain takeover risk) as the ones
  you'd run right after an incident.
- **[`optimize_images.py`](./optimize-images)** — download and re-save
  any flagged image as optimized JPEG/WebP, no resizing needed.
- **[Templates](./templates)** — fill-in-the-blank hardening/recovery
  playbook, plus a Google reconsideration request draft for when a hack
  did happen and search rankings need repairing.
- **[Safe Browsing / PageSpeed API setup](./api-setup)** — walkthrough
  for the two optional Google API keys the recon script can use.

## Quick start

```bash
git clone https://github.com/JackHowa/help-a-friend.git
cd help-a-friend/nonprofit-recovery-toolkit
python3 recon_check.py their-domain.org --output findings/their-domain-recon-report.md
```

No dependencies beyond the Python standard library for the recon script.
See [Recon Check](./recon-check) for the full option list.
