// About page: what CALab is, how to run the desktop app, the web app and the static site, and credits (README).
import { route, app, isStatic } from './core.js';

route('about', () => {
  app().innerHTML = `
  <p class="kicker">About</p>
  <h1>CALab</h1>
  <p class="lead">CALab, the Cellular Automata Laboratory, is a modular framework for creating and visualising cellular
  automata simulations. Each automaton is a plugin implementing <code>PluginInterface</code> (metadata, a factory, default
  patterns and a colour map), registered in <code>plugins.PLUGIN_REGISTRY</code>; a core engine provides the base classes,
  rule handling and a threaded simulator, and a PyQt5 desktop GUI wraps it all.</p>

  <h2>This web version</h2>
  <p>The site is a working lab: all thirteen registered automata are ported to a small JavaScript engine
  (<code>ca_engine.js</code> and three rule-family modules) that mirrors each plugin's <code>step()</code>, including its edge
  wrap-around and fall-back behaviour. The catalogue and every preset grid are produced by the Python plugins themselves and
  exported as JSON. Node tests require the JS engine to reproduce grids computed by the Python code exactly, and the local
  app can step any grid you draw through the real Python plugin to compare.</p>
  <div class="callout">The plugins are run exactly as written, including their simplifications: Langton's Loop uses what its
  source calls "a working subset" of the 219-rule table, <code>von_neumann</code> is described in its source as a simplified
  implementation, and both von Neumann plugins fall back to decaying a cell's state when no rule in their table matches.</div>
  ${isStatic() ? '<p class="static-note">You are on the static site: everything runs in your browser; only the "Check with Python" button needs the local app.</p>' : ''}

  <h2>Run the desktop app</h2>
  <pre>pip install PyQt5 numpy matplotlib
python main.py</pre>
  <p>The desktop GUI has simulation, rule editor, pattern editor, diagnostics, documentation and sonification tabs.
  The core also works without the GUI: <code>python scripts/demo.py</code>.</p>

  <h2>Run the web app</h2>
  <pre>pip install -r requirements-web.txt
python run_web.py          # http://127.0.0.1:8103</pre>
  <p>Build the static site (what GitHub Pages serves) with <code>python scripts/build_static.py</code>; run the web tests with
  <code>python -m pytest -q tests/test_web.py</code> (includes the node engine test).</p>

  <h2>Credits</h2>
  <ul>
    <li>John von Neumann: original self-replicating automata concept</li>
    <li>Chris Langton: simplified self-replicating loops</li>
    <li>John Conway: Game of Life</li>
    <li>Rule authors named in the plugins: Brian Silverman (Brian's Brain, Seeds, WireWorld), Nathan Thompson (Day and Night,
      HighLife), Stephen Wolfram (elementary CA), David Griffeath (cyclic CA)</li>
  </ul>
  <p>MIT licence. Built with AI assistance from <a href="https://claude.com/" target="_blank" rel="noopener">Claude (Anthropic)</a>.
  Source: <a href="https://github.com/gddickinson/CALab" target="_blank" rel="noopener">github.com/gddickinson/CALab</a>.</p>`;
});
