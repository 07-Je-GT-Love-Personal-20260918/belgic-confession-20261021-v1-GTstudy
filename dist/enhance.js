/* GTstudy v2: progressive maps, navigation and text-only persistent annotations. */
(() => {
  'use strict';
  const $ = s => document.querySelector(s);
  const $$ = s => Array.from(document.querySelectorAll(s));
  const reduce = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  let toastTimer;
  function toast(message) {
    const box = $('#studyToast'); if (!box) return;
    box.textContent = message; box.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(() => { box.hidden = true; }, 3400);
  }
  const scrollTo = top => window.scrollTo({ top, behavior: reduce() ? 'instant' : 'smooth' });
  $('#quickToggle')?.addEventListener('click', () => {
    const open = $('#quickItems').hidden;
    $('#quickItems').hidden = !open;
    $('#quickToggle').setAttribute('aria-expanded', String(open));
    $('#quickToggle').setAttribute('aria-label', open ? '收起快捷导航' : '展开快捷导航');
  });
  $('#navBack')?.addEventListener('click', () => { if (history.length > 1) history.back(); else location.href = 'index.html'; });
  $('#navForward')?.addEventListener('click', () => history.forward());
  $('#navTop')?.addEventListener('click', () => scrollTo(0));
  $('#navBottom')?.addEventListener('click', () => scrollTo(document.documentElement.scrollHeight));
  if (window.navigation) {
    $('#navForward')?.toggleAttribute('disabled', !window.navigation.canGoForward);
    window.navigation.addEventListener('currententrychange', () => $('#navForward')?.toggleAttribute('disabled', !window.navigation.canGoForward));
  }

  // Keep motion on the compositor and only while a decorative element is on screen.
  if ('IntersectionObserver' in window && !reduce()) {
    const motion = new IntersectionObserver(entries => entries.forEach(entry => entry.target.classList.toggle('motion-active', entry.isIntersecting)), { rootMargin: '80px' });
    $$('.hero-art,.concept-map,.atlas-invite,.live-map-card').forEach(el => motion.observe(el));
  }

  // Six historical scenes: roving keyboard focus and linked city selection.
  function chooseScene(button, focus = false) {
    $$('.scene-tabs [role=tab]').forEach(tab => {
      const active = tab === button; tab.setAttribute('aria-selected', String(active)); tab.tabIndex = active ? 0 : -1;
    });
    $$('.scene-panel').forEach(panel => panel.hidden = panel.id !== 'scene-' + button.dataset.scene);
    const city = $('#scene-' + button.dataset.scene)?.dataset.city;
    if (city) selectCity(city, false);
    if (focus) button.focus();
  }
  $$('.scene-tabs [role=tab]').forEach((button, index, tabs) => {
    button.addEventListener('click', () => chooseScene(button));
    button.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); chooseScene(tabs[next], true); }
    });
  });

  // All libraries are served locally. Only tiles are external, after an explicit load.
  const cities = $('#mapCities') ? JSON.parse($('#mapCities').textContent) : [];
  let map, tileLayer, markerGroup, watchdog, generation = 0, succeeded = 0, errors = 0, libraryPromise;
  const providers = {
    esri: { name: 'Esri 街道地图', url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', maxZoom: 19, attribution: 'Tiles © Esri — Esri, HERE, Garmin, USGS, NGA, EPA, NPS and contributors' },
    imagery: { name: 'Esri 卫星影像', url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', maxZoom: 19, attribution: 'Tiles © Esri — Esri, Maxar, Earthstar Geographics and the GIS User Community' },
    osm: { name: 'OpenStreetMap', url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png', maxZoom: 19, attribution: '© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap contributors</a> · ODbL' }
  };
  function mapStatus(text) { if ($('#mapStatus')) $('#mapStatus').textContent = text; }
  function loadLibrary() {
    if (window.L) return Promise.resolve();
    if (libraryPromise) return libraryPromise;
    libraryPromise = new Promise((resolve, reject) => {
      if (!$('link[data-leaflet]')) { const css = document.createElement('link'); css.rel = 'stylesheet'; css.href = 'vendor/leaflet/leaflet.css'; css.dataset.leaflet = 'true'; document.head.append(css); }
      const script = document.createElement('script'); script.src = 'vendor/leaflet/leaflet.js'; script.onload = () => resolve(); script.onerror = () => { libraryPromise = null; script.remove(); reject(new Error('本地地图引擎未能载入')); }; document.head.append(script);
    });
    return libraryPromise;
  }
  function selectCity(id, move = true) {
    const city = cities.find(c => c.id === id); if (!city) return;
    if ($('#mapCity')) $('#mapCity').value = id;
    $$('.concept-city').forEach(node => node.classList.toggle('selected', node.dataset.city === id));
    if ($('#mapExternal')) $('#mapExternal').href = `https://www.bing.com/maps?cp=${city.lat}~${city.lon}&lvl=12`;
    if ($('#mapOsmExternal')) $('#mapOsmExternal').href = `https://www.openstreetmap.org/?mlat=${city.lat}&mlon=${city.lon}#map=12/${city.lat}/${city.lon}`;
    if (map) {
      map.setView([city.lat, city.lon], 10, { animate: !reduce() });
      markerGroup.eachLayer(marker => { if (marker.options.studyCity === id) marker.openPopup(); });
    } else mapStatus(`${city.name} · ${city.lat.toFixed(3)}°N / ${city.lon.toFixed(3)}°E；点击“载入现代地图”查看。`);
    if (move) $('#modern-map')?.scrollIntoView({ behavior: reduce() ? 'instant' : 'smooth', block: 'start' });
  }
  function setProvider(id, automatic = false) {
    if (!map || !providers[id]) return;
    clearTimeout(watchdog); const token = ++generation;
    if (tileLayer) map.removeLayer(tileLayer);
    succeeded = 0; errors = 0; $('#mapProvider').value = id;
    mapStatus((automatic ? '主图层暂不可达，已切换备用。' : '') + `正在载入${providers[id].name}…`);
    const config = providers[id];
    tileLayer = L.tileLayer(config.url, { attribution: config.attribution, maxZoom: config.maxZoom, updateWhenIdle: true, keepBuffer: 1, crossOrigin: false });
    function failed() {
      if (token !== generation || succeeded > 0) return;
      clearTimeout(watchdog);
      if (id !== 'osm') setProvider('osm', true);
      else mapStatus('在线图层暂不可达。历史示意、城市坐标与正文仍可用；可用独立地图链接，或切换图层重试。');
    }
    tileLayer.on('tileload', () => { if (token !== generation) return; succeeded++; clearTimeout(watchdog); mapStatus(`${config.name}已载入 · 可缩放、拖动与选择城市。现代影像不代表历史疆界。`); });
    tileLayer.on('tileerror', () => { if (token !== generation) return; errors++; if (errors >= 3 && !succeeded) failed(); });
    watchdog = setTimeout(failed, 12000);
    tileLayer.addTo(map);
  }
  async function startMap() {
    const button = $('#loadMap'); if (button) { button.disabled = true; button.textContent = '正在载入…'; }
    try {
      await loadLibrary();
      if (!map) {
        map = L.map('liveMap', { scrollWheelZoom: false, preferCanvas: true, fadeAnimation: false, zoomAnimation: !reduce(), attributionControl: true });
        markerGroup = L.layerGroup().addTo(map);
        cities.forEach(city => {
          const popup = document.createElement('div'); const title = document.createElement('strong'); title.textContent = city.name + ' · ' + city.en;
          const text = document.createElement('p'); text.textContent = city.role; popup.append(title, text);
          const marker = L.marker([city.lat, city.lon], { studyCity: city.id, title: city.name, icon: L.divIcon({ className: 'study-map-pin', html: '<span></span>', iconSize: [22, 28], iconAnchor: [11, 28] }) });
          marker.bindPopup(popup); marker.addTo(markerGroup);
        });
      }
      $('#mapStart').hidden = true;
      map.invalidateSize();
      const city = cities.find(c => c.id === $('#mapCity').value) || cities[0];
      map.setView([city.lat, city.lon], 7, { animate: false });
      setProvider($('#mapProvider').value);
    } catch (error) { mapStatus(error.message + '。离线示意与独立地图链接仍可使用。'); }
    finally { if (button) { button.disabled = false; button.textContent = '载入现代地图'; } }
  }
  $('#loadMap')?.addEventListener('click', startMap);
  $('#mapProvider')?.addEventListener('change', () => { if (map) setProvider($('#mapProvider').value); });
  $('#mapCity')?.addEventListener('change', () => selectCity($('#mapCity').value, false));
  $('#mapExtent')?.addEventListener('click', () => { if (map) map.fitBounds(cities.map(c => [c.lat, c.lon]), { padding: [30, 30], animate: !reduce() }); else toast('先载入现代地图，即可查看全部城市。'); });
  $('#stopMap')?.addEventListener('click', () => {
    ++generation; clearTimeout(watchdog); if (map) { map.remove(); map = null; tileLayer = null; markerGroup = null; }
    $('#mapStart').hidden = false; mapStatus('在线地图已暂停，不再请求图层；示意图与正文不受影响。');
  });
  $$('.locate-scene,.concept-city').forEach(button => {
    button.addEventListener('click', () => selectCity(button.dataset.city));
    if (button.classList.contains('concept-city')) button.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); selectCity(button.dataset.city); } });
  });
  $$('.city-btn').forEach(button => button.addEventListener('click', () => selectCity(button.dataset.city, false)));

  // TextQuote + offsets: render spans only. Never save or execute annotated HTML.
  const storageKey = 'gtstudy-belgic-marks-v2';
  const styles = new Set(['bold', 'ink-blue', 'ink-rose', 'gold', 'green', 'underline', 'dash', 'block']);
  let marks = [], undo = [], selectedRange, selectedRoot, selectionTimer, lastFocus;
  function validMark(mark) {
    return mark && typeof mark.id === 'string' && mark.id.length <= 100 && typeof mark.block === 'string' && mark.block.length <= 180 && typeof mark.quote === 'string' && mark.quote.length > 0 && mark.quote.length <= 2500 && Number.isInteger(mark.start) && Number.isInteger(mark.end) && mark.start >= 0 && mark.end > mark.start && styles.has(mark.style);
  }
  function readMarks() { try { const data = JSON.parse(localStorage.getItem(storageKey) || '[]'); marks = Array.isArray(data) ? data.filter(validMark).slice(0, 2000) : []; } catch { marks = []; } }
  readMarks();
  function persist() { try { localStorage.setItem(storageKey, JSON.stringify(marks)); } catch { toast('浏览器未允许保存，请先导出重点备份。'); } renderList(); }
  function remember() { undo.push(JSON.stringify(marks)); if (undo.length > 20) undo.shift(); }
  const roots = new Map();
  $$('[data-original]').forEach(el => { el.dataset.noteBlock = 'original:' + el.dataset.original; });
  $$('main .overview-card p:not(.refs), main .timeline-item p:not(.eyebrow), main .callout p, .culture p').forEach((el, i) => { if (!el.dataset.noteBlock && !el.closest('[data-note-block]')) el.dataset.noteBlock = 'reading:' + location.pathname.split('/').pop().replace('index.html', '') + ':' + i; });
  $$('[data-note-block]').forEach(el => { if (!roots.has(el.dataset.noteBlock)) roots.set(el.dataset.noteBlock, el); });
  function clearRoot(root) { root.querySelectorAll('[data-study-mark]').forEach(span => span.replaceWith(...span.childNodes)); root.normalize(); }
  function resolve(mark, text) {
    if (text.slice(mark.start, mark.end) === mark.quote) return [mark.start, mark.end];
    const first = text.indexOf(mark.quote); if (first < 0) return null;
    const second = text.indexOf(mark.quote, first + 1);
    if (second < 0) return [first, first + mark.quote.length];
    for (let at = first; at >= 0; at = text.indexOf(mark.quote, at + 1)) {
      if (mark.prefix && text.slice(Math.max(0, at - mark.prefix.length), at) === mark.prefix && (!mark.suffix || text.slice(at + mark.quote.length, at + mark.quote.length + mark.suffix.length) === mark.suffix)) return [at, at + mark.quote.length];
    }
    return null;
  }
  function wrap(root, from, to, mark) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); const parts = []; let node, offset = 0;
    while ((node = walker.nextNode())) { const end = offset + node.length; if (end > from && offset < to) parts.push({ node, start: Math.max(0, from - offset), end: Math.min(node.length, to - offset) }); offset = end; }
    parts.reverse().forEach(part => {
      let text = part.node; if (part.end < text.length) text.splitText(part.end); if (part.start) text = text.splitText(part.start);
      const span = document.createElement('span'); span.className = 'study-mark style-' + mark.style; span.dataset.studyMark = mark.id; text.replaceWith(span); span.append(text);
    });
  }
  function renderRoot(root) {
    clearRoot(root); const text = root.textContent;
    marks.filter(mark => mark.block === root.dataset.noteBlock).forEach(mark => { const range = resolve(mark, text); if (range) wrap(root, range[0], range[1], mark); });
  }
  function applyAll() { roots.forEach(root => { if (marks.some(mark => mark.block === root.dataset.noteBlock)) renderRoot(root); }); renderList(); }
  function captureSelection() {
    const selection = getSelection(); if (!selection || selection.isCollapsed || !selection.rangeCount) { if (!$('#markToolbar')?.contains(document.activeElement)) $('#markToolbar').hidden = true; return; }
    const range = selection.getRangeAt(0); const start = range.startContainer.nodeType === 1 ? range.startContainer : range.startContainer.parentElement;
    const end = range.endContainer.nodeType === 1 ? range.endContainer : range.endContainer.parentElement;
    const root = start.closest('[data-note-block]');
    if (!root || root !== end.closest('[data-note-block]') || range.toString().trim().length < 1 || range.toString().length > 2500 || root.closest('.masked .reader-passage:not(.revealed)')) { $('#markToolbar').hidden = true; return; }
    selectedRange = range.cloneRange(); selectedRoot = root; $('#markToolbar').hidden = false;
  }
  document.addEventListener('selectionchange', () => { clearTimeout(selectionTimer); selectionTimer = setTimeout(captureSelection, 150); });
  $$('#markToolbar button').forEach(button => button.addEventListener('pointerdown', event => event.preventDefault()));
  $$('[data-mark-style]').forEach(button => button.addEventListener('click', () => {
    if (!selectedRange || !selectedRoot?.isConnected) return;
    const before = selectedRange.cloneRange(); before.selectNodeContents(selectedRoot); before.setEnd(selectedRange.startContainer, selectedRange.startOffset);
    const start = before.toString().length, quote = selectedRange.toString(), end = start + quote.length, text = selectedRoot.textContent;
    if (text.slice(start, end) !== quote) { toast('选区已变化，请重新选中文字。'); return; }
    remember();
    marks = marks.filter(mark => !(mark.block === selectedRoot.dataset.noteBlock && mark.start < end && mark.end > start));
    marks.push({ id: 'mark-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 7), block: selectedRoot.dataset.noteBlock, start, end, quote, prefix: text.slice(Math.max(0, start - 28), start), suffix: text.slice(end, end + 28), style: button.dataset.markStyle, page: location.pathname.split('/').pop() || 'index.html', created: new Date().toISOString() });
    getSelection().removeAllRanges(); renderRoot(selectedRoot); persist(); $('#markToolbar').hidden = true; selectedRange = null; toast('重点已保存。可从右下角笔记回看，或继续选择文字标记。');
  }));
  $('#undoMark')?.addEventListener('click', () => { if (!undo.length) { toast('暂无可撤销操作。'); return; } marks = JSON.parse(undo.pop()); roots.forEach(clearRoot); applyAll(); persist(); toast('已撤销最近一次标记。'); });
  $('#closeMarkToolbar')?.addEventListener('click', () => { $('#markToolbar').hidden = true; getSelection()?.removeAllRanges(); });
  function showMarks(open) {
    $('#marksDrawer').hidden = !open; $('#marksBackdrop').hidden = !open; document.body.classList.toggle('marks-open', open);
    if (open) { lastFocus = document.activeElement; renderList(); $('#closeMarks').focus(); } else lastFocus?.focus();
  }
  $('#openMarks')?.addEventListener('click', () => showMarks(true));
  $('#closeMarks')?.addEventListener('click', () => showMarks(false));
  $('#marksBackdrop')?.addEventListener('click', () => showMarks(false));
  $('#marksDrawer')?.addEventListener('keydown', event => {
    if (event.key === 'Escape') { showMarks(false); return; }
    if (event.key === 'Tab') { const nodes = $$('#marksDrawer button:not([disabled]),#marksDrawer a,#marksDrawer input'); const first = nodes[0], last = nodes[nodes.length - 1]; if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); } else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); } }
  });
  function jumpMark(mark) {
    const root = roots.get(mark.block);
    if (!root) { location.href = (mark.page && /^[\w-]+\.html$/.test(mark.page) ? mark.page : 'index.html') + '?mark=' + encodeURIComponent(mark.id); return; }
    showMarks(false);
    const scene = root.closest('.scene-panel');
    if (scene?.hidden) { const tab = document.querySelector('[data-scene="' + scene.id.replace('scene-', '') + '"]'); if (tab) chooseScene(tab); }
    if (root.closest('.article-card[hidden]')) $('#resetSearch')?.click();
    for (let el = root.parentElement; el; el = el.parentElement) if (el.tagName === 'DETAILS') el.open = true;
    root.scrollIntoView({ behavior: reduce() ? 'instant' : 'smooth', block: 'center' }); root.classList.add('mark-located'); setTimeout(() => root.classList.remove('mark-located'), 2000);
  }
  function renderList() {
    if (!$('#marksList')) return;
    $('#markCount').textContent = marks.length;
    const list = $('#marksList'); list.replaceChildren();
    if (!marks.length) { const p = document.createElement('p'); p.className = 'marks-empty'; p.textContent = '还没有重点。回到正文，选中一句话，再选择颜色、底纹或线条。'; list.append(p); return; }
    [...marks].reverse().forEach(mark => {
      const item = document.createElement('article'); item.className = 'saved-mark';
      const quote = document.createElement('p'); quote.className = 'style-' + mark.style; quote.textContent = mark.quote;
      const meta = document.createElement('small'); const root = roots.get(mark.block); meta.textContent = mark.block.startsWith('original:') ? '认信原文 · 个人标记' : '学习解读 · 个人标记';
      if (root && !resolve(mark, root.textContent)) meta.textContent += ' · 原段已变动，请复核';
      const actions = document.createElement('div'); actions.className = 'toolbar';
      const go = document.createElement('button'); go.type = 'button'; go.textContent = '回到原处'; go.addEventListener('click', () => jumpMark(mark));
      const remove = document.createElement('button'); remove.type = 'button'; remove.textContent = '删除此条'; remove.addEventListener('click', () => { remember(); marks = marks.filter(m => m.id !== mark.id); if (root) renderRoot(root); persist(); });
      actions.append(go, remove); item.append(meta, quote, actions); list.append(item);
    });
  }
  function download(data, name) { const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })); const a = document.createElement('a'); a.href = url; a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000); }
  $('#exportMarks')?.addEventListener('click', () => download({ format: storageKey, version: 2, marks }, 'GTstudy-重点笔记.json'));
  $('#importMarks')?.addEventListener('change', async event => {
    try {
      const file = event.target.files[0]; if (!file) return; if (file.size > 4000000) throw new Error('文件过大');
      const data = JSON.parse(await file.text()); if (data.format !== storageKey || !Array.isArray(data.marks) || !data.marks.every(validMark)) throw new Error('重点格式不符');
      remember(); const merged = new Map(marks.map(mark => [mark.id, mark])); data.marks.forEach(mark => merged.set(mark.id, mark)); marks = [...merged.values()].slice(-2000); roots.forEach(clearRoot); applyAll(); persist(); toast('重点已合并导入，原有笔记保持不变。');
    } catch (error) { toast('导入失败：' + error.message); }
    event.target.value = '';
  });
  window.addEventListener('gtstudy:marks-imported', () => { roots.forEach(clearRoot); readMarks(); applyAll(); });
  window.addEventListener('gtstudy:merge-marks', event => {
    if (!Array.isArray(event.detail) || !event.detail.every(validMark)) { toast('正文笔记已导入；重点数据格式不符，现有重点保持不变。'); return; }
    remember(); const merged = new Map(marks.map(mark => [mark.id, mark])); event.detail.forEach(mark => merged.set(mark.id, mark)); marks = [...merged.values()].slice(-2000); roots.forEach(clearRoot); applyAll(); persist();
  });
  applyAll();
  const wanted = new URLSearchParams(location.search).get('mark');
  if (wanted) { const mark = marks.find(m => m.id === wanted); if (mark) requestAnimationFrame(() => jumpMark(mark)); }
})();
