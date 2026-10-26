# my-static-sites

集中管理所有产品的静态页面（官网、落地页、介绍页等）。

## 目录约定

根目录下的**每个目录对应一个产品**，目录内存放该产品的静态网页：

```
my-static-sites/
├── <产品名>/
│   ├── index.html      # 产品官网入口
│   └── ...             # 该产品的其他页面与静态资源
└── README.md
```

## 当前产品

| 目录 | 产品 | 说明 |
| --- | --- | --- |
| [`ScreenClock/`](./ScreenClock) | ScreenClock | 开源 Android 全屏床头 / 桌面时钟官网，支持多主题钟面、番茄钟、纪念日倒计时与天气 |
| [`DicomFLow-App/`](./DicomFLow-App) | DicomFlow | 网页版 + App 的统一官网（医院 CT / MRI 片子转 MP4 / GIF），中英文双语 |
| [`Jot/`](./Jot) | Jot（简迹） | 本地优先的碎片笔记 + AI 周期总结，支持 Windows / macOS / Android，中英文双语 |
| [`easy-docker-proxy/`](./easy-docker-proxy) | easy-docker-proxy（EDP） | 多上游 Docker Registry 加速代理（零镜像缓存、内置拉取统计），中英文双语，域名 `edp.wuewa.cn` |

## 新增产品

1. 在根目录新建以产品名命名的目录。
2. 在目录中放入静态页面，入口文件命名为 `index.html`。
3. 在上方「当前产品」表格中补充一行。
4. 在根目录的 `products.json` 里加一项（名称、网址、中英文简介）。
5. 在新产品页面的页脚放好友情链接标记（见下节），并复制 `.friends` 相关样式。
6. 在 `products.json` 的新条目里填 `repo`（`owner/repo`），页面 `</body>` 前加 `<script src="/releases.js" data-repo="owner/repo" defer></script>`，运行 `python3 scripts/sync_releases_js.py` 和 `python3 scripts/sync_releases_data.py`（见下文「版本号与更新日志」）。
7. 提交并推送。已有产品页面底部的友情链接会自动补上新产品。
8. 在 Cloudflare 新建对应的 Pages 项目，根目录指向该产品目录。

## 中英文页面（自动同步）

- 中文页是源文件，英文页（`en/index.html`）由脚本生成，**不要手动编辑英文页**。

  | 产品 | 中文页 | 生成脚本 |
  | --- | --- | --- |
  | ScreenClock | `ScreenClock/index.html` | `scripts/screenclock_gen_en.py` |
  | DicomFlow | `DicomFLow-App/index.html` | `scripts/dicomflow_gen_en.py` |
  | Jot | `Jot/index.html` | `scripts/jot_gen_en.py` |
  | easy-docker-proxy | `easy-docker-proxy/index.html` | `scripts/edp_gen_en.py` |

- 手动运行：`python3 scripts/<脚本名>.py`。
- 自动同步：仓库自带 `pre-commit` 钩子（`.githooks/`），提交中包含上表中的中文页时，会自动重新生成并一并提交对应的英文页。克隆仓库后需启用一次：

  ```bash
  git config core.hooksPath .githooks
  ```

- 若改动了中文页里脚本替换过的文案，脚本会报错并指出哪段文案没匹配上，此时同步更新脚本中的原文与译文即可。

## 友情链接（产品互链）

各产品页面底部都有“友情链接”，互相链接到其他产品的官网。数据来源是根目录的 `products.json`，**不要手动改页面里的友链**。

- 页面页脚里需要有这一对标记，脚本只会改动两者之间的内容：

  ```html
  <!-- friends:start -->
  <!-- friends:end -->
  ```

- 同步脚本：`python3 scripts/sync_friend_links.py`。它会给每个产品的中文页和英文页写入“除自己外的其他产品”链接。
- 自动同步：`pre-commit` 钩子在提交包含 `products.json` 或中文页时会自动运行，并把改动一并提交。
- 新增产品：在 `products.json` 里加一项，并给新产品页面放好上面的标记；提交后，所有已有产品页面底部会自动出现新产品的链接。

## 版本号与更新日志（取自 GitHub Releases）

页面上的最新版本号和「更新日志」区块都由 `releases.js` 在浏览器里实时请求 GitHub Releases API 得到，**发版后不需要改网站代码**。

- 源文件是 `scripts/assets/releases.js`，`python3 scripts/sync_releases_js.py` 会把它复制到各产品目录（`pre-commit` 钩子也会自动做）。**不要直接改产品目录里的副本**。
- 页面里引入一行：`<script src="/releases.js" data-repo="owner/repo" defer></script>`，脚本会自动加上导航入口和 `#changelog` 区块。
- 想显示最新版本号的地方写 `<span data-latest-version>v0.0.0</span>`，里面的文字是请求失败时的兜底。
- 结果缓存在 sessionStorage 10 分钟，避免触发 GitHub 匿名 API 的限流（每 IP 每小时 60 次）。
- 访问者连不上 GitHub 时的兜底：`.github/workflows/sync-releases.yml` 每 2 小时运行 `scripts/sync_releases_data.py`，把各仓库的 release 抓成 `<产品目录>/releases.json` 并提交（有变化才提交）。页面同时读这份同域快照和 GitHub API，快照先到先显示，API 成功后再刷新；API 超过 6 秒无响应就放弃。
- 站点托管在 Cloudflare Pages，快照提交到 `main` 后会自动触发重新部署。发版后想立刻更新，可在 GitHub 的 Actions 页手动运行 `sync-releases`。
- 新产品要在 `products.json` 里填 `repo`（`owner/repo`），快照和页面共用它。
- Actions 会直接往 `main` 提交快照，本地推送被拒绝时先 `git pull --rebase` 再推。

## 本地预览

页面均为纯静态文件，可直接用浏览器打开 `index.html`，或在对应目录启动一个静态服务器：

```bash
cd ScreenClock
python3 -m http.server 8000
# 访问 http://localhost:8000
```

## 约定

- 每个产品目录自包含，不依赖其他产品目录中的文件。
- 静态资源（图片、样式、脚本）放在各自产品目录内。
