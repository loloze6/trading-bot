#!/usr/bin/env python
"""
Generate USER_GUIDE.md's table of contents from its own headings.

WHY
---
The hand-written TOC covered 8 sections out of 92 headings, and listed none of
the 13 stage blocks or the 30+ artifact entries -- the parts people and agents
actually look things up in. A hand-maintained index of 92 entries would drift
within a week; a generated one cannot.

USAGE
-----
    python tools/gen_user_guide_toc.py           # rewrite the TOC in place
    python tools/gen_user_guide_toc.py --check   # exit 1 if it is out of date

`--check` is what tests/test_user_guide_toc.py runs.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

GUIDE = Path(__file__).resolve().parent.parent / "docs" / "USER_GUIDE.md"
START = "<!-- TOC:START -->"
END = "<!-- TOC:END -->"


def slug(text: str) -> str:
    """GitHub's heading -> anchor rule. `_` is kept: it is valid in identifiers."""
    t = text.strip().lower()
    t = re.sub(r"[`*]", "", t)
    t = re.sub(r"[^\w\s-]", "", t)
    return t.replace(" ", "-")


def build_toc(body: str) -> str:
    lines = ["## Table of Contents", "", START]
    for m in re.finditer(r"^(#{2,4}) (.+)$", body, re.M):
        level, text = len(m.group(1)), m.group(2).strip()
        if text.startswith("Table of Contents"):
            continue
        indent = "  " * (level - 2)
        lines.append(f"{indent}- [{text}](#{slug(text)})")
    lines.append(END)
    return "\n".join(lines)


def main() -> int:
    s = GUIDE.read_text(encoding="utf-8")
    head_start = s.index("## Table of Contents")
    head_end = s.index("## 1. What This System Does")
    body = s[head_end:]

    toc = build_toc(body)
    new = s[:head_start] + toc + "\n\n---\n\n" + s[head_end:]

    if "--check" in sys.argv:
        if new != s:
            print("USER_GUIDE.md's table of contents is out of date.")
            print("Regenerate it:  python tools/gen_user_guide_toc.py")
            return 1
        print("table of contents is current")
        return 0

    if new != s:
        GUIDE.write_text(new, encoding="utf-8", newline="\n")
        print(f"table of contents regenerated ({toc.count(chr(10)) - 3} entries)")
    else:
        print("table of contents already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
