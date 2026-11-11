// CALab browser engine: a pure-JS port of every automaton in plugins/PLUGIN_REGISTRY (no DOM, runs in node too).
// A state is { w, h, cells: Int32Array (row-major), gen, row }; `row` is the elementary CA's current_row.
// Each rule's step(src, dst, w, h, params, state) mirrors the Python plugin's step() exactly, including its quirks
// (wrap-around edges, neighbour *sums* of state values for the Life-likes, table fall-backs); ca_engine.test.mjs
// checks it against grids produced by the Python code (tests/fixtures/ca_engine_fixtures.json).
import { MOORE_RULES } from './ca_rules_moore.js';
import { TABLE_RULES } from './ca_rules_table.js';
import { ELEMENTARY } from './ca_rules_1d.js';

export const RULES = { ...MOORE_RULES, ...TABLE_RULES, elementary: ELEMENTARY };
const ALIAS = { rule_30: 'elementary', rule_110: 'elementary', rule_90: 'elementary' };
// Fixed rule numbers of the three registered elementary plugins (Rule30Plugin etc.); a `rule` param overrides it.
const DEFAULTS = { rule_30: { rule: 30 }, rule_110: { rule: 110 }, rule_90: { rule: 90 } };
export const engineFor = key => RULES[ALIAS[key] || key];
export const isPorted = key => !!engineFor(key);

export function makeState(w, h, cells = null, row = 0) {
  return { w, h, cells: cells ? Int32Array.from(cells) : new Int32Array(w * h), gen: 0, row };
}

// One generation. Returns false when the rule had nothing left to do (an elementary CA whose grid is full).
export function step(key, s, params = {}) {
  const rule = engineFor(key);
  if (!rule) throw new Error(`no JS engine for ${key}`);
  const dst = new Int32Array(s.cells.length);
  const advanced = rule.step(s.cells, dst, s.w, s.h, { ...DEFAULTS[key], ...params }, s);
  if (advanced === false) return false;
  s.cells = dst;
  s.gen += 1;
  return true;
}

export function run(key, s, params, n) {
  for (let i = 0; i < n; i++) step(key, s, params);
  return s;
}

// --- base-36 grid text (mirrors web/grid_codec.py) ---------------------------------------------------------------
export function decode(text, w, h) {
  if (text.length !== w * h) throw new Error(`expected ${w * h} cells, got ${text.length}`);
  const out = new Int32Array(w * h);
  for (let i = 0; i < out.length; i++) out[i] = parseInt(text[i], 36);
  return out;
}
export function encode(cells) {
  let s = '';
  for (let i = 0; i < cells.length; i++) s += cells[i].toString(36);
  return s;
}

// --- statistics (mirrors CellularAutomaton.compute_statistics) ---------------------------------------------------
export function stats(s) {
  const counts = new Map();
  let active = 0;
  for (const v of s.cells) { counts.set(v, (counts.get(v) || 0) + 1); if (v) active++; }
  const n = s.cells.length;
  let entropy = 0;
  for (const c of counts.values()) { const p = c / n; entropy -= p * Math.log2(p + 1e-10); }
  return { generation: s.gen, active_cells: active, density: active / n * 100, entropy, unique_states: counts.size };
}

// Resample a grid into a new size, centred (used when the grid size changes).
export function resize(s, w, h) {
  const out = makeState(w, h, null, 0);
  const ox = Math.floor((w - s.w) / 2), oy = Math.floor((h - s.h) / 2);
  for (let y = 0; y < s.h; y++) for (let x = 0; x < s.w; x++) {
    const nx = x + ox, ny = y + oy;
    if (nx >= 0 && ny >= 0 && nx < w && ny < h) out.cells[ny * w + nx] = s.cells[y * s.w + x];
  }
  out.gen = s.gen;
  return out;
}
