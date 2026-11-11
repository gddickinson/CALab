// Node test: the JS engine must reproduce, cell for cell, the grids the Python plugins reach from the same start.
// Fixtures: tests/fixtures/ca_engine_fixtures.json (python scripts/make_engine_fixtures.py). Run: node ca_engine.test.mjs
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { RULES, makeState, run, step, decode, encode, stats, isPorted } from './ca_engine.js';
import { ruleTable } from './ca_rules_1d.js';

const here = fileURLToPath(new URL('.', import.meta.url));
const { cases } = JSON.parse(readFileSync(here + '../../tests/fixtures/ca_engine_fixtures.json', 'utf8'));
let fails = 0, checks = 0;
const ok = (cond, msg) => { checks++; if (!cond) { fails++; console.error('FAIL', msg); } };

// 1. every fixture case
const rulesSeen = new Set();
for (const c of cases) {
  rulesSeen.add(c.rule);
  const s = makeState(c.width, c.height, decode(c.start, c.width, c.height), c.row);
  run(c.rule, s, c.params, c.steps);
  const got = encode(s.cells);
  let diff = 0;
  for (let i = 0; i < got.length; i++) diff += got[i] !== c.end[i];
  ok(diff === 0, `${c.rule} / ${c.label}: ${diff} cells differ after ${c.steps} steps`);
  ok(s.gen === c.generation, `${c.rule} / ${c.label}: generation ${s.gen} != ${c.generation}`);
  ok(s.row === c.end_row, `${c.rule} / ${c.label}: row ${s.row} != ${c.end_row}`);
}

// 2. every registered automaton has a JS port and at least one fixture
for (const k of rulesSeen) ok(isPorted(k), `no JS engine for ${k}`);
ok(rulesSeen.size === 13, `expected fixtures for all 13 registered automata, got ${rulesSeen.size}`);

// 3. small hand checks
ok(ruleTable(30).join('') === '01111000', 'rule 30 lookup table');
ok(encode(decode('0a1s', 2, 2)) === '0a1s', 'codec round trip');
const blinker = makeState(5, 5, decode('0000000000011100000000000', 5, 5));
step('game_of_life', blinker); step('game_of_life', blinker);
ok(encode(blinker.cells) === '0000000000011100000000000', 'blinker has period 2');
const st = stats(makeState(2, 2, [0, 1, 1, 0]));
ok(st.active_cells === 2 && Math.abs(st.entropy - 1) < 1e-6, 'stats: density and entropy');
ok(Object.keys(RULES).length === 11, 'eleven rule engines (rule_30/110/90 share the elementary engine)');

console.log(`${checks - fails}/${checks} checks passed (${cases.length} Python fixture cases, ${rulesSeen.size} automata)`);
process.exit(fails ? 1 : 0);
