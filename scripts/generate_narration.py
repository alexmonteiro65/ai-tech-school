#!/usr/bin/env python3
"""
Generates the "professorial narrator voice" audio for every lesson and for
the AI Universe explainer, using Piper — a free, open-source, offline
neural text-to-speech engine (MIT-licensed, no account, no API key; see
CLAUDE.md section 2 and claude/change-plan-sept1.md section 4 for why this
is the right tool for a static, no-paid-API site).

Why this runs in GitHub Actions and not anywhere else: synthesis itself is
local and keyless, but the Piper *voice models* (~60-100MB .onnx files per
language) are fetched once from Hugging Face's public model hub, and this
project's own build/dev sandbox has no route to huggingface.co. GitHub
Actions runners do. So this follows the exact pattern already used by
scripts/fetch_and_rewrite_news.py (Anthropic API) and
scripts/post_to_instagram.py (Instagram Graph API): a script that only
runs from .github/workflows/generate-narration.yml, with real internet
access, committing its output back to the repo. The one difference from
those two: this script needs no secret at all. Piper is free compute, not
a billed/key-authenticated API.

What it does, end to end:
  1. Reads the plain-prose narration scripts in video/*-lesson-*-script.md
     (one per lesson, EN/PT/ES sections) and the scene table in
     video/ai-universe-script.md (same three languages, table format).
  2. Downloads (and caches) the three Piper voice models chosen in
     claude/change-plan-sept1.md section 4:
       en_US-norman-medium   (English  — deep, calm, "authoritative narrator")
       pt_BR-faber-medium    (Brazilian Portuguese)
       es_ES-davefx-medium   (Spanish — Spain-accented; the clearest option
                               Piper currently ships, flagged here as in the
                               change plan since no Latin-American Spanish
                               voice exists yet)
  3. Synthesizes each narration to WAV with Piper, then encodes to a small
     mono MP3 with ffmpeg (spoken narration doesn't need stereo or a high
     bitrate).
  4. Writes lesson audio to audio/lessons/<lesson-id>-<lang>.mp3 and the
     universe narration to audio/universe/ai-universe-<lang>.mp3.
  5. Patches each lesson's LESSON_AUDIO.urls (and the universe page's own
     audio config, if present) from empty strings to the real generated
     path — the same "empty = coming soon placeholder" contract js/audio.js
     already implements, so a partial run never breaks a page. Only ever
     replaces an *empty* url; never overwrites a URL a human already set.

Safe to run repeatedly: existing voice model downloads are cached, and
audio for a script whose text hasn't changed is regenerated but ends up
byte-for-byte equivalent in practice; the workflow only commits files that
actually changed.
"""
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_DIR = os.path.join(REPO_ROOT, "video")
LESSONS_AUDIO_DIR = os.path.join(REPO_ROOT, "audio", "lessons")
UNIVERSE_AUDIO_DIR = os.path.join(REPO_ROOT, "audio", "universe")
VOICE_CACHE_DIR = os.environ.get(
    "PIPER_VOICE_CACHE", os.path.join(REPO_ROOT, ".piper-voices")
)

HF_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main"

LANGS = ("en", "pt", "es")

LANG_HEADINGS = {
    "en": "## English",
    "pt": "## Português (Brasil)",
    "es": "## Español (Latinoamérica)",
}

# Piper voice IDs chosen in claude/change-plan-sept1.md section 4.
# key -> (huggingface path segments..., voice file stem)
VOICES = {
    "en": ("en", "en_US", "norman", "medium", "en_US-norman-medium"),
    "pt": ("pt", "pt_BR", "faber", "medium", "pt_BR-faber-medium"),
    "es": ("es", "es_ES", "davefx", "medium", "es_ES-davefx-medium"),
}

LESSON_FILENAME_RE = re.compile(
    r"^(beginner|intermediate|expert)-lesson-(\d+)-script\.md$"
)


def log(msg):
    print(f"[generate_narration] {msg}", flush=True)


# --------------------------------------------------------------------------
# Voice model download
# --------------------------------------------------------------------------

def voice_paths(lang):
    _, _, _, _, stem = VOICES[lang]
    model_path = os.path.join(VOICE_CACHE_DIR, f"{stem}.onnx")
    config_path = os.path.join(VOICE_CACHE_DIR, f"{stem}.onnx.json")
    return model_path, config_path


def download(url, dest):
    log(f"downloading {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "ai-tech-school-narration/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp, open(dest, "wb") as f:
            f.write(resp.read())
    except urllib.error.URLError as exc:
        log(f"FAILED to download {url}: {exc}")
        raise


def ensure_voice(lang):
    lang_seg, region_seg, voice_seg, quality_seg, stem = VOICES[lang]
    model_path, config_path = voice_paths(lang)
    os.makedirs(VOICE_CACHE_DIR, exist_ok=True)

    base = f"{HF_BASE}/{lang_seg}/{region_seg}/{voice_seg}/{quality_seg}"
    if not os.path.exists(model_path):
        download(f"{base}/{stem}.onnx", model_path)
    else:
        log(f"{lang}: voice model already cached ({model_path})")

    if not os.path.exists(config_path):
        download(f"{base}/{stem}.onnx.json", config_path)
    else:
        log(f"{lang}: voice config already cached ({config_path})")

    return model_path, config_path


# --------------------------------------------------------------------------
# Script parsing
# --------------------------------------------------------------------------

def extract_lang_section(markdown_text, lang):
    """Returns the raw text between this language's '## Heading' and the
    next '## ' heading (or end of file)."""
    heading = LANG_HEADINGS[lang]
    idx = markdown_text.find(heading)
    if idx == -1:
        return None
    start = idx + len(heading)
    next_idx = markdown_text.find("\n## ", start)
    section = markdown_text[start : next_idx if next_idx != -1 else len(markdown_text)]
    return section.strip()


def prose_narration(section_text):
    """Most lesson scripts (see video/beginner-lesson-2-script.md onward)
    are plain narration paragraphs. Join them into one block, collapsing
    internal blank-line-separated paragraphs onto their own lines so
    Piper's sentence splitter still gets natural pauses."""
    paragraphs = [p.strip() for p in section_text.split("\n\n") if p.strip()]
    return "\n".join(paragraphs)


TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
TABLE_SEPARATOR_RE = re.compile(r"^\|?[\s:-]+\|[\s:|-]+$")


def is_table_format(section_text):
    """beginner-lesson-1-script.md and ai-universe-script.md predate the
    plain-prose narration format (see the note at the top of
    video/beginner-lesson-2-script.md) and are written as a
    Time | On-screen | Narration table instead. Detect that shape so both
    formats can share one pipeline."""
    for raw_line in section_text.splitlines():
        if TABLE_ROW_RE.match(raw_line.strip()) and not TABLE_SEPARATOR_RE.match(raw_line.strip()):
            return True
    return False


def table_narration(section_text):
    """Pull just the narration column (always the last one) out of each
    data row of a Time | On-screen/Focus | Narration table, skipping the
    header row and the '---|---|---' separator row."""
    lines = []
    for raw_line in section_text.splitlines():
        stripped = raw_line.strip()
        if TABLE_SEPARATOR_RE.match(stripped):
            continue
        m = TABLE_ROW_RE.match(stripped)
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if len(cells) < 3:
            continue
        narration = cells[-1]
        if not narration or narration.lower() in ("narration", "narração", "narración"):
            continue
        lines.append(narration)
    return "\n".join(lines)


def extract_narration_text(section_text):
    """Dispatches to the table or plain-prose extractor depending on which
    format this script section was written in — see is_table_format()."""
    if is_table_format(section_text):
        return table_narration(section_text)
    return prose_narration(section_text)


def find_lesson_scripts():
    """Returns [(lesson_id, script_path), ...] sorted for stable output."""
    found = []
    for name in sorted(os.listdir(VIDEO_DIR)):
        m = LESSON_FILENAME_RE.match(name)
        if not m:
            continue
        level, num = m.group(1), m.group(2)
        lesson_id = f"{level}-{num}"
        found.append((lesson_id, os.path.join(VIDEO_DIR, name)))
    return found


# --------------------------------------------------------------------------
# Synthesis
# --------------------------------------------------------------------------

def synthesize_mp3(text, lang, out_mp3_path):
    model_path, config_path = ensure_voice(lang)
    os.makedirs(os.path.dirname(out_mp3_path), exist_ok=True)

    tmp_wav = out_mp3_path + ".tmp.wav"
    cmd = [
        sys.executable,
        "-m",
        "piper",
        "--model",
        model_path,
        "--config",
        config_path,
        "--output_file",
        tmp_wav,
        "--sentence-silence",
        "0.4",
    ]
    log(f"synthesizing -> {out_mp3_path}")
    proc = subprocess.run(cmd, input=text, text=True, capture_output=True)
    if proc.returncode != 0:
        log(proc.stdout)
        log(proc.stderr)
        raise RuntimeError(f"piper failed for {out_mp3_path}")

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-loglevel",
        "error",
        "-i",
        tmp_wav,
        "-ac",
        "1",
        "-codec:a",
        "libmp3lame",
        "-b:a",
        "96k",
        out_mp3_path,
    ]
    proc = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    os.remove(tmp_wav)
    if proc.returncode != 0:
        log(proc.stdout)
        log(proc.stderr)
        raise RuntimeError(f"ffmpeg failed for {out_mp3_path}")


# --------------------------------------------------------------------------
# Patch generated URLs into the HTML pages
# --------------------------------------------------------------------------

def patch_lesson_html(lesson_id, generated_paths):
    level, num = lesson_id.rsplit("-", 1)
    html_path = os.path.join(REPO_ROOT, "levels", level, f"lesson-{num}.html")
    if not os.path.exists(html_path):
        log(f"WARNING: no HTML page for {lesson_id} at {html_path}, skipping URL patch")
        return

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Scope the replacement strictly to the LESSON_AUDIO urls line (not
    # just any "lang: """ in the file — a lesson's PAGE_I18N dictionary
    # could coincidentally contain an empty string under the same key)
    # by matching the whole `urls: { en: "...", pt: "...", es: "..." }`
    # object and rewriting only the languages we generated audio for.
    urls_line_re = re.compile(r"urls:\s*\{[^}]*\}")

    def rewrite_urls_line(m):
        line = m.group(0)
        for lang, rel_path in generated_paths.items():
            # Only replace an *empty* url for this language, so a
            # human-set value (or a value from a previous run) is never
            # clobbered.
            lang_re = re.compile(r"(" + re.escape(lang) + r':\s*")(")')
            line = lang_re.sub(lambda lm, p=rel_path: lm.group(1) + p + '"', line)
        return line

    content = urls_line_re.sub(rewrite_urls_line, content, count=1)

    if content != original:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)
        log(f"patched LESSON_AUDIO urls in {html_path}")
    else:
        log(f"{html_path}: LESSON_AUDIO urls already set, nothing to patch")


def patch_universe_html(generated_paths):
    """ai-universe-video.html doesn't have a narration-audio slot yet (it
    plays the assembled video, which will carry its own muxed audio track
    once video/ is built — see scripts note in CLAUDE.md section 2, item
    6). Nothing to patch here today; this function is a placeholder so
    wiring the universe narration into that page later is a one-line
    addition, not a rediscovery."""
    return


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    lesson_scripts = find_lesson_scripts()
    if not lesson_scripts:
        log("no lesson scripts found under video/ — nothing to do")
    for lesson_id, script_path in lesson_scripts:
        with open(script_path, "r", encoding="utf-8") as f:
            markdown_text = f.read()

        generated_paths = {}
        for lang in LANGS:
            section = extract_lang_section(markdown_text, lang)
            if not section:
                log(f"WARNING: {script_path} has no '{LANG_HEADINGS[lang]}' section")
                continue
            text = extract_narration_text(section)
            if not text:
                continue

            rel_path = f"audio/lessons/{lesson_id}-{lang}.mp3"
            out_path = os.path.join(REPO_ROOT, rel_path)
            synthesize_mp3(text, lang, out_path)
            generated_paths[lang] = rel_path

        patch_lesson_html(lesson_id, generated_paths)

    # AI Universe explainer narration (table-format script).
    universe_script_path = os.path.join(VIDEO_DIR, "ai-universe-script.md")
    if os.path.exists(universe_script_path):
        with open(universe_script_path, "r", encoding="utf-8") as f:
            markdown_text = f.read()

        universe_paths = {}
        for lang in LANGS:
            section = extract_lang_section(markdown_text, lang)
            if not section:
                log(f"WARNING: {universe_script_path} has no '{LANG_HEADINGS[lang]}' section")
                continue
            text = extract_narration_text(section)
            if not text:
                continue

            rel_path = f"audio/universe/ai-universe-{lang}.mp3"
            out_path = os.path.join(REPO_ROOT, rel_path)
            synthesize_mp3(text, lang, out_path)
            universe_paths[lang] = rel_path

        patch_universe_html(universe_paths)
    else:
        log(f"WARNING: {universe_script_path} not found, skipping universe narration")

    log("done")


if __name__ == "__main__":
    main()
