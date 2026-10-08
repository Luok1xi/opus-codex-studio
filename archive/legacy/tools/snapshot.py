"""
snapshot.py —— 改之前留一份快照（Opus 和 Codex 共用）
------------------------------------------------------------
python tools/snapshot.py 标签
把 js/、css/、index.html、assets/manifest.js 复制到
production/snapshots/<时间>-<标签>/ （约 3 MB，不含图片和音乐）。
出事了就从这里把文件拿回去。只读写游戏文件夹。
"""
import os
import shutil
import sys
import time

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
label = sys.argv[1] if len(sys.argv) > 1 else "snap"
label = "".join(c for c in label if c.isalnum() or c in "-_") or "snap"
dst = os.path.join(ROOT, "production", "snapshots", time.strftime("%Y%m%d-%H%M%S") + "-" + label)

n = 0
for rel in ("js", "css"):
    for base, dirs, files in os.walk(os.path.join(ROOT, rel)):
        dirs[:] = [d for d in dirs if d != "node_modules"]
        for f in files:
            src = os.path.join(base, f)
            out = os.path.join(dst, os.path.relpath(src, ROOT))
            os.makedirs(os.path.dirname(out), exist_ok=True)
            shutil.copy2(src, out)
            n += 1
for rel in ("index.html", os.path.join("assets", "manifest.js")):
    out = os.path.join(dst, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shutil.copy2(os.path.join(ROOT, rel), out)
    n += 1
print("snapshot:", os.path.relpath(dst, ROOT), "files:", n)
