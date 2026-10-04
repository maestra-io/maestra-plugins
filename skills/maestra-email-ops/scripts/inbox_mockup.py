#!/usr/bin/env python3
"""
Inbox-style mockup of a Maestra email: the email as it would look opened in a phone mail app,
for showing a client or a teammate. With two inputs it also builds a before/after image.

Input  — the temporary `htmlUrl` (or a downloaded .html file) from `visual_template_preview`,
         one for the new version (--after) and optionally one for the old version (--before).
Output — <prefix>-after.png, <prefix>-before.png and <prefix>-before-after.png in --out-dir,
         each with a small Maestra badge in the bottom-right corner (--no-logo to leave it out).

What the script does to the backend render, and nothing else:
  * decodes e-mail addresses that the CDN obfuscated ("[email protected]");
  * replaces editor sample values inside personalization chips with the --replace pairs and
    removes the dashed chip outline, so the picture reads as a received email;
  * puts a phone mail-app header above it (status bar, Inbox, sender, recipient, subject);
  * screenshots the whole page with Playwright/Chromium at phone width.
The email's own markup is never rewritten or assembled by hand.

Usage:
    python3 inbox_mockup.py --after <htmlUrl|file> [--before <htmlUrl|file>] --list-chips
    python3 inbox_mockup.py --after <htmlUrl|file> [--before <htmlUrl|file>] \
        --sender "Brand Name" --subject "Sarah, Thank You" --to "Sarah" \
        --replace "Hello Name!=Hello, Sarah!" --replace "330770=481527" \
        [--accent "#E71F61"] [--time "10:24 AM"] [--out-dir .] [--prefix email-mockup]

Fallback without Playwright/Chromium (exit code 3 tells you to use it):
    python3 inbox_mockup.py --after-png <mobile snapshot url|file> [--before-png <...>] ...
    — puts the preview's mobile snapshots side by side with BEFORE/AFTER labels and the badge
    (Pillow only). The editor's sample values and chip outlines stay visible in this mode.
"""

import argparse
import asyncio
import html as htmlmod
import io
import os
import re
import sys
import urllib.request
from pathlib import Path

UA = "maestra-email-ops/inbox_mockup.py"
LOGO = Path(__file__).resolve().parent.parent / "assets" / "maestra-badge.png"
CANVAS_BG = "#F2F2F5"


def fetch(src: str) -> bytes:
    if re.match(r"^https?://", src):
        req = urllib.request.Request(src, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    return Path(src).read_bytes()


def cf_decode(hexstr: str) -> str:
    key = int(hexstr[:2], 16)
    return "".join(chr(int(hexstr[i:i + 2], 16) ^ key) for i in range(2, len(hexstr), 2))


def decode_obfuscated(s: str) -> str:
    s = re.sub(r'<script[^>]*email-decode[^>]*>\s*</script>', "", s)
    s = re.sub(r'<a [^>]*class="__cf_email__"[^>]*data-cfemail="([0-9a-f]+)"[^>]*>.*?</a>',
               lambda m: cf_decode(m.group(1)), s, flags=re.S)
    s = re.sub(r'<a href="/cdn-cgi/l/email-protection"[^>]*data-cfemail="([0-9a-f]+)"[^>]*>.*?</a>',
               lambda m: cf_decode(m.group(1)), s, flags=re.S)
    s = re.sub(r'<span class="__cf_email__" data-cfemail="([0-9a-f]+)">.*?</span>',
               lambda m: cf_decode(m.group(1)), s, flags=re.S)
    # links of the form href="/cdn-cgi/l/email-protection#<hex>"
    s = re.sub(r'href="/cdn-cgi/l/email-protection#([0-9a-f]+)"',
               lambda m: 'href="mailto:%s"' % cf_decode(m.group(1)), s)
    return s


CHIP_RE = re.compile(r'<span class="parameter-preview">(.*?)</span>', re.S)


def chips(s: str):
    seen = []
    for m in CHIP_RE.finditer(s):
        t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if t and t not in seen:
            seen.append(t)
    return seen


def apply_replacements(s: str, pairs):
    def sub(m):
        inner = m.group(1)
        text = re.sub(r"<[^>]+>", "", inner).strip()
        for old, new in pairs:
            if text == old:
                return htmlmod.escape(new)
        return inner
    return CHIP_RE.sub(sub, s)


CHIP_CSS = ("<style>.parameter-preview{outline:none!important;border:none!important;"
            "padding:0!important;border-radius:0!important}"
            "html,body{margin:0!important;padding:0!important}</style>")


def initials(name: str) -> str:
    parts = [p for p in re.split(r"\s+", name.strip()) if p]
    return "".join(p[0] for p in parts[:2]).upper() or "M"


def header_html(a) -> str:
    e = htmlmod.escape
    return f"""
<div style="font-family:-apple-system,'SF Pro Text',Inter,Helvetica,Arial,sans-serif;background:#fff;color:#000;-webkit-font-smoothing:antialiased;">
  <div style="height:47px;display:flex;align-items:center;justify-content:space-between;padding:0 30px 0 34px;font-weight:600;font-size:16px;letter-spacing:-0.2px;">
    <span>9:41</span>
    <span style="display:flex;gap:6px;align-items:center;">
      <svg width="18" height="12" viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5.5" width="3" height="6.5" rx="1"/><rect x="10" y="3" width="3" height="9" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/></svg>
      <svg width="16" height="12" viewBox="0 0 16 12"><path d="M8 2.2c2.3 0 4.4.9 6 2.4l1.2-1.3C13.3 1.5 10.8.4 8 .4S2.7 1.5.8 3.3L2 4.6c1.6-1.5 3.7-2.4 6-2.4z"/><path d="M8 5.7c1.4 0 2.6.5 3.6 1.4l1.2-1.3C11.5 4.6 9.8 3.9 8 3.9s-3.5.7-4.8 1.9l1.2 1.3c1-.9 2.2-1.4 3.6-1.4z"/><path d="M8 9.2c.5 0 1 .2 1.3.5L8 11.2 6.7 9.7c.3-.3.8-.5 1.3-.5z"/></svg>
      <svg width="27" height="13" viewBox="0 0 27 13"><rect x="0.5" y="0.5" width="23" height="12" rx="3.5" fill="none" stroke="#000" stroke-opacity=".4"/><rect x="2" y="2" width="20" height="9" rx="2"/><path d="M25 4.5v4c.8-.3 1.3-1.1 1.3-2s-.5-1.7-1.3-2z" fill-opacity=".4"/></svg>
    </span>
  </div>
  <div style="height:44px;display:flex;align-items:center;justify-content:space-between;padding:0 16px 0 10px;color:#007AFF;font-size:17px;">
    <span style="display:flex;align-items:center;gap:4px;"><svg width="12" height="20" viewBox="0 0 12 20"><path d="M10 2 2 10l8 8" stroke="#007AFF" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>Inbox</span>
    <span style="display:flex;gap:22px;align-items:center;">
      <svg width="16" height="20" viewBox="0 0 16 20"><path d="M2 19V2h12l-3 4.5L14 11H2" stroke="#007AFF" stroke-width="1.8" fill="none" stroke-linejoin="round"/></svg>
      <svg width="20" height="18" viewBox="0 0 20 18"><path d="M2 5h16l-1.5 12h-13zM1 2.5h18M7 2.5V1h6v1.5" stroke="#007AFF" stroke-width="1.8" fill="none" stroke-linejoin="round"/></svg>
    </span>
  </div>
  <div style="padding:6px 16px 14px;border-bottom:1px solid #E5E5EA;">
    <div style="display:flex;gap:12px;align-items:flex-start;">
      <div style="width:42px;height:42px;border-radius:50%;background:{e(a.accent)};color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:17px;flex:none;">{e(initials(a.sender))}</div>
      <div style="flex:1;min-width:0;">
        <div style="display:flex;justify-content:space-between;align-items:baseline;gap:8px;">
          <span style="font-weight:600;font-size:17px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{e(a.sender)}</span>
          <span style="color:#8E8E93;font-size:14px;flex:none;">{e(a.time)}</span>
        </div>
        <div style="color:#8E8E93;font-size:14px;margin-top:2px;">To: {e(a.to)}</div>
      </div>
    </div>
    <div style="font-weight:700;font-size:20px;margin-top:14px;letter-spacing:-0.3px;">{e(a.subject)}</div>
  </div>
</div>
"""


def prepare(raw: str, a) -> str:
    s = decode_obfuscated(raw)
    s = apply_replacements(s, a.pairs)
    s = s.replace("</head>", CHIP_CSS + "</head>", 1) if "</head>" in s else CHIP_CSS + s
    s, n = re.subn(r"(<body[^>]*>)", lambda m: m.group(1) + header_html(a), s, count=1)
    if not n:
        s = header_html(a) + s
    return s


async def shoot(pages, a):
    from playwright.async_api import async_playwright
    out = {}
    async with async_playwright() as p:
        browser = None
        errors = []
        for kwargs in ({}, {"channel": "chrome"}, {"executable_path": os.environ.get("MAESTRA_CHROMIUM", "")}):
            if "executable_path" in kwargs and not kwargs["executable_path"]:
                continue
            try:
                browser = await p.chromium.launch(**kwargs)
                break
            except Exception as ex:  # noqa: BLE001
                errors.append(str(ex).splitlines()[0])
        if browser is None:
            raise RuntimeError("; ".join(errors))
        for key, html_text in pages.items():
            tmp = Path(a.out_dir) / f".{a.prefix}-{key}.html"
            tmp.write_text(html_text, encoding="utf-8")
            pg = await browser.new_page(viewport={"width": a.width, "height": 844},
                                        device_scale_factor=a.scale)
            await pg.goto(tmp.resolve().as_uri(), wait_until="networkidle", timeout=60000)
            await pg.wait_for_timeout(600)
            text = await pg.inner_text("body")
            for bad in ("email protected", "[email"):
                if bad in text:
                    print(f"warning: {key}: an obfuscated address is still visible", file=sys.stderr)
            path = Path(a.out_dir) / f"{a.prefix}-{key}.png"
            await pg.screenshot(path=str(path), full_page=True)
            await pg.close()
            tmp.unlink(missing_ok=True)
            out[key] = path
        await browser.close()
    return out


def load_logo(height):
    """The Maestra badge scaled to `height` px, or None when it is switched off or missing."""
    if height <= 0 or not LOGO.exists():
        return None
    from PIL import Image
    logo = Image.open(LOGO).convert("RGBA")
    return logo.resize((round(logo.width * height / logo.height), height), Image.LANCZOS)


def add_logo_band(path, logo, band=96, margin=32):
    """Single mockup: a light band under the screenshot with the badge in the bottom-right corner."""
    if logo is None:
        return path
    from PIL import Image
    img = Image.open(path).convert("RGB")
    out = Image.new("RGB", (img.width, img.height + band), CANVAS_BG)
    out.paste(img, (0, 0))
    out.paste(logo, (img.width - margin - logo.width, img.height + (band - logo.height) // 2), logo)
    out.save(path, optimize=True)
    return path


def side_by_side(before_img, after_img, out_path, labels=("BEFORE", "AFTER"), accent="#E71F61", logo=None):
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    b, a_ = before_img.convert("RGB"), after_img.convert("RGB")
    if b.width != a_.width:
        b = b.resize((a_.width, round(b.height * a_.width / b.width)))
    w, pad, gap, label_h = a_.width, 70, 80, 120
    bottom = pad + (logo.height + 40 if logo is not None else 0)
    canvas = Image.new("RGB", (pad * 2 + w * 2 + gap, max(b.height, a_.height) + pad + bottom + label_h), CANVAS_BG)
    font = None
    for cand in ("Inter-Bold.otf", "/usr/share/fonts/opentype/inter/Inter-Bold.otf", "DejaVuSans-Bold.ttf",
                 "Arial Bold.ttf", "arialbd.ttf", "Helvetica.ttc"):
        try:
            font = ImageFont.truetype(cand, 44)
            break
        except OSError:
            continue
    font = font or ImageFont.load_default()
    d = ImageDraw.Draw(canvas)
    for img, x, label, color in ((b, pad, labels[0], "#8E8E93"), (a_, pad + w + gap, labels[1], accent)):
        y = pad + label_h
        shadow = Image.new("L", canvas.size, 0)
        ImageDraw.Draw(shadow).rounded_rectangle((x, y + 8, x + img.width, y + img.height + 8), 40, fill=90)
        canvas.paste(Image.new("RGB", canvas.size, "#C9C9D1"), (0, 0), shadow.filter(ImageFilter.GaussianBlur(18)))
        mask = Image.new("L", img.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, img.width - 1, img.height - 1), 40, fill=255)
        canvas.paste(img, (x, y), mask)
        tw = d.textlength(label, font=font)
        d.text((x + (img.width - tw) / 2, pad + 20), label, font=font, fill=color)
    if logo is not None:
        canvas.paste(logo, (canvas.width - pad - logo.width, canvas.height - pad - logo.height), logo)
    canvas.save(out_path, optimize=True)
    return out_path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--after", help="htmlUrl or .html of the new version")
    ap.add_argument("--before", help="htmlUrl or .html of the old version")
    ap.add_argument("--after-png", help="fallback: mobile snapshot of the new version")
    ap.add_argument("--before-png", help="fallback: mobile snapshot of the old version")
    ap.add_argument("--list-chips", action="store_true", help="print the sample values in chips and exit")
    ap.add_argument("--sender", default="Sender")
    ap.add_argument("--subject", default="")
    ap.add_argument("--to", default="Sarah")
    ap.add_argument("--time", default="10:24 AM")
    ap.add_argument("--accent", default="#E71F61", help="avatar and AFTER label colour, #RRGGBB")
    ap.add_argument("--replace", action="append", default=[], metavar="OLD=NEW",
                    help="replace a chip's sample value; repeatable")
    ap.add_argument("--width", type=int, default=390)
    ap.add_argument("--scale", type=float, default=2)
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--prefix", default="email-mockup")
    ap.add_argument("--labels", default="BEFORE,AFTER")
    ap.add_argument("--no-logo", action="store_true", help="leave out the Maestra badge")
    a = ap.parse_args()
    a.pairs = []
    for r in a.replace:
        if "=" not in r:
            ap.error(f"--replace needs OLD=NEW, got {r!r}")
        old, new = r.split("=", 1)
        a.pairs.append((old.strip(), new))
    labels = tuple(x.strip() for x in a.labels.split(",", 1)) if "," in a.labels else ("BEFORE", "AFTER")
    Path(a.out_dir).mkdir(parents=True, exist_ok=True)

    if a.after_png or a.before_png:
        try:
            from PIL import Image
        except ImportError:
            print("Pillow is not installed: install it (pip install pillow) for the fallback.", file=sys.stderr)
            sys.exit(2)
        if not (a.after_png and a.before_png):
            print("fallback mode needs both --before-png and --after-png", file=sys.stderr)
            sys.exit(2)
        b = Image.open(io.BytesIO(fetch(a.before_png)))
        n = Image.open(io.BytesIO(fetch(a.after_png)))
        logo = None if a.no_logo else load_logo(round(48 * n.width / 780))
        if not a.no_logo and logo is None:
            print(f"warning: badge not found at {LOGO}; the image is made without it", file=sys.stderr)
        out = side_by_side(b, n, Path(a.out_dir) / f"{a.prefix}-before-after.png", labels, a.accent, logo)
        print(out)
        return

    if not a.after:
        ap.error("--after is required")
    sources = {"after": a.after}
    if a.before:
        sources["before"] = a.before
    raw = {k: decode_obfuscated(fetch(v).decode("utf-8", errors="replace")) for k, v in sources.items()}

    if a.list_chips:
        for k, s in raw.items():
            print(f"{k}:")
            for c in chips(s):
                print(f"  {c}")
        return

    pages = {k: prepare(s, a) for k, s in raw.items()}
    try:
        import playwright  # noqa: F401
    except ImportError:
        print("Playwright is not installed. Use the fallback: --before-png/--after-png with the "
              "preview's mobile snapshot links.", file=sys.stderr)
        sys.exit(3)
    try:
        shots = asyncio.run(shoot(pages, a))
    except Exception as ex:  # noqa: BLE001
        print(f"Chromium could not start ({ex}). Use the fallback: --before-png/--after-png with the "
              "preview's mobile snapshot links.", file=sys.stderr)
        sys.exit(3)
    try:
        from PIL import Image
    except ImportError:
        for k in ("before", "after"):
            if k in shots:
                print(shots[k])
        print("Pillow is not installed: the images are ready without the Maestra badge, and the "
              "side-by-side one was skipped.", file=sys.stderr)
        return
    logo = None if a.no_logo else load_logo(round(48 * a.scale / 2))
    if not a.no_logo and logo is None:
        print(f"warning: badge not found at {LOGO}; images are made without it", file=sys.stderr)
    if "before" in shots:
        out = side_by_side(Image.open(shots["before"]), Image.open(shots["after"]),
                           Path(a.out_dir) / f"{a.prefix}-before-after.png", labels, a.accent, logo)
    for k in ("before", "after"):
        if k in shots:
            add_logo_band(shots[k], logo)
            print(shots[k])
    if "before" in shots:
        print(out)


if __name__ == "__main__":
    main()
