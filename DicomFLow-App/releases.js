/*
 * 从 GitHub Releases 读取版本信息（源文件：scripts/assets/releases.js，
 * 由 scripts/sync_releases_js.py 复制到各产品目录，不要直接改产品目录里的副本）。
 *
 * 页面用法：
 *   <script src="/releases.js" data-repo="owner/repo" defer></script>
 * 效果：
 *   1. 所有带 data-latest-version 的元素，文本替换为最新版本号（失败时保留原文）；
 *   2. 在页脚/CTA 前插入“更新日志”区块，并在导航栏加入口（#changelog）。
 * 语言取自 <html lang>（en 为英文，其余为中文）。
 */
(function () {
  'use strict';

  var script = document.currentScript;
  var repo = script && script.getAttribute('data-repo');
  if (!repo) return;

  var LIMIT = 10;
  var TTL = 10 * 60 * 1000; // 缓存 10 分钟，避免触发匿名 API 的限流
  var en = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  var T = en ? {
    nav: 'Changelog', label: 'Changelog', title: 'Changelog',
    desc: 'Release notes are loaded live from GitHub Releases.',
    loading: 'Loading…', failed: 'Could not load release notes.', retry: 'Open on GitHub',
    empty: 'No release notes yet.', latest: 'Latest', pre: 'Pre-release',
    noNotes: 'No release notes.', ver: 'Latest', all: 'All releases on GitHub'
  } : {
    nav: '更新日志', label: 'Changelog', title: '更新日志',
    desc: '内容实时取自 GitHub Releases。',
    loading: '加载中…', failed: '更新日志加载失败。', retry: '去 GitHub 查看',
    empty: '暂无发布记录。', latest: '最新', pre: '预发布',
    noNotes: '这个版本没有填写说明。', ver: '最新版', all: '在 GitHub 查看全部版本'
  };

  var releasesUrl = 'https://github.com/' + repo + '/releases';

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function safeUrl(u) { return /^https?:\/\//i.test(u) ? u : '#'; }

  // 行内：先转义，再还原 code / 加粗 / 链接 / 裸链接
  function inline(s) {
    s = esc(s);
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
    s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    s = s.replace(/\[([^\]]+)\]\(([^\s)]+)\)/g, function (_, t, u) {
      // 仓库内相对路径（如 docs/x.md）指向仓库里的文件；其他协议（javascript: 等）一律丢弃
      if (!/^[a-z][a-z0-9+.-]*:/i.test(u) && u.charAt(0) !== '#' && u.charAt(0) !== '/') {
        u = 'https://github.com/' + repo + '/blob/HEAD/' + u.replace(/^\.\//, '');
      }
      return '<a href="' + safeUrl(u) + '" target="_blank" rel="noopener noreferrer">' + t + '</a>';
    });
    s = s.replace(/(^|[\s(])(https?:\/\/[^\s<)]+)/g, function (_, p, u) {
      return p + '<a href="' + safeUrl(u) + '" target="_blank" rel="noopener noreferrer">' + u + '</a>';
    });
    return s;
  }

  function cells(line) {
    line = line.trim().replace(/^\|/, '').replace(/\|$/, '');
    return line.split(/(?<!\\)\|/).map(function (c) { return c.replace(/\\\|/g, '|').trim(); });
  }
  var SEP = /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/;

  // 精简 Markdown：标题、列表、表格、段落（够用于 release notes）
  function md(src) {
    var out = [], list = false, lines = String(src || '').replace(/\r/g, '').split('\n');
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i], m;
      // 围栏代码块：```lang ... ```
      if ((m = /^\s*```\s*([\w+-]*)/.exec(line))) {
        if (list) { out.push('</ul>'); list = false; }
        var lang = m[1].toLowerCase(), buf = [];
        for (i++; i < lines.length && !/^\s*```\s*$/.test(lines[i]); i++) buf.push(lines[i]);
        lang = { sh: 'bash', shell: 'bash', zsh: 'bash', console: 'bash', yml: 'yaml' }[lang] || lang;
        out.push('<div class="cl-code" data-lang="' + esc(lang) + '" data-title="' +
          esc(lang === 'bash' || !lang ? 'Terminal' : lang) + '"><pre>' + esc(buf.join('\n')) + '</pre></div>');
        continue;
      }
      // 表格：表头行含 |，下一行是 --- 分隔行
      if (line.indexOf('|') >= 0 && i + 1 < lines.length && SEP.test(lines[i + 1]) && lines[i + 1].indexOf('-') >= 0) {
        if (list) { out.push('</ul>'); list = false; }
        var head = cells(line), t = '<div class="cl-table"><table><thead><tr>' +
          head.map(function (c) { return '<th>' + inline(c) + '</th>'; }).join('') + '</tr></thead><tbody>';
        i += 2;
        for (; i < lines.length && lines[i].indexOf('|') >= 0 && lines[i].trim(); i++) {
          t += '<tr>' + cells(lines[i]).map(function (c) { return '<td>' + inline(c) + '</td>'; }).join('') + '</tr>';
        }
        i--;
        out.push(t + '</tbody></table></div>');
        continue;
      }
      if ((m = /^\s*[-*+]\s+(.*)$/.exec(line))) {
        if (!list) { out.push('<ul>'); list = true; }
        out.push('<li>' + inline(m[1]) + '</li>');
        continue;
      }
      if (list) { out.push('</ul>'); list = false; }
      if ((m = /^(#{1,6})\s+(.*)$/.exec(line))) out.push('<h4 class="cl-h' + Math.min(m[1].length, 4) + '">' + inline(m[2]) + '</h4>');
      else if (line.trim()) out.push('<p>' + inline(line.trim()) + '</p>');
    }
    if (list) out.push('</ul>');
    return out.join('');
  }

  function fmtDate(iso) {
    var d = new Date(iso);
    if (isNaN(d)) return '';
    return d.toLocaleDateString(en ? 'en-US' : 'zh-CN', { year: 'numeric', month: en ? 'short' : '2-digit', day: '2-digit' });
  }

  // 数据来源（都失败才算失败）：
  //  1. 同域快照 releases.json —— 由定时任务从 GitHub 抓取，国内也能秒开；
  //  2. GitHub API —— 能连上就用它（更新更及时），超时 6 秒放弃。
  // 两个并行请求，谁先到先渲染；API 成功后再用它刷新一次。
  var snapUrl = new URL('releases.json', script.src).href;
  var subs = [], current = null;

  function publish(list) {
    current = list;
    subs.forEach(function (fn) { fn(list); });
  }
  function subscribe(fn) { subs.push(fn); if (current) fn(current); }

  function fromSnapshot() {
    return fetch(snapUrl, { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function (d) { return (d && d.releases) || []; });
  }
  function fromApi() {
    var key = 'releases:' + repo;
    try {
      var c = JSON.parse(sessionStorage.getItem(key) || 'null');
      if (c && Date.now() - c.t < TTL) return Promise.resolve(c.d);
    } catch (e) {}
    var ctl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctl) ctl.abort(); }, 6000);
    return fetch('https://api.github.com/repos/' + repo + '/releases?per_page=' + LIMIT, {
      headers: { Accept: 'application/vnd.github+json' }, signal: ctl && ctl.signal
    }).then(function (r) {
      clearTimeout(timer);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function (list) {
      list = list.filter(function (r) { return !r.draft; });
      try { sessionStorage.setItem(key, JSON.stringify({ t: Date.now(), d: list })); } catch (e) {}
      return list;
    });
  }

  var failures = 0, onAllFailed = function () {};
  function failed() { if (++failures === 2 && !current) onAllFailed(); }
  var started = false;
  function startLoading() {
    if (started) return;
    started = true;
    fromSnapshot().then(function (l) { if (!apiDone) publish(l); }, failed);
    fromApi().then(function (l) { apiDone = true; publish(l); }, failed);
  }
  var apiDone = false;

  // ---- 1. 最新版本号 ----
  var tags = document.querySelectorAll('[data-latest-version]');
  if (tags.length) {
    for (var k = 0; k < tags.length; k++) tags[k].setAttribute('data-label', T.ver);
    subscribe(function (list) {
      var latest = list.filter(function (r) { return !r.prerelease; })[0] || list[0];
      if (!latest) return;
      for (var i = 0; i < tags.length; i++) {
        tags[i].textContent = latest.tag_name;
        tags[i].hidden = false;
      }
    });
    startLoading();
  }

  // ---- 2. 更新日志区块 + 导航入口 ----
  var style = document.createElement('style');
  style.textContent =
    '.ver-badge{display:inline-block;margin-right:6px;padding:2px 11px;border-radius:99px;font-size:.92rem;font-weight:700;letter-spacing:.2px;' +
    'color:var(--accent);background:var(--accent-soft);border:1px solid var(--accent);text-decoration:none;vertical-align:baseline;transition:background .2s,color .2s}' +
    '.ver-badge[data-label]::before{content:attr(data-label);margin-right:8px;padding-right:8px;border-right:1px solid currentColor;font-weight:600;font-size:.82em;opacity:.9}' +
    '.ver-badge:hover{background:var(--accent);color:var(--accent-ink)}' +
    '.ver-badge[hidden]{display:none}' +
    '.cl-list{margin-top:28px;display:grid;gap:14px}' +
    '.cl-item{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius,16px);padding:0}' +
    '.cl-item>summary{list-style:none;cursor:pointer;display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;padding:16px 20px}' +
    '.cl-item>summary::-webkit-details-marker{display:none}' +
    '.cl-item>summary::after{content:"+";margin-left:auto;color:var(--muted);font-size:1.2rem;line-height:1}' +
    '.cl-item[open]>summary::after{content:"\\2212"}' +
    '.cl-tag{font-weight:700;color:var(--text);font-size:1.05rem}' +
    '.cl-name{color:var(--text-soft);font-size:.92rem}' +
    '.cl-date{color:var(--muted);font-size:.85rem}' +
    '.cl-badge{font-size:.72rem;font-weight:600;padding:2px 8px;border-radius:99px;background:var(--accent-soft);color:var(--accent)}' +
    '.cl-body{padding:0 20px 18px;color:var(--text-soft);font-size:.94rem;line-height:1.7;border-top:1px solid var(--border)}' +
    '.cl-body h4{margin:14px 0 4px;color:var(--text);font-size:.95rem;font-weight:650;line-height:1.4}' +
    '.cl-body h4.cl-h1{margin-top:22px;font-size:1.3rem;font-weight:800}' +
    '.cl-body h4.cl-h2{margin-top:22px;padding-bottom:6px;border-bottom:1px solid var(--border);font-size:1.15rem;font-weight:750}' +
    '.cl-body h4.cl-h3{margin-top:18px;font-size:1.02rem;font-weight:700}' +
    '.cl-body p{margin:8px 0}.cl-body ul{margin:8px 0;padding-left:1.3em}.cl-body li{margin:3px 0}' +
    '.cl-code:not(.code){margin:12px 0;border-radius:10px;overflow:hidden;background:#0e1621;border:1px solid #22344a}' +
    '.cl-code:not(.code) pre{margin:0;padding:14px 16px;overflow-x:auto;color:#d6e2f0;font:.82rem/1.7 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}' +
    '.cl-table{overflow-x:auto;margin:10px 0}' +
    '.cl-table table{border-collapse:collapse;font-size:.9rem;min-width:50%}' +
    '.cl-table th,.cl-table td{border:1px solid var(--border);padding:6px 12px;text-align:left;vertical-align:top}' +
    '.cl-table th{background:var(--surface-2);color:var(--text);font-weight:600}' +
    '.cl-body code{background:var(--surface-2);padding:1px 5px;border-radius:5px;font-size:.88em}' +
    '.cl-body a,.cl-more a{color:var(--accent);text-decoration:underline;text-underline-offset:2px}' +
    '.cl-body>:first-child{margin-top:14px!important}' +
    '.cl-status,.cl-more{margin-top:18px;color:var(--muted);font-size:.92rem}';
  document.head.appendChild(style);

  var sec = document.createElement('section');
  sec.className = 'section';
  sec.id = 'changelog';
  sec.innerHTML =
    '<div class="container">' +
      '<div class="section-head">' +
        '<span class="section-label">' + T.label + '</span>' +
        '<h2>' + T.title + '</h2>' +
        '<p class="section-desc">' + T.desc + '</p>' +
      '</div>' +
      '<div class="cl-list" id="clList"><p class="cl-status">' + T.loading + '</p></div>' +
    '</div>';
  var anchor = document.querySelector('section.cta') || document.querySelector('footer');
  if (!anchor) return;
  anchor.parentNode.insertBefore(sec, anchor);

  var lang = document.querySelector('.nav-actions .lang-link');
  if (lang) {
    var a = document.createElement('a');
    a.className = 'nav-link';
    a.href = '#changelog';
    a.textContent = T.nav;
    lang.parentNode.insertBefore(a, lang);
  }

  var box = document.getElementById('clList');
  onAllFailed = function () {
    box.innerHTML = '<p class="cl-status">' + T.failed + ' <a href="' + releasesUrl +
      '" target="_blank" rel="noopener noreferrer" style="color:var(--accent)">' + T.retry + '</a></p>';
  };
  function render(list) {
    if (!list.length) { box.innerHTML = '<p class="cl-status">' + T.empty + '</p>'; return; }
    var firstStable = -1;
    list.forEach(function (r, i) { if (firstStable < 0 && !r.prerelease) firstStable = i; });
    var opened = {};
    [].forEach.call(box.querySelectorAll('details'), function (d) { opened[d.getAttribute('data-tag')] = d.open; });
    box.innerHTML = list.map(function (r, i) {
      var name = r.name && r.name !== r.tag_name ? '<span class="cl-name">' + esc(r.name) + '</span>' : '';
      var badge = r.prerelease ? '<span class="cl-badge">' + T.pre + '</span>'
        : (i === firstStable ? '<span class="cl-badge">' + T.latest + '</span>' : '');
      var open = r.tag_name in opened ? opened[r.tag_name] : false;
      return '<details class="cl-item" data-tag="' + esc(r.tag_name) + '"' + (open ? ' open' : '') + '>' +
        '<summary><span class="cl-tag">' + esc(r.tag_name) + '</span>' + badge + name +
        '<span class="cl-date">' + fmtDate(r.published_at || r.created_at) + '</span></summary>' +
        '<div class="cl-body">' + (md(r.body) || '<p>' + T.noNotes + '</p>') + '</div></details>';
    }).join('') +
      '<p class="cl-more"><a href="' + releasesUrl + '" target="_blank" rel="noopener noreferrer">' + T.all + ' →</a></p>';
    // 页面如果提供了代码块增强函数（Mac 窗口 + 语法高亮），就交给它
    if (window.edpEnhanceCode) window.edpEnhanceCode(box);
  }
  subscribe(render);
  // 区块滚动到视口附近才请求（若上面的版本号已触发则不重复）
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { io.disconnect(); startLoading(); }
    }, { rootMargin: '600px 0px' });
    io.observe(sec);
  } else {
    startLoading();
  }
})();
