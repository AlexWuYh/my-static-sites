#!/usr/bin/env python3
"""根据 ScreenClock/index.html（中文页）生成 ScreenClock/en/index.html（英文页）。

英文页是生成产物，请不要手动编辑；改中文页后运行本脚本（或直接提交，
pre-commit 钩子会自动运行）。若中文页里被替换的文案改了，下面的 rep() 会
报错，此时同步更新本脚本中对应的中文原文与英文译文即可。

用法: python3 scripts/screenclock_gen_en.py [源文件] [输出文件]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / 'ScreenClock/index.html')
dst = sys.argv[2] if len(sys.argv) > 2 else str(ROOT / 'ScreenClock/en/index.html')
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    if s.count(a)!=n:
        sys.exit(f'生成英文页失败：中文页中应有 {n} 处、实际 {s.count(a)} 处匹配以下文案，请同步更新 scripts/screenclock_gen_en.py：\n{a}')
    s=s.replace(a,b)

rep('<html lang="zh-CN"','<html lang="en"')
rep('<title>ScreenClock — Android 全屏时钟 · 床头时钟 · 番茄钟 · 旧手机改造</title>','<title>ScreenClock — Fullscreen Clock for Android · Bedside &amp; Desk Clock · Pomodoro</title>')
rep('content="ScreenClock 是一款免费开源的 Android 全屏时钟（床头时钟 / 桌面时钟），把闲置旧手机变成好看的翻页钟，支持十余款主题钟面、番茄钟专注、纪念日倒计时与可选天气。"',
    'content="ScreenClock is a free, open-source fullscreen clock for Android. Turn an old phone or tablet into a bedside or desk flip clock with 10+ clock themes, a Pomodoro focus timer, anniversary countdowns and optional weather."')
rep('content="Android 全屏时钟, 床头时钟, 桌面时钟, 翻页时钟, 番茄钟, 纪念日倒计时, 旧手机改造, 开源, ScreenClock"',
    'content="Android fullscreen clock, bedside clock, desk clock, flip clock, Pomodoro timer, countdown, old phone clock, open source, ScreenClock"')
rep('<link rel="canonical" href="https://screenclock.wuewa.cn/">','<link rel="canonical" href="https://screenclock.wuewa.cn/en/">')
rep('<meta property="og:locale" content="zh_CN">\n<meta property="og:locale:alternate" content="en_US">','<meta property="og:locale" content="en_US">\n<meta property="og:locale:alternate" content="zh_CN">')
rep('<meta property="og:url" content="https://screenclock.wuewa.cn/">','<meta property="og:url" content="https://screenclock.wuewa.cn/en/">')
rep('ScreenClock — Android 全屏时钟 · 床头时钟 · 番茄钟"','ScreenClock — Fullscreen Clock for Android"',2)
rep('content="把闲置的手机或平板变成好看、安静的全屏时钟：十余款主题钟面、番茄钟专注、纪念日倒计时。免费开源。"','content="Turn an idle phone or tablet into a calm, beautiful fullscreen clock: 10+ themes, Pomodoro focus timer, anniversary countdowns. Free and open source."')
rep('content="把闲置的手机或平板变成好看、安静的全屏时钟。免费开源。"','content="Turn an idle phone or tablet into a calm, beautiful fullscreen clock. Free and open source."')
rep('"alternateName": "ScreenClock 全屏时钟",','"alternateName": "ScreenClock Fullscreen Clock",')
rep('"description": "免费开源的 Android 全屏时钟，支持十余款主题钟面、番茄钟专注、纪念日倒计时与可选天气。",','"description": "Free, open-source fullscreen clock for Android with 10+ clock themes, a Pomodoro focus timer, anniversary countdowns and optional weather.",')
rep('"url": "https://screenclock.wuewa.cn/",','"url": "https://screenclock.wuewa.cn/en/",')
rep('"price": "0", "priceCurrency": "CNY"','"price": "0", "priceCurrency": "USD"')
rep('href="app-icon.png"','href="/app-icon.png"',2)
rep('src="app-icon.png"','src="/app-icon.png"')
rep('alt="ScreenClock 应用图标"','alt="ScreenClock app icon"')
rep('<a class="lang-link" href="/en/" hreflang="en" lang="en" title="English">EN</a>','<a class="lang-link" href="/" hreflang="zh-CN" lang="zh-CN" title="简体中文">中文</a>')
pairs=[
('aria-label="打开 ScreenClock GitHub 仓库" title="GitHub 仓库"','aria-label="Open ScreenClock on GitHub" title="GitHub repository"',1),
('aria-label="切换明暗主题"','aria-label="Toggle light/dark theme"',1),
('>界面预览</a>','>Screenshots</a>',1),
('>功能</a>','>Features</a>',1),
('<b>开源</b> · Android 8.0+ · 免费','<b>Open source</b> · Android 8.0+ · Free',1),
('把闲置的手机或平板，变成一面<strong>好看、安静</strong>的全屏时钟。','Turn an idle phone or tablet into a <strong>calm, beautiful</strong> fullscreen clock.',1),
('''      一款免费开源的 Android 床头时钟 / 桌面时钟：多款主题钟面、番茄钟专注、
      纪念日倒计时与可选天气，旧手机改造后放在床头或桌面都刚刚好。''','''      A free, open-source bedside and desk clock for Android: multiple clock themes,
      a Pomodoro focus timer, anniversary countdowns and optional weather.
      Give your old phone a second life on the nightstand or desk.''',1),
('下载最新版 APK','Download the latest APK',1),
('查看源码','View source',1),
('v0.4.0 · 发布密钥签名 · 从 GitHub Releases 直接下载','v0.4.0 · Signed with a release key · Download directly from GitHub Releases',1),
('<span class="section-label">界面预览</span>','<span class="section-label">Screenshots</span>',1),
('看看它在桌面上是什么样','See how it looks on your desk',1),
('''        从翻页钟面到番茄钟专注，再到纪念日倒计时，
        这里是在手机上实际运行时的样子。''','''        From the flip clock to the Pomodoro timer and anniversary countdowns —
        here is how it actually looks running on a phone.''',1),
('alt="ScreenClock 翻页主题横屏钟面：黑底两块时分页片"','alt="ScreenClock flip clock theme in landscape: two large hour and minute flaps on a black background"',1),
('<h3>翻页主题 · 横屏</h3>','<h3>Flip theme · Landscape</h3>',1),
('机械页片翻折的翻页钟面，墨黑底色配大字号时分页片，是项目最经典的外观之一。','A mechanical flip clock with large hour and minute flaps on an ink-black background — one of the most classic looks in the app.',1),
('alt="ScreenClock 番茄钟专注页面：环形进度与倒计时"','alt="ScreenClock Pomodoro focus screen with a ring progress indicator and countdown"',1),
('<h3>番茄钟专注</h3>\n          <p>环形进度配大号倒计时，支持专注 / 短休 / 长休 / 自定义时长，暂停后返回钟面计时也不会中断。</p>','<h3>Pomodoro focus</h3>\n          <p>A progress ring with a big countdown. Focus, short break, long break or custom durations; the timer keeps running when you go back to the clock.</p>',1),
('alt="ScreenClock 纪念日倒计时页面：天、时、分、秒的完整倒计时"','alt="ScreenClock anniversary countdown showing days, hours, minutes and seconds"',1),
('<h3>纪念日倒计时</h3>\n          <p>以“天 : 时 : 分 : 秒”完整呈现，支持卡片与沉浸两种样式，亮色 / 暗色可独立设置。</p>','<h3>Anniversary countdown</h3>\n          <p>Shown as days : hours : minutes : seconds, in a card or immersive style, with separate light and dark looks.</p>',1),
('themes-zh.webp','themes-en.webp',2),
('alt="ScreenClock 全部主题预览：翻页为左上大图，其余按网格排列"','alt="All ScreenClock themes: the flip clock on the top left, the rest arranged in a grid"',1),
('<h3>全部主题一览</h3>\n          <p>翻页、简约数字、经典模拟、地球、流体、复古霓虹、管钟、情侣、小屋等十余款钟面，一张图看完所有选择。</p>','<h3>All themes at a glance</h3>\n          <p>Flip, minimal digits, classic analog, earth, fluid, retro neon, tube, couple, cozy house and more — 10+ clock faces in one picture.</p>',1),
('不只是时钟','More than a clock',1),
('在显示时间之外，ScreenClock 还准备了几个长期陪伴的小功能。','Beyond telling the time, ScreenClock comes with a few small features that stay useful every day.',1),
('<h3>多款主题钟面</h3>\n        <p>翻页、极简数字、经典指针、地球、流体、霓虹、管钟、情侣、小屋等十余款风格，每款都有独立的数字字体。</p>','<h3>Multiple clock themes</h3>\n        <p>Flip, minimal digits, classic hands, earth, fluid, neon, tube, couple, cozy house and more — 10+ styles, each with its own digit font.</p>',1),
('<h3>番茄钟专注</h3>\n        <p>环形进度配大号倒计时，专注 / 短休 / 长休 / 自定义模式，暂停可续，中途返回钟面计时不中断。</p>','<h3>Pomodoro focus timer</h3>\n        <p>A progress ring with a big countdown. Focus, short break, long break and custom modes; pause and resume, and the timer survives switching back to the clock.</p>',1),
('<h3>纪念日倒计时</h3>\n        <p>卡片与沉浸两种风格，支持亮色与暗色，每条纪念日可选图标，提供 7 天 / 30 天 / 100 天 / 明年今日快捷日期。</p>','<h3>Anniversary countdown</h3>\n        <p>Card and immersive styles in light or dark, a custom icon per event, and quick dates for 7 days, 30 days, 100 days and this day next year.</p>',1),
('<h3>可选天气</h3>\n        <p>需要时在钟面上显示天气信息，不需要时完全隐藏。日期、农历、星期与节假日均可独立开关。</p>',"<h3>Optional weather</h3>\n        <p>Show the weather on the clock when you want it, hide it completely when you don't. Date, lunar calendar, weekday and holidays can each be toggled on their own.</p>",1),
('Flip 翻页','Flip',1),('Earth 地球','Earth',1),('Fluid 流体','Fluid',1),('Tube 管钟','Tube',1),('Couple 情侣','Couple',1),('Minimal 极简','Minimal',1),
('准备好让旧手机重新上岗了吗？','Ready to put your old phone back to work?',1),
('下载最新 APK，在 Android 8.0 及以上设备安装即可。','Download the latest APK and install it on any device running Android 8.0 or later.',1),
('前往 GitHub Releases','Go to GitHub Releases',1),
('ScreenClock 是开源项目 ·','ScreenClock is open source ·',1),
('>GitHub 仓库</a>','>GitHub repository</a>',1),
('>发布页面</a>','>Releases</a>',1),
("aria-label=\"作者 AlexWuYh，打开 GitHub 个人主页\" title=\"GitHub 个人主页\"","aria-label=\"Author AlexWuYh — open GitHub profile\" title=\"GitHub profile\"",1),
("<span>作者 <b>AlexWuYh</b></span>","<span>Author <b>AlexWuYh</b></span>",1),
("'切换到亮色主题' : '切换到暗色主题'","'Switch to light theme' : 'Switch to dark theme'",1),
]
for a,b,n in pairs: rep(a,b,n)
Path(dst).parent.mkdir(parents=True, exist_ok=True)
open(dst, 'w', encoding='utf-8').write(s)
