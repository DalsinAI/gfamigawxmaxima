#!/usr/bin/env python3
"""Packs a drawer into an Amiga LhA archive (level-1 headers) with our own
packer (lha_archive.py, AmiCradle's LhA writer), each file packed and checked
on its own core.
Usage: mklha.py <drawer> <archive.lha> [auto|lh5|lh0]
auto packs a file with lh5 when that makes it smaller; lh0 stores (quick,
for labs). Every packed file is unpacked again and compared before it goes in.
Copyright (c) 2026 AmiCradle Team."""
import os
import sys
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lha_archive as L

SCRIPTS = {"Install"}


def pack_one(job):
    data, method = job
    if method in ("auto", "lh5") and data:
        c = L.lh5_compress(data)
        if method == "lh5" or len(c) < len(data):
            if L.lh5_decompress(c, len(data)) != data:
                raise SystemExit("lh5 round trip differs")
            return b"-lh5-", c
    return b"-lh0-", data


def main():
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    method = sys.argv[3] if len(sys.argv) > 3 else "auto"
    files = [p for p in sorted(root.rglob("*")) if p.is_file()]
    members = [L.Member(p.relative_to(root.parent).as_posix(), p.read_bytes(),
                        0x40 if p.name in SCRIPTS else 0, "", p.stat().st_mtime)
               for p in files]
    # biggest first, so the long ones start early
    order = sorted(range(len(members)), key=lambda i: -len(members[i].data))
    with Pool(os.cpu_count() or 1) as pool:
        done = pool.map(pack_one, [(members[i].data, method) for i in order], chunksize=1)
    packed = [None] * len(members)
    for i, r in zip(order, done):
        packed[i] = r
    arc = bytearray()
    for m, (meth, data) in zip(members, packed):
        arc += L._header(m, meth, len(data), L.crc16(m.data)) + data
    arc.append(0)
    out.write_bytes(bytes(arc))
    print(f"{out.name}: {len(members)} files, {len(arc)} bytes, each file checked")


if __name__ == "__main__":
    main()
