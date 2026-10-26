#!/usr/bin/env python3
"""根据 easy-docker-proxy/index.html（中文页）生成 easy-docker-proxy/en/index.html（英文页）。

英文页是生成产物，请不要手动编辑；改中文页后运行本脚本（或直接提交，
pre-commit 钩子会自动运行）。若中文页里被替换的文案改了，下面的 PAIRS
会报错并指出没匹配上的文案，此时同步更新对应的中文原文与英文译文即可。

用法: python3 scripts/edp_gen_en.py [源文件] [输出文件]
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / 'easy-docker-proxy/index.html')
dst = sys.argv[2] if len(sys.argv) > 2 else str(ROOT / 'easy-docker-proxy/en/index.html')

s = open(src, encoding='utf-8').read()

# (中文原文, 英文译文, 期望出现次数)
PAIRS = [
    # ---- head ----
    ('<html lang="zh-CN"', '<html lang="en"', 1),
    ('<title>easy-docker-proxy — 多上游 Docker 镜像加速代理 · 零镜像缓存 · 拉取统计 · 开源免费</title>',
     '<title>easy-docker-proxy — Multi-Upstream Docker Registry Proxy · No Layer Cache · Pull Stats · Free and Open Source</title>', 1),
    ('content="easy-docker-proxy（EDP）是一个轻量的多上游 Docker Registry 加速代理：流式转发、不缓存镜像层，一个自有域名同时加速 Docker Hub、GHCR、Quay、registry.k8s.io 等，内置拉取统计控制台。开源免费，Docker Compose 一键部署。"',
     'content="easy-docker-proxy (EDP) is a lightweight multi-upstream Docker Registry proxy: streaming pull-through with no image layer cache, one domain of your own for Docker Hub, GHCR, Quay, registry.k8s.io and more, plus a built-in pull stats console. Free and open source, deployed with Docker Compose."', 1),
    ('content="Docker 镜像加速, Docker 镜像代理, Registry 代理, registry-mirrors, Docker Hub 加速, ghcr 加速, 自建镜像加速, 拉取统计, easy-docker-proxy, EDP"',
     'content="Docker registry proxy, Docker mirror, registry-mirrors, Docker Hub mirror, ghcr mirror, self-hosted registry mirror, pull-through proxy, pull stats, easy-docker-proxy, EDP"', 1),
    ('<link rel="canonical" href="https://edp.wuewa.cn/">', '<link rel="canonical" href="https://edp.wuewa.cn/en/">', 1),
    ('<meta property="og:locale" content="zh_CN">\n<meta property="og:locale:alternate" content="en_US">',
     '<meta property="og:locale" content="en_US">\n<meta property="og:locale:alternate" content="zh_CN">', 1),
    ('<meta property="og:url" content="https://edp.wuewa.cn/">', '<meta property="og:url" content="https://edp.wuewa.cn/en/">', 1),
    ('content="easy-docker-proxy — 一个域名，加速所有 Docker 镜像仓库"', 'content="easy-docker-proxy — One domain to speed up every Docker registry"', 2),
    ('content="轻量的多上游 Docker Registry 加速代理：流式转发、零镜像缓存、内置拉取统计。开源免费。"',
     'content="A lightweight multi-upstream Docker Registry proxy: streaming pull-through, no layer cache, built-in pull stats. Free and open source."', 1),
    ('content="多上游 Docker Registry 加速代理，零镜像缓存，内置拉取统计。开源免费。"',
     'content="Multi-upstream Docker Registry proxy with no layer cache and built-in pull stats. Free and open source."', 1),
    ('"description": "轻量的多上游 Docker Registry 加速代理，流式转发、不缓存镜像层，内置拉取统计控制台。",',
     '"description": "A lightweight multi-upstream Docker Registry proxy with streaming pull-through, no image layer cache and a built-in pull stats console.",', 1),
    ('"url": "https://edp.wuewa.cn/",', '"url": "https://edp.wuewa.cn/en/",', 1),
    ('"priceCurrency": "CNY"', '"priceCurrency": "USD"', 1),
    # ---- nav ----
    ('alt="easy-docker-proxy 应用图标"', 'alt="easy-docker-proxy app icon"', 2),
    ('<a class="nav-link" href="#features">功能</a>', '<a class="nav-link" href="#features">Features</a>', 1),
    ('<a class="nav-link" href="#upstreams">上游</a>', '<a class="nav-link" href="#upstreams">Upstreams</a>', 1),
    ('<a class="nav-link" href="#deploy">部署</a>', '<a class="nav-link" href="#deploy">Deploy</a>', 1),
    ('<a class="lang-link" href="/en/" hreflang="en" lang="en" title="English">EN</a>',
     '<a class="lang-link" href="/" hreflang="zh-CN" lang="zh-CN" title="简体中文">中文</a>', 1),
    ('aria-label="打开 easy-docker-proxy GitHub 仓库" title="GitHub 仓库"', 'aria-label="Open easy-docker-proxy on GitHub" title="GitHub repository"', 1),
    ('aria-label="切换明暗主题"', 'aria-label="Toggle light/dark theme"', 1),
    # ---- hero ----
    ('<b>开源</b> · 零镜像缓存 · 自托管 · Docker 部署', '<b>Open source</b> · No layer cache · Self-hosted · Docker deploy', 1),
    ('多上游 Docker 镜像<strong>加速代理</strong>，一个域名全搞定。', 'A multi-upstream Docker <strong>registry proxy</strong> — one domain for all of them.', 1),
    ('''      流式转发，不缓存镜像层，也不碰 Docker socket。
      Docker Hub 保持原镜像名，其他仓库用域名路径前缀，还自带一个拉取统计控制台。''',
     '''      Streaming pull-through: no image layer cache, and no Docker socket.
      Docker Hub keeps its original image names, other registries use a path prefix on your domain, and a pull stats console is built in.''', 1),
    ('        快速部署\n      </a>', '        Quick deploy\n      </a>', 1),
    ('target="_blank" rel="noopener noreferrer">查看源码</a>\n    </div>\n    <p class="hero-note">', 'target="_blank" rel="noopener noreferrer">View source</a>\n    </div>\n    <p class="hero-note">', 1),
    ('</a> MIT 开源 · 数据面与管理面分离</p>', '</a> MIT licensed · Data plane and admin plane are separate</p>', 1),
    ('alt="EDP 统计控制台分析看板：拉取趋势、上游占比、错误率和活跃客户端"', 'alt="EDP stats console dashboard: pull trends, upstream share, error rate and active clients"', 1),
    ('统计控制台（演示数据）：拉取趋势、上游占比和错误率一目了然。', 'Stats console (demo data): pull trends, upstream share and error rate at a glance.', 1),
    # ---- about ----
    ('<h2>一个轻量的 Registry 加速代理</h2>', '<h2>A lightweight registry proxy</h2>', 1),
    ('只做一件事：把拉取请求转发给对应的上游仓库，不囤镜像，也不管容器。', 'It does one thing: forward pull requests to the right upstream registry. No hoarding images, no managing containers.', 1),
    ('<tr><th>定位</th><td>多上游 Docker Registry 加速代理，自己的服务器、自己的域名</td></tr>',
     '<tr><th>What</th><td>A multi-upstream Docker Registry proxy on your own server and your own domain</td></tr>', 1),
    ('<tr><th>缓存</th><td>不缓存镜像层，流式转发；磁盘里只有 SQLite 元数据（拉取记录）</td></tr>',
     '<tr><th>Cache</th><td>No image layer cache, streaming pull-through; only SQLite metadata (pull records) on disk</td></tr>', 1),
    ('<tr><th>入口</th><td>一个域名：Docker Hub 走 <code>registry-mirrors</code>，其他上游用路径前缀</td></tr>',
     '<tr><th>Entry</th><td>One domain: Docker Hub goes through <code>registry-mirrors</code>, other upstreams use a path prefix</td></tr>', 1),
    ('<tr><th>管理</th><td>内置统计网页；没有 Docker socket，也没有容器管理</td></tr>',
     '<tr><th>Admin</th><td>Built-in stats web UI; no Docker socket, no container management</td></tr>', 1),
    ('<tr><th>技术</th><td>Go 编写，Docker Compose 部署，MIT 开源</td></tr>',
     '<tr><th>Stack</th><td>Written in Go, deployed with Docker Compose, MIT licensed</td></tr>', 1),
    # ---- features ----
    ('<h2>轻、省心、看得见</h2>', '<h2>Light, low-maintenance, observable</h2>', 1),
    ('<h3>流式转发，零层缓存</h3>', '<h3>Streaming, no layer cache</h3>', 1),
    ('<p>镜像层边下边转，不落盘，不必为缓存预留磁盘空间。</p>', '<p>Layers are relayed as they download and never written to disk, so there is no cache to size or clean up.</p>', 1),
    ('<h3>一个域名，多个上游</h3>', '<h3>One domain, many upstreams</h3>', 1),
    ('<p>Docker Hub 通过 <code>registry-mirrors</code> 保持原镜像名；<code>ghcr.io</code>、<code>quay.io</code> 等在域名后加路径前缀。</p>',
     '<p>Docker Hub keeps its image names through <code>registry-mirrors</code>; <code>ghcr.io</code>, <code>quay.io</code> and others add a path prefix after your domain.</p>', 1),
    ('<h3>九类上游开箱即用</h3>', '<h3>Nine upstreams out of the box</h3>', 1),
    ('<p>Docker Hub、GHCR、Quay、GCR、registry.k8s.io、MCR、NVCR、Elastic、公共 ECR，可以关闭，也能自己加。</p>',
     '<p>Docker Hub, GHCR, Quay, GCR, registry.k8s.io, MCR, NVCR, Elastic and public ECR. Turn any off, or add your own.</p>', 1),
    ('<h3>拉取统计控制台</h3>', '<h3>Pull stats console</h3>', 1),
    ('<p>分析看板、上游仓库分析、镜像列表和事件记录，支持亮色与暗色主题。</p>',
     '<p>A dashboard, per-upstream analytics, an image list and an event log, in light and dark themes.</p>', 1),
    ('<h3>上游凭据可选</h3>', '<h3>Optional upstream credentials</h3>', 1),
    ('<p>默认匿名拉取公开镜像；填上各上游的用户名和令牌，就能拉私有镜像，或避开 Docker Hub 的限流。</p>',
     '<p>Public images are pulled anonymously by default. Add a username and token per upstream to pull private images or avoid Docker Hub rate limits.</p>', 1),
    ('<h3>客户端登录鉴权</h3>', '<h3>Client login</h3>', 1),
    ('<p>可以开启 <code>pull_auth</code>，只有 <code>docker login</code> 过本代理的客户端才能拉取，避免被陌生人蹭用。</p>',
     '<p>Turn on <code>pull_auth</code> so only clients that ran <code>docker login</code> against the proxy can pull, and strangers cannot use it.</p>', 1),
    ('<h3>数据面与管理面分离</h3>', '<h3>Separate data and admin planes</h3>', 1),
    ('<p>数据面默认只监听 <code>127.0.0.1:5000</code>，由 TLS 反代对外发布；管理面 <code>:5001</code> 默认不对公网开放。</p>',
     '<p>The data plane listens on <code>127.0.0.1:5000</code> by default and is published through a TLS reverse proxy; the admin plane on <code>:5001</code> is not exposed publicly by default.</p>', 1),
    ('<h3>不碰 Docker socket</h3>', '<h3>No Docker socket</h3>', 1),
    ('<p>不挂载 <code>docker.sock</code>，也不管理任何容器，权限边界一目了然。</p>',
     '<p>It never mounts <code>docker.sock</code> and manages no containers, so the permission boundary is easy to see.</p>', 1),
    ('<h3>免费开源</h3>', '<h3>Free and open source</h3>', 1),
    ('<p>以 MIT 协议开源，中英文 README、安装指南和排障文档都在 GitHub 上。</p>',
     '<p>MIT-licensed, with English and Chinese READMEs, an install guide and troubleshooting docs on GitHub.</p>', 1),
    # ---- upstreams ----
    ('<h2>支持的上游仓库</h2>', '<h2>Supported upstreams</h2>', 1),
    ('在域名后面加上对应的路径前缀，代理会据此选择上游，并在转发前去掉前缀。',
     'Add the matching path prefix after your domain. The proxy picks the upstream from it and strips the prefix before forwarding.', 1),
    ('<tr><th>上游</th><th>路径前缀</th><th>拉取示例</th></tr>', '<tr><th>Upstream</th><th>Path prefix</th><th>Pull example</th></tr>', 1),
    ('<td><code>docker.io</code>，另可用 mirrors（无前缀）</td>', '<td><code>docker.io</code>, or mirrors (no prefix)</td>', 1),
    ('<td>AWS 公共 ECR</td>', '<td>AWS Public ECR</td>', 1),
    ('<b>说明：</b>表中的 <code>reg.example.com</code> 只是示例，请换成你自己的域名。上游默认匿名拉取；需要私有镜像或想避开限流时，在 <code>.env</code> 里填对应的用户名和令牌。不需要的上游把 <code>enabled</code> 设为 <code>false</code> 即可关闭。',
     '<b>Note:</b> <code>reg.example.com</code> in the table is only an example; use your own domain. Upstreams are pulled anonymously by default; to pull private images or avoid rate limits, put the matching username and token in <code>.env</code>. Set <code>enabled</code> to <code>false</code> to turn off an upstream you do not need.', 1),
    # ---- how ----
    ('<h2>三步用起来</h2>', '<h2>Three steps</h2>', 1),
    ('<h3>部署代理</h3>', '<h3>Deploy the proxy</h3>', 1),
    ('<p>克隆仓库，填好环境变量，一条 Docker Compose 命令启动。</p>', '<p>Clone the repo, fill in the environment variables and start it with one Docker Compose command.</p>', 1),
    ('<h3>配域名和 HTTPS</h3>', '<h3>Set up the domain and HTTPS</h3>', 1),
    ('<p>域名解析到代理机，用 Caddy 或 Nginx 反代到 <code>127.0.0.1:5000</code>，再把同一个域名写进 <code>config.yaml</code>。</p>',
     '<p>Point the domain at the proxy host, reverse-proxy it to <code>127.0.0.1:5000</code> with Caddy or Nginx, and put the same domain in <code>config.yaml</code>.</p>', 1),
    ('<h3>改客户端配置</h3>', '<h3>Update the clients</h3>', 1),
    ('<p>Docker Hub 在 <code>daemon.json</code> 里加一行 mirror；其他仓库在镜像名前加你的域名。</p>',
     '<p>For Docker Hub, add one mirror line to <code>daemon.json</code>; for other registries, put your domain in front of the image name.</p>', 1),
    # ---- usage ----
    ('<h2>客户端怎么用</h2>', '<h2>Client usage</h2>', 1),
    ('下面的 <code>reg.example.com</code> 都换成你自己的域名。', 'Replace every <code>reg.example.com</code> below with your own domain.', 1),
    ('<h3 style="margin-top:0">Docker Hub：registry-mirrors</h3>', '<h3 style="margin-top:0">Docker Hub: registry-mirrors</h3>', 1),
    ('<p>镜像名完全不用改。把下面的 JSON 写进 <code>/etc/docker/daemon.json</code>：</p>', '<p>Image names stay exactly the same. Put this JSON in <code>/etc/docker/daemon.json</code>:</p>', 1),
    ('<p>如果入口是纯 HTTP，还需要把它加进 <code>insecure-registries</code>。</p>', '<p>If the entry point is plain HTTP, also add it to <code>insecure-registries</code>.</p>', 1),
    ('<h3 style="margin-top:0">其他上游：路径前缀</h3>', '<h3 style="margin-top:0">Other upstreams: path prefix</h3>', 1),
    ('<p>在同一个域名后面加上上游的前缀：</p>', '<p>Add the upstream\'s prefix after the same domain:</p>', 1),
    ('<p>代理按前缀选择上游，并在请求真实仓库前去掉前缀。</p>', '<p>The proxy picks the upstream by prefix and strips it before calling the real registry.</p>', 1),
    ('<b>不要</b>用 <code>/etc/hosts</code> 把 <code>ghcr.io</code> 这类官方域名劫持到代理上，证书对不上会导致 TLS 失败。',
     '<b>Do not</b> hijack official names like <code>ghcr.io</code> to the proxy via <code>/etc/hosts</code>; the certificate will not match and TLS will fail.', 1),
    # ---- deploy ----
    ('<h2>快速部署</h2>', '<h2>Quick deploy</h2>', 1),
    ('需要 64 位 Linux 主机（或本机 Docker Desktop）、Docker 与 Docker Compose v2，以及能访问上游仓库的出站 HTTPS。',
     'You need a 64-bit Linux host (or Docker Desktop locally), Docker with Docker Compose v2, and outbound HTTPS to the upstream registries.', 1),
    ('<h3>获取代码</h3>', '<h3>Get the code</h3>', 1),
    ('<p>克隆仓库并进入目录，后面的命令都在这个目录里执行。</p>', '<p>Clone the repo and enter the directory; run the remaining commands from there.</p>', 1),
    ('<h3>准备环境变量</h3>', '<h3>Prepare the environment variables</h3>', 1),
    ('<p>复制模板，再生成随机的管理令牌和统计页密码写入 <code>.env</code>。统计页账号默认是 <code>admin</code>，密码就是 <code>PROXY_WEB_PASSWORD</code>。</p>',
     '<p>Copy the template, then generate a random admin token and stats password into <code>.env</code>. The stats login defaults to <code>admin</code>, and its password is <code>PROXY_WEB_PASSWORD</code>.</p>', 1),
    ('# 生成随机的管理令牌和统计页密码', '# Generate a random admin token and stats password', 1),
    ('# 写入 .env', '# Write them into .env', 1),
    ('# 清掉当前终端里的明文变量', '# Clear the plaintext variables from this shell', 1),
    ('<h3>填入你的域名</h3>', '<h3>Put in your domain</h3>', 1),
    ('<p>复制业务配置，再把 dockerhub 的 <code>hosts</code> 改成你自己的域名（不要带 <code>https://</code>）。</p>',
     '<p>Copy the config, then change <code>hosts</code> of dockerhub to your own domain (without <code>https://</code>).</p>', 1),
    ('# ← 换成你的真实域名', '# ← replace with your real domain', 1),
    ('<h3>启动</h3>', '<h3>Start it</h3>', 1),
    ('<p>在仓库根目录执行，第一次会先构建镜像。</p>', '<p>Run it from the repo root; the first run builds the image.</p>', 1),
    ('<tr><th>数据面</th><td>默认只在主机 <code>127.0.0.1:5000</code> 监听，通过 TLS 反代对外发布</td></tr>',
     '<tr><th>Data plane</th><td>Listens on host <code>127.0.0.1:5000</code> by default; publish it through a TLS reverse proxy</td></tr>', 1),
    ('<tr><th>管理面</th><td><code>:5001</code>，默认不对公网开放</td></tr>', '<tr><th>Admin plane</th><td><code>:5001</code>, not exposed publicly by default</td></tr>', 1),
    ('<tr><th>HTTPS</th><td>推荐用已有的 Caddy 反代到 <code>127.0.0.1:5000</code></td></tr>',
     '<tr><th>HTTPS</th><td>Prefer your existing Caddy proxying to <code>127.0.0.1:5000</code></td></tr>', 1),
    ('<tr><th>统计页</th><td>把 <code>127.0.0.1:5001</code> 映射出来，打开 <code>/stats/login.html</code></td></tr>',
     '<tr><th>Stats UI</th><td>Map <code>127.0.0.1:5001</code> and open <code>/stats/login.html</code></td></tr>', 1),
    ('<b>域名要自己准备：</b>文档里的 <code>reg.example.com</code> 只是示例。先注册域名，把 A / AAAA（或 CNAME）解析到代理机，再把真实域名写进 Caddy / Nginx 和 <code>config.yaml</code> 的 <code>hosts</code>。解析生效前，客户端会拉取失败。',
     '<b>Bring your own domain:</b> <code>reg.example.com</code> in the docs is only an example. Register a domain, point A / AAAA (or CNAME) at the proxy host, then put the real hostname in Caddy / Nginx and in <code>hosts</code> of <code>config.yaml</code>. Until DNS takes effect, client pulls will fail.', 1),
    ('完整的安装、配置和排障说明见\n      <a href="https://github.com/AlexWuYh/easy-docker-proxy/blob/main/docs/install.md" target="_blank" rel="noopener noreferrer">安装与配置指南</a>、\n      <a href="https://github.com/AlexWuYh/easy-docker-proxy/blob/main/docs/troubleshooting.md" target="_blank" rel="noopener noreferrer">排障文档</a>。',
     'Full install, configuration and troubleshooting notes (currently in Chinese):\n      <a href="https://github.com/AlexWuYh/easy-docker-proxy/blob/main/docs/install.md" target="_blank" rel="noopener noreferrer">install guide</a>,\n      <a href="https://github.com/AlexWuYh/easy-docker-proxy/blob/main/docs/troubleshooting.md" target="_blank" rel="noopener noreferrer">troubleshooting</a>.', 1),
    # ---- screenshots ----
    ('<h2>统计控制台</h2>', '<h2>Stats console</h2>', 1),
    ('谁在拉、拉了什么、哪个上游出错，一个网页看清。截图为演示数据，点击可看大图。',
     'Who pulls what, and which upstream fails — all in one page. Screenshots use demo data; click for full size.', 1),
    ('alt="上游仓库分析"', 'alt="Upstream analytics"', 1),
    ('上游仓库分析：按上游看拉取量与流量', 'Upstream analytics: pulls and traffic per upstream', 1),
    ('alt="镜像列表"', 'alt="Image list"', 1),
    ('镜像列表：哪些镜像被拉得最多', 'Images: which images are pulled the most', 1),
    ('alt="事件记录"', 'alt="Event log"', 1),
    ('事件：逐条查看每次拉取与错误', 'Events: every pull and error, one by one', 1),
    ('alt="登录页"', 'alt="Login page"', 1),
    ('登录：统计页需要账号才能访问', 'Login: the stats page requires an account', 1),
    # ---- cta / footer ----
    ('<h2>几分钟，把镜像拉取加速起来</h2>', '<h2>Speed up image pulls in minutes</h2>', 1),
    ('<p>免费、开源，跑在你自己的服务器上。</p>', '<p>Free, open source, and running on your own server.</p>', 1),
    ('<a class="btn btn-primary" href="#deploy">快速部署</a>', '<a class="btn btn-primary" href="#deploy">Quick deploy</a>', 1),
    ('target="_blank" rel="noopener noreferrer">查看源码</a>\n    </div>\n  </div>\n</section>', 'target="_blank" rel="noopener noreferrer">View source</a>\n    </div>\n  </div>\n</section>', 1),
    ('easy-docker-proxy 是开源项目（MIT） ·', 'easy-docker-proxy is open source (MIT) ·', 1),
    ('>GitHub 仓库</a> ·\n      <a href="https://github.com/AlexWuYh/easy-docker-proxy/releases" target="_blank" rel="noopener noreferrer">发布页面</a>',
     '>GitHub repository</a> ·\n      <a href="https://github.com/AlexWuYh/easy-docker-proxy/releases" target="_blank" rel="noopener noreferrer">Releases</a>', 1),
    ('aria-label="作者 AlexWuYh，打开 GitHub 个人主页" title="GitHub 个人主页"', 'aria-label="Author AlexWuYh — open GitHub profile" title="GitHub profile"', 1),
    ('<span>作者 <b>AlexWuYh</b></span>', '<span>Author <b>AlexWuYh</b></span>', 1),
    ("'切换到亮色主题' : '切换到暗色主题'", "'Switch to light theme' : 'Switch to dark theme'", 1),
]

for zh, en, n in PAIRS:
    found = s.count(zh)
    if found != n:
        sys.exit(f'生成英文页失败：中文页中应有 {n} 处、实际 {found} 处匹配以下文案，请同步更新 scripts/edp_gen_en.py：\n{zh}')
    s = s.replace(zh, en)

Path(dst).parent.mkdir(parents=True, exist_ok=True)
open(dst, 'w', encoding='utf-8').write(s)

# 友情链接依赖 products.json，生成英文页后统一同步一次
subprocess.run([sys.executable, str(ROOT / 'scripts/sync_friend_links.py')], check=True, stdout=subprocess.DEVNULL)
