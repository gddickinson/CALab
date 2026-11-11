// Automata catalogue: every plugin in the registry with its metadata, state colours, presets (each opens the lab)
// and the documentation text from its Python source.
import { route, api, app, esc, list, tags } from './core.js';
import { swatches } from './home.js';

route('automata', async (args, query) => {
  const rules = await api('/rules');
  const cats = [...new Set(rules.flatMap(r => r.categories))];
  const only = query.category;
  const shown = only ? rules.filter(r => r.categories.includes(only)) : rules;
  app().innerHTML = `
  <p class="kicker">Catalogue</p>
  <h1>Automata</h1>
  <p class="lead">The ${rules.length} automata registered in <code>plugins.PLUGIN_REGISTRY</code>, with the descriptions, state
  counts, colour maps and preset patterns their plugins define. Pick a preset to open it in the lab.</p>
  <div class="toc" role="group" aria-label="Filter by category">
    <a class="tag ${only ? '' : 'a'}" href="#/automata">All</a>
    ${list(cats, c => `<a class="tag ${c === only ? 'a' : ''}" href="#/automata?category=${encodeURIComponent(c)}">${esc(c)}</a>`)}
  </div>
  ${list(shown, r => `
  <section class="panel auto" id="a-${esc(r.key)}">
    <h2>${esc(r.name)}</h2>
    <p class="mute">${esc(r.info)}. ${esc(r.description)}. <span class="small">Author: ${esc(r.author)} · plugin v${esc(r.version)}</span></p>
    <div>${tags([`${r.num_states} states`, `${r.neighborhood_type.replace('_', ' ')} neighbourhood`,
      r.is_totalistic ? 'totalistic' : 'rule table / custom'], 'c')}${tags(r.categories, 'b')}
      ${r.params.length ? tags(r.params.map(p => `parameter: ${p.name} (default ${p.default})`), 'a') : ''}</div>
    ${swatches(r.colormap, r.num_states)}
    <h3>Presets</h3>
    <div class="pat">${list(r.patterns, p => `<a href="#/lab/${esc(r.key)}?pattern=${encodeURIComponent(p.name)}">
      <b>${esc(p.name.replace(/_/g, ' '))}</b>${esc(p.description)} <span class="mute">· ${p.size[0]} x ${p.size[1]}</span></a>`)}</div>
    <details class="src"><summary>Documentation from the plugin source</summary>
      <pre class="doc">${esc(r.module_doc)}</pre><pre class="doc">${esc(r.doc)}</pre></details>
  </section>`)}`;
});
