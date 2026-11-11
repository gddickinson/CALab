// The lab: pick an automaton and a preset (both from the Python plugin registry), play / pause / step, change speed
// and rule parameters, draw on the grid, fill a random soup, resize, and (in the local app) check against Python.
import { route, api, app, esc, list, go, slider, animate, onLeave, rng } from './core.js';
import { makeState, step, decode, stats, resize } from './ca_engine.js';
import { makeView, stateColors } from './lab_view.js';
import { checkPanel } from './lab_check.js';

const SIZES = [50, 80, 100, 150, 200, 250];
const ELEMENTARY = new Set(['rule_30', 'rule_110', 'rule_90']);

route('lab', async (args, query) => {
  const rules = await api('/rules');
  const rule = rules.find(r => r.key === args[0]) || rules.find(r => r.key === 'game_of_life');
  const { patterns } = await api('/patterns/' + rule.key);
  const preset0 = patterns.find(p => p.name === query.pattern) || patterns[0];
  const defaults = Object.fromEntries(rule.params.map(p => [p.name, p.default]));
  const is1d = ELEMENTARY.has(rule.key);

  let params = { ...defaults }, s = null, preset = preset0, playing = false, speed = 15, brush = 1, dirty = true;
  const nStates = () => (rule.key === 'cyclic_ca' ? params.num_states : rule.num_states);

  app().innerHTML = `
  <p class="kicker">Lab · ${esc(rule.categories.join(' · '))}</p>
  <h1>${esc(rule.name)}</h1>
  <p class="lead">${esc(rule.info || rule.description)}. ${esc(rule.description)}.</p>
  <div class="lab">
    <div class="panel controls">
      <label for="sel-rule">Automaton</label>
      <select id="sel-rule">${list(rules, r => `<option value="${esc(r.key)}"${r.key === rule.key ? ' selected' : ''}>${esc(r.name)}</option>`)}</select>
      <label for="sel-preset">Preset pattern</label>
      <select id="sel-preset">${list(patterns, p => `<option value="${esc(p.name)}">${esc(p.name.replace(/_/g, ' '))}: ${esc(p.description)}</option>`)}</select>
      <div class="bar">
        <button id="b-play" type="button">Play</button><button id="b-step" type="button" class="alt">Step</button>
        <button id="b-reset" type="button" class="alt">Reset</button><button id="b-clear" type="button" class="alt">Clear</button>
      </div>
      <div id="speed"></div>
      <div id="params"></div>
      <label>Draw with state</label>
      <div class="palette" id="palette" role="radiogroup" aria-label="Drawing state"></div>
      <p class="hint">Click or drag on the grid to paint; right-click or Shift-drag erases. Keys: Space play/pause, S step.</p>
      <h3>Random soup</h3>
      <div id="density"></div>
      <button id="b-soup" type="button" class="alt">Fill randomly</button>
      <label for="sel-size">Grid size (cells)</label>
      <select id="sel-size"></select>
      <div class="readout" id="readout" aria-live="off"></div>
    </div>
    <div class="view"><div class="stage ca" id="stage"></div></div>
    <div class="extra">
      <div class="legend" id="legend"></div>
      <div class="panel" id="check"></div>
      <details class="src panel"><summary>About this automaton (from the plugin source)</summary>
        <pre class="doc">${esc(rule.module_doc)}</pre><pre class="doc">${esc(rule.doc)}</pre></details>
    </div>
  </div>`;
  const $ = sel => app().querySelector(sel);

  const view = makeView($('#stage'), {
    label: `${rule.name} grid: click or drag to draw cells`,
    onPaint(x, y, erase) { s.cells[y * s.w + x] = erase ? 0 : brush; dirty = true; },
  });

  function load(p) {
    preset = p;
    params = { ...defaults, ...p.params };
    s = makeState(p.width, p.height, decode(p.cells, p.width, p.height), p.row);
    $('#sel-preset').value = p.name;
    history.replaceState(null, '', `#/lab/${rule.key}?pattern=${encodeURIComponent(p.name)}${playing ? '&play=1' : ''}`);
    buildParams(); buildPalette(); buildSizes(); dirty = true;
  }

  function buildParams() {
    const host = $('#params');
    host.innerHTML = '';
    rule.params.forEach(p => slider(host, { id: p.name, label: p.label, min: p.min, max: p.max, value: params[p.name] }, v => {
      params[p.name] = v;
      if (p.name === 'num_states') { buildPalette(); }
      dirty = true;
    }));
  }

  function buildPalette() {
    const n = nStates(), cols = stateColors(rule.colormap, n);
    view.setColors(cols);
    brush = Math.min(Math.max(brush, 1), n - 1);
    $('#palette').innerHTML = list(Array.from({ length: n }, (_, i) => i), i => `<button type="button" role="radio"
      aria-checked="${i === brush}" class="${i === brush ? 'on' : ''}" data-s="${i}" style="background:${esc(cols[i])}"
      title="State ${i}" aria-label="State ${i}">${i}</button>`);
    $('#legend').innerHTML = `<span class="mute small">States:</span>` + list(Array.from({ length: n }, (_, i) => i),
      i => `<span><i style="background:${esc(cols[i])}"></i>${i}</span>`);
  }
  $('#palette').addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    brush = +b.dataset.s;
    $('#palette').querySelectorAll('button').forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-checked', x === b); });
  });

  function buildSizes() {
    const opts = [...new Set([...SIZES, s.w].map(String))].map(Number).sort((a, b) => a - b);
    $('#sel-size').innerHTML = list(opts, n => `<option value="${n}"${n === s.w && s.w === s.h ? ' selected' : ''}>${n} x ${n}</option>`) +
      (s.w !== s.h ? `<option selected value="">${s.w} x ${s.h}</option>` : '');
  }
  $('#sel-size').onchange = e => { const n = +e.target.value; if (n) { s = resize(s, n, n); dirty = true; } };

  // controls
  $('#sel-rule').onchange = e => go('#/lab/' + e.target.value);
  $('#sel-preset').onchange = e => load(patterns.find(p => p.name === e.target.value));
  const setPlaying = on => { playing = on; $('#b-play').textContent = on ? 'Pause' : 'Play'; };
  const once = () => { if (!step(rule.key, s, params)) setPlaying(false); dirty = true; };
  $('#b-play').onclick = () => setPlaying(!playing);
  $('#b-step').onclick = () => { setPlaying(false); once(); };
  $('#b-reset').onclick = () => { setPlaying(false); load(preset); };
  $('#b-clear').onclick = () => { s = makeState(s.w, s.h); dirty = true; };
  slider($('#speed'), { id: 'speed', label: 'Speed', min: 1, max: 120, value: speed, unit: ' gen/s' }, v => { speed = v; });
  let density = rule.key === 'cyclic_ca' ? 1 : is1d ? 0.5 : 0.3;
  slider($('#density'), { id: 'density', label: 'Density', min: 0.05, max: 1, step: 0.05, value: density, fmt: v => v.toFixed(2) }, v => { density = v; });
  let seed = 1;
  $('#b-soup').onclick = () => {
    const r = rng(seed++), n = s.w * s.h;
    const fresh = makeState(s.w, s.h);
    if (rule.key === 'cyclic_ca') for (let i = 0; i < n; i++) fresh.cells[i] = r() < density ? Math.floor(r() * params.num_states) : 0;
    else if (is1d) for (let x = 0; x < s.w; x++) fresh.cells[x] = r() < density ? 1 : 0;
    else for (let i = 0; i < n; i++) fresh.cells[i] = r() < density ? 1 : 0;
    s = fresh; dirty = true;
  };

  if (query.play) setPlaying(true);   // #/lab/<key>?pattern=..&play=1 starts running (shareable links, screenshots)
  checkPanel($('#check'), { key: () => rule.key, state: () => s, params: () => ({ ...params }) });
  load(preset0);

  // animation loop: fixed generations per second, at most 8 generations per frame
  let lastT = 0, acc = 0, lastStats = 0;
  const stop = animate(t => {
    const dt = lastT ? Math.min(t - lastT, 250) : 0;
    lastT = t;
    if (playing) {
      acc += dt * speed / 1000;
      let n = Math.min(8, Math.floor(acc));
      acc -= Math.floor(acc);
      while (n-- > 0 && playing) once();
    }
    if (dirty) { view.render(s); dirty = false; }
    if (t - lastStats > 200) { lastStats = t; readout(); }
  });
  const keys = e => {
    if (e.target.closest('input, select, textarea') || e.metaKey || e.ctrlKey) return;
    if (e.key === ' ') { e.preventDefault(); setPlaying(!playing); } else if (e.key === 's' || e.key === 'S') { setPlaying(false); once(); }
  };
  document.addEventListener('keydown', keys);
  onLeave(() => { stop(); document.removeEventListener('keydown', keys); });

  function readout() {
    const st = stats(s);
    $('#readout').innerHTML = [['Generation', st.generation], ['Grid', `${s.w} x ${s.h}`], ['Active cells', st.active_cells],
      ['Density', st.density.toFixed(1) + ' %'], ['Entropy', st.entropy.toFixed(3) + ' bits'], ['States present', st.unique_states]]
      .concat(is1d ? [['Current row', s.row]] : [])
      .map(([k, v]) => `<div><span>${esc(k)}</span><b>${esc(v)}</b></div>`).join('');
  }
});

