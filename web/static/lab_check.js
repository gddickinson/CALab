// Lab side panel: step the current grid through the real Python plugin (POST /api/run, local app only) and compare
// with the browser engine; plus a JSON download of the grid that works everywhere.
import { api, esc, isStatic, needsServer, download } from './core.js';
import { makeState, run, encode } from './ca_engine.js';

const MAX_WORK = 1_000_000;   // same cap as web/catalogue.py MAX_WORK

export function checkPanel(host, ctx) {
  // ctx: { key(), state(), params() }
  host.innerHTML = `<h3>Check against Python</h3>
    ${isStatic() ? needsServer('Stepping your grid through the Python plugin')
      : `<p class="small mute">Runs the current grid through the plugin's own <code>step()</code> on the server and compares it,
        cell for cell, with this page's JavaScript engine.</p>
      <div class="row"><div><label for="chk-n">Generations</label><input id="chk-n" type="number" min="1" max="500" value="10"></div>
      <div><button id="chk-go" type="button">Check with Python</button></div></div>`}
    <p id="chk-out" class="small" aria-live="polite"></p>
    <button id="chk-dl" type="button" class="alt">Download grid (JSON)</button>`;
  const out = host.querySelector('#chk-out');
  host.querySelector('#chk-dl').onclick = () => {
    const s = ctx.state();
    download(`calab_${ctx.key()}_gen${s.gen}.json`, JSON.stringify({
      rule: ctx.key(), params: ctx.params(), width: s.w, height: s.h, row: s.row, generation: s.gen,
      encoding: 'base-36 digit per cell, row-major', cells: encode(s.cells),
    }), 'application/json');
  };
  const go = host.querySelector('#chk-go');
  if (!go) return;
  go.onclick = async () => {
    const s = ctx.state(), n = Math.max(1, Math.min(500, +host.querySelector('#chk-n').value || 1));
    if (s.w * s.h * n > MAX_WORK) {
      out.className = 'small err';
      out.textContent = `Too much work for the pure-Python loops: width x height x generations must be at most ${MAX_WORK.toLocaleString()}.`;
      return;
    }
    go.disabled = true;
    out.className = 'small mute';
    out.textContent = 'Running the Python plugin...';
    try {
      const t0 = performance.now();
      const py = await api('/run', { body: { rule: ctx.key(), width: s.w, height: s.h, cells: encode(s.cells), steps: n, params: ctx.params(), row: s.row } });
      const ms = performance.now() - t0;
      const js = run(ctx.key(), makeState(s.w, s.h, s.cells, s.row), ctx.params(), n);
      const a = encode(js.cells);
      let diff = 0;
      for (let i = 0; i < a.length; i++) diff += a[i] !== py.cells[i];
      out.className = diff ? 'small err' : 'small ok';
      out.innerHTML = diff
        ? `${diff} of ${a.length} cells differ after ${n} generations.`
        : `Identical: all ${a.length.toLocaleString()} cells match after ${n} generations (Python took ${Math.round(ms)} ms;
          ${py.stats.active_cells} active cells, entropy ${py.stats.entropy.toFixed(3)} bits).`;
    } catch (e) {
      out.className = 'small err';
      out.textContent = esc(e.message);
    } finally {
      go.disabled = false;
    }
  };
}
