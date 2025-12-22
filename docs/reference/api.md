# API Reference

Complete Python API documentation for CALab.

---

## Core Classes

### Automaton Base Classes

#### `CellularAutomaton`

Base class for all cellular automata.

```python
class CellularAutomaton:
    """
    Base class for cellular automaton implementations
    """
    
    def __init__(self, width: int, height: int):
        """
        Initialize automaton
        
        Args:
            width: Grid width in cells
            height: Grid height in cells
        """
        
    def step(self) -> None:
        """
        Execute one evolution step
        
        Updates self.grid in-place
        """
        
    def get_grid(self) -> np.ndarray:
        """
        Get current grid state
        
        Returns:
            NumPy array of shape (height, width)
        """
        
    @property
    def num_states(self) -> int:
        """
        Number of possible states
        
        Returns:
            Integer number of states
        """
```

**Example**:
```python
auto = CellularAutomaton(width=100, height=100)
auto.step()
grid = auto.get_grid()
```

---

## Plugin System

### Plugin Functions

#### `get_plugin(name: str)`

Retrieve a plugin by name.

```python
def get_plugin(name: str) -> Callable:
    """
    Get plugin creator function
    
    Args:
        name: Plugin identifier (e.g., 'game_of_life')
    
    Returns:
        Factory function that creates automaton
    
    Raises:
        KeyError: If plugin not found
    """
```

**Example**:
```python
from plugins import get_plugin

# Get Game of Life plugin
plugin = get_plugin('game_of_life')

# Create automaton
auto = plugin(width=150, height=150, pattern='glider')

# Run simulation
for i in range(100):
    auto.step()
```

#### `list_plugins()`

List all available plugins.

```python
def list_plugins() -> List[str]:
    """
    Get list of all plugin names
    
    Returns:
        List of plugin identifier strings
    """
```

**Example**:
```python
from plugins import list_plugins

plugins = list_plugins()
print(f"Available: {', '.join(plugins)}")
```

#### `get_plugin_info(name: str)`

Get plugin metadata.

```python
def get_plugin_info(name: str) -> Dict[str, Any]:
    """
    Get plugin information
    
    Args:
        name: Plugin identifier
    
    Returns:
        Dictionary with metadata:
            - 'name': Human-readable name
            - 'description': Brief description
            - 'num_states': Number of states
            - 'patterns': Available patterns
            - 'category': Plugin category
    
    Raises:
        KeyError: If plugin not found
    """
```

**Example**:
```python
info = get_plugin_info('game_of_life')
print(f"Name: {info['name']}")
print(f"States: {info['num_states']}")
print(f"Patterns: {info['patterns']}")
```

### Plugin Categories

#### `get_plugins_by_category(category: str)`

Get plugins in a category.

```python
def get_plugins_by_category(category: str) -> List[str]:
    """
    Get all plugins in a category
    
    Args:
        category: Category name
            'self-replicating'
            'circuit'
            'life-like'
            'wave'
            'elementary'
            'self-organizing'
            'custom'
    
    Returns:
        List of plugin names in category
    """
```

**Example**:
```python
life_likes = get_plugins_by_category('life-like')
# ['game_of_life', 'highlife', 'day_and_night']
```

---

## Pattern Management

### Pattern Functions

#### `load_pattern(plugin_name: str, pattern_name: str)`

Load a predefined pattern.

```python
def load_pattern(plugin_name: str, 
                pattern_name: str) -> np.ndarray:
    """
    Load pattern from plugin
    
    Args:
        plugin_name: Plugin identifier
        pattern_name: Pattern identifier
    
    Returns:
        NumPy array with pattern
    
    Raises:
        KeyError: If plugin or pattern not found
    """
```

**Example**:
```python
pattern = load_pattern('game_of_life', 'glider')
print(pattern.shape)  # (3, 3)
```

#### `save_pattern(filename: str, grid: np.ndarray)`

Save pattern to file.

```python
def save_pattern(filename: str, grid: np.ndarray) -> None:
    """
    Save pattern to .npy file
    
    Args:
        filename: Path to save to
        grid: NumPy array to save
    """
```

**Example**:
```python
pattern = np.array([[0, 1, 0],
                    [0, 0, 1],
                    [1, 1, 1]])
save_pattern('my_glider.npy', pattern)
```

---

## Simulation Control

### Simulator Class

#### `Simulator`

Main simulation controller.

```python
class Simulator:
    """
    Controls cellular automaton simulation
    """
    
    def __init__(self, automaton):
        """
        Initialize simulator
        
        Args:
            automaton: CellularAutomaton instance
        """
        
    def run(self, steps: int) -> None:
        """
        Run simulation for N steps
        
        Args:
            steps: Number of steps to execute
        """
        
    def reset(self) -> None:
        """
        Reset to initial state
        """
        
    def get_statistics(self) -> Dict[str, float]:
        """
        Get current statistics
        
        Returns:
            Dictionary with metrics:
                - 'generation': Current step
                - 'active_cells': Non-zero cells
                - 'density': Percentage active
                - 'entropy': Shannon entropy
        """
```

**Example**:
```python
from simulator import Simulator
from plugins import get_plugin

auto = get_plugin('game_of_life')(150, 150, 'glider')
sim = Simulator(auto)

# Run 100 steps
sim.run(100)

# Get statistics
stats = sim.get_statistics()
print(f"Generation: {stats['generation']}")
print(f"Density: {stats['density']:.2f}%")
```

---

## Diagnostics

### Diagnostics Class

#### `Diagnostics`

Analysis and metrics collection.

```python
class Diagnostics:
    """
    Collect and analyze automaton behavior
    """
    
    def __init__(self):
        """Initialize diagnostics collector"""
        
    def analyze(self, automaton, steps: int = 100) -> Dict:
        """
        Analyze automaton behavior
        
        Args:
            automaton: Automaton to analyze
            steps: Steps to run for analysis
        
        Returns:
            Dictionary with analysis:
                - 'classification': Behavior type
                - 'metrics': Statistical metrics
                - 'events': Event log
        """
        
    def classify_behavior(self, metrics: Dict) -> str:
        """
        Classify automaton behavior
        
        Args:
            metrics: Collected metrics
        
        Returns:
            Classification string:
                'STATIC' - No changes
                'OSCILLATING' - Periodic
                'GROWING' - Expanding
                'DYING' - Shrinking
                'CHAOTIC' - Unpredictable
                'STABLE' - Equilibrium
                'COMPLEX' - Mixed behavior
        """
```

**Example**:
```python
from diagnostics import Diagnostics

diag = Diagnostics()
results = diag.analyze(automaton, steps=200)

print(f"Classification: {results['classification']}")
print(f"Average density: {results['metrics']['avg_density']:.2f}")
```

---

## Utility Functions

### Grid Operations

#### `count_neighbors(grid, x, y, neighborhood='moore')`

Count cell neighbors.

```python
def count_neighbors(grid: np.ndarray, 
                   x: int, 
                   y: int,
                   neighborhood: str = 'moore') -> int:
    """
    Count neighbors of cell
    
    Args:
        grid: Grid array
        x, y: Cell coordinates
        neighborhood: 'moore' or 'von_neumann'
    
    Returns:
        Number of alive neighbors
    """
```

**Example**:
```python
count = count_neighbors(grid, 10, 10, neighborhood='moore')
```

#### `apply_boundary(grid, boundary='periodic')`

Apply boundary conditions.

```python
def apply_boundary(grid: np.ndarray,
                  boundary: str = 'periodic') -> np.ndarray:
    """
    Apply boundary conditions
    
    Args:
        grid: Grid array
        boundary: Type of boundary
            'periodic' - Wrap around (torus)
            'fixed' - Fixed values at edges
            'reflective' - Mirror at boundaries
    
    Returns:
        Grid with boundaries applied
    """
```

---

## Analysis Functions

### Statistical Measures

#### `calculate_entropy(grid)`

Calculate Shannon entropy.

```python
def calculate_entropy(grid: np.ndarray) -> float:
    """
    Calculate Shannon entropy
    
    Args:
        grid: State grid
    
    Returns:
        Entropy in bits
    """
```

#### `calculate_density(grid)`

Calculate population density.

```python
def calculate_density(grid: np.ndarray) -> float:
    """
    Calculate density (% non-zero)
    
    Args:
        grid: State grid
    
    Returns:
        Density as percentage (0-100)
    """
```

#### `detect_period(automaton, max_steps=1000)`

Detect oscillation period.

```python
def detect_period(automaton, 
                 max_steps: int = 1000) -> Optional[int]:
    """
    Detect if pattern is periodic
    
    Args:
        automaton: Automaton instance
        max_steps: Maximum steps to check
    
    Returns:
        Period length, or None if not periodic
    """
```

---

## File I/O

### Saving and Loading

#### `save_simulation(filename, automaton)`

Save complete simulation state.

```python
def save_simulation(filename: str, 
                   automaton) -> None:
    """
    Save simulation to file
    
    Args:
        filename: Output file path (.pkl)
        automaton: Automaton to save
    """
```

#### `load_simulation(filename)`

Load simulation state.

```python
def load_simulation(filename: str):
    """
    Load simulation from file
    
    Args:
        filename: Input file path (.pkl)
    
    Returns:
        Loaded automaton instance
    """
```

---

## Visualization

### Visualization Functions

#### `visualize_grid(grid, colormap=None)`

Visualize grid as image.

```python
def visualize_grid(grid: np.ndarray,
                  colormap: Optional[List] = None) -> np.ndarray:
    """
    Convert grid to RGB image
    
    Args:
        grid: State grid
        colormap: List of (R,G,B) tuples
    
    Returns:
        RGB image array (H, W, 3)
    """
```

#### `animate_evolution(automaton, steps, interval=100)`

Create animation.

```python
def animate_evolution(automaton,
                     steps: int,
                     interval: int = 100):
    """
    Create matplotlib animation
    
    Args:
        automaton: Automaton to animate
        steps: Number of steps
        interval: Milliseconds between frames
    
    Returns:
        matplotlib.animation.FuncAnimation
    """
```

---

## Constants

### Standard Values

```python
# Grid sizes
GRID_SIZE_SMALL = 50
GRID_SIZE_MEDIUM = 150
GRID_SIZE_LARGE = 300

# Neighborhoods
MOORE_NEIGHBORHOOD = 'moore'
VON_NEUMANN_NEIGHBORHOOD = 'von_neumann'

# Boundaries
BOUNDARY_PERIODIC = 'periodic'
BOUNDARY_FIXED = 'fixed'
BOUNDARY_REFLECTIVE = 'reflective'

# Classification types
CLASS_STATIC = 'STATIC'
CLASS_OSCILLATING = 'OSCILLATING'
CLASS_GROWING = 'GROWING'
CLASS_DYING = 'DYING'
CLASS_CHAOTIC = 'CHAOTIC'
CLASS_STABLE = 'STABLE'
CLASS_COMPLEX = 'COMPLEX'
```

---

## Type Hints

### Common Types

```python
from typing import Tuple, List, Dict, Optional, Callable

# Grid types
Grid = np.ndarray  # Shape (height, width)
Pattern = np.ndarray  # Shape (ph, pw)

# Color types
RGB = Tuple[int, int, int]  # (R, G, B) each 0-255
Colormap = List[RGB]

# Plugin types
PluginFactory = Callable[[int, int, str], CellularAutomaton]
PluginInfo = Dict[str, Any]

# Coordinate types
Coordinate = Tuple[int, int]  # (x, y)
```

---

## Error Handling

### Exceptions

#### `PluginNotFoundError`

Raised when plugin doesn't exist.

```python
class PluginNotFoundError(KeyError):
    """Plugin with given name not found"""
    pass
```

#### `PatternNotFoundError`

Raised when pattern doesn't exist.

```python
class PatternNotFoundError(KeyError):
    """Pattern with given name not found"""
    pass
```

#### `InvalidGridSizeError`

Raised for invalid grid dimensions.

```python
class InvalidGridSizeError(ValueError):
    """Grid size out of valid range"""
    pass
```

**Example**:
```python
try:
    plugin = get_plugin('nonexistent')
except PluginNotFoundError as e:
    print(f"Plugin not found: {e}")
```

---

## Usage Examples

### Complete Workflow

```python
# Import modules
from plugins import get_plugin, get_plugin_info
from simulator import Simulator
from diagnostics import Diagnostics
import numpy as np

# 1. Get plugin
plugin = get_plugin('game_of_life')

# 2. Create automaton
auto = plugin(width=150, height=150, pattern='glider')

# 3. Create simulator
sim = Simulator(auto)

# 4. Run simulation
sim.run(100)

# 5. Get statistics
stats = sim.get_statistics()
print(f"Generation: {stats['generation']}")
print(f"Active cells: {stats['active_cells']}")

# 6. Analyze behavior
diag = Diagnostics()
results = diag.analyze(auto, steps=200)
print(f"Classification: {results['classification']}")

# 7. Save state
from file_io import save_simulation
save_simulation('my_simulation.pkl', auto)
```

### Custom Automaton

```python
# Create custom automaton class
class MyAutomaton(CellularAutomaton):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.grid = np.random.randint(0, 2, (height, width))
        self.num_states = 2
    
    def step(self):
        # Custom evolution logic
        new_grid = self.grid.copy()
        # ... implement rules
        self.grid = new_grid
    
    def get_grid(self):
        return self.grid.copy()

# Use it
auto = MyAutomaton(100, 100)
auto.step()
```

---

## Performance Tips

### Optimization

```python
# Use NumPy vectorization
neighbors = (
    np.roll(grid, 1, axis=0) +
    np.roll(grid, -1, axis=0) +
    # ... more operations
)

# Avoid loops when possible
# Bad: for i in range(height): for j in range(width): ...
# Good: Use NumPy array operations

# Use appropriate data types
grid = np.zeros((h, w), dtype=np.uint8)  # Not float64!

# Pre-allocate arrays
new_grid = np.empty_like(grid)  # Not np.zeros
```

---

## Quick Reference

### Most Common Operations

```python
# Create automaton
auto = get_plugin('game_of_life')(150, 150, 'glider')

# Run simulation
for i in range(100):
    auto.step()

# Get current state
grid = auto.get_grid()

# Count active cells
active = np.count_nonzero(grid)

# Calculate density
density = np.mean(grid) * 100

# Visualize
import matplotlib.pyplot as plt
plt.imshow(grid, cmap='binary')
plt.show()
```

---

## Version Compatibility

**Python**: 3.7+
**NumPy**: 1.18+
**Optional**: PyQt5 5.15+ (for GUI)

---

## Further Reading

- [Plugin System](plugin_system.md) - Architecture details
- [File Formats](file_formats.md) - Data formats
- [Creating Plugins](../tutorials/creating_plugins.md) - Tutorial

---

**Complete API for CALab automation!** 📚
