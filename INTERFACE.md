# CALab Interface Map

## Project Structure

```
CALab/
  main.py              -- GUI application entry point
  core/                -- Core simulation engine
    automaton_base.py  -- Base classes: CellularAutomaton, PluginInterface, AutomatonMetadata
    rule_engine.py     -- Rule parsing and application
    simulator.py       -- SimulationEngine (threaded), BatchSimulation
  plugins/             -- Cellular automata implementations (13 total)
    __init__.py        -- Plugin registry (PLUGIN_REGISTRY), get_plugin(), list_plugins()
    game_of_life.py    -- GameOfLife, GameOfLifePlugin
    langton_loop.py    -- LangtonLoop, LangtonLoopPlugin
    wireworld.py       -- WireWorld, WireWorldPlugin
    brians_brain.py    -- BriansBrain, BriansBrainPlugin
    seeds.py           -- Seeds, SeedsPlugin
    elementary_ca.py   -- ElementaryCA + Rule30/Rule110/Rule90 plugins
    cyclic_ca.py       -- CyclicCA, CyclicCAPlugin
    life_variants.py   -- DayAndNight, HighLife + plugins
    von_neumann.py     -- VonNeumannConstructor (simplified, 29 states)
    von_neumann_full.py -- VonNeumannFull (complete rule table, 29 states)
  gui/                 -- PyQt5 GUI tabs
    main_window.py     -- MainWindow
    simulation_tab.py  -- Simulation display and controls
    rule_editor_tab.py -- Rule editing
    pattern_editor_tab.py -- Pattern editing
    diagnostics_tab.py -- Runtime diagnostics
    documentation_tab.py -- In-app docs
    sonification_tab.py -- Audio generation from patterns (complete, requires sounddevice)
    error_console.py   -- Error display widget
  utils/               -- Utility modules
  scripts/             -- Demo and diagnostic scripts
    demo.py            -- Core framework demo (non-GUI)
    demo_all.py        -- Interactive plugin showcase
    test_plugins.py    -- Legacy manual plugin test (replaced by tests/)
    list_plugins.py    -- List available plugins
    diagnose_plugins.py -- Plugin diagnostics
    build_static.py    -- export the static site (front end + every STATIC_ENDPOINTS GET as JSON) to site/
    screenshots.py     -- Playwright smoke test of routes (console errors, phone overflow) + README PNGs in docs/img
    make_engine_fixtures.py -- regenerate tests/fixtures/ca_engine_fixtures.json from the Python plugins
  tests/               -- Pytest test suite
    test_plugins.py    -- Tests for all 13 plugins (metadata, creation, simulation, patterns, colormaps)
    test_simulator.py  -- Tests for SimulationEngine and BatchSimulation
    test_regressions.py -- Regression tests for fixed bugs (cyclic CA defaults/presets, colormap, rule parsing, HighLife)
    test_web.py        -- Web API tests, static build, Python-vs-fixture cross-check, runs the node engine test
    fixtures/ca_engine_fixtures.json -- Python reference grids (start + after N steps) for the JS engine
  web/                 -- Web interface (FastAPI + static ES-module front end; also the GitHub Pages site)
    app.py             -- FastAPI app: /api/info, /api/rules, /api/patterns/{key}, POST /api/run; STATIC_ENDPOINTS
    catalogue.py       -- catalogue(), patterns(key), make_pattern(), build_automaton(), run() -- all via PLUGIN_REGISTRY
    grid_codec.py      -- encode()/decode(): base-36 one-char-per-cell grid text (shared with the JS engine)
    static/            -- front end (no build step)
      index.html, style.css (shared kit theme), style_app.css (CALab accents + page styles), core.js (kit router/helpers)
      main.js          -- registers lazy pages, footer mode, background
      static_api.js    -- answers api() from exported JSON on the static site (refuses POST /run)
      ca_engine.js     -- JS engine API: RULES, step(), run(), makeState(), decode()/encode(), stats(), resize()
      ca_rules_moore.js -- Life, Day and Night, HighLife, Seeds, Brian's Brain, WireWorld, cyclic CA
      ca_rules_table.js -- Langton's Loop, von Neumann (simplified), von Neumann (full) rule tables
      ca_rules_1d.js   -- elementary CA (rules 30/110/90 and any Wolfram rule)
      ca_engine.test.mjs -- node test: JS engine == Python fixtures
      home.js, lab.js (+ lab_view.js canvas/drawing, lab_check.js Python cross-check), automata.js, about.js, bg.js
  run_web.py           -- start the web app on 127.0.0.1:8103
  requirements-web.txt -- pinned web/test dependencies
  .github/workflows/pages.yml -- test, build and publish the static site on push to main
  _archive/            -- Archived old files
    gui_old/           -- Previous GUI iteration (deprecated)
  data/                -- Data files and patterns
  docs/                -- Documentation
```

## Key Entry Points

- `main.py` -- Launch the GUI application
- `plugins.get_plugin(name)` -- Get a plugin by name
- `plugins.PLUGIN_REGISTRY` -- Dict of all registered plugins
- `core.simulator.SimulationEngine` -- Run simulations programmatically
- `core.simulator.BatchSimulation` -- Run parameter sweeps
- `run_web.py` -- Launch the web app (imports `web.app:app`; repo root on sys.path, like tests/ and main.py)

## Web interface data flow

`plugins.PLUGIN_REGISTRY` -> `web/catalogue.py` (metadata, docstrings, colour maps, preset grids built by each plugin's
`create_automaton`, stepping via the plugin's own `step()`) -> `web/app.py` JSON API -> `scripts/build_static.py` writes
the GETs to `site/api/*.json` -> the front end loads them through `core.api()` (server) or `static_api.js` (static site),
and steps grids with `ca_engine.js`. `scripts/make_engine_fixtures.py` records Python results that `ca_engine.test.mjs`
(JS) and `tests/test_web.py` (Python API) both have to reproduce.

## Plugin API

Each plugin implements `PluginInterface` with:
- `get_metadata()` -> AutomatonMetadata
- `create_automaton(width, height, **kwargs)` -> CellularAutomaton
- `get_default_patterns()` -> dict
- `get_colormap()` -> list of hex colors
