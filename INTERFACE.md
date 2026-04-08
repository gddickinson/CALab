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
  tests/               -- Pytest test suite
    test_plugins.py    -- Tests for all 13 plugins (metadata, creation, simulation, patterns, colormaps)
    test_simulator.py  -- Tests for SimulationEngine and BatchSimulation
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

## Plugin API

Each plugin implements `PluginInterface` with:
- `get_metadata()` -> AutomatonMetadata
- `create_automaton(width, height, **kwargs)` -> CellularAutomaton
- `get_default_patterns()` -> dict
- `get_colormap()` -> list of hex colors
