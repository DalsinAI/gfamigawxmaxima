#!/usr/bin/env python3
"""sync-tree.py NEW DST: make DST hold what NEW holds, copying only files
whose contents differ (so their times change and make rebuilds just those)
and removing files NEW doesn't have. Copyright (c) 2026 AmiCradle Team."""
import filecmp
import os
import shutil
import sys

new, dst = sys.argv[1], sys.argv[2]
keep = {".patched"}
changed = 0
for root, dirs, files in os.walk(new):
    rel = os.path.relpath(root, new)
    os.makedirs(os.path.join(dst, rel), exist_ok=True)
    for f in files:
        a, b = os.path.join(root, f), os.path.join(dst, rel, f)
        if not os.path.exists(b) or not filecmp.cmp(a, b, shallow=False):
            shutil.copy2(a, b)
            os.utime(b)
            changed += 1
removed = 0
for root, dirs, files in os.walk(dst, topdown=False):
    rel = os.path.relpath(root, dst)
    if rel.split(os.sep)[0] == ".git":
        continue
    for f in files:
        if rel == "." and f in keep:
            continue
        if not os.path.exists(os.path.join(new, rel, f)):
            os.remove(os.path.join(root, f))
            removed += 1
print(f"sync-tree: {changed} files changed, {removed} removed")
