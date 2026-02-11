#!/usr/bin/env python3
"""Build the AI Panorama dashboard.

Reads data from JSON files, injects icons from existing HTML,
and produces a self-contained ``ai_panorama.html``.
"""
import json, pathlib

# Resolve paths relative to this script
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = HERE / "data"
TMPL = HERE / "templates" / "dashboard.html"
OUT  = ROOT / "ai_panorama.html"

# ── 1. Load data ──
tools: list[dict]    = json.loads((DATA / "tools.json").read_text("utf-8"))
bloggers: list[dict] = json.loads((DATA / "bloggers.json").read_text("utf-8"))
cats: dict           = json.loads((DATA / "categories.json").read_text("utf-8"))
tool_cats: list[str]    = cats["tool_cats"]
blogger_cats: list[str] = cats["blogger_cats"]

# ── 2. Extract & inject icons ──
from utils import extract_icons, inject_icons, build_js_data  # noqa: E402

if OUT.exists():
    icon_map = extract_icons(OUT.read_text("utf-8", errors="ignore"))
    inject_icons(tools, icon_map)
else:
    for t in tools:
        t.setdefault("icon", "")



# ── 3. Build JS data blob ──
js_data = build_js_data(tools, bloggers, tool_cats, blogger_cats)

# ── 4. Render template ──
template = TMPL.read_text("utf-8")
html = template.replace("{{JS_DATA}}", js_data)

# ── 5. Write output ──
OUT.write_text(html, encoding="utf-8")

# ── 6. Report ──
print(f"✅ Dashboard rebuilt: {len(tools)} tools + {len(bloggers)} bloggers")
for c in tool_cats:
    n = sum(1 for t in tools if t["cat"] == c)
    print(f"   {c}: {n} tools")
for c in blogger_cats:
    n = sum(1 for b in bloggers if b["cat"] == c)
    print(f"   {c}: {n} bloggers")
