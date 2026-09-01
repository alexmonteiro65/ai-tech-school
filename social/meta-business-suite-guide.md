# Scheduling Instagram posts yourself — Meta Business Suite

This is the "you already know a tool exists, you just need to manage it"
piece: **Meta Business Suite** (business.facebook.com), Meta's own free
dashboard for scheduling Instagram and Facebook posts. It's built by Meta
itself, not a third-party service — free, no developer account, no API key,
nothing to renew every couple of months. You upload an image, write a
caption, pick a date and time, and it posts itself. That's it.

## Why this instead of the automated GitHub pipeline

This project also has a fully automated Instagram poster
(`.github/workflows/instagram-autopost.yml`, set up in
`social/instagram-api-setup.md`) that posts on its own from
`social/schedule.json` with zero manual steps once it's running. That's the
"never touch it again" option — but it needs a Meta developer app and an
access token that **expires roughly every 60 days**, which means logging
back into developer tools periodically to refresh it.

Meta Business Suite is the opposite trade-off: you do a couple of minutes of
clicking per post, but there's no token, no developer console, no expiry to
track. Since you said you want to manage this yourself day-to-day rather
than maintain a technical pipeline, this is the one to actually use.
(The automated pipeline can stay there unused, or be removed later — your
call, no rush either way.)

## One-time setup (a few minutes, once)

1. Go to **business.facebook.com** and log in with the Facebook account
   connected to the AI Tech School Page.
2. If @ai.tech.school isn't already linked: on Instagram, go to
   **Settings → Account → Linked accounts → Facebook**, and connect it to
   the AI Tech School Facebook Page. (Same Page used in
   `social/instagram-api-setup.md`, if you already did that step — no need
   to create a second one.)
3. Back in Meta Business Suite, confirm you can see @ai.tech.school listed
   as a connected account (usually under **Settings** or the account
   switcher in the top corner).

That's the entire setup. No app to create, no key to copy anywhere.

## Scheduling one post (repeat this per post)

1. In Meta Business Suite, click **Create post** (sometimes labeled
   **Create** → **Post**).
2. Under "Share to," make sure Instagram is checked for @ai.tech.school.
   Uncheck Facebook if you only want it on Instagram.
3. Upload the image — for the 9 launch posts, that's the PNG files in
   `social/` (`post-1-launch.png` through `post-9-cta.png`).
4. Paste in the caption for that post from `social/captions.md`.
5. Click **Set date and time**, pick when it should go out (use the dates
   already planned in `social/content-calendar.md` if you want to follow
   that schedule).
6. Click **Schedule**. Done — it posts itself at that time, no further
   action needed.

Repeat for each of the 9 posts. Meta Business Suite also has an "Active
times" suggestion feature that shows when your followers are usually most
active, if you'd rather use that than the fixed calendar dates.

## The 3 Reels

Same flow, using **Create reel** instead of **Create post**. These still
need to be recorded from `social/reels-scripts.md` first — no video file
exists for them yet (see `CLAUDE.md` for why this project doesn't generate
video from a script directly).

## If something looks different

Meta changes this interface's exact button names every so often. If a step
above doesn't match what you see, the shape of the flow — connect account →
create post → upload → caption → schedule — has stayed consistent for
years, so look for those same ideas under slightly different button names.
