// Moore-neighbourhood automata (8 neighbours, edges wrap), ported line by line from the Python plugins:
// game_of_life.py, life_variants.py (Day and Night, HighLife), seeds.py, brians_brain.py, wireworld.py, cyclic_ca.py.
// step(src, dst, w, h, params) fills dst; src is never modified.

// Sum of the 8 neighbour *values* (the Life-like plugins add grid values, not a count of live cells).
function mooreSum(src, w, h, x, y) {
  const ym = ((y - 1 + h) % h) * w, y0 = y * w, yp = ((y + 1) % h) * w;
  const xm = (x - 1 + w) % w, xp = (x + 1) % w;
  return src[ym + xm] + src[ym + x] + src[ym + xp] + src[y0 + xm] + src[y0 + xp] + src[yp + xm] + src[yp + x] + src[yp + xp];
}

// Number of the 8 neighbours equal to v.
function mooreCount(src, w, h, x, y, v) {
  const ym = ((y - 1 + h) % h) * w, y0 = y * w, yp = ((y + 1) % h) * w;
  const xm = (x - 1 + w) % w, xp = (x + 1) % w;
  return (src[ym + xm] === v) + (src[ym + x] === v) + (src[ym + xp] === v) + (src[y0 + xm] === v) +
    (src[y0 + xp] === v) + (src[yp + xm] === v) + (src[yp + x] === v) + (src[yp + xp] === v);
}

function each(w, h, fn) {
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) fn(x, y, y * w + x);
}

// Conway: an alive cell (== 1) dies with < 2 or > 3; any other cell is born with exactly 3.
const gameOfLife = {
  step(src, dst, w, h) {
    each(w, h, (x, y, i) => {
      const n = mooreSum(src, w, h, x, y), c = src[i];
      dst[i] = c;
      if (c === 1) { if (n < 2 || n > 3) dst[i] = 0; } else if (n === 3) dst[i] = 1;
    });
  },
};

// Life-like rule where 0 is dead and any other value alive (DayAndNight / HighLife plugins).
function birthSurvive(birth, survive) {
  const B = new Set(birth), S = new Set(survive);
  return {
    birth, survive,
    step(src, dst, w, h) {
      each(w, h, (x, y, i) => {
        const n = mooreSum(src, w, h, x, y), c = src[i];
        dst[i] = c;
        if (c === 0) { if (B.has(n)) dst[i] = 1; } else if (!S.has(n)) dst[i] = 0;
      });
    },
  };
}

// Seeds (B2/S): every cell dies; a 0 cell with neighbour sum 2 is born.
const seeds = {
  step(src, dst, w, h) {
    each(w, h, (x, y, i) => { dst[i] = (src[i] === 0 && mooreSum(src, w, h, x, y) === 2) ? 1 : 0; });
  },
};

// Brian's Brain: off -> on with exactly 2 on neighbours; on -> dying; dying -> off.
const briansBrain = {
  step(src, dst, w, h) {
    each(w, h, (x, y, i) => {
      const c = src[i];
      dst[i] = c;
      if (c === 0) { if (mooreCount(src, w, h, x, y, 1) === 2) dst[i] = 1; } else if (c === 1) dst[i] = 2; else if (c === 2) dst[i] = 0;
    });
  },
};

// WireWorld: head -> tail -> wire; wire -> head with 1 or 2 heads around.
const wireworld = {
  step(src, dst, w, h) {
    each(w, h, (x, y, i) => {
      const c = src[i];
      dst[i] = c;
      if (c === 2) dst[i] = 3;
      else if (c === 3) dst[i] = 1;
      else if (c === 1) { const k = mooreCount(src, w, h, x, y, 2); if (k === 1 || k === 2) dst[i] = 2; }
    });
  },
};

// Cyclic CA: advance to (c + 1) % N when at least T neighbours are already in that state.
const cyclic = {
  step(src, dst, w, h, p = {}) {
    const N = p.num_states ?? 3, T = p.threshold ?? 3;   // CyclicCA DEFAULT_NUM_STATES / DEFAULT_THRESHOLD
    each(w, h, (x, y, i) => {
      const next = (src[i] + 1) % N;
      dst[i] = mooreCount(src, w, h, x, y, next) >= T ? next : src[i];
    });
  },
};

export const MOORE_RULES = {
  game_of_life: gameOfLife,
  day_and_night: birthSurvive([3, 6, 7, 8], [3, 4, 6, 7, 8]),
  highlife: birthSurvive([3, 6], [2, 3]),
  seeds,
  brians_brain: briansBrain,
  wireworld,
  cyclic_ca: cyclic,
};
