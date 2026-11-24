#!/usr/bin/env python3
"""Entry point for the News 24 image entry.

Renders the front page with render.py and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default ./output/entry.png).
Deterministic: the same code always writes identical bytes.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from render import render  # noqa: E402


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "./output")
    os.makedirs(out_dir, exist_ok=True)
    img = render()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", compress_level=6)
    print(path)


if __name__ == "__main__":
    main()
