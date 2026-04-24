#!/usr/bin/env python3
"""
Extract per-slide TTS narration scripts from a reveal.js HTML deck.

Reads <aside class="notes">...</aside> blocks from each <section>, and writes
them as a Python list to stdout (or a file), matching the AutoLecture
`scripts = [...]` format.

Usage:
    python3 tools/extract_scripts.py chapters/chapter20.html
    python3 tools/extract_scripts.py chapters/chapter20.html --out build_ch20_scripts.py

TTS rules (from AutoLecture):
    1. First word must be English.
    2. Numbers should already be spelled out.
    3. Each script under 2000 chars.
This script VERIFIES those rules and warns on violations.
"""
from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class NotesExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_section = 0
        self.in_notes = 0
        self.current_notes: list[str] = []
        self.slides: list[str] = []
        self._section_has_notes = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == "section":
            # Start a new slide only for top-level sections of the deck.
            # reveal.js allows vertical stacks, but we treat each <section>
            # (regardless of nesting) as a rendered slide.
            self.in_section += 1
            if self.in_section == 1:
                self.current_notes = []
                self._section_has_notes = False
        elif tag == "aside" and attr_map.get("class") == "notes":
            self.in_notes += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "aside" and self.in_notes:
            self.in_notes -= 1
        elif tag == "section":
            self.in_section -= 1
            if self.in_section == 0:
                text = " ".join("".join(self.current_notes).split()).strip()
                self.slides.append(text)
                self.current_notes = []

    def handle_data(self, data: str) -> None:
        if self.in_notes:
            self.current_notes.append(data)


def verify(scripts: list[str]) -> list[str]:
    warnings: list[str] = []
    for i, s in enumerate(scripts):
        if not s:
            warnings.append(f"slide {i:02d}: EMPTY notes")
            continue
        first = s.lstrip().split(" ", 1)[0].strip(".,;:!?")
        if not re.match(r"^[A-Za-z][A-Za-z'-]*$", first):
            warnings.append(f"slide {i:02d}: first token '{first}' is not plain English")
        if len(s) > 2000:
            warnings.append(f"slide {i:02d}: {len(s)} chars exceeds 2000-char TTS limit")
        if re.search(r"\d", s):
            warnings.append(f"slide {i:02d}: contains digits — spell them out")
    return warnings


def to_python_list(scripts: list[str], source: Path) -> str:
    lines = [
        "# Auto-generated TTS scripts from reveal.js speaker notes.",
        f"# Source: {source.name}",
        "# Each entry corresponds to one <section> slide.",
        "",
        "scripts = [",
    ]
    for i, s in enumerate(scripts):
        escaped = s.replace('"""', '\\"\\"\\"')
        lines.append(f'    # ---- slide {i:02d} ----')
        lines.append(f'    """{escaped}""",')
    lines.append("]")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html", type=Path, help="path to reveal.js deck HTML")
    ap.add_argument("--out", type=Path, help="write Python script file (default: stdout)")
    ap.add_argument("--strict", action="store_true", help="exit non-zero on any warnings")
    args = ap.parse_args()

    if not args.html.exists():
        print(f"error: {args.html} not found", file=sys.stderr)
        return 1

    parser = NotesExtractor()
    parser.feed(args.html.read_text(encoding="utf-8"))
    scripts = parser.slides

    # Drop trailing empty slides (from nested sections closing late).
    while scripts and not scripts[-1]:
        scripts.pop()

    warnings = verify(scripts)
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    output = to_python_list(scripts, args.html)
    if args.out:
        args.out.write_text(output, encoding="utf-8")
        print(f"wrote {len(scripts)} slides → {args.out}", file=sys.stderr)
    else:
        print(output)

    if args.strict and warnings:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
