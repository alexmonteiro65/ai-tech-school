# Getting Instagram auto-posting live — steps only you can do

This is the one-time setup for `.github/workflows/instagram-autopost.yml` and
`scripts/post_to_instagram.py`, which auto-post the 9 feed posts in
`social/schedule.json` to **@ai.tech.school** on their scheduled dates, using
Meta's own free Instagram Graph API. No Buffer, no Later, no paid plan —
just your own Instagram/Facebook account and GitHub's free Actions minutes.

Every step below has to happen in your own browser, logged into your own
accounts — creating accounts and entering credentials isn't something Claude
does for you, on this or any project. Once you've done these, the
automation runs by itself with no further action from you.

## 1. Make @ai.tech.school a Business or Creator account

In the Instagram app: **Settings → Account type and tools → Switch to
professional account** → choose **Business**. (Skip this if it's already
professional — check the same menu.)

## 2. Link it to a Facebook Page

The Graph API only reaches Instagram through a connected Facebook Page.
If you don't already have a Page for AI Tech School, create one at
facebook.com/pages/create (free, takes a minute). Then, in Instagram:
**Settings → Account → Linked accounts → Facebook** → connect that Page.

## 3. Create a Meta developer app

Go to developers.facebook.com/apps → **Create App** → type **Business** →
name it something like "AI Tech School Autopost". You do not need to submit
it for App Review — using your own account as the developer/admin works
immediately, no approval wait.

In the app dashboard, **Add Product** → add **Instagram Graph API**.

## 4. Generate an access token

Go to developers.facebook.com/tools/explorer, select your new app in the
top-right dropdown, and generate a **User Access Token** with these
permissions checked: `instagram_basic`, `instagram_content_publish`,
`pages_show_list`, `pages_read_engagement`.

That token is short-lived (about an hour). Exchange it for a long-lived one
(60 days) by running this in your own terminal or browser address bar —
replace the three placeholders with your own app ID, app secret (both on
your app's dashboard under **Settings → Basic**), and the short-lived token
you just generated:

```
https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_LIVED_TOKEN
```

The response's `access_token` is the long-lived one — that's what goes into
GitHub as `IG_ACCESS_TOKEN` in step 6. It expires in ~60 days, so mark a
reminder to redo this step before then (Meta doesn't offer a
non-expiring token for this API).

## 5. Find your Instagram Business Account ID

Still in Graph API Explorer, run:

```
GET /me/accounts
```

Find your Page in the results and copy its `id`. Then run:

```
GET /{that-page-id}?fields=instagram_business_account
```

The number in the response is your `IG_USER_ID` for step 6.

## 6. Add both as GitHub Actions secrets

In your repo on GitHub: **Settings → Secrets and variables → Actions → New
repository secret**. Add two:

- `IG_ACCESS_TOKEN` — the long-lived token from step 4
- `IG_USER_ID` — the ID from step 5

Nothing else to configure — the workflow already exists and starts checking
`social/schedule.json` on its next scheduled run (twice a day; see the cron
comment in `.github/workflows/instagram-autopost.yml`). You can also trigger
a test run immediately from the **Actions** tab → **Instagram auto-post** →
**Run workflow**, to confirm it works before the real schedule kicks in.

## What this does not automate

The 3 Reels in week 4 of `content-calendar.md` still need to be recorded
from `reels-scripts.md` by hand and posted manually — the Graph API can
publish a video the same way as an image, but no video file exists yet for
those, and this project doesn't generate video from a script. Once you have
real Reel files, ask and this can be extended to post those too.

## Token expiry

Your `IG_ACCESS_TOKEN` expires roughly every 60 days. When it does, the
workflow will fail with a Graph API auth error — check the Actions tab
occasionally, or just redo steps 4–6 preemptively every couple of months.
