#!/usr/bin/env python3
"""Extract every evidence item from the AISMM dimension files into a CSV checklist.

Usage:
    python3 tools/build_checklist.py                       # all profiles -> stdout
    python3 tools/build_checklist.py --profile LLM -o llm.csv
    python3 tools/build_checklist.py --profile Agentic --stage Advanced

--profile applies stacking: ML -> All+ML; LLM -> All+ML+LLM; Agentic -> everything.
--stage is cumulative: Advanced returns Initial + Advanced items.
Elements whose "Applies to" excludes the profile are omitted.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIM_DIR = ROOT / "dimensions"

STAGES = {"I": "Initial", "A": "Advanced", "O": "Optimal"}
STAGE_ORDER = ["Initial", "Advanced", "Optimal"]
PROFILE_STACK = {
    "ML": {"All", "ML"},
    "LLM": {"All", "ML", "LLM"},
    "Agentic": {"All", "ML", "LLM", "Agentic"},
}

ELEMENT_RE = re.compile(r"^## (\S+) (.+)$")
APPLIES_RE = re.compile(r"^\*\*Applies to:\*\*\s*(.+)$")
ROW_RE = re.compile(r"^\|\s*`([A-Z]+(?:-\d+)?)\.([IAO])\.(\d+)`\s*\|(.*)\|\s*$")
DIM_RE = re.compile(r"^# (.+)$")


def parse(path):
    dimension = element_id = element_name = None
    applies = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if m := DIM_RE.match(line):
            dimension = m.group(1).strip()
        elif m := ELEMENT_RE.match(line):
            element_id, element_name = m.group(1), m.group(2).strip()
            applies = set()
        elif m := APPLIES_RE.match(line):
            applies = {p.strip() for p in re.split(r"[·,]", m.group(1)) if p.strip()}
        elif m := ROW_RE.match(line):
            cells = [c.strip() for c in m.group(4).split("|")]
            if len(cells) < 4:
                continue
            evidence, etype, profile, criteria = cells[0], cells[1], cells[2], "|".join(cells[3:])
            yield {
                "dimension": dimension,
                "element_id": element_id,
                "element": element_name,
                "element_applies_to": " · ".join(sorted(applies)),
                "stage": STAGES[m.group(2)],
                "evidence_id": f"{m.group(1)}.{m.group(2)}.{m.group(3)}",
                "evidence": evidence,
                "type": etype.strip("`"),
                "profile": profile,
                "acceptance_criteria": criteria,
                "_applies": applies,
            }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", choices=sorted(PROFILE_STACK))
    ap.add_argument("--stage", choices=STAGE_ORDER, help="highest target stage (cumulative)")
    ap.add_argument("-o", "--output", help="CSV path (default stdout)")
    args = ap.parse_args()

    rows = [r for f in sorted(DIM_DIR.glob("*.md")) for r in parse(f)]
    if args.profile:
        allowed = PROFILE_STACK[args.profile]
        rows = [r for r in rows if args.profile in r["_applies"] and r["profile"] in allowed]
    if args.stage:
        keep = set(STAGE_ORDER[: STAGE_ORDER.index(args.stage) + 1])
        rows = [r for r in rows if r["stage"] in keep]

    fields = [k for k in rows[0] if not k.startswith("_")] if rows else []
    fields += ["status", "owner", "evidence_location", "date", "notes"]
    out = open(args.output, "w", newline="", encoding="utf-8") if args.output else sys.stdout
    w = csv.DictWriter(out, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
    if args.output:
        out.close()
        print(f"wrote {len(rows)} evidence items to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
