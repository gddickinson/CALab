# Plugin System Architecture

Complete reference for the CALab plugin architecture.

---

## Overview

CALab uses a **plugin-based architecture** that allows:
- Easy addition of new automata
- Modular code organization
- Independent testing
- Community contributions

**Core Concept**: Each cellular automaton is a self-contained plugin.

---

## Architecture

### Directory Structure

```
CALab/
├── core/
│   ├── automaton.py          # Base class
│   ├── simulator.py          # Simulation engine
│   └── diagnostics.py        # Analysis tools
├── plugins/
│   ├── __init__.py           # Plugin registry
│   ├── game_of_life.py       # Plugin example
│   ├── wireworld.py          # Plugin example
│   └── ...                   # More plugins
└── gui/
    └── ...                   # GUI components
```

### Key Components

**1. Base Class** (`core/automaton.py`)
```python
class CellularAutomaton:
    """Abstract base class for all automata"""
    
    def __init__(self, width, height, num_states):
        """Initialize grid and properties"""
        
    def get_next_state(self, center, neighbors):
        """Calculate next state - MUST OVERRIDE"""
        
    def step(self):
        """Execute one generation"""
        
    # ... more methods
```

**2. Plugin Module** (`plugins/my_ca.py`)
```python
from core.automaton import CellularAutomaton

class MyCA(CellularAutomaton):
    """Specific automaton implementation"""
    # Override methods here

def create_automaton(width, height, pattern='default'):
    """Factory function"""
    return MyCA(width, height, pattern)

def get_info():
    """Metadata"""
    return {...}
```

**3. Plugin Registry** (`plugins/__init__.py`)
```python
from plugins import game_of_life, my_ca

PLUGIN_REGISTRY = {
    'game_of_life': game_of_life,
    'my_ca': my_ca,
}

def get_plugin(name):
    """Retrieve plugin by name"""
    return PLUGIN_REGISTRY.get(name)
```

---

## Base Class API

### CellularAutomaton

**Constructor**:
```python
def __init__(self, width: int, height: int, num_states: int):
    """
    Initialize automaton
    
    Args:
        width: Grid width in cells
        height: Grid height in cells
        num_states: Number of possible states (2-29)
    
    Creates:
        self.grid: numpy array of shape (height, width)
        self.num_states: number of states
    """
```

**Abstract Methods** (must override):
```python
def get_next_state(self, center: int, neighbors: List[int]) -> int:
    """
    Calculate next state for a cell
    
    Args:
        center: Current state of the cell
        neighbors: List of 8 neighbor states [N, E, S, W, NW, NE, SE, SW]
    
    Returns:
        Next state (0 to num_states-1)
    
    Raises:
        NotImplementedError if not overridden
    """
```

**Provided Methods**:
```python
def step(self):
    """Execute one time step - updates entire grid"""

def get_state(self, x: int, y: int) -> int:
    """Get state at position"""

def set_state(self, x: int, y: int, value: int):
    """Set state at position"""

def clear(self):
    """Reset grid to all zeros"""

def get_neighbors(self, x: int, y: int) -> List[int]:
    """
    Get Moore neighborhood (8 neighbors)
    
    Returns:
        [N, E, S, W, NW, NE, SE, SW]
    """

def get_density(self) -> float:
    """Calculate percentage of non-zero cells"""

def get_entropy(self) -> float:
    """Calculate Shannon entropy"""
```

---

## Plugin Requirements

### Minimal Plugin

Every plugin MUST provide:

**1. Automaton Class**:
```python
class MyCA(CellularAutomaton):
    def __init__(self, width, height, pattern='default'):
        super().__init__(width, height, num_states)
        # Initialize pattern
    
    def get_next_state(self, center, neighbors):
        # Implement rules
        return next_state
    
    @staticmethod
    def get_patterns():
        # Return available patterns
        return {...}
    
    def set_pattern(self, pattern_name):
        # Set initial configuration
        pass
```

**2. Factory Function**:
```python
def create_automaton(width, height, pattern='default'):
    """
    Create automaton instance
    
    Args:
        width: Grid width
        height: Grid height
        pattern: Initial pattern name
    
    Returns:
        Instance of MyCA
    """
    return MyCA(width, height, pattern)
```

**3. Metadata Function**:
```python
def get_info():
    """
    Return plugin metadata
    
    Returns:
        dict with keys:
            - name (str): Display name
            - description (str): Brief description
            - author (str): Author name
            - version (str): Version string
            - states (int): Number of states
            - neighborhood (str): 'moore' or 'von_neumann'
            - patterns (dict): Available patterns
    """
    return {
        'name': 'My Automaton',
        'description': 'Brief description',
        'author': 'Your Name',
        'version': '1.0',
        'states': 2,
        'neighborhood': 'moore',
        'patterns': MyCA.get_patterns()
    }
```

---

## Pattern System

### Pattern Dictionary

Format:
```python
@staticmethod
def get_patterns():
    return {
        'pattern_name': {
            'description': 'Human-readable description',
            'grid_size': (min_width, min_height),  # Optional
            'recommended': True  # Optional, mark as default
        },
        # ... more patterns
    }
```

Example:
```python
@staticmethod
def get_patterns():
    return {
        'glider': {
            'description': 'Small spaceship moving diagonally',
            'grid_size': (50, 50),
            'recommended': True
        },
        'random': {
            'description': 'Random initial state (30% density)',
            'grid_size': (50, 50)
        },
        'acorn': {
            'description': 'Methuselah (5206 generations)',
            'grid_size': (200, 200)
        }
    }
```

### Pattern Implementation

```python
def set_pattern(self, pattern_name):
    """
    Set grid to initial pattern
    
    Args:
        pattern_name: Key from get_patterns()
    
    Raises:
        ValueError: If pattern unknown
    """
    h, w = self.grid.shape
    
    if pattern_name not in self.get_patterns():
        raise ValueError(f"Unknown pattern: {pattern_name}")
    
    # Clear grid first
    self.grid.fill(0)
    
    # Set pattern
    if pattern_name == 'glider':
        cx, cy = w//2, h//2
        self.grid[cy, cx+1] = 1
        self.grid[cy+1, cx+2] = 1
        self.grid[cy+2, cx:cx+3] = 1
    
    elif pattern_name == 'random':
        import numpy as np
        self.grid = np.random.choice(
            range(self.num_states),
            size=(h, w),
            p=[0.7] + [0.3/(self.num_states-1)]*(self.num_states-1)
        )
    
    # ... more patterns
```

---

## Registration

### Adding to Registry

**Step 1**: Create plugin file
```bash
# plugins/my_automaton.py
```

**Step 2**: Import and register

Edit `plugins/__init__.py`:
```python
# Import plugin
from plugins import my_automaton

# Add to registry
PLUGIN_REGISTRY = {
    'game_of_life': game_of_life,
    'my_automaton': my_automaton,  # <-- Add here
    # ... more plugins
}

# Add to categories
PLUGIN_CATEGORIES = {
    'My Category': ['my_automaton'],
    # ... more categories
}

# Add info
PLUGIN_INFO = {
    'my_automaton': 'Brief one-liner',
}
```

### Plugin Discovery

**Automatic**:
```python
from plugins import get_plugin, list_plugins

# Get all plugins
all_plugins = list_plugins()

# Get specific plugin
plugin = get_plugin('my_automaton')

# Get by category
from plugins import get_plugins_by_category
life_like = get_plugins_by_category('Life-like')
```

---

## Advanced Features

### Custom Neighborhood

Override `get_neighbors()`:
```python
def get_neighbors(self, x, y):
    """
    Custom neighborhood (e.g., Von Neumann)
    
    Returns:
        [N, E, S, W]  # Only cardinal directions
    """
    h, w = self.grid.shape
    
    N = self.grid[(y-1) % h, x]
    E = self.grid[y, (x+1) % w]
    S = self.grid[(y+1) % h, x]
    W = self.grid[y, (x-1) % w]
    
    return [N, E, S, W]
```

### Custom Colormap

Provide `get_colormap()`:
```python
def get_colormap(self):
    """
    Define colors for each state
    
    Returns:
        List of (R, G, B) tuples, one per state
    """
    return [
        (0, 0, 0),       # State 0: Black
        (0, 255, 0),     # State 1: Green
        (255, 0, 0),     # State 2: Red
        (0, 0, 255),     # State 3: Blue
        # ... up to num_states
    ]
```

### Pre-computed Rules

Cache expensive computations:
```python
def __init__(self, width, height, pattern='default'):
    super().__init__(width, height, num_states=8)
    
    # Pre-compute rule table
    self._rule_table = self._build_rule_table()
    
    if pattern in self.get_patterns():
        self.set_pattern(pattern)

def _build_rule_table(self):
    """Build transition lookup table"""
    table = {}
    
    # Format: (center, N, E, S, W) -> next
    table[(0, 1, 1, 1, 0)] = 2
    table[(2, 0, 1, 0, 1)] = 3
    # ... many more
    
    return table

def get_next_state(self, center, neighbors):
    """Use pre-computed table"""
    N, E, S, W = neighbors[:4]  # Cardinal only
    key = (center, N, E, S, W)
    return self._rule_table.get(key, center)
```

### Boundary Conditions

Override for non-toroidal:
```python
def get_neighbors(self, x, y):
    """Use fixed boundaries instead of wrapping"""
    h, w = self.grid.shape
    neighbors = []
    
    for dy, dx in [(-1,0), (0,1), (1,0), (0,-1),
                   (-1,-1), (-1,1), (1,1), (1,-1)]:
        ny, nx = y + dy, x + dx
        
        # Fixed boundary (don't wrap)
        if 0 <= ny < h and 0 <= nx < w:
            neighbors.append(self.grid[ny, nx])
        else:
            neighbors.append(0)  # Treat outside as dead
    
    return neighbors
```

---

## Testing Framework

### Test Structure

```
tests/
├── test_core.py              # Test base class
├── test_plugins.py           # Test all plugins
└── test_my_automaton.py      # Test specific plugin
```

### Plugin Test Template

```python
import pytest
import numpy as np
from plugins import get_plugin

@pytest.fixture
def plugin():
    """Fixture providing plugin"""
    return get_plugin('my_automaton')

@pytest.fixture
def automaton(plugin):
    """Fixture providing automaton instance"""
    return plugin.create_automaton(50, 50)

def test_plugin_exists(plugin):
    """Test plugin loads"""
    assert plugin is not None

def test_metadata(plugin):
    """Test metadata complete"""
    info = plugin.get_info()
    assert 'name' in info
    assert 'states' in info
    assert 'patterns' in info

def test_create_automaton(plugin):
    """Test creation"""
    auto = plugin.create_automaton(50, 50)
    assert auto.grid.shape == (50, 50)
    assert hasattr(auto, 'get_next_state')

def test_patterns(plugin):
    """Test all patterns"""
    info = plugin.get_info()
    patterns = info['patterns']
    
    for pattern_name in patterns:
        auto = plugin.create_automaton(100, 100, pattern=pattern_name)
        assert auto is not None
        assert np.sum(auto.grid >= 0) > 0

def test_evolution(automaton):
    """Test evolution occurs"""
    initial = automaton.grid.copy()
    
    for _ in range(10):
        automaton.step()
    
    # State should change (unless all still lifes)
    assert not np.array_equal(automaton.grid, initial) or \
           np.sum(automaton.grid) == 0

def test_states_valid(automaton):
    """Test states remain valid"""
    for _ in range(50):
        automaton.step()
        
        assert np.all(automaton.grid >= 0)
        assert np.all(automaton.grid < automaton.num_states)

def test_deterministic(plugin):
    """Test determinism"""
    auto1 = plugin.create_automaton(50, 50, pattern='default')
    auto2 = plugin.create_automaton(50, 50, pattern='default')
    
    for _ in range(10):
        auto1.step()
        auto2.step()
    
    assert np.array_equal(auto1.grid, auto2.grid)
```

---

## Performance Optimization

### Vectorization

**Slow** (per-cell loop):
```python
def step(self):
    new_grid = np.zeros_like(self.grid)
    h, w = self.grid.shape
    
    for y in range(h):
        for x in range(w):
            center = self.grid[y, x]
            neighbors = self.get_neighbors(x, y)
            new_grid[y, x] = self.get_next_state(center, neighbors)
    
    self.grid = new_grid
```

**Fast** (vectorized):
```python
def step(self):
    """Vectorized step for Life-like rules"""
    # Use convolution for neighbor counting
    from scipy.signal import convolve2d
    
    kernel = np.array([[1,1,1], [1,0,1], [1,1,1]])
    neighbor_count = convolve2d(self.grid, kernel, mode='same', boundary='wrap')
    
    # Apply rules vectorized
    birth = (self.grid == 0) & (neighbor_count == 3)
    survival = (self.grid == 1) & ((neighbor_count == 2) | (neighbor_count == 3))
    
    self.grid = (birth | survival).astype(int)
```

### Caching

```python
class CachedCA(CellularAutomaton):
    def __init__(self, width, height, pattern='default'):
        super().__init__(width, height, num_states=2)
        
        # Cache for get_next_state
        self._state_cache = {}
        
        if pattern in self.get_patterns():
            self.set_pattern(pattern)
    
    def get_next_state(self, center, neighbors):
        """Cached version"""
        key = (center, tuple(neighbors))
        
        if key not in self._state_cache:
            # Compute once
            alive = sum(1 for n in neighbors if n == 1)
            
            if center == 0 and alive == 3:
                result = 1
            elif center == 1 and alive in [2, 3]:
                result = 1
            else:
                result = 0
            
            self._state_cache[key] = result
        
        return self._state_cache[key]
```

---

## Integration with GUI

### Simulator Integration

GUI uses simulator:
```python
from core.simulator import Simulator

# Create simulator with plugin
sim = Simulator('my_automaton', width=150, height=150)

# Load pattern
sim.set_pattern('default')

# Run
for _ in range(100):
    sim.step()
    # GUI updates display
```

### GUI Expectations

Plugin should:
1. Work with any grid size
2. Handle pattern changes
3. Provide reasonable defaults
4. Not crash on edge cases
5. Run efficiently (>30 FPS at 150×150)

---

## Documentation Standards

### Plugin Docstring Template

```python
"""
[Plugin Name] - [Brief Description]

[Longer description paragraph explaining what the automaton
does, what makes it interesting, and any historical context.]

States:
    0: [Meaning of state 0]
    1: [Meaning of state 1]
    [... more states]

Rules:
    - [Rule 1 description]
    - [Rule 2 description]
    - [... more rules]

Patterns:
    - pattern_name: [Description]
    - [... more patterns]

Examples:
    >>> from plugins import get_plugin
    >>> plugin = get_plugin('my_automaton')
    >>> auto = plugin.create_automaton(100, 100, pattern='default')
    >>> auto.step()
    >>> print(f"Active cells: {np.sum(auto.grid > 0)}")

References:
    - [Paper/Website if applicable]
    - [Original author if not you]

Author: [Your name]
Version: [Version number]
"""
```

---

## Best Practices

### Code Quality

✅ **Do**:
- Follow PEP 8 style
- Add comprehensive docstrings
- Write unit tests
- Handle edge cases
- Validate inputs
- Use type hints
- Profile performance

❌ **Don't**:
- Hardcode values
- Ignore errors
- Skip documentation
- Write untested code
- Make assumptions

### Plugin Design

✅ **Do**:
- Make patterns interesting
- Provide variety
- Document behavior
- Optimize performance
- Test thoroughly
- Keep code clean

❌ **Don't**:
- Make only one pattern
- Skip edge cases
- Ignore performance
- Leave bugs
- Forget documentation

---

## Common Patterns

### Plugin Template

Use this as starting point:

```python
"""Plugin: [Name]"""

import numpy as np
from core.automaton import CellularAutomaton

class [ClassName](CellularAutomaton):
    """[Description]"""
    
    def __init__(self, width, height, pattern='default'):
        super().__init__(width, height, num_states=[N])
        if pattern in self.get_patterns():
            self.set_pattern(pattern)
    
    def get_next_state(self, center, neighbors):
        """[Rule description]"""
        # YOUR RULES HERE
        pass
    
    @staticmethod
    def get_patterns():
        return {
            'default': {'description': '[...]'},
            # More patterns
        }
    
    def set_pattern(self, pattern_name):
        h, w = self.grid.shape
        # SET PATTERNS HERE
        pass

def create_automaton(width, height, pattern='default'):
    return [ClassName](width, height, pattern)

def get_info():
    return {
        'name': '[Name]',
        'description': '[Description]',
        'author': '[Your Name]',
        'version': '1.0',
        'states': [N],
        'neighborhood': 'moore',
        'patterns': [ClassName].get_patterns()
    }
```

---

## Troubleshooting

### Plugin Not Found

**Check**:
- File in `plugins/` directory?
- Imported in `__init__.py`?
- Added to `PLUGIN_REGISTRY`?
- No syntax errors?

### Pattern Not Working

**Check**:
- Pattern name in `get_patterns()`?
- `set_pattern()` implemented?
- Grid large enough?
- Coordinates correct?

### Performance Issues

**Solutions**:
- Vectorize operations
- Cache computations
- Optimize hot paths
- Profile code
- Reduce grid size for testing

---

## Summary

Plugin system provides:
- **Modularity**: Independent plugins
- **Extensibility**: Easy to add new CA
- **Testing**: Isolated testing
- **Organization**: Clean structure

**Requirements**:
- Inherit from `CellularAutomaton`
- Implement required methods
- Register in `__init__.py`
- Provide patterns
- Document thoroughly

---

## See Also

- [Creating Plugins Tutorial](../tutorials/creating_plugins.md)
- [API Reference](api.md)
- [File Formats](file_formats.md)

---

**Build amazing plugins!** 🔌✨
