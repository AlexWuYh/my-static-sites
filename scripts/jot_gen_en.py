#!/usr/bin/env python3
"""根据 Jot/index.html（中文页）生成 Jot/en/index.html（英文页）。

英文页是生成产物，请不要手动编辑；改中文页后运行本脚本（或直接提交，
pre-commit 钩子会自动运行）。若中文页里被替换的文案改了，下面的 PAIRS
会报错并指出没匹配上的文案，此时同步更新对应的中文原文与英文译文即可。

用法: python3 scripts/jot_gen_en.py [源文件] [输出文件]
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / 'Jot/index.html')
dst = sys.argv[2] if len(sys.argv) > 2 else str(ROOT / 'Jot/en/index.html')

s = open(src, encoding='utf-8').read()

# (中文原文, 英文译文, 期望出现次数)
PAIRS = [
    # ---- head ----
    ('<html lang="zh-CN"', '<html lang="en"', 1),
    ('<title>Jot（简迹）— 本地优先的碎片笔记 · AI 周期总结 · 开源免费</title>',
     '<title>Jot — Local-First Fragment Notes with AI Period Summaries · Free and Open Source</title>', 1),
    ('content="Jot（简迹）是一款本地优先的碎片笔记应用：随手记下生活、学习、工作里的片刻，需要时再让 AI 归纳成日 / 周 / 月 / 年总结。数据默认只在本机，支持 Windows、macOS、Android，开源免费。"',
     'content="Jot is a local-first fragment notes app: jot down moments from life, learning and work, then let AI turn them into daily / weekly / monthly / yearly summaries when you want. Data stays on your device by default. Windows, macOS and Android. Free and open source."', 1),
    ('content="碎片笔记, 随手记, 本地优先, AI 总结, 日报 周报 生成, 日记 App, 个人复盘, Ollama, 开源笔记, Jot, 简迹"',
     'content="fragment notes, quick notes, local-first, AI summary, weekly report generator, journal app, personal review, Ollama, open source notes, Jot"', 1),
    ('<link rel="canonical" href="https://jot.wuewa.cn/">', '<link rel="canonical" href="https://jot.wuewa.cn/en/">', 1),
    ('<meta property="og:site_name" content="Jot（简迹）">', '<meta property="og:site_name" content="Jot">', 1),
    ('<meta property="og:locale" content="zh_CN">\n<meta property="og:locale:alternate" content="en_US">',
     '<meta property="og:locale" content="en_US">\n<meta property="og:locale:alternate" content="zh_CN">', 1),
    ('<meta property="og:url" content="https://jot.wuewa.cn/">', '<meta property="og:url" content="https://jot.wuewa.cn/en/">', 1),
    ('content="Jot（简迹）— 随手记碎片，AI 见全貌"', 'content="Jot — Jot the fragments, get the whole picture"', 2),
    ('content="本地优先的碎片笔记：随手记下每个片刻，需要时让 AI 归纳成日 / 周 / 月 / 年总结。开源免费。"',
     'content="Local-first fragment notes: jot down every moment, and let AI turn them into daily / weekly / monthly / yearly summaries when you want. Free and open source."', 1),
    ('content="本地优先的碎片笔记，AI 周期总结按需生成。开源免费。"',
     'content="Local-first fragment notes with AI period summaries on demand. Free and open source."', 1),
    ('"alternateName": "简迹",', '"alternateName": "Jot (简迹)",', 1),
    ('"description": "本地优先的碎片笔记应用，可选 AI 日 / 周 / 月 / 年总结，数据默认只保存在本机。",',
     '"description": "A local-first fragment notes app with optional AI daily / weekly / monthly / yearly summaries. Data stays on your device by default.",', 1),
    ('"url": "https://jot.wuewa.cn/",', '"url": "https://jot.wuewa.cn/en/",', 1),
    ('"priceCurrency": "CNY"', '"priceCurrency": "USD"', 1),
    # ---- nav ----
    ('alt="Jot 应用图标"', 'alt="Jot app icon"', 2),
    ('<a class="nav-link" href="#features">功能</a>', '<a class="nav-link" href="#features">Features</a>', 1),
    ('<a class="nav-link" href="#privacy">隐私</a>', '<a class="nav-link" href="#privacy">Privacy</a>', 1),
    ('<a class="nav-link" href="#download">下载</a>', '<a class="nav-link" href="#download">Download</a>', 1),
    ('<a class="lang-link" href="/en/" hreflang="en" lang="en" title="English">EN</a>',
     '<a class="lang-link" href="/" hreflang="zh-CN" lang="zh-CN" title="简体中文">中文</a>', 1),
    ('aria-label="打开 Jot GitHub 仓库" title="GitHub 仓库"', 'aria-label="Open Jot on GitHub" title="GitHub repository"', 1),
    ('aria-label="切换明暗主题"', 'aria-label="Toggle light/dark theme"', 1),
    # ---- hero ----
    ('<b>开源</b> · 本地优先 · Windows / macOS / Android', '<b>Open source</b> · Local-first · Windows / macOS / Android', 1),
    ('<h1>Jot<small>简迹</small></h1>', '<h1>Jot<small>简迹</small></h1>', 1),
    ('随手记碎片，<strong>AI 见全貌</strong>。', 'Jot the fragments, <strong>get the whole picture</strong>.', 1),
    ('''      把生活、学习、工作里的片刻随手记下来，不必写冗长日记或 KPI 日报。
      需要回顾时，再让 AI 归纳成日 / 周 / 月 / 年总结。''',
     '''      Capture short moments from life, learning and work — no long diaries or KPI-style reports.
      When you want to look back, let AI turn them into daily / weekly / monthly / yearly summaries.''', 1),
    ('        下载最新版\n      </a>\n      <a class="btn btn-ghost" href="https://github.com/AlexWuYh/Jot" target="_blank" rel="noopener noreferrer">查看源码</a>\n    </div>\n    <p class="hero-note">',
     '        Download the latest release\n      </a>\n      <a class="btn btn-ghost" href="https://github.com/AlexWuYh/Jot" target="_blank" rel="noopener noreferrer">View source</a>\n    </div>\n    <p class="hero-note">', 1),
    ('免费开源（MIT） · 不配置模型也能完整记录', 'Free and open source (MIT) · Works fully without any model configured', 1),
    ('alt="Jot 今日页：左侧导航、顶部输入框和今日碎片列表"', 'alt="Jot Today screen (Chinese UI): side nav, composer on top and today\'s fragment list"', 1),
    ('今日页：随手记一句，碎片留在本机；需要时再让 AI 归纳。', 'Today: jot a moment, keep it on your device, and let AI summarize when you want.', 1),
    # ---- about ----
    ('<h2>一款本地优先的碎片笔记</h2>', '<h2>A local-first fragment notes app</h2>', 1),
    ('记录和总结是两件事：记录永远轻、永远在本机；总结是一个独立模块，想要时才生成。',
     'Capturing and summarizing are two separate things: capturing stays light and on-device; summaries are a dedicated module you generate only when you want.', 1),
    ('<tr><th>定位</th><td>日常碎片笔记，加上可选的 AI 周期总结</td></tr>', '<tr><th>Focus</th><td>Daily fragment notes plus optional AI period summaries</td></tr>', 1),
    ('<tr><th>数据</th><td>默认存在本机 SQLite；支持导出与加密备份</td></tr>', '<tr><th>Data</th><td>On-device SQLite by default; export and encrypted backup</td></tr>', 1),
    ('<tr><th>AI</th><td>本地模型（如 Ollama）或云端模型（OpenAI 兼容的厂商预设）</td></tr>', '<tr><th>AI</th><td>Local models (e.g. Ollama) or cloud models (OpenAI-compatible vendor presets)</td></tr>', 1),
    ('<tr><th>同步</th><td>可选：用你自己的存储做端到端加密的快照同步</td></tr>', '<tr><th>Sync</th><td>Optional end-to-end encrypted snapshot sync on storage you own</td></tr>', 1),
    # ---- features ----
    ('<h2>记得轻，回顾得清楚</h2>', '<h2>Capture lightly, review clearly</h2>', 1),
    ('<h3>低摩擦记录</h3>', '<h3>Low-friction capture</h3>', 1),
    ('输入框就在页面顶部，支持 Markdown 预览，也能补记过去的日期。桌面端有托盘和全局热键（默认 <kbd>Alt</kbd>+<kbd>Shift</kbd>+<kbd>J</kbd>）。',
     'The composer sits at the top of the page, with Markdown preview and backdating. On desktop there is a tray icon and a global hotkey (default <kbd>Alt</kbd>+<kbd>Shift</kbd>+<kbd>J</kbd>).', 1),
    ('<h3>AI 日 / 周 / 月 / 年总结</h3>', '<h3>AI daily / weekly / monthly / yearly summaries</h3>', 1),
    ('按周期逐层汇总，文首有“事项归纳”，把零散碎片合并概括、按周期分组。',
     'Summaries build up period by period, with a condensed item list at the top that merges scattered fragments and groups them by period.', 1),
    ('<h3>四种总结风格</h3>', '<h3>Four summary styles</h3>', 1),
    ('在设置里选择：均衡复盘、简洁清单、深度复盘或日记叙事。', 'Pick one in Settings: balanced, concise, reflective or narrative.', 1),
    ('<h3>历史版本可恢复</h3>', '<h3>Restorable version history</h3>', 1),
    ('重新生成或手动编辑总结时，旧版本都会保留，随时可以恢复。', 'When you regenerate or edit a summary, earlier versions are kept and can be restored anytime.', 1),
    ('<h3>本地与云端模型都行</h3>', '<h3>Local or cloud models</h3>', 1),
    ('本地和云端使用各自独立的地址，云端的 API Key 按厂商隔离保存。', 'Local and cloud use separate endpoints, and cloud API keys are stored separately per vendor.', 1),
    ('<h3>定时总结</h3>', '<h3>Scheduled summaries</h3>', 1),
    ('可以只提醒你该总结了，也可以自动生成。自动生成需要你明确开启。', 'Get a reminder that it is time to summarize, or generate automatically. Auto-generation is opt-in.', 1),
    ('<h3>搜索与活跃概览</h3>', '<h3>Search and activity</h3>', 1),
    ('支持全文搜索，并能看到近 7 天、30 天的记录情况和连续记录天数。', 'Full-text search, plus an overview of the last 7 and 30 days and your current streak.', 1),
    ('<h3>多平台，中英双语</h3>', '<h3>Multi-platform, bilingual</h3>', 1),
    ('提供 Windows、macOS、Android 安装包，界面支持中文和 English，主色是柔和的紫。', 'Installers for Windows, macOS and Android; the UI supports Chinese and English, with a soft purple accent.', 1),
    ('<h3>免费开源</h3>', '<h3>Free and open source</h3>', 1),
    ('以 MIT 协议开源，源码、安装包和开发文档都在 GitHub 上。', 'MIT-licensed. Source code, installers and developer docs are all on GitHub.', 1),
    # ---- how ----
    ('<h2>三步用起来</h2>', '<h2>Three steps</h2>', 1),
    ('<h3>随手记一句</h3>', '<h3>Jot a line</h3>', 1),
    ('想到什么就写什么：读了什么、聊了什么、做了什么。一句话就够。', 'Write whatever comes to mind: what you read, discussed or did. One sentence is enough.', 1),
    ('<h3>碎片自动成时间轴</h3>', '<h3>Fragments become a timeline</h3>', 1),
    ('每条碎片按时间归档在本机，可以搜索、补记，不依赖任何网络。', 'Each fragment is filed by time on your device. Search it, backdate it — no network needed.', 1),
    ('<h3>需要时让 AI 总结</h3>', '<h3>Let AI summarize when needed</h3>', 1),
    ('选好周期和风格再生成日、周、月或年总结。不配置模型，就完全不会发生。', 'Choose a period and a style, then generate a daily, weekly, monthly or yearly summary. If you configure no model, it never happens.', 1),
    # ---- privacy ----
    ('<h2>你的碎片，默认只在你手里</h2>', '<h2>Your fragments stay with you by default</h2>', 1),
    ('<h3 style="margin-top:0">默认怎么处理</h3>', '<h3 style="margin-top:0">How data is handled</h3>', 1),
    ('<li>笔记和总结默认保存在本机</li>', '<li>Notes and summaries are stored on your device by default</li>', 1),
    ('<li>只有你用云端模型生成某个时间范围的总结时，那段文字才会发给云端模型</li>', '<li>Text is sent to a cloud model only when you generate a summary for a selected range with a cloud provider</li>', 1),
    ('<li>API Key 存放在系统安全存储里，普通导出不会包含它</li>', '<li>API keys live in the system secure store and are excluded from plain exports</li>', 1),
    ('<h3 style="margin-top:0">想要多设备同步</h3>', '<h3 style="margin-top:0">Syncing across devices</h3>', 1),
    ('<li>同步是可选的，由你自己提供存储（文件夹、WebDAV 或 S3）</li>', '<li>Sync is optional and runs on storage you provide (folder, WebDAV or S3)</li>', 1),
    ('<li>同步内容端到端加密，存储服务商只能看到密文</li>', '<li>Synced data is end-to-end encrypted; storage providers only see ciphertext</li>', 1),
    ('<li>不想联网，用本地模型（如 Ollama）就能全程离线</li>', '<li>Prefer to stay offline? A local model (e.g. Ollama) keeps everything on your machine</li>', 1),
    # ---- download ----
    ('<h2>下载 Jot</h2>', '<h2>Download Jot</h2>', 1),
    ('安装包都发布在 GitHub Releases，点击按钮前往最新版本页面，选择对应平台的文件。',
     'All installers are published on GitHub Releases. Click through to the latest release and pick the file for your platform.', 1),
    ('<p>安装向导版，另附免安装的便携压缩包。</p>', '<p>A setup wizard, plus a portable zip that needs no installation.</p>', 1),
    ('<p>分 Apple 芯片和 Intel 两个版本，打开 DMG 后拖进“应用程序”即可。</p>', '<p>Separate builds for Apple Silicon and Intel. Open the DMG and drag the app to Applications.</p>', 1),
    ('<p>直接安装 APK，未上架应用商店。</p>', '<p>Sideload the APK. Not on Play Store.</p>', 1),
    ('>前往下载</a>', '>Go to download</a>', 3),
    ('<b>说明：</b>Android 安装包由 CI 构建，使用调试签名，需要在系统里允许安装来自此来源的应用。\n      iOS 目前没有安装包，可以按\n      <a href="https://github.com/AlexWuYh/Jot" target="_blank" rel="noopener noreferrer">仓库说明</a>用 Flutter 自行构建。',
     '<b>Note:</b> The Android package is built by CI and signed with a debug keystore, so you need to allow installing apps from this source.\n      There is no iOS installer yet; you can build it yourself with Flutter following the\n      <a href="https://github.com/AlexWuYh/Jot" target="_blank" rel="noopener noreferrer">repository instructions</a>.', 1),
    # ---- cta / footer ----
    ('<h2>从今天的第一句碎片开始</h2>', '<h2>Start with today\'s first fragment</h2>', 1),
    ('<p>免费、开源，数据在你手里。</p>', '<p>Free, open source, and your data stays with you.</p>', 1),
    ('target="_blank" rel="noopener noreferrer">下载最新版</a>', 'target="_blank" rel="noopener noreferrer">Download the latest release</a>', 1),
    ('target="_blank" rel="noopener noreferrer">查看源码</a>\n    </div>\n  </div>\n</section>', 'target="_blank" rel="noopener noreferrer">View source</a>\n    </div>\n  </div>\n</section>', 1),
    ('Jot（简迹）是开源项目（MIT） ·', 'Jot is open source (MIT) ·', 1),
    ('>GitHub 仓库</a> ·\n      <a href="https://github.com/AlexWuYh/Jot/releases/latest" target="_blank" rel="noopener noreferrer">发布页面</a>',
     '>GitHub repository</a> ·\n      <a href="https://github.com/AlexWuYh/Jot/releases/latest" target="_blank" rel="noopener noreferrer">Releases</a>', 1),
    ('aria-label="作者 AlexWuYh，打开 GitHub 个人主页" title="GitHub 个人主页"', 'aria-label="Author AlexWuYh — open GitHub profile" title="GitHub profile"', 1),
    ('<span>作者 <b>AlexWuYh</b></span>', '<span>Author <b>AlexWuYh</b></span>', 1),
    ("'切换到亮色主题' : '切换到暗色主题'", "'Switch to light theme' : 'Switch to dark theme'", 1),
]

for zh, en, n in PAIRS:
    found = s.count(zh)
    if found != n:
        sys.exit(f'生成英文页失败：中文页中应有 {n} 处、实际 {found} 处匹配以下文案，请同步更新 scripts/jot_gen_en.py：\n{zh}')
    s = s.replace(zh, en)

Path(dst).parent.mkdir(parents=True, exist_ok=True)
open(dst, 'w', encoding='utf-8').write(s)

# 友情链接依赖 products.json，生成英文页后统一同步一次
subprocess.run([sys.executable, str(ROOT / 'scripts/sync_friend_links.py')], check=True, stdout=subprocess.DEVNULL)
