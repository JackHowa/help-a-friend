---
sidebar_position: 4
---

# API key setup (Safe Browsing & PageSpeed Insights)

Both keys are optional and follow the same setup process on the same
Google Cloud project — just enable a different API in step 2. Without
either key, `recon_check.py` still runs fine; it just links you to the
manual check instead of pulling live data.

This is a **server-side script running from your terminal**, not a
webpage — that distinction matters for the key restriction step below,
where people most often get it wrong.

## 1. Create/select a Google Cloud project

1. Go to [console.cloud.google.com](https://console.cloud.google.com/).
2. Top bar → project selector → **New Project** (or reuse an existing
   one). No billing account is required for Safe Browsing's free quota;
   PageSpeed Insights may require billing linked even on the free tier —
   check **Billing** in the console if you hit a plain 403.

## 2. Enable the API(s) you want

**APIs & Services → Library** → search for:
- **"Safe Browsing API"** — malware/phishing check
- **"PageSpeed Insights API"** — Lighthouse performance scores

Click **Enable** for whichever you want. If you skip this step, the API
key creation screen's restriction dropdown will show "No items to
display" for that API — it only lists APIs already enabled on the
project.

## 3. Create the API key

1. **APIs & Services → Credentials → Create Credentials → API key**.
2. Click into the new key to edit its restrictions:
   - **API restrictions:** select "Restrict key" → check only the
     API(s) you enabled above. Limits the blast radius if the key ever
     leaks.
   - **Application restrictions:** set this to **None** for a quick
     local dev key on your own machine.

     :::warning
     **"None" means anyone who obtains this key can use it from
     anywhere** — there's no restriction at all. Acceptable for a
     personal key you keep in a gitignored `.env` and never share, but
     don't reuse a "None" key in anything deployed or shared with
     teammates — use **IP addresses** instead, locked to the specific
     machine(s)/CI runner(s) that will call the API.
     :::

     :::danger
     **Do not use "HTTP referrers (websites)" here.** Referrer
     restrictions only work for requests made *from a browser*, where
     the browser attaches a `Referer` header matching the page's URL. A
     server-side script sends no referrer header at all, so Google will
     reject every request with `API_KEY_HTTP_REFERRER_BLOCKED`. Use
     **None** or **IP addresses** instead.
     :::

## 4. Store the key locally

From `nonprofit-recovery-toolkit/`:

```bash
cp .env.example .env
```

Edit `.env` and paste your key(s):

```
GOOGLE_SAFE_BROWSING_API_KEY=your-key-here
GOOGLE_PAGESPEED_API_KEY=your-key-here
```

`.env` is already covered by the repo's root `.gitignore` — it will
never get committed. `recon_check.py` loads it automatically at startup.
A real shell `export GOOGLE_SAFE_BROWSING_API_KEY=...` still takes
priority over the `.env` file if both are set.

## 5. Verify it works

```bash
python3 recon_check.py their-domain.org --output /tmp/test-report.md
grep -A1 "Safe Browsing status" /tmp/test-report.md
```

Expected output once the key is set up correctly:

```
## Safe Browsing status
- Verdict: **✅ clean**
```

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `API_KEY_HTTP_REFERRER_BLOCKED` | Key restricted to HTTP referrers | Change Application restrictions to None or IP addresses |
| Plain 403, no reason given | API not enabled on this project, or billing not linked | Re-check step 2; some GCP projects require linked billing even for free-tier APIs |
| 400 Bad Request | Malformed key (copy/paste truncation) | Re-copy the key into `.env`, check for trailing whitespace/quotes |

## Reusing across engagements

The key and setup are per-volunteer, not per-org — one key works for
checking any domain. Just run `python3 recon_check.py <their-domain>`
with the same `.env` in place.
