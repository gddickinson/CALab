"""
Pytest tests for the CALab simulation engine.

Tests input validation, state management, and batch simulation.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.simulator import SimulationEngine, BatchSimulation
from plugins import get_plugin


@pytest.fixture
def engine():
    """Create a fresh simulation engine."""
    return SimulationEngine()


@pytest.fixture
def gol_automaton():
    """Create a Game of Life automaton."""
    plugin = get_plugin('game_of_life')
    return plugin.create_automaton(50, 50)


class TestSimulationEngine:
    """Test the core simulation engine."""

    def test_create_engine(self, engine):
        assert engine is not None
        assert engine.running is False

    def test_start_without_automaton_raises(self, engine):
        with pytest.raises(ValueError, match="No automaton set"):
            engine.start()

    def test_set_automaton(self, engine, gol_automaton):
        engine.set_automaton(gol_automaton)
        assert engine.automaton is gol_automaton

    def test_step_once(self, engine, gol_automaton):
        engine.set_automaton(gol_automaton)
        engine.step_once()
        assert engine.total_steps == 1

    def test_set_speed_valid(self, engine):
        engine.set_speed(100)
        assert engine.speed_ms == 100

    def test_set_speed_clamps_minimum(self, engine):
        engine.set_speed(0)
        assert engine.speed_ms == 1

    def test_set_speed_invalid_type_raises(self, engine):
        with pytest.raises(TypeError):
            engine.set_speed("fast")

    def test_get_status(self, engine, gol_automaton):
        engine.set_automaton(gol_automaton)
        status = engine.get_status()
        assert 'running' in status
        assert 'generation' in status
        assert status['running'] is False


class TestBatchSimulation:
    """Test batch simulation runner."""

    def test_run_batch(self):
        batch = BatchSimulation()
        plugin = get_plugin('game_of_life')

        results = batch.run_batch(
            automaton_factory=plugin.create_automaton,
            parameter_sets=[
                {'width': 20, 'height': 20},
                {'width': 30, 'height': 30},
            ],
            num_steps=5
        )
        assert len(results) == 2

    def test_run_batch_negative_steps_raises(self):
        batch = BatchSimulation()
        with pytest.raises(ValueError, match="non-negative"):
            batch.run_batch(
                automaton_factory=lambda **kw: None,
                parameter_sets=[{'width': 10, 'height': 10}],
                num_steps=-1
            )

    def test_run_batch_empty_params_raises(self):
        batch = BatchSimulation()
        with pytest.raises(ValueError, match="must not be empty"):
            batch.run_batch(
                automaton_factory=lambda **kw: None,
                parameter_sets=[],
                num_steps=5
            )
