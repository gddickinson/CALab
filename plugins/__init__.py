"""
CALab Plugins - Cellular Automata Collection
=============================================

Complete collection of 13 cellular automata implementations.

Categories:
-----------
Self-Replicating: Langton's Loop, Von Neumann Constructor, HighLife
Circuit Simulation: Wire World
Life-like: Game of Life, Day and Night, HighLife
Wave/Propagation: Brian's Brain, Seeds
Elementary: Rule 30, Rule 110, Rule 90
Self-Organizing: Cyclic CA

Total: 13 automata, 57+ patterns
"""

# Self-replicating automata
from .langton_loop import LangtonLoop, LangtonLoopPlugin
from .von_neumann import VonNeumannConstructor, VonNeumannConstructorPlugin
from .von_neumann_full import VonNeumannFull, VonNeumannFullPlugin

# Circuit simulation
from .wireworld import WireWorld, WireWorldPlugin

# Life-like automata
from .game_of_life import GameOfLife, GameOfLifePlugin
from .life_variants import (DayAndNight, DayAndNightPlugin,
                            HighLife, HighLifePlugin)

# Wave/propagation automata
from .brians_brain import BriansBrain, BriansBrainPlugin
from .seeds import Seeds, SeedsPlugin

# Elementary cellular automata
from .elementary_ca import (ElementaryCA, ElementaryCAPlugin,
                            Rule30Plugin, Rule110Plugin, Rule90Plugin)

# Self-organizing automata
from .cyclic_ca import CyclicCA, CyclicCAPlugin

__all__ = [
    'LangtonLoop', 'LangtonLoopPlugin',
    'WireWorld', 'WireWorldPlugin',
    'GameOfLife', 'GameOfLifePlugin',
    'BriansBrain', 'BriansBrainPlugin',
    'Seeds', 'SeedsPlugin',
    'VonNeumannConstructor', 'VonNeumannConstructorPlugin',
    'VonNeumannFull', 'VonNeumannFullPlugin',
    'ElementaryCA', 'ElementaryCAPlugin', 'Rule30Plugin', 'Rule110Plugin', 'Rule90Plugin',
    'CyclicCA', 'CyclicCAPlugin',
    'DayAndNight', 'DayAndNightPlugin',
    'HighLife', 'HighLifePlugin'
]

# Registry of all available plugins
PLUGIN_REGISTRY = {
    # Self-replicating
    'langton_loop': LangtonLoopPlugin,
    'von_neumann': VonNeumannConstructorPlugin,
    'von_neumann_full': VonNeumannFullPlugin,

    # Circuit simulation
    'wireworld': WireWorldPlugin,

    # Life-like
    'game_of_life': GameOfLifePlugin,
    'day_and_night': DayAndNightPlugin,
    'highlife': HighLifePlugin,

    # Wave/propagation
    'brians_brain': BriansBrainPlugin,
    'seeds': SeedsPlugin,

    # Elementary CA
    'rule_30': Rule30Plugin,
    'rule_110': Rule110Plugin,
    'rule_90': Rule90Plugin,

    # Self-organizing
    'cyclic_ca': CyclicCAPlugin,
}

# Category metadata
PLUGIN_CATEGORIES = {
    'Self-Replicating': ['langton_loop', 'von_neumann', 'von_neumann_full', 'highlife'],
    'Circuit Simulation': ['wireworld'],
    'Life-like': ['game_of_life', 'day_and_night', 'highlife'],
    'Wave/Propagation': ['brians_brain', 'seeds'],
    'Elementary CA': ['rule_30', 'rule_110', 'rule_90'],
    'Self-Organizing': ['cyclic_ca'],
}

# Plugin descriptions for quick reference
PLUGIN_INFO = {
    'langton_loop': 'Simplified self-replicating loop (8 states)',
    'von_neumann': 'Simplified von Neumann constructor (29 states)',
    'von_neumann_full': 'Complete von Neumann constructor with full rule table (29 states)',
    'wireworld': 'Digital circuit simulation with electrons',
    'game_of_life': "Conway's classic Game of Life",
    'day_and_night': 'Symmetric Life variant (B3678/S34678)',
    'highlife': 'Life with replicator pattern (B36/S23)',
    'brians_brain': 'Beautiful wave patterns (3 states)',
    'seeds': 'Explosive growth automaton (B2/S)',
    'rule_30': 'Chaotic elementary CA',
    'rule_110': 'Turing complete elementary CA',
    'rule_90': 'Sierpinski triangle generator',
    'cyclic_ca': 'Rainbow spiral patterns',
}


def get_plugin(name: str):
    """
    Get plugin by name.

    Args:
        name: Plugin name (case-insensitive)

    Returns:
        Plugin class or None if not found

    Example:
        >>> plugin = get_plugin('game_of_life')
        >>> automaton = plugin.create_automaton(100, 100)
    """
    return PLUGIN_REGISTRY.get(name.lower())


def list_plugins():
    """
    List all available plugin names.

    Returns:
        List of plugin names

    Example:
        >>> plugins = list_plugins()
        >>> print(f"Available: {len(plugins)} plugins")
    """
    return list(PLUGIN_REGISTRY.keys())


def get_plugins_by_category(category: str):
    """
    Get plugins in a specific category.

    Args:
        category: Category name

    Returns:
        List of plugin names in category

    Example:
        >>> life_like = get_plugins_by_category('Life-like')
        >>> print(life_like)
    """
    return PLUGIN_CATEGORIES.get(category, [])


def list_categories():
    """
    List all plugin categories.

    Returns:
        List of category names
    """
    return list(PLUGIN_CATEGORIES.keys())


def get_plugin_info(name: str):
    """
    Get quick info about a plugin.

    Args:
        name: Plugin name

    Returns:
        Description string or None

    Example:
        >>> info = get_plugin_info('rule_110')
        >>> print(info)
        'Turing complete elementary CA'
    """
    return PLUGIN_INFO.get(name.lower())


def print_plugin_catalog():
    """
    Print a formatted catalog of all plugins.

    Example:
        >>> print_plugin_catalog()
    """
    print("\n" + "="*60)
    print("CALab Plugin Catalog")
    print("="*60)

    for category, plugins in PLUGIN_CATEGORIES.items():
        print(f"\n{category}:")
        for plugin_name in plugins:
            plugin = PLUGIN_REGISTRY[plugin_name]
            metadata = plugin.get_metadata()
            info = PLUGIN_INFO[plugin_name]
            num_patterns = len(plugin.get_default_patterns())

            print(f"  • {metadata.name}")
            print(f"    {info}")
            print(f"    States: {metadata.num_states} | Patterns: {num_patterns}")

    print(f"\n{'='*60}")
    print(f"Total: {len(PLUGIN_REGISTRY)} automata")
    print("="*60 + "\n")
