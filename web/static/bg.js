// Subtle animated background: a coarse cyclic cellular automaton run by the lab's JS engine with the plugin's own
// default parameters (read from /api/rules, i.e. CyclicCA's DEFAULT_NUM_STATES / DEFAULT_THRESHOLD), drawn behind
// the page in dimmed site accents. Static single frame under prefers-reduced-motion; paused while the tab is hidden.
import { makeState, step } from './ca_engine.js';
import { api, rng } from './core.js';

const CELL = 10, TICK_MS = 200;
const ACCENTS = [[46, 242, 192], [157, 140, 255], [255, 165, 61]];

function palette(n) {
  return Array.from({ length: n }, (_, i) => {
    const t = (i / n) * ACCENTS.length, k = Math.floor(t), u = t - k;
    const a = ACCENTS[k % ACCENTS.length], b = ACCENTS[(k + 1) % ACCENTS.length];
    return a.map((v, j) => Math.round((v + (b[j] - v) * u) * 0.55));
  });
}

export async function background(canvas) {
  if (!canvas) return;
  const rules = await api('/rules');
  const cyc = rules.find(r => r.key === 'cyclic_ca');
  const params = Object.fromEntries(cyc.params.map(p => [p.name, p.default]));
  const N = params.num_states, colors = palette(N);
  const ctx = canvas.getContext('2d');
  let s = null, img = null;
  const reset = () => {
    const w = Math.min(200, Math.ceil(innerWidth / CELL)), h = Math.min(130, Math.ceil(innerHeight / CELL));
    canvas.width = w; canvas.height = h;
    const r = rng(7);
    s = makeState(w, h, Array.from({ length: w * h }, () => Math.floor(r() * N)));
    img = ctx.createImageData(w, h);
  };
  const draw = () => {
    const d = img.data;
    for (let i = 0; i < s.cells.length; i++) {
      const [r, g, b] = colors[s.cells[i]];
      d[i * 4] = r; d[i * 4 + 1] = g; d[i * 4 + 2] = b; d[i * 4 + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
  };
  reset();
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    for (let i = 0; i < 60; i++) step('cyclic_ca', s, params);   // a settled frame, not raw noise
    draw();
    return;
  }
  draw();
  addEventListener('resize', () => { reset(); draw(); });
  setInterval(() => {
    if (document.hidden) return;
    step('cyclic_ca', s, params);
    draw();
  }, TICK_MS);
}
