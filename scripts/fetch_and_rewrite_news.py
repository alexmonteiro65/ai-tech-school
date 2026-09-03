#!/usr/bin/env python3
"""
Fetches recent AI-industry headlines from free, public RSS feeds, picks the
ones actually relevant to Claude/Anthropic/the wider AI ecosystem, and asks
the Anthropic API to write short, original, AITS-toned summaries of each one
in English, Brazilian Portuguese, and Latin American Spanish. Each item also
gets a longer "details" write-up (5-8 sentences) for the card's expanded
view — added 2026-09-03 at Alex's request, so clicking "Click to learn
more" actually reveals substantially more to read, not just the same short
summary with a source link attached. The result is written to
news/news-data.js, which ai-news.html loads directly.

Why this exists (see CLAUDE.md section 2 for the full architecture rule):
this project doesn't hand-copy other outlets' text — every item on the page
is rewritten in AITS's own words, with a small citation link back to the
original source. Doing that rewrite well needs a real language model, so
this script calls the Anthropic API the same way scripts/post_to_instagram.py
calls the Instagram Graph API: server-side, from a GitHub Actions workflow,
using a secret Alex enters himself into this repo's Actions secrets
(ANTHROPIC_API_KEY). Claude never sees or handles that key — see
news/ai-news-setup.md for the one-time setup steps.

The RSS feeds themselves need no key or account — they're each outlet's own
public feed:
  - https://techcrunch.com/category/artificial-intelligence/feed/
  - https://venturebeat.com/category/ai/feed/

Runs from .github/workflows/ai-news-autoupdate.yml on a schedule. Safe to
run by hand too (python scripts/fetch_and_rewrite_news.py) — it always
overwrites news/news-data.js with a fresh snapshot; the workflow only
commits that file if it actually changed.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(REPO_ROOT, "news", "news-data.js")

# Free, public, no-key-required RSS feeds. Anthropic doesn't publish an
# official RSS feed of its own (checked 2026-09-01), so Claude/Anthropic
# coverage is picked up via keyword filtering on general AI-industry feeds —
# the same way a human editor would scan the tech press for it.
FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
]

# Items mentioning any of these (case-insensitive) are treated as
# Claude/Anthropic-relevant and prioritized first; everything else is
# treated as general AI-ecosystem news and used to fill out the list.
PRIORITY_KEYWORDS = [
    "claude", "anthropic", "mcp", "model context protocol",
]

MAX_ITEMS = 7
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5")
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"


def fetch_feed_items(feed_url):
    """Downloads and parses one RSS 2.0 feed into a list of
    {title, link, summary, pubDate, source} dicts. Skips a feed entirely on
    any network/parse error rather than failing the whole run."""
    try:
        req = urllib.request.Request(feed_url, headers={"User-Agent": "AITS-news-bot/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"warning: could not fetch {feed_url}: {exc}", file=sys.stderr)
        return []

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        print(f"warning: could not parse {feed_url}: {exc}", file=sys.stderr)
        return []

    channel = root.find("channel")
    if channel is None:
        return []
    source_name = (channel.findtext("title") or feed_url).strip()

    items = []
    for item in channel.findall("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        summary_raw = item.findtext("description") or ""
        summary = re.sub("<[^<]+?>", "", summary_raw).strip()  # strip any inline HTML
        pub_date = (item.findtext("pubDate") or "").strip()
        if title and link:
            items.append({
                "title": title,
                "link": link,
                "summary": summary,
                "pubDate": pub_date,
                "source": source_name,
            })
    return items


def is_priority(item):
    haystack = (item["title"] + " " + item["summary"]).lower()
    return any(kw in haystack for kw in PRIORITY_KEYWORDS)


def select_items(all_items, max_items):
    """Claude/Anthropic-relevant items first (most recent first within that
    group), then general AI-ecosystem items to fill out the rest. Drops
    obvious near-duplicate titles across feeds."""
    seen_titles = set()
    deduped = []
    for item in all_items:
        key = re.sub(r"[^a-z0-9]+", "", item["title"].lower())[:40]
        if key in seen_titles:
            continue
        seen_titles.add(key)
        deduped.append(item)

    priority = [i for i in deduped if is_priority(i)]
    rest = [i for i in deduped if not is_priority(i)]
    return (priority + rest)[:max_items]


def call_anthropic_rewrite(items, api_key):
    """Sends all selected items in a single request and asks for a short,
    original, factual summary of each — in AITS's plain, no-hype teaching
    voice (see CLAUDE.md section 7) — in en/pt/es. Returns the parsed JSON
    list, or raises on any failure (the caller decides how to degrade)."""
    numbered = "\n\n".join(
        f"{idx + 1}. TITLE: {item['title']}\nSOURCE SUMMARY: {item['summary'] or '(no summary provided)'}"
        for idx, item in enumerate(items)
    )

    prompt = (
        "You are writing news cards for AI Tech School (AITS), an educational "
        "site that teaches Claude, Claude Code, MCP, and the AI ecosystem. For each "
        "numbered item below, do three things in each of three languages — English (en), "
        "Brazilian Portuguese (pt), and Latin American Spanish (es):\n"
        "1. Translate the headline (TITLE) naturally for that language — keep proper "
        "nouns/product names (Claude, Anthropic, MCP, company names) as-is, translate "
        "the rest.\n"
        "2. Write your OWN original 1-2 sentence factual summary of what happened — "
        "never copy phrases from the source summary. Plain, direct, no hype, no "
        "marketing adjectives, written the way you'd explain it to someone learning "
        "the field. This is the short version shown on the card before it's expanded.\n"
        "3. Write your OWN original, expanded write-up of the same story — "
        "5-8 sentences, still never copying phrases from the source summary. This is "
        "the long version a reader sees after clicking to expand the card, so it "
        "should add real substance beyond the short summary: more concrete detail on "
        "what actually happened, why it matters for someone learning to build with AI "
        "(what changes for them in practice), and relevant context or background a "
        "newcomer to the topic would need. Same plain, direct, no-hype tone as the "
        "summary — write it as flowing prose paragraphs, not a list.\n\n"
        "Respond with ONLY a JSON array, one object per item, in the same order, each "
        'shaped exactly like: {"en": {"title": "...", "summary": "...", "details": "..."}, '
        '"pt": {"title": "...", "summary": "...", "details": "..."}, "es": {"title": "...", '
        '"summary": "...", "details": "..."}}. '
        "No other text before or after the JSON.\n\n"
        f"{numbered}"
    )

    body = json.dumps({
        "model": ANTHROPIC_MODEL,
        "max_tokens": 8192,  # bumped from 4096 now that each item also
                             # includes a 5-8 sentence "details" write-up
                             # per language, not just a 1-2 sentence summary
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        ANTHROPIC_API_URL,
        data=body,
        method="POST",
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = json.loads(resp.read())

    text = "".join(block.get("text", "") for block in payload.get("content", []))
    text = text.strip()
    # Be tolerant of a model that wraps the JSON in a code fence anyway.
    text = re.sub(r"^```[a-zA-Z]*\n?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    return json.loads(text)


def format_date_label(pub_date_str, lang):
    """Best-effort human date label per language; falls back to the raw
    RSS date string (or today) if parsing fails."""
    months = {
        "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "pt": ["jan.", "fev.", "mar.", "abr.", "mai.", "jun.", "jul.", "ago.", "set.", "out.", "nov.", "dez."],
        "es": ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."],
    }
    dt = None
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z"):
        try:
            dt = datetime.strptime(pub_date_str, fmt)
            break
        except (ValueError, TypeError):
            continue
    if dt is None:
        dt = datetime.now(timezone.utc)

    month = months[lang][dt.month - 1]
    if lang == "en":
        return f"{month} {dt.day}, {dt.year}"
    return f"{dt.day} de {month} de {dt.year}"


def build_output(items, rewrites):
    langs = ("en", "pt", "es")
    out = {lang: {"snapshotDate": "", "items": []} for lang in langs}
    snapshot_dt = datetime.now(timezone.utc)
    snapshot_labels = {
        "en": snapshot_dt.strftime("%B %d, %Y").replace(" 0", " "),
        "pt": format_date_label(None, "pt"),
        "es": format_date_label(None, "es"),
    }

    for item, rewrite in zip(items, rewrites):
        for lang in langs:
            lang_rewrite = rewrite.get(lang) or rewrite.get("en") or {}
            out[lang]["items"].append({
                "date": format_date_label(item["pubDate"], lang),
                "title": lang_rewrite.get("title", item["title"]),
                "summary": lang_rewrite.get("summary", ""),
                # Longer expanded write-up shown when a reader expands the
                # card — falls back to the summary if the model somehow
                # omitted it, so the page never shows an empty expansion.
                "details": lang_rewrite.get("details") or lang_rewrite.get("summary", ""),
                "source": item["source"],
                "url": item["link"],
            })
    for lang in langs:
        out[lang]["snapshotDate"] = snapshot_labels[lang]
    return out


def write_output_js(data):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    header = (
        "/* Auto-generated by scripts/fetch_and_rewrite_news.py — do not hand-edit.\n"
        "   Regenerated on a schedule by .github/workflows/ai-news-autoupdate.yml.\n"
        "   See news/ai-news-setup.md for how the pipeline is configured. */\n"
    )
    body = "window.AITS_NEWS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(header + body)


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(
            "ANTHROPIC_API_KEY is not set — see news/ai-news-setup.md to add it as a "
            "GitHub Actions secret. Leaving news/news-data.js untouched.",
            file=sys.stderr,
        )
        return 0  # not a failure — just nothing to do yet

    all_items = []
    for feed_url in FEEDS:
        all_items.extend(fetch_feed_items(feed_url))

    if not all_items:
        print("warning: no items fetched from any feed; leaving news-data.js untouched.", file=sys.stderr)
        return 0

    selected = select_items(all_items, MAX_ITEMS)

    try:
        rewrites = call_anthropic_rewrite(selected, api_key)
    except Exception as exc:  # noqa: BLE001 - degrade gracefully in CI
        print(f"warning: Anthropic rewrite failed ({exc}); leaving news-data.js untouched.", file=sys.stderr)
        return 0

    if len(rewrites) != len(selected):
        print("warning: rewrite count mismatch; leaving news-data.js untouched.", file=sys.stderr)
        return 0

    data = build_output(selected, rewrites)
    write_output_js(data)
    print(f"Wrote {len(selected)} items to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
