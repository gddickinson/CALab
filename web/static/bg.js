// Subtle animated background: a coarse cyclic cellular automaton (the same JS engine as the lab) drawn behind the
// page. Static single frame under prefers-reduced-motion; paused while the tab is hidden.
import { makeState, step } from './ca_engine.js';
import { rng } from './core.js';

const N = 8, CELL = 10;   // N=8, T=2 keeps forming slow spirals from a random start
const PALETTE = Array.from({ length: N }, (_, i) => {
  const t = i / N, a = [46, 242, 192], b = [157, 140, 255], c = [255, 165, 61];
  const mix = (p, q, u) => p.map((v, k) => Math.round(v + (q[k] - v) * u));
  const rgb = t < 0.5 ? mix(a, b, t * 2) : mix(b, c, (t - 0.5) * 2);
  return rgb.map(v => Math.round(v * 0.55));
});

export function background(canvas) {
  if (!canvas) return;
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
      const [r, g, b] = PALETTE[s.cells[i]];
      d[i * 4] = r; d[i * 4 + 1] = g; d[i * 4 + 2] = b; d[i * 4 + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
  };
  reset(); draw();
  addEventListener('resize', () => { reset(); draw(); });
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  setInterval(() => {
    if (document.hidden) return;
    step('cyclic_ca', s, { num_states: N, threshold: 2 });
    draw();
  }, 140);
}
