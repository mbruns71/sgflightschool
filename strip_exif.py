#!/usr/bin/env python3
"""
Remove EXIF/metadata from a JPEG in place.

Photos straight off a phone carry GPS coordinates, device identifiers and
timestamps. None of that belongs on a public web page. macOS ships no tool that
strips it (sips preserves EXIF), and Pillow isn't installed, so this walks the
JPEG segment structure directly and drops every APPn and COM segment.

Usage: python3 strip_exif.py <file.jpg> [...]
"""
import sys

# Segments with no payload length field.
STANDALONE = {0xD8, 0xD9} | set(range(0xD0, 0xD8))
# APP0..APP15 and COM — metadata containers, all safe to drop.
DROP = set(range(0xE0, 0xF0)) | {0xFE}


def strip(path):
    with open(path, "rb") as f:
        data = f.read()

    if data[:2] != b"\xff\xd8":
        raise ValueError(f"{path}: not a JPEG")

    out = bytearray(b"\xff\xd8")
    i = 2
    dropped = []
    while i < len(data) - 1:
        if data[i] != 0xFF:
            raise ValueError(f"{path}: bad marker at byte {i}")
        marker = data[i + 1]

        if marker == 0xDA:               # start of scan — copy the rest verbatim
            out += data[i:]
            break
        if marker in STANDALONE:
            out += data[i:i + 2]
            i += 2
            continue

        seg_len = int.from_bytes(data[i + 2:i + 4], "big")
        end = i + 2 + seg_len
        if marker in DROP:
            dropped.append(f"0x{marker:02X}")
        else:
            out += data[i:end]
        i = end

    before = len(data)
    with open(path, "wb") as f:
        f.write(out)
    print(f"  {path}")
    print(f"    dropped segments: {', '.join(dropped) or 'none'}")
    print(f"    {before:,} -> {len(out):,} bytes")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        strip(p)
