// Elementary (1D, Wolfram) CA drawn as a space-time diagram, ported from plugins/elementary_ca.py ElementaryCA:
// each step computes row `current_row + 1` from row `current_row` (left/right wrap) and stops once the last row is
// filled. Every other row is left exactly as it is.

export function ruleTable(rule) {
  // pattern index (left << 2 | centre << 1 | right) -> new state, i.e. bit i of the rule number
  return Array.from({ length: 8 }, (_, i) => (rule >> i) & 1);
}

export const ELEMENTARY = {
  step(src, dst, w, h, p = {}, s) {
    if (s.row >= h - 1) return false;            // filled the grid: Python returns without counting a generation
    dst.set(src);
    const t = ruleTable(p.rule ?? 30), r = s.row * w, nr = r + w;
    for (let x = 0; x < w; x++) {
      const l = src[r + (x - 1 + w) % w], c = src[r + x], rt = src[r + (x + 1) % w];
      const v = t[(l << 2) | (c << 1) | rt];
      if (v === undefined) throw new Error('elementary CA cells must be 0 or 1');
      dst[nr + x] = v;
    }
    s.row += 1;
    return true;
  },
};
