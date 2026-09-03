#!/usr/bin/env python3
"""
Assembles "The AI Universe" explainer video (one MP4 per language) from
material that already exists in this repo — no stock footage, no
generative video API (see CLAUDE.md section 2 for why that's ruled out).

Inputs:
  - diagrams/ai-universe.svg          the single source diagram
  - video/ai-universe-script.md       scene timing + on-screen text + narration
  - audio/universe/ai-universe-<lang>.mp3   narration, produced by
                                       scripts/generate_narration.py (run
                                       that first — this script fails
                                       loudly if the audio is missing)

What it does:
  1. Rasterizes the diagram once at high resolution with rsvg-convert, then
     pads it with matching background color so later crops can extend
     past the drawn edges.
  2. Walks the same 8 scenes the script already times out (title card ->
     Claude core -> Prompts & Chat -> API -> MCP -> Connectors -> Agents
     orbit -> pull back), each scene a slow pan/zoom ("Ken Burns") between
     a start and end crop of that one diagram, matching the ring radii
     actually drawn in the SVG (see SCENES below) — i.e. this isn't a
     generic zoom-and-pan of a photo, the crop boxes are keyed to the
     diagram's real geometry.
  3. Rescales the authored scene durations (which assume ~130 wpm
     English) to the real length of the generated narration for that
     language, so PT/ES — which run longer, per the script's own timing
     note — stay in sync instead of racing ahead of the voice.
  4. Burns in a short on-screen caption per scene (from the script's own
     "on-screen" column) and mixes in the narration track.
  5. Appends a simple end card (AI Tech School + the three skill paths)
     and writes video/ai-universe-<lang>.mp4.

Runs in GitHub Actions for the same reason scripts/generate_narration.py
does: it depends on that script's output. Encoding itself (rsvg-convert,
ffmpeg) needs no network at all once the two apt packages below are
installed — this could run locally too, if audio/universe/ already has
the MP3s.
"""
import os
import re
import subprocess

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIAGRAM_SVG = os.path.join(REPO_ROOT, "diagrams", "ai-universe.svg")
SCRIPT_MD = os.path.join(REPO_ROOT, "video", "ai-universe-script.md")
AUDIO_DIR = os.path.join(REPO_ROOT, "audio", "universe")
OUTPUT_DIR = os.path.join(REPO_ROOT, "video")
WORK_DIR = os.environ.get("UNIVERSE_VIDEO_WORKDIR", "/tmp/universe-video-build")

LANGS = ("en", "pt", "es")
LANG_HEADINGS = {
    "en": "## English",
    "pt": "## Português (Brasil)",
    "es": "## Español (Latinoamérica)",
}

# Diagram geometry (SVG viewBox is 1000x1020, center 500,480 — see
# diagrams/ai-universe.svg's RINGS comment block). Each scene is a crop
# box in SVG units: (cx, cy, half_extent). The video pans/zooms from the
# previous scene's end box to this scene's box over the scene's duration.
# Scene order matches the script table exactly (both EN/PT/ES use the
# same 8 rows in the same order), so this list is language-independent.
BG_COLOR = "#0a0c12"  # diagrams/ai-universe.svg's bgGlow outer stop
CX, CY = 500, 480
SCENES = [
    {"box": (CX, CY, 540)},   # 0: title card, full diagram
    {"box": (CX, CY, 170)},   # 1: Claude core (r=62 + glow)
    {"box": (CX, CY, 190)},   # 2: Prompts & Chat ring (r=100)
    {"box": (CX, CY, 250)},   # 3: API ring (r=165)
    {"box": (CX, CY, 310)},   # 4: MCP ring (r=230)
    {"box": (CX, CY, 430)},   # 5: Connectors ring + chips (r=300)
    {"box": (CX, CY, 460)},   # 6: Agents outer orbit (r=350)
    {"box": (CX, CY, 540)},   # 7: pull back to full diagram
]

RASTER_SCALE = 2   # SVG units -> px (2x is already sharp for a 1080 output crop)
# Padding added on every side, in SVG units, before cropping. 9:16 output
# (see OUT_W/OUT_H below) needs a much taller crop box than the old square
# 1080x1080 did at the widest zoom-out (scenes 0 and 7, half=540): at a
# 16:9 vertical ratio that's a ~960-unit half-height above/below the
# diagram's own 480 center, so 300 of padding isn't enough (500 is, with
# room to spare) — see the "9:16 vertical" note in CLAUDE.md.
PAD_SVG = 500
OUT_W = 1080        # output canvas, px — 9:16 vertical (Reels/TikTok/Shorts
OUT_H = 1920        # framing), changed from the old 1080x1080 square on
                    # 2026-09-03 at Alex's request; see CLAUDE.md.
FPS = 15            # a slow Ken Burns pan doesn't need 30fps, and this keeps
                    # per-language render time reasonable (see write_scene_frames)
END_CARD_SECONDS = 4.0

MASCOT_IMAGE = os.path.join(REPO_ROOT, "social", "aits-mascot.png")
CONNECTOR_SCENE_INDEX = 5  # SCENES[5] == the Connectors ring scene below

# The six connector chips as drawn in diagrams/ai-universe.svg (center +
# half-extent, in SVG units — rect x/y/width/height there, halved). Order
# matches the narration's own listing ("GitHub, Slack, Gmail, Notion, your
# calendar... Composio"), so the pop-in below reveals each chip in the
# order the voice actually names it.
CONNECTOR_CHIPS = [
    ("GitHub", 500, 180, 75, 22),
    ("Slack", 760, 330, 75, 22),
    ("Gmail", 760, 630, 75, 22),
    ("Notion", 500, 780, 75, 22),
    ("Calendar", 240, 630, 75, 22),
    ("Composio", 240, 330, 75, 22),
]
CONNECTOR_GLOW_RGB = (56, 189, 248)  # #38bdf8 — same cyan as the connectors
                                     # ring stroke in the SVG, so the glow
                                     # reads as "part of this ring" rather
                                     # than an unrelated added color.

END_CARD_TEXT = {
    "en": ("AI TECH SCHOOL", "Beginner  ·  Intermediate  ·  Expert"),
    "pt": ("AI TECH SCHOOL", "Iniciante  ·  Intermediário  ·  Avançado"),
    "es": ("AI TECH SCHOOL", "Principiante  ·  Intermedio  ·  Experto"),
}


def log(msg):
    print(f"[build_universe_video] {msg}", flush=True)


def run(cmd, **kwargs):
    proc = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    if proc.returncode != 0:
        log(f"COMMAND FAILED: {' '.join(cmd)}")
        log(proc.stdout)
        log(proc.stderr)
        raise RuntimeError(f"command failed: {cmd[0]}")
    return proc


# --------------------------------------------------------------------------
# Script parsing (time range + on-screen text, per language)
# --------------------------------------------------------------------------

TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
TABLE_SEPARATOR_RE = re.compile(r"^\|?[\s:-]+\|[\s:|-]+$")
TIME_RANGE_RE = re.compile(r"(\d+):(\d+)\s*[–-]\s*(\d+):(\d+)")


def extract_lang_section(markdown_text, lang):
    heading = LANG_HEADINGS[lang]
    idx = markdown_text.find(heading)
    if idx == -1:
        return None
    start = idx + len(heading)
    next_idx = markdown_text.find("\n## ", start)
    return markdown_text[start : next_idx if next_idx != -1 else len(markdown_text)].strip()


def parse_scenes(section_text):
    """Returns [{"duration": seconds, "on_screen": str}, ...] in row order."""
    rows = []
    for raw_line in section_text.splitlines():
        stripped = raw_line.strip()
        if TABLE_SEPARATOR_RE.match(stripped):
            continue
        m = TABLE_ROW_RE.match(stripped)
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if len(cells) != 3:
            continue
        time_cell, on_screen, narration = cells
        tm = TIME_RANGE_RE.search(time_cell)
        if not tm:
            continue  # header row
        start_s = int(tm.group(1)) * 60 + int(tm.group(2))
        end_s = int(tm.group(3)) * 60 + int(tm.group(4))
        rows.append({"duration": max(end_s - start_s, 1), "on_screen": on_screen})
    return rows


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


# --------------------------------------------------------------------------
# Diagram rasterization
# --------------------------------------------------------------------------

def rasterize_diagram():
    os.makedirs(WORK_DIR, exist_ok=True)
    raw_png = os.path.join(WORK_DIR, "diagram_raw.png")
    w = 1000 * RASTER_SCALE
    h = 1020 * RASTER_SCALE
    run(["rsvg-convert", "-w", str(w), "-h", str(h), DIAGRAM_SVG, "-o", raw_png])

    raw = Image.open(raw_png).convert("RGB")
    pad_px = PAD_SVG * RASTER_SCALE
    padded = Image.new("RGB", (w + 2 * pad_px, h + 2 * pad_px), hex_to_rgb(BG_COLOR))
    padded.paste(raw, (pad_px, pad_px))
    padded_path = os.path.join(WORK_DIR, "diagram_padded.png")
    padded.save(padded_path)
    log(f"rasterized + padded diagram -> {padded_path} ({padded.size[0]}x{padded.size[1]})")
    return padded_path


def half_extent_h(half_w):
    """The vertical half-extent matching a given horizontal half-extent at
    the output canvas's aspect ratio (9:16, so taller than it is wide)."""
    return half_w * (OUT_H / OUT_W)


def crop_frame(padded_img, cx, cy, half):
    """Crops a (cx±half, cy±half_h) SVG-space rectangle — sized to the
    output canvas's 9:16 aspect ratio, not a square — out of the padded
    diagram and resizes it to the output canvas."""
    half_h = half_extent_h(half)
    px_cx = (cx + PAD_SVG) * RASTER_SCALE
    px_cy = (cy + PAD_SVG) * RASTER_SCALE
    px_half_w = half * RASTER_SCALE
    px_half_h = half_h * RASTER_SCALE
    box = (px_cx - px_half_w, px_cy - px_half_h, px_cx + px_half_w, px_cy + px_half_h)
    return padded_img.crop(box).resize((OUT_W, OUT_H), Image.Resampling.BILINEAR)


def svg_to_frame_px(px_svg, py_svg, cx, cy, half):
    """Maps an SVG-space point to output-frame pixel coordinates for the
    current pan/zoom box (cx, cy, half) — used to place overlays (the
    connector pop-in glow, etc.) so they track the diagram under the
    camera instead of sitting at a fixed screen position."""
    half_h = half_extent_h(half)
    fx = (px_svg - (cx - half)) / (2 * half) * OUT_W
    fy = (py_svg - (cy - half_h)) / (2 * half_h) * OUT_H
    return fx, fy


def ease_out_back(t):
    """Small overshoot easing (t in [0,1]) so an element "pops" into place
    rather than just fading up linearly."""
    t = max(0.0, min(1.0, t))
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def draw_connector_pop(frame, cx, cy, half, scene_elapsed_s, scene_duration_s):
    """"Light refresh" added 2026-09-03 at Alex's request (the AI Universe
    video was "too basic" — see CLAUDE.md): during the Connectors scene,
    each of the six chips gets a soft glow that pops in behind it, one at
    a time in narration order, instead of the camera just panning past
    six static boxes. Chips themselves never move (they're baked into the
    rasterized diagram) — only the glow halo is drawn per frame, on top of
    the already-cropped frame, positioned via svg_to_frame_px so it tracks
    each chip correctly through the pan/zoom."""
    n = len(CONNECTOR_CHIPS)
    slot = scene_duration_s / n
    pop_duration = min(slot, 0.5)
    px_per_svg_x = OUT_W / (2 * half)
    px_per_svg_y = OUT_H / (2 * half_extent_h(half))

    overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    any_visible = False

    for i, (_name, chip_cx, chip_cy, chip_hw, chip_hh) in enumerate(CONNECTOR_CHIPS):
        appear_at = i * slot
        if scene_elapsed_s < appear_at:
            continue
        progress = min((scene_elapsed_s - appear_at) / pop_duration, 1.0)
        scale = ease_out_back(progress)
        settle_alpha = min((scene_elapsed_s - appear_at) / (pop_duration * 0.6), 1.0)
        alpha = max(settle_alpha, 0.0) * 0.55  # glow tops out under full
                                                # opacity so it stays a
                                                # highlight, not a block
        if alpha <= 0:
            continue
        any_visible = True
        gx, gy = svg_to_frame_px(chip_cx, chip_cy, cx, cy, half)
        base_w = chip_hw * 2.4 * scale * px_per_svg_x
        base_h = chip_hh * 2.6 * scale * px_per_svg_y
        # Three concentric rounded rects standing in for a soft blur —
        # cheap per-frame (no actual Gaussian blur needed at this scale).
        for step, mult in ((0, 1.0), (1, 0.6), (2, 0.35)):
            a = int(255 * alpha * mult)
            if a <= 0:
                continue
            w = base_w * (1 + step * 0.4)
            h = base_h * (1 + step * 0.4)
            draw.rounded_rectangle(
                [gx - w / 2, gy - h / 2, gx + w / 2, gy + h / 2],
                radius=min(w, h) / 2,
                fill=CONNECTOR_GLOW_RGB + (a,),
            )

    if not any_visible:
        return frame
    return Image.alpha_composite(frame.convert("RGBA"), overlay).convert("RGB")


def draw_mascot_intro(frame, elapsed_s, scene_duration_s):
    """Puts the AITS mascot in the bottom-right corner during the opening
    title-card scene, fading in as the "Hi, I'm AITS" line starts and
    fading back out before the pan into the Claude core begins — a small,
    cheap way to put a face to the narration voice without touching the
    diagram itself. Part of the same 2026-09-03 "light refresh" as the
    connector pop-in above."""
    fade = 0.5
    if elapsed_s < fade:
        alpha = elapsed_s / fade
    elif elapsed_s > scene_duration_s - fade:
        alpha = max(scene_duration_s - elapsed_s, 0.0) / fade
    else:
        alpha = 1.0
    alpha = max(0.0, min(1.0, alpha))
    if alpha <= 0:
        return frame

    mascot = _load_mascot()
    if mascot is None:
        return frame
    size = int(OUT_W * 0.22)
    resized = mascot.resize((size, size), Image.Resampling.LANCZOS)
    if alpha < 1.0:
        r, g, b, a = resized.split()
        a = a.point(lambda v: int(v * alpha))
        resized = Image.merge("RGBA", (r, g, b, a))
    margin = int(OUT_W * 0.05)
    pos = (OUT_W - size - margin, OUT_H - size - margin)
    base = frame.convert("RGBA")
    base.paste(resized, pos, resized)
    return base.convert("RGB")


_MASCOT_CACHE = {}


def _load_mascot():
    if "img" not in _MASCOT_CACHE:
        if os.path.exists(MASCOT_IMAGE):
            _MASCOT_CACHE["img"] = Image.open(MASCOT_IMAGE).convert("RGBA")
        else:
            log(f"WARNING: {MASCOT_IMAGE} not found — skipping mascot overlay")
            _MASCOT_CACHE["img"] = None
    return _MASCOT_CACHE["img"]


# --------------------------------------------------------------------------
# Frame sequence + encode
# --------------------------------------------------------------------------

def lerp(a, b, t):
    return a + (b - a) * t


def write_scene_frames(padded_img, prev_box, this_box, duration_s, stdin_pipe, scene_index=None):
    """Streams this scene's frames straight into ffmpeg's stdin as raw
    RGB24 bytes — no per-frame PNG encode/decode/disk-write, which is by
    far the slowest part of generating a few thousand frames. Returns the
    frame count actually written.

    scene_index selects the per-scene overlay (mascot intro on the title
    card, the connector pop-in on the Connectors scene) — see
    draw_mascot_intro / draw_connector_pop above."""
    n_frames = max(int(round(duration_s * FPS)), 1)
    for i in range(n_frames):
        t = i / max(n_frames - 1, 1)
        # ease-in-out so the pan doesn't feel mechanical
        eased = t * t * (3 - 2 * t)
        cx = lerp(prev_box[0], this_box[0], eased)
        cy = lerp(prev_box[1], this_box[1], eased)
        half = lerp(prev_box[2], this_box[2], eased)
        frame = crop_frame(padded_img, cx, cy, half)
        elapsed_s = i / FPS
        if scene_index == 0:
            frame = draw_mascot_intro(frame, elapsed_s, duration_s)
        elif scene_index == CONNECTOR_SCENE_INDEX:
            frame = draw_connector_pop(frame, cx, cy, half, elapsed_s, duration_s)
        stdin_pipe.write(frame.tobytes())
    return n_frames


def build_end_card(lang, out_path):
    img = Image.new("RGB", (OUT_W, OUT_H), hex_to_rgb(BG_COLOR))
    draw = ImageDraw.Draw(img)
    title, subtitle = END_CARD_TEXT[lang]

    def load_font(size, bold=True):
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        for c in candidates:
            if os.path.exists(c):
                return ImageFont.truetype(c, size)
        return ImageFont.load_default()

    title_font = load_font(64, bold=True)
    subtitle_font = load_font(30, bold=False)

    # Mascot above the title — ties the end card back to the narration
    # voice (AITS), added in the same 2026-09-03 "light refresh" as the
    # title-card intro and connector pop-in. Center of gravity sits a bit
    # above the vertical midpoint since OUT_H is now much taller than it
    # is wide (9:16), not square.
    mascot = _load_mascot()
    mascot_h = 0
    if mascot is not None:
        mascot_size = int(OUT_W * 0.32)
        resized = mascot.resize((mascot_size, mascot_size), Image.Resampling.LANCZOS)
        img.paste(resized, ((OUT_W - mascot_size) // 2, int(OUT_H * 0.34)), resized)
        mascot_h = mascot_size

    title_y = int(OUT_H * 0.34) + mascot_h + 50
    tw = draw.textlength(title, font=title_font)
    draw.text(((OUT_W - tw) / 2, title_y), title, font=title_font, fill=(244, 246, 251))
    sw = draw.textlength(subtitle, font=subtitle_font)
    draw.text(((OUT_W - sw) / 2, title_y + 90), subtitle, font=subtitle_font, fill=(154, 163, 184))

    img.save(out_path)


CAPTION_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def shorten_caption(text):
    """The script's "on-screen / diagram focus" column is written for a
    reader following along with the full table, so a few rows carry a
    parenthetical aside (e.g. "...Connectors (GitHub, Slack, Gmail,
    Notion, Calendar, Composio chips)") or a second clause after a comma
    ("Pull back..., then cut to...") that's too long to burn in as one
    line without overflowing a 1080px-wide frame. The diagram itself
    already shows the connector names and the narration says the rest,
    so trimming to the first clause loses nothing on screen."""
    for sep in (" (", ", then", ", depois", ", luego"):
        idx = text.find(sep)
        if idx != -1:
            text = text[:idx]
    return text.strip().rstrip(",")


def caption_font_size(text):
    if len(text) > 45:
        return 26
    if len(text) > 30:
        return 30
    return 34


def caption_drawtext_filter(captions):
    """captions: [(start_s, end_s, text), ...]. Returns an ffmpeg
    drawtext filter chain burning in each scene's on-screen text near the
    bottom of the frame, one caption visible at a time.

    y=h-300 (not the old square format's h-140) keeps the caption clear of
    the bottom ~15% of a 1920-tall 9:16 frame — the safe zone Reels/TikTok/
    Shorts reserve for their own caption/like/share UI, so text stays
    readable if this MP4 is ever reused as a native vertical post."""
    parts = []
    for start_s, end_s, raw_text in captions:
        text = shorten_caption(raw_text)
        escaped = (
            text.replace("\\", "\\\\")
            .replace(":", "\\:")
            .replace("'", "’")
            .replace(",", "\\,")
        )
        parts.append(
            "drawtext=fontfile='%s':text='%s':fontcolor=white:fontsize=%d:"
            "box=1:boxcolor=black@0.45:boxborderw=16:"
            "x=(w-text_w)/2:y=h-300:enable='between(t,%.2f,%.2f)'"
            % (CAPTION_FONT, escaped, caption_font_size(text), start_s, end_s)
        )
    return ",".join(parts)


def ffprobe_duration(path):
    proc = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            path,
        ]
    )
    return float(proc.stdout.strip())


def build_video_for_lang(lang, padded_img, script_scenes):
    audio_path = os.path.join(AUDIO_DIR, f"ai-universe-{lang}.mp3")
    if not os.path.exists(audio_path):
        log(f"WARNING: {audio_path} not found — run scripts/generate_narration.py first. Skipping {lang}.")
        return None

    audio_duration = ffprobe_duration(audio_path)
    narration_budget = max(audio_duration - END_CARD_SECONDS, 5.0)
    authored_total = sum(s["duration"] for s in script_scenes)
    scale = narration_budget / authored_total

    os.makedirs(WORK_DIR, exist_ok=True)

    # Work out every scene's real (rescaled) duration and caption window
    # first, so the ffmpeg process (and its drawtext filter, which needs
    # the full caption list up front) can be started before any frames
    # are generated.
    captions = []
    elapsed = 0.0
    scene_durations = []
    for scene_script in script_scenes:
        duration = scene_script["duration"] * scale
        scene_durations.append(duration)
        captions.append((elapsed, elapsed + duration, scene_script["on_screen"]))
        elapsed += duration

    # Frames are streamed straight into ffmpeg's stdin as raw RGB24 bytes
    # instead of written to disk as individual PNGs first — with a few
    # thousand frames per language, per-frame PNG encode+disk I/O was by
    # far the slowest part of building this video; piping raw frames
    # avoids it entirely.
    diagram_video = os.path.join(WORK_DIR, f"diagram_{lang}.mp4")
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-loglevel",
        "error",
        "-f",
        "rawvideo",
        "-pixel_format",
        "rgb24",
        "-video_size",
        f"{OUT_W}x{OUT_H}",
        "-framerate",
        str(FPS),
        "-i",
        "-",
        "-vf",
        caption_drawtext_filter(captions),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        diagram_video,
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    prev_box = SCENES[0]["box"]
    for scene_index, (scene_def, duration) in enumerate(zip(SCENES, scene_durations)):
        write_scene_frames(padded_img, prev_box, scene_def["box"], duration, proc.stdin, scene_index)
        prev_box = scene_def["box"]
    proc.stdin.close()
    stderr = proc.stderr.read()
    returncode = proc.wait()
    if returncode != 0:
        log(stderr.decode("utf-8", "replace"))
        raise RuntimeError(f"ffmpeg (raw frame encode) failed for {lang}")

    end_card_png = os.path.join(WORK_DIR, f"end_card_{lang}.png")
    build_end_card(lang, end_card_png)
    end_card_video = os.path.join(WORK_DIR, f"end_card_{lang}.mp4")
    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-loop",
            "1",
            "-i",
            end_card_png,
            "-t",
            str(END_CARD_SECONDS),
            "-vf",
            f"fps={FPS}",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            end_card_video,
        ]
    )

    concat_list = os.path.join(WORK_DIR, f"concat_{lang}.txt")
    with open(concat_list, "w") as f:
        f.write(f"file '{diagram_video}'\n")
        f.write(f"file '{end_card_video}'\n")

    silent_video = os.path.join(WORK_DIR, f"silent_{lang}.mp4")
    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            concat_list,
            "-c",
            "copy",
            silent_video,
        ]
    )

    out_path = os.path.join(OUTPUT_DIR, f"ai-universe-{lang}.mp4")
    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            silent_video,
            "-i",
            audio_path,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            out_path,
        ]
    )
    log(f"wrote {out_path}")
    return f"video/ai-universe-{lang}.mp4"


def patch_urls_block(file_path, marker_re, generated_paths, label):
    """Shared HTML-patch helper: finds the first `urls: { en: "...", ... }`
    object following marker_re and replaces only the languages in
    generated_paths whose current value is empty — never overwriting a
    URL a human (or an earlier run) already set. Mirrors
    scripts/generate_narration.py's patch_lesson_html."""
    if not os.path.exists(file_path):
        log(f"WARNING: {file_path} not found, skipping {label} URL patch")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    marker_match = marker_re.search(content)
    if not marker_match:
        log(f"WARNING: {label} marker not found in {file_path}, skipping URL patch")
        return

    urls_line_re = re.compile(r"urls:\s*\{[^}]*\}")
    tail = content[marker_match.end() :]
    urls_match = urls_line_re.search(tail)
    if not urls_match:
        log(f"WARNING: no urls: {{...}} block found after {label} marker in {file_path}")
        return

    line = urls_match.group(0)
    for lang, rel_path in generated_paths.items():
        lang_re = re.compile(r"(" + re.escape(lang) + r':\s*")(")')
        line = lang_re.sub(lambda m, p=rel_path: m.group(1) + p + '"', line)

    abs_start = marker_match.end() + urls_match.start()
    abs_end = marker_match.end() + urls_match.end()
    content = content[:abs_start] + line + content[abs_end:]

    if content != original:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        log(f"patched {label} urls in {file_path}")
    else:
        log(f"{file_path}: {label} urls already set, nothing to patch")


def patch_video_pages(generated_paths):
    """Wires the freshly-built MP4s into the two places that reference
    them: the dedicated AI Universe video page's own config, and the
    shared AI_UNIVERSE_CONFIG in js/video.js that each level hub page's
    course-intro slot reads via ATS.video.renderInto()."""
    if not generated_paths:
        return

    patch_urls_block(
        os.path.join(REPO_ROOT, "ai-universe-video.html"),
        re.compile(r"var AI_UNIVERSE_VIDEO\s*=\s*\{"),
        generated_paths,
        "ai-universe-video.html AI_UNIVERSE_VIDEO",
    )
    patch_urls_block(
        os.path.join(REPO_ROOT, "js", "video.js"),
        re.compile(r"var AI_UNIVERSE_CONFIG\s*=\s*\{"),
        generated_paths,
        "js/video.js AI_UNIVERSE_CONFIG",
    )


def main():
    if not os.path.exists(CAPTION_FONT):
        raise RuntimeError(
            f"{CAPTION_FONT} not found — install the fonts-dejavu-core apt "
            "package (see .github/workflows/generate-universe-video.yml)"
        )

    with open(SCRIPT_MD, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    padded_path = rasterize_diagram()
    padded_img = Image.open(padded_path)

    generated_paths = {}
    for lang in LANGS:
        section = extract_lang_section(markdown_text, lang)
        if not section:
            log(f"WARNING: no '{LANG_HEADINGS[lang]}' section in {SCRIPT_MD}")
            continue
        scenes = parse_scenes(section)
        if len(scenes) != len(SCENES):
            log(
                f"WARNING: {lang} has {len(scenes)} scenes, expected {len(SCENES)} "
                "(script table changed shape?) — skipping"
            )
            continue
        rel_path = build_video_for_lang(lang, padded_img, scenes)
        if rel_path:
            generated_paths[lang] = rel_path

    patch_video_pages(generated_paths)

    log("done")


if __name__ == "__main__":
    main()
