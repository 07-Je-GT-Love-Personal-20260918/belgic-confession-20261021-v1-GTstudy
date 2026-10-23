(() => {
  'use strict';
  const $ = s => document.querySelector(s), $$ = s => Array.from(document.querySelectorAll(s));
  if (!$('#readerData')) return;
  const doc = JSON.parse($('#readerData').textContent), select = $('#docSelect');
  const file = key => key === 'apostles' ? 'reader.html' : 'reader-' + key + '.html';
  const request = new URLSearchParams(location.search).get('doc');
  const allowed = Array.from(select.options).map(o => o.value);
  if (request && allowed.includes(request) && request !== doc.key) { location.replace(file(request) + location.hash); return; }
  select.addEventListener('change', () => { if (select.value !== doc.key) location.href = file(select.value); });
  const status = message => $('#readerStatus').textContent = message;
  let speechRun = 0;
  function stop() { speechRun++; if ('speechSynthesis' in window) speechSynthesis.cancel(); }
  function mask(on) {
    document.body.classList.toggle('masked', on); $('#readerMask').setAttribute('aria-pressed', String(on)); $('#readerMask').textContent = on ? '显示全部正文' : '遮盖正文 · 背诵';
    $$('.reader-passage').forEach(p => { p.classList.remove('revealed'); p.setAttribute('aria-expanded', String(!on)); p.querySelector('.original-text').setAttribute('aria-hidden', String(on)); });
  }
  $('#readerMask').addEventListener('click', () => mask(!document.body.classList.contains('masked')));
  $$('.reader-passage').forEach(p => {
    const toggle = () => { if (!document.body.classList.contains('masked') || getSelection()?.toString()) return; p.classList.toggle('revealed'); const show = p.classList.contains('revealed'); p.setAttribute('aria-expanded', String(show)); p.querySelector('.original-text').setAttribute('aria-hidden', String(!show)); };
    p.addEventListener('click', toggle); p.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); } });
  });
  const text = () => doc.title + '\n\n' + doc.sections.map(s => (doc.sections.length > 1 ? s.title + '\n\n' : '') + s.text).join('\n\n');
  $('#readerCopy').addEventListener('click', async () => { try { await navigator.clipboard.writeText(text()); status('原始全文已复制，不包含个人标记样式。'); } catch { status('浏览器未允许复制，请选择正文手动复制。'); } });
  $('#readerPrint').addEventListener('click', () => window.print());
  $('#readerSpeak').addEventListener('click', () => {
    if (!('speechSynthesis' in window)) { status('此设备未提供语音朗读。'); return; }
    stop(); const run = speechRun; const chunks = text().match(/[^。！？\n]+[。！？]?/g) || []; let index = 0;
    function next() { if (run !== speechRun) return; if (index >= chunks.length) { status('朗读结束。'); return; } const u = new SpeechSynthesisUtterance(chunks[index++]); u.lang = 'zh-CN'; u.rate = .88; u.onend = next; u.onerror = event => { if (run === speechRun && event.error !== 'canceled' && event.error !== 'interrupted') status('朗读中止，请检查设备中文语音。'); }; speechSynthesis.speak(u); }
    status('设备语音朗读中，可随时停止。'); next();
  });
  $('#readerStop').addEventListener('click', () => { stop(); status('朗读已停止。'); });
  window.addEventListener('pagehide', stop);
})();
