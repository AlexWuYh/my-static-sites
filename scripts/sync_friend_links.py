#!/usr/bin/env python3
"""把 products.json 里的产品互相作为友情链接，写进每个产品页面底部栏。

每个产品页面（<dir>/index.html 与 <dir>/en/index.html）的页脚里需有一对标记：

    <!-- friends:start -->
    <!-- friends:end -->

脚本会把标记之间的内容替换为“除自己以外的其他产品”的链接（中文页用中文，
英文页用英文）。只有一个产品时标记之间保持为空。

新增产品时：在 products.json 里加一项，并在新产品页面页脚放好上面的标记，
再运行本脚本即可（pre-commit 钩子会在 products.json 变更时自动运行）。

用法: python3 scripts/sync_friend_links.py
输出: 每个被修改的文件路径（相对仓库根目录），一行一个。
"""
import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = '<!-- friends:start -->', '<!-- friends:end -->'
LABEL = {'zh': '友情链接', 'en': 'Friend links'}

products = json.loads((ROOT / 'products.json').read_text(encoding='utf-8'))


def build_block(me, lang):
    others = [p for p in products if p['id'] != me['id']]
    if not others:
        return ''
    links = []
    for p in others:
        href = p.get('url_en', p['url']) if lang == 'en' else p['url']
        links.append(
            f'<a href="{escape(href)}" target="_blank" rel="noopener" '
            f'title="{escape(p["desc"][lang])}">{escape(p["name"])}</a>'
        )
    return (
        '\n    <p class="friends">\n'
        f'      <span class="friends-label">{LABEL[lang]}</span>\n'
        + ''.join(f'      {l}\n' for l in links)
        + '    </p>\n    '
    )


changed = []
for p in products:
    for lang, rel in (('zh', f'{p["dir"]}/index.html'), ('en', f'{p["dir"]}/en/index.html')):
        path = ROOT / rel
        if not path.exists():
            if lang == 'zh':
                print(f'警告：{rel} 不存在，已跳过', file=sys.stderr)
            continue
        text = path.read_text(encoding='utf-8')
        if START not in text or END not in text:
            print(f'警告：{rel} 页脚缺少 {START} / {END} 标记，已跳过', file=sys.stderr)
            continue
        new = re.sub(
            re.escape(START) + r'.*?' + re.escape(END),
            lambda _: START + build_block(p, lang) + END,
            text, count=1, flags=re.S,
        )
        if new != text:
            path.write_text(new, encoding='utf-8')
            changed.append(rel)

print('\n'.join(changed))
