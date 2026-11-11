"""Rule catalogue, preset patterns and Python stepping for the web API, all read from the real plugin registry.

Nothing here re-implements a rule: metadata, descriptions, colour maps and patterns come from `plugins.PLUGIN_REGISTRY`
and every step is the plugin's own `step()`. The browser engine (static/ca_engine.js) is checked against `run()`.
"""
import inspect
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins import PLUGIN_CATEGORIES, PLUGIN_INFO, PLUGIN_REGISTRY  # noqa: E402
from plugins.cyclic_ca import CyclicCA  # noqa: E402

from web.grid_codec import decode, encode  # noqa: E402

ELEMENTARY = {"rule_30", "rule_110", "rule_90"}
DEFAULT_SIZE = 100          # grid size for presets whose plugin gives no recommended_size
PATTERN_SEED = 0            # numpy seed for presets that use np.random (random soups, spiral seeds)
MAX_WORK = 1_000_000        # cap on width * height * steps for one /run request (pure-Python loops)


def _defaults(fn):
    return {k: p.default for k, p in inspect.signature(fn).parameters.items() if p.default is not inspect.Parameter.empty}


def rule_params(key: str) -> list:
    """Editable rule parameters, with defaults taken from the Python constructors."""
    if key == "cyclic_ca":
        d = _defaults(CyclicCA.__init__)
        colours = len(PLUGIN_REGISTRY[key].get_colormap())
        return [
            {"name": "num_states", "label": "Number of states", "min": 2, "max": colours, "default": d["num_states"]},
            {"name": "threshold", "label": "Threshold (neighbours in next state)", "min": 1, "max": 8,
             "default": d["threshold"]},
        ]
    if key in ELEMENTARY:
        rule = PLUGIN_REGISTRY[key].create_automaton(8, 8).rule_number
        return [{"name": "rule", "label": "Wolfram rule number", "min": 0, "max": 255, "default": rule}]
    return []


def _automaton_class(key: str):
    return type(PLUGIN_REGISTRY[key].create_automaton(32, 32))


def _pattern_list(key: str) -> list:
    out = []
    for name, info in PLUGIN_REGISTRY[key].get_default_patterns().items():
        size = info.get("recommended_size") or (DEFAULT_SIZE, DEFAULT_SIZE)
        out.append({"name": name, "description": info.get("description", ""),
                    "parameters": info.get("parameters", {}), "size": list(size)})
    return out


def rule_entry(key: str) -> dict:
    plugin = PLUGIN_REGISTRY[key]
    meta = plugin.get_metadata().to_dict()
    cats = [c for c, keys in PLUGIN_CATEGORIES.items() if key in keys]
    return {
        "key": key, "engine": "elementary" if key in ELEMENTARY else key,
        **meta, "info": PLUGIN_INFO.get(key, ""), "categories": cats,
        "doc": inspect.getdoc(_automaton_class(key)) or "",
        "module_doc": inspect.getdoc(sys.modules[plugin.__module__]) or "",
        "colormap": [c.lower() for c in plugin.get_colormap()],
        "params": rule_params(key), "patterns": _pattern_list(key),
    }


def catalogue() -> list:
    """Every registered automaton, in registry order."""
    return [rule_entry(k) for k in PLUGIN_REGISTRY]


def _ctor_kwargs(key: str, params: dict) -> dict:
    if key == "cyclic_ca":
        return {k: int(params[k]) for k in ("num_states", "threshold") if k in params}
    return {}


def make_pattern(key: str, name: str, width: int, height: int, params: dict | None = None, seed: int = PATTERN_SEED):
    """Build a named preset with the plugin's own create_automaton (numpy seeded for random presets)."""
    params = dict(params or {})
    np.random.seed(seed)
    automaton = PLUGIN_REGISTRY[key].create_automaton(width, height, pattern=name, **params)
    return automaton


def patterns(key: str) -> dict:
    """All presets of one automaton as encoded grids at their recommended size."""
    out = []
    for p in _pattern_list(key):
        w, h = p["size"]
        a = make_pattern(key, p["name"], w, h, p["parameters"])
        out.append({**p, "width": w, "height": h, "cells": encode(a.grid),
                    "params": {k: v for k, v in p["parameters"].items() if k in ("num_states", "threshold")},
                    "row": int(getattr(a, "current_row", 0))})
    return {"key": key, "patterns": out}


def build_automaton(key: str, width: int, height: int, params: dict | None = None):
    """A fresh automaton of this kind with the given rule parameters (grid contents are replaced by the caller)."""
    params = params or {}
    a = PLUGIN_REGISTRY[key].create_automaton(width, height, **_ctor_kwargs(key, params))
    if key in ELEMENTARY and "rule" in params:
        a.rule_number = int(params["rule"])
        a.rule_table = a._generate_rule_table(a.rule_number)
    return a


def run(key: str, cells: str, width: int, height: int, steps: int, params: dict | None = None, row: int = 0) -> dict:
    """Step a grid with the real Python plugin and return the encoded result."""
    if key not in PLUGIN_REGISTRY:
        raise KeyError(key)
    if width * height * max(steps, 1) > MAX_WORK:
        raise ValueError(f"too much work: width*height*steps must be <= {MAX_WORK}")
    a = build_automaton(key, width, height, params)
    grid = decode(cells, width, height)
    if grid.max(initial=0) >= a.metadata.num_states:
        raise ValueError("cell state out of range for this automaton")
    a.import_grid(grid)
    a.generation = 0
    if hasattr(a, "current_row"):
        a.current_row = int(row)
    for _ in range(steps):
        a.step()
    stats = a.compute_statistics()
    return {"rule": key, "width": width, "height": height, "generation": a.generation,
            "row": int(getattr(a, "current_row", 0)), "cells": encode(a.grid),
            "stats": {k: stats[k] for k in ("active_cells", "density", "entropy", "unique_states")}}

