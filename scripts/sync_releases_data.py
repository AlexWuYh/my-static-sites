#!/usr/bin/env python3
"""从 GitHub 抓取各产品仓库的 release，保存成各产品目录下的 releases.json 快照。

页面（releases.js）优先读取这份同域快照，所以访问者即使连不上 GitHub 也能看到
版本号和更新日志；能连上 GitHub 时页面会用 API 的实时数据刷新。

某个仓库抓取失败时保留旧快照（不会清空），并以非 0 退出码提示。
设置环境变量 GITHUB_TOKEN 可提高 API 限额（GitHub Actions 里自带）。

用法: python3 scripts/sync_releases_data.py
输出: 每个被修改的文件路径（相对仓库根目录），一行一个。
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEEP = ('tag_name', 'name', 'published_at', 'prerelease', 'body', 'html_url')
LIMIT = 10

products = json.loads((ROOT / 'products.json').read_text(encoding='utf-8'))
failed = False
for p in products:
    repo = p.get('repo')
    if not repo:
        continue
    req = urllib.request.Request(
        f'https://api.github.com/repos/{repo}/releases?per_page={LIMIT}',
        headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'my-static-sites-sync'},
    )
    if os.environ.get('GITHUB_TOKEN'):
        req.add_header('Authorization', 'Bearer ' + os.environ['GITHUB_TOKEN'])
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
    except Exception as e:  # 网络或限流：保留旧快照
        print(f'警告：{repo} 抓取失败（{e}），保留旧快照', file=sys.stderr)
        failed = True
        continue
    releases = [{k: x.get(k) for k in KEEP} for x in data if not x.get('draft')]
    path = ROOT / p['dir'] / 'releases.json'
    # 不写入抓取时间，内容没变化就不产生提交
    text = json.dumps({'repo': repo, 'releases': releases}, ensure_ascii=False, indent=1) + '\n'
    if not path.exists() or path.read_text(encoding='utf-8') != text:
        path.write_text(text, encoding='utf-8')
        print(f'{p["dir"]}/releases.json')
sys.exit(1 if failed else 0)
