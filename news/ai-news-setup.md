# Getting AI news auto-updates live — steps only you can do

This is the one-time setup for `.github/workflows/ai-news-autoupdate.yml` and
`scripts/fetch_and_rewrite_news.py`, which keep the **AI News** page current
automatically: once a day, it scans free public news feeds, picks out what's
actually relevant to Claude/Anthropic and the wider AI ecosystem, writes an
original short summary of each item in AITS's own voice (English, Portuguese,
Spanish), and commits the result to `news/news-data.js` — the file
`ai-news.html` reads. No news gets copy-pasted from anywhere; every summary
is freshly written.

Until you do the one step below, the page just shows the hand-written
snapshot already in `news/news-data.js` — nothing is broken, it simply won't
refresh itself yet.

## Why this needs one secret

Scanning a news feed and picking headlines needs no account. Turning a raw
headline into a short, original, well-written summary in three languages is
a job for a real language model — that's the one paid step in this pipeline,
the same way the Instagram auto-poster needed your own Meta access token.
Claude does not create accounts, generate API keys, or handle credentials on
your behalf — that's a firm rule, not a preference — so this one step is
yours to do, in your own browser, logged into your own account.

## 1. Get an Anthropic API key

Go to **console.anthropic.com** → sign in (or create an account, if you
don't already have one for API use — this is separate from your normal
claude.ai login) → **API Keys** → **Create Key**. Copy it immediately; you
won't be able to see it again after leaving the page.

This is billed per use, not a flat fee. The pipeline makes one small API
call per day, summarizing about 7 short headlines at a time — real-world
cost for this is on the order of a few cents a month, not a subscription.
You can set a spend limit on the account if you want a hard ceiling; see
console.anthropic.com's **Billing** settings.

## 2. Add it as a GitHub Actions secret

In your repo on GitHub: **Settings → Secrets and variables → Actions → New
repository secret**. Add one:

- `ANTHROPIC_API_KEY` — the key from step 1

That's the only secret this pipeline needs.

## 3. Nothing else to configure

The workflow already exists and starts running on its own schedule (once a
day; see the cron comment in `.github/workflows/ai-news-autoupdate.yml` —
change that line any time you want it to run more or less often). You can
also trigger a test run immediately from the **Actions** tab →
**AI news auto-update** → **Run workflow**, to confirm it works before
waiting for the schedule.

## What it actually pulls from

Two free, public RSS feeds that need no login — TechCrunch's AI section and
VentureBeat's AI section. Anthropic doesn't publish its own RSS feed (checked
September 2026), so Claude/Anthropic coverage is caught the same way a human
editor would do it: by scanning general AI-industry feeds for those
keywords. If you'd like more sources added later, just say which ones.

## If a run fails or produces nothing

The script is deliberately conservative: if the API key is missing, a feed
is unreachable, or the model's response doesn't parse cleanly, it leaves
`news/news-data.js` exactly as it was and logs a warning — it never
publishes a broken or half-written page. Check the **Actions** tab for the
failed run's log if that happens.
