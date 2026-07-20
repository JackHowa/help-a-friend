# help-a-friend

A reusable toolkit for volunteer engagements where a nonprofit's
WordPress site has been hacked and needs help recovering its Google
search standing — built during a real Catchafire volunteer engagement,
designed to be reused for any org by pointing it at a different domain.

**[📖 Full documentation site](https://jackhowa.github.io/help-a-friend/)**

## What's here

- **[`nonprofit-recovery-toolkit/`](./nonprofit-recovery-toolkit)** — the
  actual toolkit: a zero-dependency recon script, an image optimizer, API
  setup docs, and fill-in-the-blank templates. See its own
  [README](./nonprofit-recovery-toolkit/README.md) for direct usage, or
  the [docs site](https://jackhowa.github.io/help-a-friend/) for the
  full walkthrough.
- **[`website/`](./website)** — the [Docusaurus](https://docusaurus.io/)
  site that renders the toolkit's docs. See below to run it locally.

## Quick start

```bash
cd nonprofit-recovery-toolkit
python3 recon_check.py their-domain.org --output findings/their-domain-recon-report.md
```

No dependencies beyond the Python standard library. Optional Google API
keys (Safe Browsing, PageSpeed Insights) unlock two more checks — see the
[API setup guide](https://jackhowa.github.io/help-a-friend/docs/api-setup).

## Running the docs site locally

```bash
cd website
npm install
npm start
```

Opens at `http://localhost:3000`. `npm run build` produces a static
`website/build/` you can deploy anywhere (GitHub Pages, Netlify,
Cloudflare Pages, etc.).

## Design principles

- **Runs under your control, not the org's.** You run the script, you
  review the report, you hand the org a finished writeup — nothing here
  is meant to be self-hosted by the nonprofit.
- **Per-engagement findings stay private.** Real recon reports, call
  scripts, and org-specific data live in a gitignored `findings/` folder
  per engagement — only the reusable tooling and templates are tracked
  in git.
- **Zero-dependency where possible.** `recon_check.py` uses only the
  Python standard library so it runs anywhere with `python3`, no
  venv/pip setup needed for a one-hour-call turnaround.
