"""Utility helpers for the AI Panorama dashboard build pipeline."""
import re, json, urllib.parse


def extract_icons(html_content: str) -> dict[str, str]:
    """Extract base64 icon map from existing HTML (title -> data-uri)."""
    icon_map: dict[str, str] = {}
    for m in re.finditer(
        r'"title"\s*:\s*"([^"]+)"[^}]*"icon"\s*:\s*"(data:image[^"]+)"',
        html_content,
    ):
        icon_map[m.group(1)] = m.group(2)
    return icon_map


def inject_icons(tools: list[dict], icon_map: dict[str, str]) -> None:
    """Mutate *tools* in place, adding an ``icon`` field from *icon_map*."""
    for tool in tools:
        if tool["title"] in icon_map:
            tool["icon"] = icon_map[tool["title"]]
        else:
            for old_title, icon in icon_map.items():
                if old_title in tool["title"] or tool["title"] in old_title:
                    tool["icon"] = icon
                    break
            if "icon" not in tool:
                tool["icon"] = ""


def _js_str(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def build_js_data(
    tools: list[dict],
    bloggers: list[dict],
    tool_cats: list[str],
    blogger_cats: list[str],
) -> str:
    """Return a JS snippet defining RESOURCES, BLOGGERS, TOOL_CATS, BLOGGER_CATS."""
    lines = []

    # Tools
    tool_lines = []
    for t in tools:
        ic = _js_str(t.get("icon", ""))
        tool_lines.append(
            f'  {{"title":"{t["title"]}","desc":"{t["desc"]}",'
            f'"url":"{t["url"]}","cat":"{t["cat"]}","icon":"{ic}"}}'
        )
    lines.append("const RESOURCES = [\n" + ",\n".join(tool_lines) + "\n];")

    # Bloggers
    blog_lines = []
    for b in bloggers:
        blog_lines.append(
            f'  {{"title":"{b["title"]}","desc":"{b["desc"]}",'
            f'"yt":"{b["yt"]}","x":"{b["x"]}","cat":"{b["cat"]}"}}'
        )
    lines.append("const BLOGGERS = [\n" + ",\n".join(blog_lines) + "\n];")

    # Categories
    lines.append("const TOOL_CATS = " + json.dumps(tool_cats, ensure_ascii=False) + ";")
    lines.append(
        "const BLOGGER_CATS = " + json.dumps(blogger_cats, ensure_ascii=False) + ";"
    )

    return "\n".join(lines)


    return "\n".join(lines)
