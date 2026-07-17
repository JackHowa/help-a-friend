# Setting up a Google Safe Browsing API key (local dev)

`recon_check.py` uses the [Safe Browsing API v4](https://developers.google.com/safe-browsing/v4)
to check whether a domain is flagged for malware/phishing. It's optional —
without a key the script just links you to the manual transparency-report
check — but a key makes the report self-contained.

This is a **server-side script running from your terminal**, not a webpage.
That distinction matters below — it's the part people get wrong.

## 1. Create/select a Google Cloud project

1. Go to [console.cloud.google.com](https://console.cloud.google.com/).
2. Top bar → project selector → **New Project** (or reuse an existing one).
   No billing account is required for Safe Browsing's free quota.

## 2. Enable the Safe Browsing API

1. **APIs & Services → Library**.
2. Search "Safe Browsing API".
3. Click **Enable**.

If you skip this step, the API key creation screen's restriction dropdown
will show "No items to display" for Safe Browsing — it only lists APIs
already enabled on the project.

## 3. Create the API key

1. **APIs & Services → Credentials → Create Credentials → API key**.
2. Click into the new key to edit its restrictions:
   - **API restrictions:** select "Restrict key" → check **Safe Browsing
     API** only. (Limits the blast radius if the key ever leaks.)
   - **Application restrictions:** set this to **None** for a quick local
     dev key on your own machine.

     ⚠️ **"None" means anyone who obtains this key can use it from
     anywhere** — there's no restriction at all. That's an acceptable
     tradeoff for a personal key you keep in a gitignored `.env` and never
     share, but don't reuse a "None" key in anything that gets deployed,
     shared with teammates, or run somewhere other than your own laptop.
     For those cases use **IP addresses** instead, locked to the specific
     machine(s)/CI runner(s) that will call the API (see below).

     ⚠️ **Do not use "HTTP referrers (websites)" here.** Referrer
     restrictions only work for requests made *from a browser*, where the
     browser attaches a `Referer` header matching the page's URL. A
     server-side script like `recon_check.py` sends no referrer header at
     all, so Google will reject every request with:

     ```json
     {
       "error": {
         "code": 403,
         "message": "Requests from referer <empty> are blocked.",
         "status": "PERMISSION_DENIED",
         "details": [{"reason": "API_KEY_HTTP_REFERRER_BLOCKED"}]
       }
     }
     ```

     If you want tighter restriction than "None", use **IP addresses**
     instead and lock it to your machine's public IP — that works for
     server-side calls.

## 4. Store the key locally

From `nonprofit-recovery-toolkit/`:

```bash
cp .env.example .env
```

Edit `.env` and paste the key:

```
GOOGLE_SAFE_BROWSING_API_KEY=your-key-here
```

`.env` is already covered by the repo's root `.gitignore` — it will never
get committed. `recon_check.py` loads it automatically at startup (see
`load_dotenv()` — stdlib only, no dependency needed). A real shell
`export GOOGLE_SAFE_BROWSING_API_KEY=...` still takes priority over the
`.env` file if both are set.

## 5. Verify it works

```bash
python3 recon_check.py seacc.org --output /tmp/test-report.md
grep -A1 "Safe Browsing status" /tmp/test-report.md
```

Expected output once the key is set up correctly:

```
## Safe Browsing status
- Verdict: **✅ clean**
```

If you instead see `⚠️ API error: HTTP Error 403: Forbidden`, it's almost
always one of:

| Symptom in error body | Cause | Fix |
|---|---|---|
| `API_KEY_HTTP_REFERRER_BLOCKED` | Key restricted to HTTP referrers | Change Application restrictions to None or IP addresses (step 3) |
| Plain 403, no reason given | Safe Browsing API not enabled on this project, or billing not linked | Re-check step 2; some GCP projects require a linked billing account even for free-tier APIs — check **Billing** in the console |
| 400 Bad Request | Malformed key (e.g. copy/paste truncation) | Re-copy the key into `.env`, check for trailing whitespace/quotes |

## Reusing this for another org's engagement

The key and setup are per-developer, not per-org — one key works for
checking any domain. Nothing here is SEACC-specific; just run
`python3 recon_check.py <their-domain>` with the same `.env` in place.
