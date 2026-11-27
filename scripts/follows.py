#!/usr/bin/env python3
"""Does the page have everything the script names?

    python3 scripts/follows.py talk.conv index.html

Every `[slide NAME]` in the script should be a `data-slide="NAME"` in the page,
and every `step:N` a `data-step="N"` inside that slide. A page with no slides
at all draws its own picture: there, every scene the script names should be
spoken of in the page as `data-stage-slide="NAME"`.

Standard library only. It reads the two files as text; it is a check of the
template, not a parser of either.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

MARK = re.compile(r"^\[slide\s+([A-Za-z0-9_-]+)(?:\s+step:(\d+))?\s*\]\s*$")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Page(HTMLParser):
    """The slides of a page, and the steps inside each."""

    def __init__(self):
        super().__init__()
        self.slides = {}
        self.open = []      # (tag, slide it opened or None)

    def handle_starttag(self, tag, attributes):
        given = dict(attributes)
        slide = given.get("data-slide")
        if slide is not None:
            self.slides.setdefault(slide, set())
        inside = next((name for _, name in reversed(self.open) if name), None) if slide is None else slide
        if "data-step" in given and inside:
            self.slides[inside].add(given["data-step"])
        if tag not in VOID:
            self.open.append((tag, slide))

    def handle_endtag(self, tag):
        for index in range(len(self.open) - 1, -1, -1):
            if self.open[index][0] == tag:
                del self.open[index:]
                return


def follows(script: str, page: str):
    """Everything the script names that the page does not have."""
    read = Page()
    read.feed(page)
    missing = []
    for number, line in enumerate(script.splitlines(), start=1):
        found = MARK.match(line.strip())
        if not found:
            continue
        slide, step = found.groups()
        if not read.slides:
            if f'data-stage-slide="{slide}"' not in page and f"'{slide}'" not in page:
                missing.append(f"line {number}: the page says nothing of a scene called `{slide}`")
        elif slide not in read.slides:
            missing.append(f"line {number}: the page has no slide called `{slide}`")
        elif step and step != "0" and step not in read.slides[slide]:
            missing.append(f"line {number}: the slide `{slide}` has no step {step}")
    return missing


def main(arguments):
    if len(arguments) != 2:
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    script, page = (Path(one).read_text(encoding="utf-8") for one in arguments)
    missing = follows(script, page)
    for one in missing:
        print(one)
    if missing:
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
