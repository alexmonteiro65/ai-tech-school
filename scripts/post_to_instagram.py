#!/usr/bin/env python3
"""
Auto-posts the next due feed post from social/schedule.json to
@ai.tech.school on Instagram, using Meta's official Instagram Graph API
directly — no Buffer, no Later, no third-party scheduler, no paid API.

Why this exists instead of Buffer (see CLAUDE.md, section 2): Buffer/Later
require an OAuth-connected account and a billed API plan managed by a
human, held nowhere in this codebase. This script instead uses the free,
official Meta Graph API. The two secrets it needs (IG_ACCESS_TOKEN,
IG_USER_ID) are entered by Alex directly into this repo's GitHub Actions
secrets — Claude never sees or handles them. See social/instagram-api-setup.md
for how to obtain and add them.

Runs from .github/workflows/instagram-autopost.yml on a schedule. Reads
social/schedule.json, finds the first post whose date is today-or-earlier,
whose slot matches this run, and that hasn't been posted yet; publishes it
via the two-step Graph API flow (create media container, then publish);
marks it posted=true and lets the workflow commit that change back.

Deliberately conservative: posts at most ONE item per run, and does
nothing (exit 0, no error) when nothing is due — a missed or delayed run
just catches up on the next scheduled run instead of double-posting.
"""
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone

GRAPH_API_VERSION = "v21.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEDULE_PATH = os.path.join(REPO_ROOT, "social", "schedule.json")

# Where the repo's own files are publicly reachable — Instagram's Graph API
# fetches the image from this URL itself, it does not accept a raw upload.
PUBLIC_BASE_URL = "https://alexmonteiro65.github.io/ai-tech-school/"


def log(msg):
    print(f"[post_to_instagram] {msg}", flush=True)


def load_schedule():
    with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_schedule(data):
    with open(SCHEDULE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def graph_request(path, params, method="POST"):
    url = f"{GRAPH_API_BASE}/{path}"
    data = urllib.parse.urlencode(params).encode("utf-8")
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode("utf-8"))
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Graph API error {e.code} on {path}: {body}") from e


def publish_post(entry, access_token, ig_user_id):
    image_url = PUBLIC_BASE_URL + entry["image"]
    log(f"Creating media container for {entry['id']} ({image_url})")
    container = graph_request(
        f"{ig_user_id}/media",
        {
            "image_url": image_url,
            "caption": entry["caption"],
            "access_token": access_token,
        },
    )
    creation_id = container["id"]

    log(f"Publishing container {creation_id}")
    result = graph_request(
        f"{ig_user_id}/media_publish",
        {
            "creation_id": creation_id,
            "access_token": access_token,
        },
    )
    log(f"Published: {result}")
    return result


def main():
    access_token = os.environ.get("IG_ACCESS_TOKEN")
    ig_user_id = os.environ.get("IG_USER_ID")
    run_slot = os.environ.get("RUN_SLOT")  # "morning" or "evening", set by the workflow

    if not access_token or not ig_user_id:
        log(
            "IG_ACCESS_TOKEN / IG_USER_ID not set yet — nothing to do. "
            "See social/instagram-api-setup.md to finish setup."
        )
        return 0

    schedule = load_schedule()
    today = datetime.now(timezone.utc).date().isoformat()

    due = [
        p
        for p in schedule["posts"]
        if not p["posted"] and p["date"] <= today and p["slot"] == run_slot
    ]

    if not due:
        log(f"No post due for slot={run_slot} on {today}.")
        return 0

    entry = due[0]
    log(f"Due: {entry['id']} (scheduled {entry['date']} {entry['slot']})")

    try:
        publish_post(entry, access_token, ig_user_id)
    except Exception as e:
        log(f"FAILED to publish {entry['id']}: {e}")
        return 1

    entry["posted"] = True
    save_schedule(schedule)
    log(f"Marked {entry['id']} as posted and saved schedule.json.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
