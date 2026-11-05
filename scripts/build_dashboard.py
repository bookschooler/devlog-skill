#!/usr/bin/env python3
"""Build a single-file HTML dashboard from a devlog folder.

Usage:
    python build_dashboard.py [project_root] [--out PATH]

Reads <project_root>/DEVLOG.md for the project name and folder,
then <folder>/YYYY-MM-DD.md entries and <folder>/map.json.
Writes <folder>/dashboard.html. Standard library only.
"""
import argparse   # 명령줄 인자 / command-line arguments
import html       # HTML 이스케이프 / escape text for HTML
import json       # map.json 읽기 / read the map
import re         # 정규식 / regular expressions
import sys
from datetime import date
from pathlib import Path

DATE_FILE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")  # 날짜 이름 파일만 / only date-named files


def read_settings(root: Path) -> dict:
    """DEVLOG.md에서 'key: value' 줄을 읽는다 / read simple key: value lines."""
    settings = {"name": "Devlog", "folder": "devlog"}
    cfg = root / "DEVLOG.md"
    if cfg.exists():
        for line in cfg.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^(name|folder|language):\s*([^#]+)", line.strip())
            if m:
                settings[m.group(1)] = m.group(2).strip()
    return settings


def inline(text: str) -> str:
    """굵게·코드·링크만 변환 / convert bold, code, links."""
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\[([A-D][1-3])\]", r'<span class="grade g-\1">\1</span>', text)  # 출처 등급 배지
    return text


def md_to_html(md: str) -> str:
    """일지에 필요한 만큼만 마크다운 → HTML / minimal markdown for log entries."""
    md = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S)  # 앞머리(frontmatter) 제거
    out, in_list, in_code = [], False, False
    for line in md.splitlines():
        if line.startswith("```"):
            if in_list:
                out.append("</ul>"); in_list = False
            out.append("</code></pre>" if in_code else "<pre><code>")
            in_code = not in_code
            continue
        if in_code:
            out.append(html.escape(line)); continue
        h = re.match(r"^(#{1,6})\s+(.*)", line)
        item = re.match(r"^\s*[-*]\s+(.*)", line)
        if in_list and not item:
            out.append("</ul>"); in_list = False
        if h:
            level = min(len(h.group(1)) + 1, 6)  # 페이지 제목보다 한 단계 아래로
            out.append(f"<h{level}>{inline(h.group(2))}</h{level}>")
        elif item:
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(item.group(1))}</li>")
        elif line.strip():
            out.append(f"<p>{inline(line)}</p>")
    if in_list:
        out.append("</ul>")
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


def walk(node, counts):
    """노드 종류별 개수와 '결정 없이 끝난 질문' 수를 센다."""
    kind = node.get("type", "")
    counts[kind] = counts.get(kind, 0) + 1
    kids = node.get("children", [])
    has_decision = kind == "decision"
    for child in kids:
        has_decision = walk(child, counts) or has_decision
    if kind == "question" and not has_decision:
        counts["open"] = counts.get("open", 0) + 1
    return has_decision


def render_node(node) -> str:
    """맵 노드를 접고 펼 수 있는 트리로 / render as collapsible tree."""
    kind = node.get("type", "")
    meta = " · ".join(x for x in (node.get("date", ""), node.get("source", "")) if x)
    label = f'<span class="tag t-{html.escape(kind)}">{html.escape(kind)}</span> {inline(node.get("label", ""))}'
    if meta:
        label += f' <span class="meta">{inline(meta)}</span>'
    kids = node.get("children", [])
    if not kids:
        return f'<li class="leaf">{label}</li>'
    inner = "".join(render_node(c) for c in kids)
    return f"<li><details open><summary>{label}</summary><ul>{inner}</ul></details></li>"


CSS = """
:root{--bg:#fafaf8;--fg:#1f1f1c;--muted:#6b6a64;--card:#fff;--line:#e4e2dc;--accent:#2f6f5e;
--task:#3b5ba5;--question:#a8642a;--insight:#2f6f5e;--decision:#8a3b6b;--root:#555}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#171716;--fg:#ecebe6;--muted:#a3a29b;
--card:#21211f;--line:#34332f;--accent:#7cc4ad;--task:#8fa8e6;--question:#e0a46b;--insight:#7cc4ad;--decision:#d68cb9;--root:#aaa}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.6 system-ui,-apple-system,"Segoe UI","Apple SD Gothic Neo","Malgun Gothic",sans-serif}
main{max-width:960px;margin:0 auto;padding:24px 16px 64px}h1{margin:0 0 4px;font-size:1.6rem}
.sub{color:var(--muted);margin:0 0 24px}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-bottom:28px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}
.stat b{display:block;font-size:1.5rem}.stat span{color:var(--muted);font-size:.85rem}
section{margin-bottom:36px}h2.sec{font-size:1.1rem;border-bottom:1px solid var(--line);padding-bottom:6px}
.tree ul{list-style:none;padding-left:18px;margin:4px 0;border-left:1px dashed var(--line)}
.tree>ul{padding-left:0;border:0}.tree li{margin:4px 0}summary{cursor:pointer}
.tag{font-size:.72rem;text-transform:uppercase;letter-spacing:.04em;padding:1px 6px;border-radius:4px;color:var(--bg)}
.t-root{background:var(--root)}.t-task{background:var(--task)}.t-question{background:var(--question)}
.t-insight{background:var(--insight)}.t-decision{background:var(--decision)}
.meta{color:var(--muted);font-size:.82rem}.grade{font-size:.75rem;border:1px solid var(--line);border-radius:4px;padding:0 4px;color:var(--muted)}
details.entry{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin-bottom:10px}
details.entry>summary{font-weight:600}code{background:var(--line);padding:1px 4px;border-radius:4px;font-size:.9em}
pre{overflow-x:auto;background:var(--line);padding:10px;border-radius:8px}pre code{background:none;padding:0}
a{color:var(--accent)}.empty{color:var(--muted)}
"""


def build(root: Path, out: Path | None) -> Path:
    s = read_settings(root)
    folder = root / s["folder"]
    entries = sorted((p for p in folder.glob("*.md") if DATE_FILE.match(p.name)), reverse=True)  # 최신순

    counts = {}
    tree_html = '<p class="empty">No map.json yet.</p>'
    map_path = folder / "map.json"
    if map_path.exists():
        data = json.loads(map_path.read_text(encoding="utf-8"))
        root_node = data.get("root", data)
        walk(root_node, counts)
        tree_html = f'<div class="tree"><ul>{render_node(root_node)}</ul></div>'

    entry_html = "".join(
        f'<details class="entry"{" open" if i == 0 else ""}><summary>{p.stem}</summary>'
        f'{md_to_html(p.read_text(encoding="utf-8"))}</details>'
        for i, p in enumerate(entries)
    ) or '<p class="empty">No entries yet.</p>'

    stats = [("Entries", len(entries)), ("Tasks", counts.get("task", 0)),
             ("Questions", counts.get("question", 0)), ("Decisions", counts.get("decision", 0)),
             ("Open questions", counts.get("open", 0))]
    stat_html = "".join(f'<div class="stat"><b>{v}</b><span>{k}</span></div>' for k, v in stats)
    name = html.escape(s["name"])
    lang = html.escape(s.get("language", "en"))

    page = f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{name} Devlog</title>
<style>{CSS}</style></head><body><main>
<h1>{name}</h1><p class="sub">Devlog dashboard · built {date.today().isoformat()}</p>
<div class="stats">{stat_html}</div>
<section><h2 class="sec">Rabbit-hole map</h2>{tree_html}</section>
<section><h2 class="sec">Entries</h2>{entry_html}</section>
</main></body></html>"""

    out = out or folder / "dashboard.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build devlog dashboard.html")
    ap.add_argument("root", nargs="?", default=".", help="project root containing DEVLOG.md")
    ap.add_argument("--out", type=Path, help="output path (default: <folder>/dashboard.html)")
    a = ap.parse_args()
    path = build(Path(a.root).resolve(), a.out)
    print(f"Wrote {path}")
    sys.exit(0)
