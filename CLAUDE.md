# Claude collaboration notes for `CALab`

This project was built with substantial assistance from **Claude (Anthropic)**, primarily via **Claude Code**.

## Global preferences

George's global Claude preferences live in `~/.claude/CLAUDE.md` and apply to every project. Highlights:

- Keep all source files under 500 lines; split into focused modules if approaching that limit.
- For Python projects, maintain an `INTERFACE.md` at the project root as a navigation map of modules, classes, and key functions.
- Prefer many small, focused files over fewer large ones.
- Group related functionality; extract reusable logic into utility modules.

## Project navigation

See [`INTERFACE.md`](./INTERFACE.md) for a navigation map of this repository's modules and how they connect. Read `INTERFACE.md` before opening individual source files.

## Working with Claude on this repo

When directing Claude Code on this codebase, follow the global rules above, prefer making targeted edits via the `Edit` tool over rewriting whole files, and update `INTERFACE.md` whenever the project structure changes.

Project-specific conventions, build instructions, and lab-specific notes should be added below as the project evolves.

## Web interface (`web/`)

- `python run_web.py` (port 8103); static site via `python scripts/build_static.py`; tests `python -m pytest -q tests/test_web.py`.
- The browser engine (`web/static/ca_engine.js` + `ca_rules_*.js`) mirrors each plugin's `step()`. If you change a
  plugin's rules or presets, run `python scripts/make_engine_fixtures.py` and update the JS port until
  `node web/static/ca_engine.test.mjs` passes again.
