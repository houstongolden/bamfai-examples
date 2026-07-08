#!/usr/bin/env python3
"""Render a BAMF post-review page from a review.json file.

Usage:
    python3 render.py review.json [-o review.html] [--open]

Stdlib only — no dependencies. See README.md for the review.json schema
and sample.review.json for a working example.

Line-break fidelity is the whole point: a blank line in post content
becomes a paragraph gap, a single newline becomes a tight stacked break,
exactly as LinkedIn renders them. Do not "clean up" whitespace in content.
"""
import argparse
import base64
import html
import json
import pathlib
import subprocess
import sys
import urllib.request

TEMPLATE = pathlib.Path(__file__).parent / "template.html"


def render_breaks(text):
    """Blank line -> new <p>; single newline survives inside <p> via pre-wrap."""
    blocks = [b for b in (text or "").replace("\r\n", "\n").split("\n\n") if b.strip()]
    return "\n".join(f"<p>{html.escape(b.strip(chr(10)))}</p>" for b in blocks)


def break_stats(text):
    blocks = [b for b in (text or "").split("\n\n") if b.strip()]
    tight = sum(b.strip("\n").count("\n") for b in blocks)
    return len(blocks), tight


def fetch_avatar(url, timeout=10):
    """Fetch avatar and return a data URI, or None on any failure."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "bamf-review-render/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            ctype = r.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
        if not ctype.startswith("image/") or not data:
            return None
        return f"data:{ctype};base64,{base64.b64encode(data).decode()}"
    except Exception:
        return None


def initials_avatar(name):
    """SVG initials circle as a data URI fallback."""
    parts = [p for p in (name or "").split() if p]
    init = html.escape("".join(p[0].upper() for p in parts[:2]) or "?")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="92" height="92">'
        '<circle cx="46" cy="46" r="46" fill="#6b7280"/>'
        f'<text x="46" y="47" fill="#fff" font-family="-apple-system,Helvetica,Arial"'
        f' font-size="34" font-weight="600" text-anchor="middle"'
        f' dominant-baseline="central">{init}</text></svg>'
    )
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def media_html(media):
    if not media:
        return ""
    items = []
    for m in media:
        src = m.get("data_uri") or m.get("url") or ""
        if not src:
            continue
        cap = f'<div class="cap">{html.escape(m["caption"])}</div>' if m.get("caption") else ""
        items.append(f'<div class="media"><img src="{html.escape(src)}" alt="'
                     f'{html.escape(m.get("alt", ""))}">{cap}</div>')
    return "".join(items)


def build(review):
    tpl = TEMPLATE.read_text()
    creator = review.get("creator", {})
    name = creator.get("name", "Creator")

    avatar_uri = None
    if creator.get("avatar_url"):
        avatar_uri = fetch_avatar(creator["avatar_url"])
    if not avatar_uri:
        avatar_uri = initials_avatar(name)
    avatar_html = f'<img src="{avatar_uri}" alt="">'

    navs, secs = [], []
    for n, post in enumerate(review.get("posts", []), 1):
        key = post.get("key", f"post{n}")
        nav_label = post.get("nav_label") or post.get("title", f"Post {n}")
        badge = post.get("badge", "")
        badge_html = f' <span class="live">{html.escape(badge)}</span>' if badge else ""
        nb, nt = break_stats(post.get("content", ""))
        words = len((post.get("content") or "").split())
        meta_left = post.get("meta_left", "")
        pid = post.get("post_id", "")
        pid_html = f'<div class="pid">post_id <code>{html.escape(pid)}</code></div>' if pid else ""
        fc = post.get("first_comment", "")
        fc_html = (f'<div class="fc-label">First comment</div>\n'
                   f'<div class="fc">{render_breaks(fc)}</div>') if fc else ""

        navs.append(
            f'<li><a href="#{key}" data-target="{key}">'
            f'<span class="dot" aria-hidden="true"></span>'
            f'<span class="n" aria-hidden="true">{n}</span>'
            f'<span class="t">{html.escape(nav_label)}</span></a></li>')
        secs.append(f"""<section id="{key}">
  <div class="tag">{html.escape(post.get("tag", f"Post {n}"))}{badge_html}</div>
  <h2>{html.escape(post.get("title", ""))}</h2>
  <div class="sub">{html.escape(post.get("subtitle", ""))}</div>
  <div class="post">{render_breaks(post.get("content", ""))}{media_html(post.get("media"))}</div>
  {fc_html}
  <div class="foot"><span>{html.escape(meta_left)}</span><span>{words} words · {nb} paragraphs · {nt} tight breaks</span></div>
  {pid_html}
</section>""")

    footer = "\n".join(f"  <p>{note}</p>" for note in review.get("footer_notes", []))

    page = (tpl
            .replace("{{PAGE_TITLE}}", html.escape(review.get("page_title") or review.get("heading", "Post review")))
            .replace("{{PAGE_HEADING}}", html.escape(review.get("heading", "Post concepts")))
            .replace("{{CREATOR_NAME}}", html.escape(name))
            .replace("{{CREATOR_META}}", html.escape(creator.get("meta", "")))
            .replace("{{AVATAR_HTML}}", avatar_html)
            .replace("{{STATUS_HTML}}", review.get("status_html", ""))
            .replace("{{NAV_ITEMS}}", "".join(navs))
            .replace("{{SECTIONS}}", "\n".join(secs))
            .replace("{{FOOTER_HTML}}", footer))
    return page


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("review", help="path to review.json")
    ap.add_argument("-o", "--out", default=None, help="output HTML path (default: <review>.html)")
    ap.add_argument("--open", action="store_true", help="open the result in the default browser (macOS)")
    args = ap.parse_args()

    review = json.loads(pathlib.Path(args.review).read_text())
    out = pathlib.Path(args.out or pathlib.Path(args.review).with_suffix(".html"))
    out.write_text(build(review))
    print(f"wrote {out}")
    if args.open:
        subprocess.run(["open", str(out)], check=False)


if __name__ == "__main__":
    sys.exit(main())
