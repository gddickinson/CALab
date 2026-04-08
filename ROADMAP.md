# CALab -- Cellular Automata Laboratory -- Roadmap

## Current State
A comprehensive cellular automata framework with a modular plugin system. Core engine (`core/automaton_base.py`, `rule_engine.py`, `simulator.py`), 9 plugins (Game of Life, Langton's Loop, WireWorld, Brian's Brain, Von Neumann, Elementary CA, Cyclic CA, Life Variants, Seeds), and a rich PyQt GUI with simulation, rule editor, pattern editor, diagnostics, documentation, and sonification tabs. Has a `gui/old/` directory with previous GUI versions still present. Diagnostic and test scripts exist at the root level.

## Short-term Improvements
- [x] Remove `gui/old/` directory -- contains `main_window_OLD.py` and duplicated tab files from a previous iteration
- [x] Move root-level scripts (`demo.py`, `demo_all.py`, `test_plugins.py`, `list_plugins.py`, `diagnose_plugins.py`) into a `scripts/` directory
- [x] Add proper pytest tests replacing `test_plugins.py` -- test each plugin's `create_automaton()` and rule application
- [x] Add `requirements.txt` listing PyQt5, numpy, matplotlib
- [ ] Complete the Langton's Loop rule table -- README notes only a subset of 219 rules is implemented
- [x] Add input validation in `core/simulator.py` for grid dimensions and step counts
- [ ] Document the plugin API with a tutorial in `docs/` showing how to create a new automaton

## Feature Enhancements
- [ ] Add hexagonal grid support in `core/automaton_base.py` (currently only rectangular grids)
- [ ] Implement 1D elementary CA spacetime diagram visualization
- [ ] Add animation export (GIF/MP4) from the simulation tab
- [ ] Implement undo/redo in the pattern editor
- [ ] Add GPU acceleration using CuPy for large grid simulations
- [ ] Complete the sonification tab -- map automaton states to audio parameters
- [ ] Add a "gallery" of famous patterns (gliders, spaceships, oscillators) loadable from `data/patterns/`
- [ ] Implement multi-grid comparison view for side-by-side simulations

## Long-term Vision
- [ ] Add 3D cellular automata with VTK or vispy-based 3D visualization
- [ ] Implement machine learning rule discovery -- evolve rules with genetic algorithms
- [ ] Build a web version for educational use (WebAssembly or server-rendered)
- [ ] Add network-based automata (graph CA, not just grid-based)
- [ ] Create an API for programmatic batch simulation and parameter sweeps
- [ ] Publish as a pip-installable package for the complexity science community

## Technical Debt
- [x] `gui/old/` contains 5 deprecated files that inflate the codebase -- delete after confirming no unique code
- [ ] `plugins/von_neumann.py` and `plugins/von_neumann_full.py` overlap -- merge or clearly differentiate
- [x] `plugins/__init__.py` plugin registration may need updating as new plugins were added
- [x] Root-level diagnostic scripts (`diagnose_plugins.py`, `list_plugins.py`) duplicate functionality
- [x] `gui/sonification_tab.py` may be incomplete or experimental -- document status
- [ ] No CI/CD pipeline for automated testing across platforms
