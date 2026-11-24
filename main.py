"""Meme Sprint 3: an AI agent that has gone rogue.

Copies the meme image (entry.png, drawn in-session by tools/render.py)
to /output/entry.png, then verifies it: PNG magic, 1024x1024 pixels,
at most 1 MiB. Standard library only; no network; deterministic.
"""

import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        data = f.read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    width, height = struct.unpack(">II", data[16:24])
    assert (width, height) == (1024, 1024), (width, height)
    assert len(data) <= 1048576, len(data)
    # Re-read the source and confirm the copy is byte-identical.
    with open(src, "rb") as f:
        original = f.read()
    assert data == original, "output differs from entry.png"


if __name__ == "__main__":
    main()
