#!/usr/bin/env python3
"""根据 jenkins-build-archive/index.html（中文页）生成 jenkins-build-archive/en/index.html（英文页）。

英文页是生成产物，请不要手动编辑；改中文页后运行本脚本（或直接提交，
pre-commit 钩子会自动运行）。若中文页里被替换的文案改了，下面的 PAIRS
会报错并指出没匹配上的文案，此时同步更新对应的中文原文与英文译文即可。

用法: python3 scripts/jba_gen_en.py [源文件] [输出文件]
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / 'jenkins-build-archive/index.html')
dst = sys.argv[2] if len(sys.argv) > 2 else str(ROOT / 'jenkins-build-archive/en/index.html')

s = open(src, encoding='utf-8').read()

# (中文原文, 英文译文, 期望出现次数)
PAIRS = [
    # ---- head ----
    ('<html lang="zh-CN"', '<html lang="en"', 1),
    ('<title>Jenkins Build Archive — Jenkins 构建历史归档 · Git / Commit / 镜像 Digest 长期追溯 · 开源免费</title>',
     '<title>Jenkins Build Archive — Jenkins Build History Archive · Long-Term Git / Commit / Image Digest Traceability · Free and Open Source</title>', 1),
    ('content="Jenkins Build Archive 是独立于 Jenkins 的构建元数据归档服务：流水线结束时记录 Git 分支、Commit、Docker 镜像 Tag 与 Digest，Jenkins 清理构建记录后依然可追溯。FastAPI + SQLite，Docker Compose 一键部署，开源免费。"',
     'content="Jenkins Build Archive is a build metadata archive that runs independently of Jenkins: when a pipeline ends it records the Git branch, commit, Docker image tag and digest, so builds stay traceable after Jenkins cleans up its build records. FastAPI + SQLite, deployed with Docker Compose. Free and open source."', 1),
    ('content="Jenkins 构建归档, Jenkins 构建历史, 构建追溯, Docker 镜像 Digest, Jenkins Shared Library, 构建记录保留, Jenkins Build Archive"',
     'content="Jenkins build archive, Jenkins build history, build traceability, Docker image digest, Jenkins Shared Library, build record retention, Jenkins Build Archive"', 1),
    ('<link rel="canonical" href="https://jba.wuewa.cn/">', '<link rel="canonical" href="https://jba.wuewa.cn/en/">', 1),
    ('<meta property="og:locale" content="zh_CN">\n<meta property="og:locale:alternate" content="en_US">',
     '<meta property="og:locale" content="en_US">\n<meta property="og:locale:alternate" content="zh_CN">', 1),
    ('<meta property="og:url" content="https://jba.wuewa.cn/">', '<meta property="og:url" content="https://jba.wuewa.cn/en/">', 1),
    ('content="Jenkins Build Archive — 构建记录被清理，追溯信息还在"', 'content="Jenkins Build Archive — Build records get cleaned up, traceability stays"', 2),
    ('content="独立于 Jenkins 的构建元数据归档服务：Git 分支、Commit、镜像 Tag 与 Digest 长期可查。开源免费。"',
     'content="A build metadata archive independent of Jenkins: Git branch, commit, image tag and digest stay searchable for the long term. Free and open source."', 1),
    ('content="独立于 Jenkins 的构建元数据归档服务，Git / Commit / 镜像 Digest 长期可查。开源免费。"',
     'content="A build metadata archive independent of Jenkins, keeping Git / commit / image digest searchable. Free and open source."', 1),
    ('"description": "独立于 Jenkins 的构建元数据归档服务，记录 Git 分支、Commit、Docker 镜像 Tag 与 Digest，构建记录被清理后依然可追溯。",',
     '"description": "A build metadata archive independent of Jenkins. It records the Git branch, commit, Docker image tag and digest, so builds stay traceable after build records are cleaned up.",', 1),
    ('"url": "https://jba.wuewa.cn/",', '"url": "https://jba.wuewa.cn/en/",', 1),
    ('"priceCurrency": "CNY"', '"priceCurrency": "USD"', 1),
    # ---- nav ----
    ('alt="Jenkins Build Archive 应用图标"', 'alt="Jenkins Build Archive app icon"', 2),
    ('<a class="nav-link" href="#features">功能</a>', '<a class="nav-link" href="#features">Features</a>', 1),
    ('<a class="nav-link" href="#integrate">接入</a>', '<a class="nav-link" href="#integrate">Integrate</a>', 1),
    ('<a class="nav-link" href="#deploy">部署</a>', '<a class="nav-link" href="#deploy">Deploy</a>', 1),
    ('<a class="lang-link" href="/en/" hreflang="en" lang="en" title="English">EN</a>',
     '<a class="lang-link" href="/" hreflang="zh-CN" lang="zh-CN" title="简体中文">中文</a>', 1),
    ('aria-label="打开 Jenkins Build Archive GitHub 仓库" title="GitHub 仓库"', 'aria-label="Open Jenkins Build Archive on GitHub" title="GitHub repository"', 1),
    ('aria-label="切换明暗主题"', 'aria-label="Toggle light/dark theme"', 1),
    # ---- hero ----
    ('<b>开源</b> · 独立于 Jenkins · 自托管 · Docker 部署', '<b>Open source</b> · Independent of Jenkins · Self-hosted · Docker deploy', 1),
    ('Jenkins 清理了构建记录，<strong>追溯信息</strong>还在。', 'Jenkins cleaned up the builds. The <strong>traceability</strong> is still here.', 1),
    ('''      独立于 Jenkins 的构建元数据归档服务：流水线结束时把 Git 分支、Commit、Docker 镜像 Tag 与 Digest 存下来，
      旧的 Build Record 被清理后，依然能查到“这个镜像是哪次提交构建的”。''',
     '''      A build metadata archive that runs independently of Jenkins: when a pipeline ends it stores the Git branch, commit, Docker image tag and digest,
      so after old Build Records are cleaned up you can still answer "which commit built this image?".''', 1),
    ('        快速部署\n      </a>', '        Quick deploy\n      </a>', 1),
    ('target="_blank" rel="noopener noreferrer">查看源码</a>\n    </div>\n    <p class="hero-note">', 'target="_blank" rel="noopener noreferrer">View source</a>\n    </div>\n    <p class="hero-note">', 1),
    ('</a> MIT 开源 · 面向内网 · SQLite 单文件存储</p>', '</a> MIT licensed · Built for internal networks · Single-file SQLite storage</p>', 1),
    ('alt="Jenkins Build Archive 构建列表：统计卡片、搜索筛选和构建记录表"', 'alt="Jenkins Build Archive build list: stat cards, search filters and the build record table"', 1),
    ('构建列表（演示数据）：按 Job、分支、Commit、镜像 Tag 搜索，默认只看当天。',
     'Build list (demo data): search by job, branch, commit or image tag; today only by default.', 1),
    # ---- about ----
    ('<h2>一个只管“留底”的归档服务</h2>', '<h2>An archive that only keeps the record</h2>', 1),
    ('Jenkins 为了省空间会清理旧构建，而排查线上问题时，恰恰需要知道某个镜像来自哪次提交。它把这些信息存到一个独立的小服务里。',
     'Jenkins cleans up old builds to save space, but when you debug a production issue you need to know which commit an image came from. This keeps that information in a small separate service.', 1),
    ('<tr><th>定位</th><td>独立于 Jenkins 的构建元数据归档，构建记录被清理后仍可追溯</td></tr>',
     '<tr><th>What</th><td>A build metadata archive independent of Jenkins; builds stay traceable after their records are cleaned up</td></tr>', 1),
    ('<tr><th>记录什么</th><td>Job、构建号、Git 仓库 / 分支 / Commit、Commit 作者与改动文件、Docker 镜像 Tag 与 Digest、构建结果和耗时</td></tr>',
     '<tr><th>Records</th><td>Job, build number, Git repository / branch / commit, commit author and changed files, Docker image tag and digest, build result and duration</td></tr>', 1),
    ('<tr><th>怎么写入</th><td>流水线结束时由 Shared Library 的 <code>buildArchive()</code> 或一条 <code>curl</code> POST 过来，<code>(jobName, buildId)</code> 幂等</td></tr>',
     '<tr><th>Ingest</th><td>The pipeline posts at the end through the Shared Library\'s <code>buildArchive()</code> or a single <code>curl</code>; <code>(jobName, buildId)</code> is idempotent</td></tr>', 1),
    ('<tr><th>怎么查</th><td>内置 Web 页面和 REST API，支持 Job / 分支 / Commit / Tag 搜索与日期筛选</td></tr>',
     '<tr><th>Query</th><td>Built-in web UI and REST API, with search by job / branch / commit / tag and date filters</td></tr>', 1),
    ('<tr><th>技术</th><td>Python + FastAPI + SQLite，Docker Compose 部署，MIT 开源</td></tr>',
     '<tr><th>Stack</th><td>Python + FastAPI + SQLite, deployed with Docker Compose, MIT licensed</td></tr>', 1),
    # ---- features ----
    ('<h2>小而够用，不碍事</h2>', '<h2>Small, sufficient, out of the way</h2>', 1),
    ('<h3>构建记录长期留存</h3>', '<h3>Build records that last</h3>', 1),
    ('<p>Jenkins 的 Build Record 被清理后，归档里的分支、Commit 和镜像信息依然在。</p>',
     '<p>After Jenkins removes a Build Record, the branch, commit and image information is still in the archive.</p>', 1),
    ('<h3>Git 与 Commit 详情</h3>', '<h3>Git and commit details</h3>', 1),
    ('<p>记录分支、Commit SHA、提交信息、作者和改动文件，详情页一眼看全。</p>',
     '<p>Branch, commit SHA, message, author and changed files are all recorded and shown on one detail page.</p>', 1),
    ('<h3>镜像 Tag 与 Digest</h3>', '<h3>Image tag and digest</h3>', 1),
    ('<p>Tag 可能被覆盖，Digest 不会。同时记录两者，长期追溯才靠得住。</p>',
     '<p>A tag can be overwritten, a digest cannot. Recording both is what makes long-term tracing reliable.</p>', 1),
    ('<h3>搜索与筛选</h3>', '<h3>Search and filters</h3>', 1),
    ('<p>按 Job、分支、Commit、镜像 Tag、结果和日期筛选。列表默认显示当天，「全部历史」一键切换。</p>',
     '<p>Filter by job, branch, commit, image tag, result and date. The list shows today by default, and "All history" is one click away.</p>', 1),
    ('<h3>Shared Library 一行接入</h3>', '<h3>One line with the Shared Library</h3>', 1),
    ('<p>在 <code>post { always { } }</code> 里调用 <code>buildArchive()</code>；不想用 Shared Library，直接 <code>curl</code> 也行。</p>',
     '<p>Call <code>buildArchive()</code> in <code>post { always { } }</code>. If you would rather skip the Shared Library, a plain <code>curl</code> works too.</p>', 1),
    ('<h3>归档失败不影响构建</h3>', '<h3>Archive failures never fail the build</h3>', 1),
    ('<p>归档调用出错只打印警告，不会让流水线变红；成功或失败的构建都会入库。</p>',
     '<p>An error in the archive call only prints a warning and never turns the pipeline red; both successful and failed builds are stored.</p>', 1),
    ('<h3>保留策略与批量删除</h3>', '<h3>Retention policy and bulk delete</h3>', 1),
    ('<p>可设置最长保留天数、每个 Job 最多保留条数；删除需要管理密码并输入确认词。</p>',
     '<p>Set a maximum age and a per-job record cap. Deleting needs the admin password and a typed confirmation word.</p>', 1),
    ('<h3>写入与管理需鉴权</h3>', '<h3>Auth for writes and admin</h3>', 1),
    ('<p>写接口用 <code>API_TOKEN</code>，Web 管理用 <code>ADMIN_PASSWORD</code>；两者没配置时一律拒绝。</p>',
     '<p>Write APIs use <code>API_TOKEN</code> and web admin uses <code>ADMIN_PASSWORD</code>; if either is not configured, those operations are refused.</p>', 1),
    ('<h3>单容器，免运维</h3>', '<h3>One container, little upkeep</h3>', 1),
    ('<p>一个容器加一个 SQLite 文件，Docker Compose 启动；表结构自动初始化，升级只要重新构建。</p>',
     '<p>One container and one SQLite file, started with Docker Compose. The schema initializes itself, and upgrading is just a rebuild.</p>', 1),
    # ---- how ----
    ('<h2>三步用起来</h2>', '<h2>Three steps</h2>', 1),
    ('<h3>部署归档服务</h3>', '<h3>Deploy the archive</h3>', 1),
    ('<p>在内网服务器上用 Docker Compose 启动，配置 <code>API_TOKEN</code> 和管理密码。</p>',
     '<p>Start it with Docker Compose on an internal server and set <code>API_TOKEN</code> and the admin password.</p>', 1),
    ('<h3>配置 Jenkins</h3>', '<h3>Configure Jenkins</h3>', 1),
    ('<p>设置 <code>BUILD_ARCHIVE_URL</code> 和 Token，并把本仓库登记为名为 <code>build-archive</code> 的 Shared Library。</p>',
     '<p>Set <code>BUILD_ARCHIVE_URL</code> and the token, and register this repo as a Shared Library named <code>build-archive</code>.</p>', 1),
    ('<h3>流水线里调用</h3>', '<h3>Call it in the pipeline</h3>', 1),
    ('<p>在 <code>post { always { buildArchive() } }</code> 中调用一次，之后每次构建都会自动入库。</p>',
     '<p>Call <code>buildArchive()</code> once in <code>post { always { } }</code>, and every build is stored automatically from then on.</p>', 1),
    # ---- integrate ----
    ('<h2>接入 Jenkins</h2>', '<h2>Integrate with Jenkins</h2>', 1),
    ('推荐用 Shared Library；也可以不装库，直接在 Jenkinsfile 里 <code>curl</code>。',
     'The Shared Library is recommended; you can also skip it and <code>curl</code> straight from the Jenkinsfile.', 1),
    ('<h3 style="margin-top:0">Shared Library（推荐）</h3>', '<h3 style="margin-top:0">Shared Library (recommended)</h3>', 1),
    ('<p>先在 Manage Jenkins 里配置全局环境变量 <code>BUILD_ARCHIVE_URL</code>、<code>BUILD_ARCHIVE_TOKEN</code>，并把本仓库登记为名为 <code>build-archive</code> 的 Global Pipeline Library。然后：</p>',
     '<p>First, under Manage Jenkins, set the global environment variables <code>BUILD_ARCHIVE_URL</code> and <code>BUILD_ARCHIVE_TOKEN</code>, and register this repo as a Global Pipeline Library named <code>build-archive</code>. Then:</p>', 1),
    ('// 必须 always，失败的构建也会入库', '// must be always, so failed builds are stored too', 1),
    ('<p>Agent 需要装有 <code>curl</code>。</p>', '<p>The agent needs <code>curl</code> installed.</p>', 1),
    ('<h3 style="margin-top:0">附带镜像 Tag 与 Digest</h3>', '<h3 style="margin-top:0">Include the image tag and digest</h3>', 1),
    ('<p>在调用 <code>buildArchive()</code> 前，把镜像信息放进环境变量即可：</p>',
     '<p>Before calling <code>buildArchive()</code>, put the image information in environment variables:</p>', 1),
    ('<p>服务不会主动去查 Registry，Digest 由流水线传入。</p>',
     '<p>The service never queries the registry itself; the digest is passed in by the pipeline.</p>', 1),
    ('<h3 style="margin-top:0">不用 Shared Library：直接 POST</h3>', '<h3 style="margin-top:0">Without the Shared Library: plain POST</h3>', 1),
    ('<p>写入接口是 <code>POST /api/v1/builds</code>，用 Bearer Token 鉴权，<code>(jobName, buildId)</code> 相同则更新。先手工验证一次：</p>',
     '<p>The ingest endpoint is <code>POST /api/v1/builds</code>, authenticated with a Bearer token; the same <code>(jobName, buildId)</code> updates the existing record. Try it by hand first:</p>', 1),
    ('alt="构建详情页：构建信息、Git 信息、Commit 详情和 Docker 镜像"', 'alt="Build detail page: build info, Git info, commit details and Docker image"', 1),
    ('构建详情（演示数据）：Git、Commit、镜像 Tag 与 Digest 一页看全',
     'Build detail (demo data): Git, commit, image tag and digest on one page', 1),
    ('<tr><th>归档字段</th><th>Jenkins 来源</th></tr>', '<tr><th>Archive field</th><th>Jenkins source</th></tr>', 1),
    ('<td>同名环境变量，或 <code>buildArchive(...)</code> 参数</td>', '<td>Same-named environment variables, or <code>buildArchive(...)</code> arguments</td>', 1),
    # ---- api ----
    ('<h2>REST API</h2>', '<h2>REST API</h2>', 1),
    ('读接口默认开放，写入与管理接口必须带 Bearer Token。', 'Read endpoints are open by default; write and admin endpoints require a Bearer token.', 1),
    ('<tr><th>方法</th><th>路径</th><th>鉴权</th><th>说明</th></tr>', '<tr><th>Method</th><th>Path</th><th>Auth</th><th>Description</th></tr>', 1),
    ('<td>无</td><td>健康检查</td>', '<td>None</td><td>Health check</td>', 1),
    ('<td>无</td><td>统计</td>', '<td>None</td><td>Statistics</td>', 1),
    ('<td>无</td><td>列表，支持 <code>', '<td>None</td><td>List, supports <code>', 1),
    ('<td>无</td><td>详情（含 Commit 信息）</td>', '<td>None</td><td>Detail (including commit info)</td>', 1),
    ('<td>创建或更新（幂等）</td>', '<td>Create or update (idempotent)</td>', 1),
    ('<td>Bearer</td><td>删除</td>', '<td>Bearer</td><td>Delete</td>', 1),
    ('<td>查看保留策略</td>', '<td>View the retention policy</td>', 1),
    ('<td>立即执行清理</td>', '<td>Run the cleanup now</td>', 1),
    ('<b>说明：</b>API 列表默认不过滤日期；Web 列表默认只显示当天，访问 <code>/?all=1</code> 查看全部历史。',
     '<b>Note:</b> the API list applies no date filter by default; the web list shows only today, and <code>/?all=1</code> shows the full history.', 1),
    # ---- deploy ----
    ('<h2>快速部署</h2>', '<h2>Quick deploy</h2>', 1),
    ('需要一台内网服务器，装有 Docker 与 Docker Compose。数据只有一个 SQLite 文件。',
     'You need an internal server with Docker and Docker Compose. All data lives in a single SQLite file.', 1),
    ('<h3>获取代码</h3>', '<h3>Get the code</h3>', 1),
    ('<p>克隆仓库并进入目录，复制环境变量模板。</p>', '<p>Clone the repo, enter the directory and copy the environment template.</p>', 1),
    ('<h3>编辑配置</h3>', '<h3>Edit the config</h3>', 1),
    ('<p>把 <code>API_TOKEN</code> 和 <code>ADMIN_PASSWORD</code> 换成你自己的值，不要使用示例里的占位符。</p>',
     '<p>Replace <code>API_TOKEN</code> and <code>ADMIN_PASSWORD</code> with your own values; do not keep the placeholders from the example.</p>', 1),
    ('API_TOKEN=请替换成足够长的随机字符串', 'API_TOKEN=replace-with-a-long-random-string', 1),
    ('ADMIN_PASSWORD=请设置管理密码', 'ADMIN_PASSWORD=set-an-admin-password', 1),
    ('<h3>启动并检查</h3>', '<h3>Start and check</h3>', 1),
    ('<p>启动后访问健康检查接口，再用浏览器打开 <code>http://服务器IP:8080</code>。</p>',
     '<p>Once started, call the health endpoint, then open <code>http://SERVER_IP:8080</code> in a browser.</p>', 1),
    ('<h3>备份与升级</h3>', '<h3>Backup and upgrade</h3>', 1),
    ('<p>数据在 <code>./data/build_archive.db</code>。在线备份用 SQLite 的 backup 接口；升级则拉取新代码后重新构建，表结构会自动初始化。</p>',
     '<p>Data lives in <code>./data/build_archive.db</code>. Use SQLite\'s backup API for online backups; to upgrade, pull the new code and rebuild, and the schema initializes itself.</p>', 1),
    ('<tr><th>变量</th><th>含义</th></tr>', '<tr><th>Variable</th><th>Meaning</th></tr>', 1),
    ('<td>写接口的 Bearer Token，Jenkins 侧的 <code>BUILD_ARCHIVE_TOKEN</code> 要与它一致</td>',
     '<td>Bearer token for the write API; <code>BUILD_ARCHIVE_TOKEN</code> on the Jenkins side must match it</td>', 1),
    ('<td>Web 管理（删除、保留策略）的密码</td>', '<td>Password for web admin (delete, retention policy)</td>', 1),
    ('<td>时区，决定列表“当天”的范围</td>', '<td>Time zone; decides what "today" means in the list</td>', 1),
    ('<td>最长保留天数，<code>0</code> 表示关闭；在 UI 保存后以数据库中的值为准</td>',
     '<td>Maximum retention in days, <code>0</code> turns it off; once saved in the UI, the value in the database wins</td>', 1),
    ('<td>每个 Job 最多保留条数，<code>0</code> 表示关闭</td>', '<td>Maximum records kept per job, <code>0</code> turns it off</td>', 1),
    ('<b>仅限内网使用：</b>读接口默认不需要登录，请不要把服务映射到公网，或在反向代理处限制来源。清理策略不可恢复，收紧之前先备份数据库。',
     '<b>Internal networks only:</b> read endpoints need no login by default, so do not expose the service to the public internet, or restrict sources at the reverse proxy. Cleanup cannot be undone; back up the database before tightening the policy.', 1),
    ('完整说明见\n      <a href="https://github.com/AlexWuYh/jenkins-build-archive#readme" target="_blank" rel="noopener noreferrer">GitHub README</a>、\n      <a href="https://github.com/AlexWuYh/jenkins-build-archive/blob/main/jenkins-shared-library/README.md" target="_blank" rel="noopener noreferrer">Shared Library 文档</a>。',
     'Full documentation (currently in Chinese):\n      <a href="https://github.com/AlexWuYh/jenkins-build-archive#readme" target="_blank" rel="noopener noreferrer">GitHub README</a>,\n      <a href="https://github.com/AlexWuYh/jenkins-build-archive/blob/main/jenkins-shared-library/README.md" target="_blank" rel="noopener noreferrer">Shared Library docs</a>.', 1),
    # ---- cta / footer ----
    ('<h2>让每一次构建都有迹可循</h2>', '<h2>Make every build traceable</h2>', 1),
    ('<p>免费、开源，跑在你自己的内网里。</p>', '<p>Free, open source, and running inside your own network.</p>', 1),
    ('<a class="btn btn-primary" href="#deploy">快速部署</a>', '<a class="btn btn-primary" href="#deploy">Quick deploy</a>', 1),
    ('target="_blank" rel="noopener noreferrer">查看源码</a>\n    </div>\n  </div>\n</section>', 'target="_blank" rel="noopener noreferrer">View source</a>\n    </div>\n  </div>\n</section>', 1),
    ('Jenkins Build Archive 是开源项目（MIT） ·', 'Jenkins Build Archive is open source (MIT) ·', 1),
    ('>GitHub 仓库</a> ·\n      <a href="https://github.com/AlexWuYh/jenkins-build-archive/releases" target="_blank" rel="noopener noreferrer">发布页面</a>',
     '>GitHub repository</a> ·\n      <a href="https://github.com/AlexWuYh/jenkins-build-archive/releases" target="_blank" rel="noopener noreferrer">Releases</a>', 1),
    ('<p>本站与 Jenkins 项目及 CDF 无关联，Jenkins 为其各自所有者的商标。</p>',
     '<p>This site is not affiliated with the Jenkins project or the CDF. Jenkins is a trademark of its respective owners.</p>', 1),
    ('aria-label="作者 AlexWuYh，打开 GitHub 个人主页" title="GitHub 个人主页"', 'aria-label="Author AlexWuYh — open GitHub profile" title="GitHub profile"', 1),
    ('<span>作者 <b>AlexWuYh</b></span>', '<span>Author <b>AlexWuYh</b></span>', 1),
    ("'切换到亮色主题' : '切换到暗色主题'", "'Switch to light theme' : 'Switch to dark theme'", 1),
]

for zh, en, n in PAIRS:
    found = s.count(zh)
    if found != n:
        sys.exit(f'生成英文页失败：中文页中应有 {n} 处、实际 {found} 处匹配以下文案，请同步更新 scripts/jba_gen_en.py：\n{zh}')
    s = s.replace(zh, en)

Path(dst).parent.mkdir(parents=True, exist_ok=True)
open(dst, 'w', encoding='utf-8').write(s)

# 友情链接依赖 products.json，生成英文页后统一同步一次
subprocess.run([sys.executable, str(ROOT / 'scripts/sync_friend_links.py')], check=True, stdout=subprocess.DEVNULL)
