#!/usr/bin/env python3
"""Build the single-page AISMM reference site from the Markdown model.

Usage:
    python3 tools/build_site.py            # writes site/index.html

Parses dimensions/*.md and model/*.md into structured data, renders the Markdown
subset the model uses (headings, paragraphs, lists, tables, code, bold, links),
and injects the result into tools/site_template.html. Standard library only.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "tools" / "site_template.html"
OUT = ROOT / "site" / "index.html"

STAGES = ["Traditional", "Initial", "Advanced", "Optimal"]
ID_RE = re.compile(r"\b((?:GOV|DATA|MDL|APP|AGT|INF)-[1-5]|VIS|IR|AUTO)\b")
DOC_LINKS = {
    "levels.md": "#doc-stages", "model/levels.md": "#doc-stages",
    "profiles.md": "#doc-profiles", "model/profiles.md": "#doc-profiles",
    "evidence.md": "#doc-evidence", "model/evidence.md": "#doc-evidence",
}


# ---------------------------------------------------------------- inline markdown
def inline(text, link_ids=True):
    slots = []

    def keep(fragment):
        slots.append(fragment)
        return f"\x00{len(slots) - 1}\x00"

    def code(m):
        return keep(f"<code>{html.escape(m.group(1))}</code>")

    def link(m):
        label, href = m.group(1), m.group(2)
        if href.startswith("http"):
            return keep(f'<a href="{html.escape(href)}" target="_blank" rel="noopener">{inline(label, False)}</a>')
        target = DOC_LINKS.get(href.split("/")[-1] if href.startswith("../") else href)
        if target:
            return keep(f'<a href="{target}">{inline(label, False)}</a>')
        return keep(inline(label, False))  # repo-only link (e.g. a script): keep text

    text = re.sub(r"`([^`]+)`", code, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    text = html.escape(text, quote=False).replace("\\*", "*")
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    if link_ids:
        text = ID_RE.sub(lambda m: f'<a class="xref" href="#{m.group(1)}">{m.group(1)}</a>', text)
    return re.sub(r"\x00(\d+)\x00", lambda m: slots[int(m.group(1))], text)


def plain(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text.replace("**", "").replace("`", "").replace("\\*", "*")


# ----------------------------------------------------------------- block markdown
LIST_RE = re.compile(r"^(\s*)([-*]|\d+\.) (.*)$")


def blocks(md, shift=0):
    lines, out, i = md.split("\n"), [], 0
    n = len(lines)

    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("```"):
            j = i + 1
            while j < n and not lines[j].startswith("```"):
                j += 1
            out.append(f"<pre><code>{html.escape(chr(10).join(lines[i + 1:j]))}</code></pre>")
            i = j + 1
        elif m := re.match(r"(#{1,6}) (.*)", line):
            level = min(6, len(m.group(1)) + shift)
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < n and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not re.fullmatch(r"[-:\s]+", "".join(r))]
            t = "<div class=\"tablewrap\"><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head)
            t += "</tr></thead><tbody>" + "".join(
                "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
            out.append(t + "</tbody></table></div>")
        elif line.startswith(">"):
            q = []
            while i < n and lines[i].startswith(">"):
                q.append(lines[i].lstrip(">").lstrip())
                i += 1
            out.append(f"<blockquote>{blocks(chr(10).join(q), shift)}</blockquote>")
        elif m := LIST_RE.match(line):
            ordered = m.group(2)[0].isdigit()
            items = []
            while i < n:
                m = LIST_RE.match(lines[i])
                if not m or len(m.group(1)) > 0:
                    break
                body = [m.group(3)]
                i += 1
                while i < n and (lines[i].startswith("  ") or (not lines[i].strip() and i + 1 < n and lines[i + 1].startswith("  "))):
                    body.append(re.sub(r"^ {1,3}", "", lines[i]))
                    i += 1
                inner = blocks("\n".join(body), shift)
                if inner.count("<p>") == 1 and inner.startswith("<p>") and inner.endswith("</p>"):
                    inner = inner[3:-4]
                items.append(f"<li>{inner}</li>")
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>{''.join(items)}</{tag}>")
        else:
            para = []
            while i < n and lines[i].strip() and not (
                    lines[i].startswith(("#", "|", "```", ">")) or LIST_RE.match(lines[i])):
                para.append(lines[i].strip())
                i += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
    return "".join(out)


# --------------------------------------------------------------- model parsing
def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def parse_stage(name, body):
    stage = {"name": name, "desc": "", "practices": [], "evidence": []}
    section, desc = "desc", []
    for line in body.split("\n"):
        s = line.strip()
        if s == "**Practices**":
            section = "practices"
            continue
        if s == "**Evidence to produce**":
            section = "evidence"
            continue
        if section == "desc":
            desc.append(line)
        elif section == "practices":
            if m := re.match(r"^- (.*)", line):
                stage["practices"].append(m.group(1))
            elif s and stage["practices"] and line.startswith(" "):
                stage["practices"][-1] += " " + s
        elif section == "evidence":
            if m := re.match(r"^\|\s*`([^`]+)`\s*\|(.*)\|\s*$", line):
                cells = [c.strip() for c in m.group(2).split("|")]
                ev_name, etype, profile, criteria = cells[0], cells[1].strip("`"), cells[2], "|".join(cells[3:])
                stage["evidence"].append({
                    "id": m.group(1), "name": plain(ev_name), "type": etype, "profile": profile,
                    "criteria": inline(criteria), "criteriaText": plain(criteria)})
    stage["desc"] = blocks("\n".join(desc).strip())
    practices = []
    for p in stage["practices"]:
        tag = None
        if m := re.match(r"^\[(ML|LLM|Agentic)\]\s*(.*)", p):
            tag, p = m.group(1), m.group(2)
        practices.append({"tag": tag, "html": inline(p)})
    stage["practices"] = practices
    return stage


def parse_element(chunk):
    header, _, rest = chunk.partition("\n")
    eid, name = header.split(" ", 1)
    meta_text, *stage_chunks = re.split(r"^### ", rest, flags=re.M)
    el = {"id": eid, "name": name.strip(), "applies": [], "scope": "", "intent": "", "risks": "", "refs": "", "stages": []}
    keys = {"Applies to": "applies", "Scope note": "scope", "Intent": "intent",
            "Key risks addressed": "risks", "References": "refs"}
    for para in paragraphs(meta_text):
        if m := re.match(r"\*\*(.+?):\*\*\s*(.*)", para, re.S):
            key = keys.get(m.group(1))
            value = " ".join(l.strip() for l in m.group(2).split("\n"))
            if key == "applies":
                el["applies"] = [p.strip() for p in value.split("·") if p.strip()]
            elif key:
                el[key] = inline(value)
    for sc in stage_chunks:
        sname, _, body = sc.partition("\n")
        sname = sname.strip()
        if sname in STAGES:
            el["stages"].append(parse_stage(sname, body.strip().rstrip("-").strip()))
    return el


def parse_dimension(path):
    text = path.read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", text, re.M).group(1).strip()
    num = int(path.name[:2])
    intro_md = text.split("\n", 1)[1].split("\n|", 1)[0]
    chunks = re.split(r"^## ", text, flags=re.M)[1:]
    elements = [parse_element(c.rsplit("\n---", 1)[0] if c.rstrip().endswith("---") else c) for c in chunks]
    short = re.sub(r"^Dimension \d+ — ", "", title)
    key = elements[0]["id"].split("-")[0] if num <= 6 else "XC"
    return {"key": key, "num": num if num <= 6 else None, "title": short,
            "intro": blocks(intro_md.strip()), "elements": elements}


def readme_section(heading):
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def main():
    dims = [parse_dimension(p) for p in sorted((ROOT / "dimensions").glob("*.md"))]
    docs = []
    for doc_id, fname in [("stages", "levels.md"), ("profiles", "profiles.md"), ("evidence", "evidence.md")]:
        md = (ROOT / "model" / fname).read_text(encoding="utf-8")
        title = re.search(r"^# (.+)$", md, re.M).group(1).strip()
        body = md.split("\n", 1)[1]
        body = re.sub(r"\nA machine-readable checklist.*\Z", "\n", body, flags=re.S)
        docs.append({"id": doc_id, "title": title, "html": blocks(body, shift=0)})
    data = {"dimensions": dims, "docs": docs,
            "alignment": blocks(readme_section("Framework alignment"))}
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    n_el = sum(len(d["elements"]) for d in dims)
    n_ev = sum(len(s["evidence"]) for d in dims for e in d["elements"] for s in e["stages"])
    print(f"wrote {OUT.relative_to(ROOT)}: {len(dims)} sections, {n_el} elements, {n_ev} evidence items, "
          f"{OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
