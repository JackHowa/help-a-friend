---
sidebar_position: 1
---

# Nonprofit Post-Hack Recovery Toolkit

Reusable tooling for volunteer engagements where a nonprofit's WordPress
site was hacked and needs help recovering its Google search standing.
Built during a real engagement, designed to be reused for any org by
pointing it at a different domain.

Everything here runs under **your** control as the volunteer — you run
it, you review the report, you hand the org a finished writeup. Nothing
is designed to be self-hosted by the nonprofit itself.

## What's in the toolkit

- **[`recon_check.py`](./recon-check)** — a CLI that runs the automatable
  parts of a pre-call recon checklist against a domain and produces a
  markdown report.
- **[`optimize_images.py`](./optimize-images)** — download and re-save
  any flagged image as optimized JPEG/WebP, no resizing needed.
- **[Templates](./templates)** — fill-in-the-blank recovery playbook and
  Google reconsideration request draft.
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
