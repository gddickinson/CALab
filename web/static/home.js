// Home page: hero, live counts from /api/info, one card per registered automaton, and how the site is built.
import { route, api, app, esc, list, tags, isStatic } from './core.js';
import { isPorted } from './ca_engine.js';
import { stateColors } from './lab_view.js';

export const swatches = (colors, n) =>
  `<div class="swatches" aria-hidden="true">${list(stateColors(colors, n), c => `<i style="background:${esc(c)}"></i>`)}</div>`;

route('home', async () => {
  const [info, rules] = await Promise.all([api('/info'), api('/rules')]);
  const ported = rules.filter(r => isPorted(r.key)).length;
  app().innerHTML = `
  <section class="hero">
    <p class="kicker">Cells · Neighbours · Rules</p>
    <h1 class="glow">CALab</h1>
    <p class="lead">The Cellular Automata Laboratory: a modular, plugin-based framework for creating and visualising cellular
    automata, from Conway's Game of Life to von Neumann's 29-state universal constructor. Every automaton in the
    plugin registry runs here, in your browser: press play, draw on the grid, change the rule.</p>
    <a class="btn" href="#/lab/game_of_life">Open the lab</a><a class="btn alt" href="#/automata">Browse the automata</a>
  </section>
  <div class="tiles">
    <div class="tile"><b>${info.automata}</b><span>registered automata</span></div>
    <div class="tile"><b>${info.patterns}</b><span>preset patterns</span></div>
    <div class="tile"><b>${info.categories}</b><span>categories</span></div>
    <div class="tile"><b>${info.max_states}</b><span>states in the largest rule</span></div>
    <div class="tile"><b>${ported}/${rules.length}</b><span>ported to the browser</span></div>
  </div>
  <h2>Automata</h2>
  <div class="grid cards-ca">${list(rules, r => `
    <a class="card" href="#/lab/${esc(r.key)}">
      <b>${esc(r.name)}</b><small>${esc(r.info || r.description)}</small>
      <div>${tags([`${r.num_states} states`, r.neighborhood_type.replace('_', ' ')], 'c')}${tags(r.categories, 'b')}</div>
      ${swatches(r.colormap, r.num_states)}
    </a>`)}</div>
  <h2>How this site works</h2>
  <div class="flow">
    <div>The rule catalogue, colour maps and every preset grid are read from CALab's Python plugin registry
      (<code>plugins.PLUGIN_REGISTRY</code>) and each plugin's own <code>create_automaton()</code>.</div>
    <div>Each rule's <code>step()</code> is ported to a small JavaScript engine, so the grid runs at full speed in the browser
      with no server.</div>
    <div>Node tests replay start grids produced by the Python code (every preset, random soups over all states, rule
      variants) and require the JS engine to reach exactly the same grid, cell for cell.</div>
    <div>${isStatic() ? 'Run the app locally (see About) and' : 'Here, in the local app, you can'} press "Check with Python"
      in the lab to step your own grid through the real Python plugin and compare.</div>
  </div>`;
});
