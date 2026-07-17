# Google Reconsideration Request — draft

Use this only if Search Console shows a **Manual Action** under Security &
Manual Actions. If there's no manual action, this isn't needed — algorithmic
ranking drops recover on their own once the site is clean and re-crawled.

Submit via Search Console → Security & Manual Actions → Manual Actions →
"Request Review", pasting a version of the text below (Google's form has its
own field, this is the narrative to paste in).

---

**Site:** https://{{DOMAIN}}/
**Organization:** {{ORG_NAME}}
**Manual action type shown in Search Console:** {{MANUAL_ACTION_TYPE}}

We recently discovered that our WordPress website was compromised via
{{ATTACK_VECTOR — e.g. "a vulnerable plugin" / "a compromised admin
credential" / "unknown, under investigation"}} on approximately
{{HACK_DATE}}. The compromise resulted in {{WHAT_HAPPENED — e.g. "injected
spam pages promoting unrelated commercial products" / "cloaked redirects
sending search visitors to third-party sites"}}.

**Steps taken to resolve the issue:**

1. {{e.g. "Restored the site from a clean backup dated before the
   compromise"}}
2. {{e.g. "Updated WordPress core, all plugins, and the active theme to
   their latest versions"}}
3. {{e.g. "Removed unused plugins/themes and rotated all admin credentials"}}
4. {{e.g. "Audited the admin user list and removed an unauthorized account
   created during the compromise"}}
5. {{e.g. "Installed [Wordfence / Cloudflare WAF] for ongoing monitoring"}}
6. Verified via `curl` with a Googlebot user-agent that no cloaked content
   remains, and confirmed via manual inspection of robots.txt and the XML
   sitemap that no injected URLs are present.
7. {{If applicable: "Submitted removal requests for the following
   spam URLs identified in Google's index: {{LIST_OF_URLS}}"}}

We believe the site is now fully clean and hardened against recurrence, and
respectfully request reconsideration.

---

**Notes for whoever submits this:**
- Be specific and honest — vague "we fixed it, trust us" requests get
  rejected. List the actual remediation steps taken.
- If spam URLs are still indexed, request their removal (Search Console →
  Removals, or a 410 response) *before* submitting reconsideration — Google
  wants to see the mess actually gone, not just the site cleaned going
  forward.
- Reviews typically take a few days to a couple of weeks.
