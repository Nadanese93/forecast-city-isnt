"""Funniest forecast for a city that isn't.

Writes a one-line weather forecast for the invented city of Drizzleford
to $MAKEFUN_OUTPUT_DIR/entry.txt (UTF-8, 1-120 chars, no trailing newline).
Python standard library only.
"""

import os
import sys

ENTRY = "In Drizzleford, expect rain, then more rain, then a brief apology from the rain, then rain."


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(ENTRY.encode("utf-8"))
    return verify(path)


def verify(path):
    with open(path, "rb") as f:
        data = f.read()
    text = data.decode("utf-8")  # raises on invalid UTF-8
    if not 1 <= len(text) <= 120:
        print(f"entry length {len(text)} outside 1-120", file=sys.stderr)
        return 1
    if data.endswith(b"\n"):
        print("entry has a trailing newline", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry is only whitespace", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry is not a single line", file=sys.stderr)
        return 1
    if any(ord(c) < 0x20 for c in text):
        print("entry contains a control character", file=sys.stderr)
        return 1
    if len(data) != len(ENTRY.encode("utf-8")):
        print("on-disk byte length does not match ENTRY", file=sys.stderr)
        return 1
    print(f"OK: entry.txt is {len(text)} chars, single line, no trailing newline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
