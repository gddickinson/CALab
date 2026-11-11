// Rule-table automata on the von Neumann neighbourhood (C, N, E, S, W; edges wrap), ported from
// langton_loop.py, von_neumann.py and von_neumann_full.py. Tables are built in the same order as the Python dicts, so
// a later assignment to the same key overrides an earlier one exactly as it does in Python.

const key = (c, n, e, s, w) => (c << 20) | (n << 15) | (e << 10) | (s << 5) | w;

// Generic table stepper: look the pattern up, else apply the plugin's fall-back for the centre value.
function tableRule(build, fallback) {
  let table = null;
  return {
    table: () => (table ||= build()),
    step(src, dst, w, h) {
      const t = table ||= build();
      for (let y = 0; y < h; y++) {
        const yn = ((y - 1 + h) % h) * w, y0 = y * w, ys = ((y + 1) % h) * w;
        for (let x = 0; x < w; x++) {
          const c = src[y0 + x];
          const r = t.get(key(c, src[yn + x], src[y0 + (x + 1) % w], src[ys + x], src[y0 + (x - 1 + w) % w]));
          dst[y0 + x] = r !== undefined ? r : fallback(c);
        }
      }
    },
  };
}

// --- Langton's Loop: the plugin's working subset of the rule table; no rule -> unchanged ---------------------------
const LANGTON = [
  [[0, 1, 1, 1, 0], 1], [[0, 1, 1, 0, 1], 1], [[0, 1, 0, 1, 1], 1], [[0, 0, 1, 1, 1], 1],
  [[0, 2, 1, 0, 0], 1], [[0, 0, 2, 1, 0], 1], [[0, 0, 0, 2, 1], 1], [[0, 1, 0, 0, 2], 1],
  [[1, 1, 1, 0, 0], 1], [[1, 1, 0, 1, 0], 1], [[1, 1, 0, 0, 1], 1], [[1, 0, 1, 1, 0], 1],
  [[1, 0, 1, 0, 1], 1], [[1, 0, 0, 1, 1], 1],
  [[2, 2, 0, 0, 0], 2], [[2, 0, 2, 0, 0], 2], [[2, 0, 0, 2, 0], 2], [[2, 0, 0, 0, 2], 2],
  [[2, 1, 1, 0, 0], 2], [[2, 1, 0, 1, 0], 2], [[2, 1, 0, 0, 1], 2], [[2, 0, 1, 1, 0], 2],
  [[2, 0, 1, 0, 1], 2], [[2, 0, 0, 1, 1], 2], [[2, 1, 2, 0, 0], 2], [[2, 2, 1, 0, 0], 2],
  [[3, 1, 0, 0, 0], 1], [[3, 0, 1, 0, 0], 1], [[3, 0, 0, 1, 0], 1], [[3, 0, 0, 0, 1], 1],
  [[0, 3, 1, 0, 0], 3], [[0, 0, 3, 1, 0], 3], [[0, 0, 0, 3, 1], 3], [[0, 1, 0, 0, 3], 3],
  [[4, 0, 0, 0, 0], 0], [[4, 1, 0, 0, 0], 4], [[4, 0, 1, 0, 0], 4], [[4, 0, 0, 1, 0], 4],
  [[4, 0, 0, 0, 1], 4], [[0, 4, 0, 0, 0], 4], [[0, 0, 4, 0, 0], 4], [[0, 0, 0, 4, 0], 4],
  [[0, 0, 0, 0, 4], 4],
  [[5, 0, 0, 0, 0], 0], [[5, 1, 0, 0, 0], 5], [[5, 0, 1, 0, 0], 5], [[0, 5, 0, 0, 0], 5],
  [[0, 0, 5, 0, 0], 5],
  [[6, 0, 0, 0, 0], 0], [[6, 1, 0, 0, 0], 6], [[0, 6, 0, 0, 0], 6], [[0, 0, 6, 0, 0], 6],
  [[7, 0, 0, 0, 0], 0], [[7, 1, 0, 0, 0], 7], [[0, 7, 0, 0, 0], 7],
  [[1, 2, 0, 0, 0], 1], [[1, 0, 2, 0, 0], 1], [[1, 0, 0, 2, 0], 1], [[1, 0, 0, 0, 2], 1],
  [[2, 3, 0, 0, 0], 2], [[2, 0, 3, 0, 0], 2], [[3, 2, 0, 0, 0], 3], [[3, 0, 2, 0, 0], 3],
];
const langton = tableRule(() => new Map(LANGTON.map(([p, r]) => [key(...p), r])), c => c);

// --- von_neumann.py (simplified constructor): no rule -> states above 5 decay by one --------------------------------
function buildVonNeumann() {
  const t = new Map();
  t.set(key(0, 0, 0, 0, 0), 0);
  for (let n = 0; n < 5; n++) for (let e = 0; e < 5; e++) for (let s = 0; s < 5; s++) for (let w = 0; w < 5; w++) {
    if (n > 0 || e > 0 || s > 0 || w > 0) t.set(key(1, n, e, s, w), Math.min(n + e + s + w, 4));
  }
  t.set(key(0, 5, 0, 0, 0), 1); t.set(key(0, 0, 5, 0, 0), 1); t.set(key(0, 0, 0, 5, 0), 1); t.set(key(0, 0, 0, 0, 5), 1);
  for (let n = 0; n < 5; n++) for (let e = 0; e < 5; e++) if (n > 0 && e > 0) t.set(key(6, n, e, 0, 0), 4);
  return t;
}
const vonNeumann = tableRule(buildVonNeumann, c => (c > 5 ? Math.max(0, c - 1) : c));

// --- von_neumann_full.py: the same _add_* calls in the same order; no rule -> states 1..14 decay by one --------------
function buildVonNeumannFull() {
  const t = new Map(), set = (p, r) => t.set(key(...p), r);
  set([0, 0, 0, 0, 0], 0);                                                     // _add_quiescent_rules
  for (let e = 0; e < 29; e++) for (let w = 0; w < 29; w++) { set([0, 1, e, 0, w], 1); set([1, 1, e, 0, w], 1); }
  for (let n = 0; n < 29; n++) for (let s = 0; s < 29; s++) { set([0, n, 0, s, 2], 2); set([2, n, 0, s, 2], 2); }
  for (let e = 0; e < 29; e++) for (let w = 0; w < 29; w++) { set([0, 0, e, 3, w], 3); set([3, 0, e, 3, w], 3); }
  for (let n = 0; n < 29; n++) for (let s = 0; s < 29; s++) { set([0, n, 4, s, 0], 4); set([4, n, 4, s, 0], 4); }
  set([1, 0, 0, 1, 0], 1);
  set([1, 0, 0, 1, 0], 1); set([2, 0, 0, 0, 2], 2); set([3, 3, 0, 0, 0], 3); set([4, 0, 4, 0, 0], 4);
  for (const ns of [1, 3]) for (const ew of [2, 4]) {                          // _add_confluent_rules
    set([9, ns, ew, 0, 0], 1); set([9, 0, ew, ns, 0], 1); set([9, ns, 0, 0, ew], 1); set([9, 0, 0, ns, ew], 1);
  }
  set([10, 1, 2, 0, 0], 2); set([11, 0, 2, 3, 0], 3); set([12, 0, 0, 3, 4], 4);
  const oc = 13, od = 14;                                                      // _add_construction_rules
  set([0, oc, 0, 0, 0], 1); set([0, 0, oc, 0, 0], 2); set([0, 0, 0, oc, 0], 3); set([0, 0, 0, 0, oc], 4);
  for (let g = 1; g < 5; g++) { set([oc, g, 0, 0, 0], oc); set([oc, 0, g, 0, 0], oc); set([oc, 0, 0, g, 0], oc); set([oc, 0, 0, 0, g], oc); }
  for (let c = 1; c < 29; c++) {                                               // _add_destruction_rules
    set([c, od, 0, 0, 0], 0); set([c, 0, od, 0, 0], 0); set([c, 0, 0, od, 0], 0); set([c, 0, 0, 0, od], 0);
  }
  for (let g = 1; g < 5; g++) { set([5, g, 0, 0, 0], 1); set([5, 0, g, 0, 0], 1); set([5, 0, 0, g, 0], 1); set([5, 0, 0, 0, g], 1); }
  for (let g = 1; g < 5; g++) { set([6, g, 0, 0, 0], 2); set([7, g, 0, 0, 0], 3); set([8, g, 0, 0, 0], 4); }
  for (let st = 15; st < 20; st++) for (let n = 0; n < 29; n++) set([st, n, 0, 0, 0], st);   // _add_special_rules
  for (let ss = 20; ss < 25; ss++) for (let g = 1; g < 5; g++) set([ss, g, 0, 0, 0], 15 + (ss - 20));
  set([25, 1, 0, 0, 0], 26); set([26, 2, 0, 0, 0], 27); set([27, 3, 0, 0, 0], 28); set([28, 4, 0, 0, 0], 25);
  return t;
}
const vonNeumannFull = tableRule(buildVonNeumannFull, c => (c > 0 && c <= 14 ? Math.max(0, c - 1) : c));

export const TABLE_RULES = { langton_loop: langton, von_neumann: vonNeumann, von_neumann_full: vonNeumannFull };
