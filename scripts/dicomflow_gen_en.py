#!/usr/bin/env python3
"""根据 DicomFLow-App/index.html（中文页）生成 DicomFLow-App/en/index.html（英文页）。

英文页是生成产物，请不要手动编辑；改中文页后运行本脚本（或直接提交，
pre-commit 钩子会自动运行）。若中文页里被替换的文案改了，下面的 PAIRS
会报错并指出没匹配上的文案，此时同步更新对应的中文原文与英文译文即可。

用法: python3 scripts/dicomflow_gen_en.py [源文件] [输出文件]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / 'DicomFLow-App/index.html')
dst = sys.argv[2] if len(sys.argv) > 2 else str(ROOT / 'DicomFLow-App/en/index.html')

s = open(src, encoding='utf-8').read()

# (中文原文, 英文译文, 期望出现次数)
PAIRS = [
    # ---- head ----
    ('<html lang="zh-CN"', '<html lang="en"', 1),
    ('<title>DicomFlow — CT / MRI 片子转 MP4 / GIF · 网页版 + App · 免费开源</title>',
     '<title>DicomFlow — Convert CT / MRI Scans to MP4 / GIF · Web &amp; App · Free and Open Source</title>', 1),
    ('content="DicomFlow 把医院给的 CT / MRI 片子压缩包转成 MP4 或 GIF，手机电脑的普通播放器就能看。提供免安装的网页版，以及完全离线的 Android / Windows App，免费开源。"',
     'content="DicomFlow converts the CT / MRI archives your hospital gives you into MP4 or GIF that any phone or computer can play. Use the web app with no install, or the fully offline Android / Windows app. Free and open source."', 1),
    ('content="CT 片子转视频, MRI 转 MP4, DICOM 转 MP4, DICOM 转 GIF, 医院影像 压缩包 播放, CT 光盘 查看, DICOM 在线转换, 离线, 开源, DicomFlow"',
     'content="convert CT scan to video, MRI to MP4, DICOM to MP4, DICOM to GIF, hospital imaging archive viewer, CT disc viewer, DICOM online converter, offline, open source, DicomFlow"', 1),
    ('<link rel="canonical" href="https://dicomflow.wuewa.cn/">', '<link rel="canonical" href="https://dicomflow.wuewa.cn/en/">', 1),
    ('<meta property="og:locale" content="zh_CN">\n<meta property="og:locale:alternate" content="en_US">',
     '<meta property="og:locale" content="en_US">\n<meta property="og:locale:alternate" content="zh_CN">', 1),
    ('<meta property="og:url" content="https://dicomflow.wuewa.cn/">', '<meta property="og:url" content="https://dicomflow.wuewa.cn/en/">', 1),
    ('content="DicomFlow — CT / MRI 片子转 MP4 / GIF，网页版 + App"',
     'content="DicomFlow — Convert CT / MRI Scans to MP4 / GIF, Web &amp; App"', 2),
    ('content="医院给的 CT、MRI 压缩包转成 MP4 或 GIF，普通播放器就能看。网页版免安装，App 完全离线，免费开源。"',
     'content="Turn hospital CT and MRI archives into MP4 or GIF that any player can open. No-install web app, fully offline app, free and open source."', 1),
    ('content="医院给的 CT、MRI 压缩包转成 MP4 或 GIF。网页版免安装，App 完全离线，免费开源。"',
     'content="Turn hospital CT and MRI archives into MP4 or GIF. No-install web app, fully offline app, free and open source."', 1),
    # JSON-LD
    ('"name": "DicomFlow 网页版",', '"name": "DicomFlow Web",', 1),
    ('"description": "上传医院的 DICOM 压缩包（zip / rar），在线转成 MP4 或 GIF，预览并下载。",',
     '"description": "Upload a hospital DICOM archive (zip / rar), convert it online to MP4 or GIF, then preview and download.",', 1),
    ('"description": "把医院 CT / MRI 片子（zip / rar / 7z）在本机转成 MP4 或 GIF 的离线应用，不作诊断依据。",',
     '"description": "An offline app that converts hospital CT / MRI scans (zip / rar / 7z) into MP4 or GIF on your own device. Not for diagnosis.",', 1),
    ('"inLanguage": "zh-CN",', '"inLanguage": "en",', 2),
    ('"url": "https://dicomflow.wuewa.cn/",', '"url": "https://dicomflow.wuewa.cn/en/",', 1),
    ('"priceCurrency": "CNY"', '"priceCurrency": "USD"', 2),
    # ---- nav ----
    ('alt="DicomFlow 应用图标"', 'alt="DicomFlow app icon"', 2),
    ('<a class="nav-link" href="#products">两种使用方式</a>', '<a class="nav-link" href="#products">Two ways to use</a>', 1),
    ('<a class="nav-link" href="#how">使用方法</a>', '<a class="nav-link" href="#how">How it works</a>', 1),
    ('<a class="nav-link" href="#download">下载</a>', '<a class="nav-link" href="#download">Download</a>', 1),
    ('<a class="lang-link" href="/en/" hreflang="en" lang="en" title="English">EN</a>',
     '<a class="lang-link" href="/" hreflang="zh-CN" lang="zh-CN" title="简体中文">中文</a>', 1),
    ('aria-label="切换明暗主题"', 'aria-label="Toggle light/dark theme"', 1),
    # ---- hero ----
    ('<b>开源</b> · 免费 · 网页版 + Android / Windows App', '<b>Open source</b> · Free · Web + Android / Windows app', 1),
    ('把医院给的 <strong>CT / MRI 片子</strong>，转成手机电脑都能直接播放的 MP4 或 GIF。',
     'Turn the <strong>CT / MRI scans</strong> from your hospital into MP4 or GIF that play on any phone or computer.', 1),
    ('''      不必再装专业阅片软件。想马上用，打开网页版即可；
      想让影像完全不离开自己的设备，就用离线的 App。''',
     '''      No more specialist viewer software. Want it right now? Open the web app.
      Want your images to never leave your device? Use the offline app.''', 1),
    ('        </svg>\n        打开网页版', '        </svg>\n        Open the web app', 1),
    ('        </svg>\n        下载 App', '        </svg>\n        Download the app', 1),
    ('<p class="hero-note">便于沟通查阅，不作诊断依据</p>', '<p class="hero-note">For communication only, not for diagnosis</p>', 1),
    # ---- products ----
    ('<span class="section-label">Two ways to use</span>\n      <h2>网页版或 App，按需选择</h2>',
     '<span class="section-label">Two ways to use</span>\n      <h2>Web app or app — your choice</h2>', 1),
    ('两者转换的都是同一类医院影像压缩包，区别在于在哪里转换。', 'Both convert the same kind of hospital imaging archives. The difference is where the conversion happens.', 1),
    ('alt="DicomFlow 网页版界面：上传医院压缩包，选择 MP4 或 GIF 输出格式并转换"',
     'alt="DicomFlow web app (Chinese UI): upload a hospital archive, choose MP4 or GIF and convert"', 1),
    ('<h3>DicomFlow 网页版<span class="tag">免安装</span></h3>', '<h3>DicomFlow Web<span class="tag">No install</span></h3>', 1),
    ('打开浏览器就能用，手机、电脑都行，临时看一次片子最省事。', 'Works in any browser on phone or computer. The easiest way to view a scan just once.', 1),
    ('<li>上传 zip / rar 压缩包，在线转换并预览下载</li>', '<li>Upload a zip / rar archive, convert online, preview and download</li>', 1),
    ('<li>可选 MP4 / GIF、清晰度、播放速度，还能合并成一个文件</li>', '<li>Choose MP4 / GIF, quality and playback speed, or merge into one file</li>', 1),
    ('<li>结果默认保留 24 小时，请及时保存</li>', '<li>Results are kept for 24 hours by default — save them promptly</li>', 1),
    ('<li>支持用 Docker 自行部署</li>', '<li>Self-host with Docker</li>', 1),
    ('>打开网页版</a>', '>Open the web app</a>', 3),
    ('>网页版源码</a>', '>Web app source</a>', 1),
    ('alt="DicomFlow App 转换页：打开医院给的 zip、rar 或 7z 压缩包，在本机转换"',
     'alt="DicomFlow app convert screen (Chinese UI): open a hospital zip, rar or 7z and convert on this device"', 1),
    ('<h3>DicomFlow App<span class="tag">完全离线</span></h3>', '<h3>DicomFlow App<span class="tag">Fully offline</span></h3>', 1),
    ('在 Android 或 Windows 上安装，全程在本机转换，影像不会离开你的设备。', 'Install it on Android or Windows. Everything is converted on your device, and your images never leave it.', 1),
    ('<li>支持 zip / rar / 7z，直接打开不用先解压</li>', '<li>zip / rar / 7z supported — open directly, no need to unpack first</li>', 1),
    ('<li>按片预览、捏合或滚轮缩放</li>', '<li>Slice-by-slice preview with pinch or scroll zoom</li>', 1),
    ('<li>分享单个文件，或导出全部结果</li>', '<li>Share a single file or export all results</li>', 1),
    ('<li>历史记录只留在本机，可设 1 / 7 / 30 天</li>', '<li>History stays on your device for 1, 7 or 30 days</li>', 1),
    ('>下载 App</a>', '>Download the app</a>', 2),
    ('>App 源码</a>', '>App source</a>', 1),
    ('<tr><th></th><th>网页版</th><th>App</th></tr>', '<tr><th></th><th>Web app</th><th>App</th></tr>', 1),
    ('<tr><th>安装</th><td>无需安装，浏览器直接用</td><td>Android 安装 APK，Windows 安装包，macOS 可试用</td></tr>',
     '<tr><th>Install</th><td>Nothing to install — just use the browser</td><td>Android APK, Windows installer, macOS build to try</td></tr>', 1),
    ('<tr><th>在哪里转换</th><td>上传到服务器转换（可自行 Docker 部署）</td><td>在你的设备本机转换，完全离线</td></tr>',
     '<tr><th>Where it converts</th><td>On a server after upload (you can self-host with Docker)</td><td>On your own device, fully offline</td></tr>', 1),
    ('<tr><th>压缩包格式</th><td>zip、rar</td><td>zip、rar、7z</td></tr>',
     '<tr><th>Archive types</th><td>zip, rar</td><td>zip, rar, 7z</td></tr>', 1),
    ('<tr><th>结果保留</th><td>默认 24 小时后自动清理</td><td>留在本机，可设 1 / 7 / 30 天</td></tr>',
     '<tr><th>Result retention</th><td>Cleaned up automatically after 24 hours by default</td><td>Kept on your device for 1, 7 or 30 days</td></tr>', 1),
    ('<tr><th>适合</th><td>临时用一次，或手边设备不方便装软件</td><td>影像较敏感、经常使用，或希望离线处理</td></tr>',
     '<tr><th>Best for</th><td>One-off use, or when you cannot install software</td><td>Sensitive images, frequent use, or offline processing</td></tr>', 1),
    ('<b>隐私提示：</b>使用网页版时，压缩包会上传到服务器处理。如果影像比较敏感，建议使用离线的 App，或按网页版仓库的说明自行部署。',
     '<b>Privacy note:</b> with the web app, your archive is uploaded to a server for processing. If your images are sensitive, use the offline app, or self-host following the web app repository.', 1),
    # ---- features ----
    ('<h2>拿到片子，不用再到处找阅片软件</h2>', '<h2>Got your scans? No more hunting for viewer software</h2>', 1),
    ('医院拷给你的光盘或压缩包里是 DICOM 文件，普通电脑和手机打不开。DicomFlow 帮你一步转成能直接播放、能发给医生的视频。',
     'The disc or archive from your hospital contains DICOM files that ordinary computers and phones cannot open. DicomFlow turns them into a video you can play and send to a doctor in one step.', 1),
    ('<h3>转成 MP4 或 GIF</h3>', '<h3>Convert to MP4 or GIF</h3>', 1),
    ('MP4 最适合发给医生播放，GIF 适合在聊天里快速查看。多个序列还可以合并成一个文件。',
     'MP4 is best for sending to a doctor; GIF is handy for a quick look in a chat. Multiple series can be merged into one file.', 1),
    ('<h3>数据可控</h3>', '<h3>You stay in control</h3>', 1),
    ('App 全程在本机转换，网页版结果定时自动清理。没有账号体系，也不需要云端存储。',
     'The app converts everything on your device, and web results are cleaned up automatically. No accounts, no cloud storage.', 1),
    ('<h3>直接用压缩包</h3>', '<h3>Works with archives directly</h3>', 1),
    ('医院给的压缩包直接选就行，不用先手动解压。App 已内置 ffmpeg 与 7-Zip，Windows 安装包开箱即用。',
     'Just pick the archive from your hospital — no manual unpacking. The app bundles ffmpeg and 7-Zip, so the Windows installer works out of the box.', 1),
    ('<h3>预览再导出</h3>', '<h3>Preview, then export</h3>', 1),
    ('转换后先预览。App 支持逐片查看、捏合或滚轮放大，网页版支持在线预览与下载。',
     'Preview before you save. The app lets you step through slices and zoom with pinch or scroll; the web app offers online preview and download.', 1),
    ('<h3>方便转发给医生</h3>', '<h3>Easy to forward to a doctor</h3>', 1),
    ('微信、相册、电脑播放器都能打开转换后的文件，会诊沟通、家属转存都更省事。',
     'Chat apps, photo galleries and desktop players can all open the result, which makes consultations and sharing with family easier.', 1),
    ('<h3>免费开源</h3>', '<h3>Free and open source</h3>', 1),
    ('网页版与 App 都以 MIT 协议开源，源码、发行包和 Docker 镜像都能在 GitHub 上获取。',
     'Both the web app and the app are MIT-licensed. Source code, releases and Docker images are all available on GitHub.', 1),
    # ---- how ----
    ('<h2>三步完成</h2>', '<h2>Three steps</h2>', 1),
    ('<h3>选择压缩包</h3>', '<h3>Choose the archive</h3>', 1),
    ('选择医院给的 zip / rar（App 还支持 7z），也可以直接拖进窗口。', 'Pick the zip / rar from your hospital (the app also supports 7z), or just drag it into the window.', 1),
    ('<h3>选格式并转换</h3>', '<h3>Pick a format and convert</h3>', 1),
    ('选 <b>MP4</b>（发给医生更合适）或 <b>GIF</b>，需要时把多个序列合并成一个文件，然后开始转换。',
     'Choose <b>MP4</b> (best for sending to a doctor) or <b>GIF</b>, optionally merge series into one file, then start converting.', 1),
    ('<h3>预览并保存</h3>', '<h3>Preview and save</h3>', 1),
    ('预览满意后下载或分享。网页版的结果默认只保留 24 小时，请及时保存。', 'Download or share once you are happy with the preview. Web results are kept for only 24 hours by default, so save them promptly.', 1),
    # ---- formats ----
    ('<h2>支持转换的片源</h2>', '<h2>What you can convert</h2>', 1),
    ('<tr><th>你拿到的</th><td>医院 CT / MRI 片子：DICOM 影像（医院拷盘、光盘里常见的那种）</td></tr>',
     '<tr><th>You have</th><td>Hospital CT / MRI scans: DICOM images (the kind found on the discs hospitals copy for you)</td></tr>', 1),
    ('<tr><th>压缩包</th><td>网页版：zip、rar；App：zip、rar、7z</td></tr>',
     '<tr><th>Archive</th><td>Web app: zip, rar; app: zip, rar, 7z</td></tr>', 1),
    ('<tr><th>包里的文件</th><td>', '<tr><th>Files inside</th><td>', 1),
    ('，或没有后缀的 DICOM 文件</td></tr>', ', or DICOM files with no extension</td></tr>', 1),
    ('<tr><th>转成</th><td>MP4 视频或 GIF 动图</td></tr>', '<tr><th>Output</th><td>MP4 video or GIF</td></tr>', 1),
    ('<b>提示：</b>常见的未压缩、JPEG、RLE 编码的片子都可以转换。JPEG 2000 等特殊压缩可能转不了，\n      可以请医院改为导出未压缩或 JPEG 格式。',
     '<b>Tip:</b> Uncompressed, JPEG and RLE images usually convert. JPEG 2000 and some other hospital compressions may not —\n      ask the hospital for an uncompressed or JPEG export.', 1),
    ('<h3 style="margin-top:0">它会做的</h3>', '<h3 style="margin-top:0">What it does</h3>', 1),
    ('<li>把 DICOM 转成 MP4 / GIF，方便播放与转发</li>', '<li>Convert DICOM into MP4 / GIF for easy playback and sharing</li>', 1),
    ('<li>预览转换结果</li>', '<li>Preview the converted result</li>', 1),
    ('<li>下载、分享或导出结果</li>', '<li>Download, share or export the result</li>', 1),
    ('<h3 style="margin-top:0">它不会做的</h3>', '<h3 style="margin-top:0">What it does not do</h3>', 1),
    ('<li>诊断：没有测量、调窗、MPR</li>', '<li>Diagnose — no measurements, windowing or MPR</li>', 1),
    ('<li>替代医院的专业阅片设备</li>', '<li>Replace your hospital\'s professional viewing equipment</li>', 1),
    ('<li>账号体系或云端存储</li>', '<li>Accounts or cloud storage</li>', 1),
    ('DicomFlow 仅便于沟通查阅，<b>不作诊断依据</b>，也不是医疗器械。如需诊断，请使用医院提供的专业阅片软件，并遵循医生的建议。',
     'DicomFlow is for communication only and is <b>not for diagnosis</b>. It is not a medical device. For diagnosis, use the professional viewer provided by your hospital and follow your doctor\'s advice.', 1),
    # ---- download ----
    ('<h2>开始使用</h2>', '<h2>Get started</h2>', 1),
    ('网页版直接打开即可；App 的安装包都发布在 GitHub Releases，点击按钮前往最新版本页面选择对应文件。',
     'Open the web app right away. The app installers are published on GitHub Releases — click through to the latest release and pick the file for your platform.', 1),
    ('<h3 style="margin-top:0">网页版<span class="tag">免安装</span></h3>', '<h3 style="margin-top:0">Web app<span class="tag">No install</span></h3>', 1),
    ('浏览器打开即用。若站点要求访问密码，请向部署方索取。', 'Works right in your browser. If the site asks for an access password, request it from the operator.', 1),
    ('<p>直接安装 APK，未上架应用商店。</p>', '<p>Sideload the APK. Not on Play Store.</p>', 1),
    ('<p>标准安装包（开始菜单、可卸载），已含 ffmpeg 和 7-Zip。</p>', '<p>Standard installer (Start Menu, uninstall). ffmpeg and 7-Zip are included.</p>', 1),
    ('>前往下载</a>', '>Go to download</a>', 2),
    ('''      macOS 试用版（<code>DicomFlow-v*-macos.zip</code>）同样在
      <a href="https://github.com/AlexWuYh/DicomFlow-App/releases/latest" target="_blank" rel="noopener noreferrer">App 的 Releases 页面</a>，
      不是商店版。想自己部署网页版，可以看
      <a href="https://github.com/AlexWuYh/DicomFlow" target="_blank" rel="noopener noreferrer">网页版仓库</a>里的 Docker 说明。''',
     '''      The macOS trial build (<code>DicomFlow-v*-macos.zip</code>) is on the
      <a href="https://github.com/AlexWuYh/DicomFlow-App/releases/latest" target="_blank" rel="noopener noreferrer">app's Releases page</a> too;
      it is not a store build. To self-host the web app, see the Docker instructions in the
      <a href="https://github.com/AlexWuYh/DicomFlow" target="_blank" rel="noopener noreferrer">web app repository</a>.''', 1),
    # ---- cta / footer ----
    ('<h2>拿到片子，三步就能看</h2>', '<h2>Got your scans? Three steps and you can watch them</h2>', 1),
    ('<p>免费、开源，网页版和 App 任选。</p>', '<p>Free and open source — pick the web app or the app.</p>', 1),
    ('DicomFlow 是开源项目（MIT） ·', 'DicomFlow is open source (MIT) ·', 1),
    ('网页版：<a href=', 'Web app: <a href=', 1),
    ('>GitHub 仓库</a> ·\n      App：<a href=', '>GitHub repository</a> ·\n      App: <a href=', 1),
    ('>GitHub 仓库</a> ·\n      <a href="https://github.com/AlexWuYh/DicomFlow-App/releases/latest" target="_blank" rel="noopener noreferrer">发布页面</a>',
     '>GitHub repository</a> ·\n      <a href="https://github.com/AlexWuYh/DicomFlow-App/releases/latest" target="_blank" rel="noopener noreferrer">App releases</a>', 1),
    ('App 捆绑的 FFmpeg（libx264）为 GPL-3.0，带编码器的安装包按 GPL-3.0 分发；捆绑的 7-Zip 为 LGPL（含 unRAR 限制）。',
     'The app bundles FFmpeg (libx264, GPL-3.0); builds that include it are distributed under GPL-3.0. The bundled 7-Zip is LGPL with the unRAR restriction.', 1),
    ("aria-label=\"作者 AlexWuYh，打开 GitHub 个人主页\" title=\"GitHub 个人主页\"","aria-label=\"Author AlexWuYh — open GitHub profile\" title=\"GitHub profile\"",1),
    ("<span>作者 <b>AlexWuYh</b></span>","<span>Author <b>AlexWuYh</b></span>",1),
    ("'切换到亮色主题' : '切换到暗色主题'", "'Switch to light theme' : 'Switch to dark theme'", 1),
]

for zh, en, n in PAIRS:
    found = s.count(zh)
    if found != n:
        sys.exit(f'生成英文页失败：中文页中应有 {n} 处、实际 {found} 处匹配以下文案，请同步更新 scripts/dicomflow_gen_en.py：\n{zh}')
    s = s.replace(zh, en)

Path(dst).parent.mkdir(parents=True, exist_ok=True)
open(dst, 'w', encoding='utf-8').write(s)
