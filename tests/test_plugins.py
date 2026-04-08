"""
Pytest tests for all CALab plugins.

Tests each plugin's create_automaton(), step(), compute_statistics(),
colormap, patterns, and metadata.
"""

import sys
import os
import pytest
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from plugins import PLUGIN_REGISTRY, list_plugins, get_plugin


@pytest.fixture(params=list(PLUGIN_REGISTRY.keys()))
def plugin_name(request):
    """Parametrize over all registered plugins."""
    return request.param


@pytest.fixture
def plugin(plugin_name):
    """Get a plugin class by name."""
    return PLUGIN_REGISTRY[plugin_name]


class TestPluginMetadata:
    """Test that plugin metadata is well-formed."""

    def test_metadata_exists(self, plugin):
        metadata = plugin.get_metadata()
        assert metadata is not None

    def test_metadata_has_name(self, plugin):
        metadata = plugin.get_metadata()
        assert isinstance(metadata.name, str)
        assert len(metadata.name) > 0

    def test_metadata_has_states(self, plugin):
        metadata = plugin.get_metadata()
        assert metadata.num_states >= 2


class TestPluginCreation:
    """Test that plugins can create automata."""

    def test_create_automaton(self, plugin):
        automaton = plugin.create_automaton(50, 50)
        assert automaton is not None
        assert automaton.grid.shape == (50, 50)

    def test_create_various_sizes(self, plugin):
        for size in [(10, 10), (50, 50), (100, 100)]:
            automaton = plugin.create_automaton(*size)
            assert automaton.grid.shape == size


class TestPluginSimulation:
    """Test that automata can step forward."""

    def test_single_step(self, plugin):
        automaton = plugin.create_automaton(50, 50)
        automaton.step()
        assert automaton.generation == 1

    def test_multiple_steps(self, plugin):
        automaton = plugin.create_automaton(50, 50)
        for _ in range(10):
            automaton.step()
        assert automaton.generation == 10

    def test_statistics(self, plugin):
        automaton = plugin.create_automaton(50, 50)
        for _ in range(5):
            automaton.step()
        stats = automaton.compute_statistics()
        assert 'active_cells' in stats
        assert 'density' in stats
        assert stats['density'] >= 0.0
        assert stats['density'] <= 100.0


class TestPluginPatterns:
    """Test that plugins provide valid patterns."""

    def test_has_patterns(self, plugin):
        patterns = plugin.get_default_patterns()
        assert isinstance(patterns, dict)
        assert len(patterns) > 0

    def test_patterns_have_descriptions(self, plugin):
        patterns = plugin.get_default_patterns()
        for name, info in patterns.items():
            assert isinstance(name, str)
            assert 'description' in info


class TestPluginColormap:
    """Test that plugins provide valid colormaps."""

    def test_has_colormap(self, plugin):
        colormap = plugin.get_colormap()
        assert isinstance(colormap, list)
        assert len(colormap) > 0

    def test_colormap_matches_states(self, plugin):
        metadata = plugin.get_metadata()
        colormap = plugin.get_colormap()
        assert len(colormap) >= metadata.num_states


class TestPluginRegistry:
    """Test the plugin registry functions."""

    def test_list_plugins(self):
        plugins = list_plugins()
        assert len(plugins) > 0
        assert 'game_of_life' in plugins

    def test_get_plugin(self):
        plugin = get_plugin('game_of_life')
        assert plugin is not None

    def test_get_plugin_case_insensitive(self):
        plugin = get_plugin('GAME_OF_LIFE')
        assert plugin is not None

    def test_get_nonexistent_plugin(self):
        plugin = get_plugin('nonexistent_plugin_xyz')
        assert plugin is None
