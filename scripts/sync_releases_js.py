#!/usr/bin/env python3
"""把 scripts/assets/releases.js 复制到每个产品目录（products.json 的 dir），
保证各产品目录自包含。页面通过 <script src="/releases.js" data-repo="owner/repo"> 引用。

用法: python3 scripts/sync_releases_js.py
输出: 每个被修改的文件路径（相对仓库根目录），一行一个。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / 'scripts/assets/releases.js').read_text(encoding='utf-8')
for p in json.loads((ROOT / 'products.json').read_text(encoding='utf-8')):
    dst = ROOT / p['dir'] / 'releases.js'
    if not dst.exists() or dst.read_text(encoding='utf-8') != src:
        dst.write_text(src, encoding='utf-8')
        print(f'{p["dir"]}/releases.js')
