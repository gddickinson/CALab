"""Regression tests for bugs fixed in the plugins and core (see SESSION_LOG.md, 2026-11-11)."""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from plugins.cyclic_ca import CyclicCA, CyclicCAPlugin  # noqa: E402


def _activity_after(automaton, steps):
    """Number of cells that change in the step after `steps` steps."""
    for _ in range(steps):
        automaton.step()
    before = automaton.grid.copy()
    automaton.step()
    return int((automaton.grid != before).sum())


@pytest.mark.parametrize("pattern", list(CyclicCAPlugin.get_default_patterns()))
def test_cyclic_presets_keep_moving(pattern):
    """Every cyclic preset, with its own parameters, is still active after 300 steps (they used to freeze)."""
    np.random.seed(0)
    params = CyclicCAPlugin.get_default_patterns()[pattern]["parameters"]
    a = CyclicCAPlugin.create_automaton(36, 36, pattern=pattern, **params)
    assert _activity_after(a, 300) > 0


def test_cyclic_defaults_form_spirals_from_random():
    """The default rule (no parameters given) stays active from a random start; the old 14/3 default froze."""
    np.random.seed(1)
    a = CyclicCAPlugin.create_automaton(36, 36)
    assert (a.num_states_ca, a.threshold) == (3, 3)
    assert _activity_after(a, 300) > 0
    old = CyclicCA(36, 36, num_states=14, threshold=3)
    np.random.seed(1)
    old.initialize_pattern('random')
    assert _activity_after(old, 300) == 0   # documents why the default changed


def test_cyclic_parameters_still_adjustable():
    a = CyclicCAPlugin.create_automaton(30, 30, num_states=9, threshold=2)
    assert (a.num_states_ca, a.threshold, a.metadata.num_states) == (9, 2, 9)


@pytest.mark.parametrize("w,h", [(150, 150), (30, 50), (50, 30)])
def test_cyclic_domains_cover_whole_grid(w, h):
    a = CyclicCA(w, h, num_states=4, threshold=3)
    a.initialize_pattern('domains')
    # bottom-right block is (i, j) = (3, 3) -> state (6 * 4 // 4) % 4 == 2; no stray state-0 strips
    assert a.grid[-1, -1] == 2 and a.grid[-1, 0] == 3 and a.grid[0, -1] == 3


# --- PluginInterface default colour map ----------------------------------------------------------------------------
def test_default_colormap_uses_plugin_metadata():
    from core.automaton_base import AutomatonMetadata, NeighborhoodType, PluginInterface

    class ThreeState(PluginInterface):
        @staticmethod
        def get_metadata():
            return AutomatonMetadata("t", "d", "a", "1", 3, NeighborhoodType.MOORE)

        @staticmethod
        def create_automaton(width, height, **kwargs):
            return None

        @staticmethod
        def get_default_patterns():
            return {}

    assert ThreeState.get_colormap() == ['#000000', '#808080', '#ffffff']   # used to raise AttributeError

