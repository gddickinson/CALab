# Tutorial: Creating Custom Plugins

Learn how to extend CALab by creating your own cellular automaton plugins!

---

## What You'll Learn

- Plugin architecture
- Creating automaton classes
- Defining rules and patterns
- Integrating with CALab
- Testing and debugging

**Time**: 60 minutes
**Difficulty**: ⭐⭐⭐⭐ Advanced

---

## Prerequisites

- Python programming knowledge
- Understanding of CA ([Theory](../theory.md))
- Familiarity with CALab
- Code editor

---

## Part 1: Plugin Architecture

### File Structure

```
CALab/
├── plugins/
│   ├── __init__.py           # Plugin registry
│   ├── my_automaton.py       # Your plugin
│   └── patterns/
│       └── my_automaton/     # Pattern files
│           ├── pattern1.npy
│           └── pattern2.npy
```

### Plugin Components

**1. Automaton Class**
```python
class MyAutomaton:
    def __init__(self, width, height):
        # Initialize grid and state
        pass
    
    def step(self):
        # Evolution logic
        pass
```

**2. Pattern Definitions**
```python
PATTERNS = {
    'pattern_name': {
        'grid': np.array(...),
        'description': 'What it does'
    }
}
```

**3. Plugin Registration**
```python
# In plugins/__init__.py
from .my_automaton import MyAutomaton
PLUGINS['my_automaton'] = MyAutomaton
```

---

## Part 2: Your First Plugin

### Step 1: Create File

Create `plugins/my_ca.py`:

```python
"""
My Custom Cellular Automaton
A simple example plugin for CALab
"""

import numpy as np


class MyCA:
    """
    Simple 2-state CA with custom rules
    """
    
    def __init__(self, width=100, height=100, pattern='single'):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)
        self.num_states = 2
        
        # Load initial pattern
        if pattern in PATTERNS:
            self._load_pattern(pattern)
    
    def _load_pattern(self, pattern_name):
        """Load initial pattern"""
        pattern_data = PATTERNS[pattern_name]
        pattern = pattern_data['grid']
        
        # Center pattern on grid
        ph, pw = pattern.shape
        y = (self.height - ph) // 2
        x = (self.width - pw) // 2
        
        self.grid[y:y+ph, x:x+pw] = pattern
    
    def step(self):
        """Execute one evolution step"""
        new_grid = self.grid.copy()
        
        for y in range(self.height):
            for x in range(self.width):
                # Count neighbors (Moore neighborhood)
                neighbors = self._count_neighbors(x, y)
                
                # Apply rules
                if self.grid[y, x] == 0:
                    # Birth rule: 3 neighbors
                    if neighbors == 3:
                        new_grid[y, x] = 1
                else:
                    # Survival rule: 2 or 3 neighbors
                    if neighbors not in [2, 3]:
                        new_grid[y, x] = 0
        
        self.grid = new_grid
    
    def _count_neighbors(self, x, y):
        """Count alive neighbors (Moore)"""
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                nx = (x + dx) % self.width
                ny = (y + dy) % self.height
                
                if self.grid[ny, nx] == 1:
                    count += 1
        
        return count
    
    def get_grid(self):
        """Return current grid state"""
        return self.grid.copy()


# Pattern definitions
PATTERNS = {
    'single': {
        'grid': np.array([[1]], dtype=np.uint8),
        'description': 'Single cell'
    },
    'block': {
        'grid': np.array([
            [1, 1],
            [1, 1]
        ], dtype=np.uint8),
        'description': 'Stable 2x2 block'
    },
    'blinker': {
        'grid': np.array([
            [1, 1, 1]
        ], dtype=np.uint8),
        'description': 'Period-2 oscillator'
    }
}


# Plugin metadata
PLUGIN_INFO = {
    'name': 'My Custom CA',
    'author': 'Your Name',
    'version': '1.0.0',
    'description': 'Example custom automaton',
    'num_states': 2,
    'patterns': list(PATTERNS.keys())
}


def create_automaton(width=100, height=100, pattern='single'):
    """Factory function for creating automaton"""
    return MyCA(width, height, pattern)
```

### Step 2: Register Plugin

Edit `plugins/__init__.py`, add:

```python
from .my_ca import create_automaton as my_ca_create

PLUGINS['my_ca'] = my_ca_create

PLUGIN_INFO['my_ca'] = {
    'name': 'My Custom CA',
    'description': 'Example custom automaton',
    'category': 'Custom'
}
```

### Step 3: Test Plugin

```python
# Test your plugin
from plugins import get_plugin

# Create automaton
plugin = get_plugin('my_ca')
auto = plugin(width=50, height=50, pattern='blinker')

# Run simulation
for i in range(10):
    print(f"Step {i}")
    auto.step()
    print(auto.get_grid())
```

---

## Part 3: Advanced Features

### Multi-State Automaton

```python
class MultiStateCA:
    def __init__(self, width=100, height=100, num_states=3):
        self.width = width
        self.height = height
        self.num_states = num_states
        self.grid = np.zeros((height, width), dtype=np.uint8)
    
    def step(self):
        """Cycle through states"""
        new_grid = self.grid.copy()
        
        for y in range(self.height):
            for x in range(self.width):
                current = self.grid[y, x]
                neighbors = self._count_state_neighbors(x, y, 
                                                       (current + 1) % self.num_states)
                
                # Rule: advance if neighbor has next state
                if neighbors > 0:
                    new_grid[y, x] = (current + 1) % self.num_states
        
        self.grid = new_grid
```

### Table-Based Rules

```python
class TableBasedCA:
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)
        self.rules = self._init_rules()
    
    def _init_rules(self):
        """Define rule table"""
        rules = {}
        
        # Format: (center, north, east, south, west) -> next_state
        rules[(0, 1, 0, 0, 0)] = 1
        rules[(1, 0, 0, 0, 0)] = 1
        rules[(1, 1, 0, 0, 0)] = 2
        # ... more rules
        
        return rules
    
    def step(self):
        """Apply rule table"""
        new_grid = self.grid.copy()
        
        for y in range(self.height):
            for x in range(self.width):
                # Get neighborhood (von Neumann)
                c = self.grid[y, x]
                n = self.grid[(y-1) % self.height, x]
                e = self.grid[y, (x+1) % self.width]
                s = self.grid[(y+1) % self.height, x]
                w = self.grid[y, (x-1) % self.width]
                
                # Look up in rule table
                pattern = (c, n, e, s, w)
                if pattern in self.rules:
                    new_grid[y, x] = self.rules[pattern]
        
        self.grid = new_grid
```

### Optimized Evolution

```python
class OptimizedCA:
    def step_numpy(self):
        """Vectorized evolution using NumPy"""
        # Use array operations instead of loops
        
        # Roll array to get neighbors
        north = np.roll(self.grid, 1, axis=0)
        south = np.roll(self.grid, -1, axis=0)
        east = np.roll(self.grid, -1, axis=1)
        west = np.roll(self.grid, 1, axis=1)
        
        # Count neighbors
        neighbors = (north + south + east + west + 
                    np.roll(north, 1, axis=1) +  # NW
                    np.roll(north, -1, axis=1) +  # NE
                    np.roll(south, 1, axis=1) +   # SW
                    np.roll(south, -1, axis=1))   # SE
        
        # Apply rules (vectorized)
        birth = (self.grid == 0) & (neighbors == 3)
        survive = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        
        self.grid = np.where(birth | survive, 1, 0).astype(np.uint8)
```

---

## Part 4: Pattern Management

### Creating Patterns

```python
def create_pattern(name, grid, description):
    """
    Create and save a pattern
    
    Args:
        name: Pattern identifier
        grid: NumPy array
        description: Human-readable description
    """
    pattern = {
        'grid': grid,
        'description': description,
        'size': grid.shape,
        'density': np.count_nonzero(grid) / grid.size
    }
    
    # Save to file
    pattern_dir = f'plugins/patterns/my_ca'
    os.makedirs(pattern_dir, exist_ok=True)
    np.save(f'{pattern_dir}/{name}.npy', grid)
    
    return pattern
```

### Loading Patterns

```python
def load_pattern_from_file(filename):
    """Load pattern from .npy file"""
    grid = np.load(filename)
    return grid

def load_all_patterns(automaton_name):
    """Load all patterns for an automaton"""
    pattern_dir = f'plugins/patterns/{automaton_name}'
    patterns = {}
    
    if os.path.exists(pattern_dir):
        for file in os.listdir(pattern_dir):
            if file.endswith('.npy'):
                name = file[:-4]  # Remove .npy
                grid = np.load(os.path.join(pattern_dir, file))
                patterns[name] = {
                    'grid': grid,
                    'description': f'Pattern: {name}'
                }
    
    return patterns
```

---

## Part 5: Color Schemes

### Define Colors

```python
def get_colormap(num_states):
    """
    Return colormap for visualization
    
    Returns:
        List of (R, G, B) tuples
    """
    if num_states == 2:
        # Binary: black and green
        return [
            (0, 0, 0),      # State 0: black
            (0, 255, 0)     # State 1: green
        ]
    
    elif num_states == 3:
        # Three states
        return [
            (0, 0, 0),      # State 0: black
            (255, 255, 255), # State 1: white
            (0, 100, 255)   # State 2: blue
        ]
    
    else:
        # Generate gradient
        colors = []
        for i in range(num_states):
            # HSV to RGB conversion for rainbow
            h = i / num_states
            r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
            colors.append((int(r*255), int(g*255), int(b*255)))
        return colors
```

---

## Part 6: Testing and Debugging

### Unit Tests

```python
import unittest

class TestMyCA(unittest.TestCase):
    def setUp(self):
        """Create automaton for testing"""
        self.ca = MyCA(width=10, height=10, pattern='single')
    
    def test_initialization(self):
        """Test automaton initializes correctly"""
        self.assertEqual(self.ca.width, 10)
        self.assertEqual(self.ca.height, 10)
        self.assertEqual(self.ca.num_states, 2)
    
    def test_evolution(self):
        """Test one evolution step"""
        initial = self.ca.get_grid().copy()
        self.ca.step()
        after = self.ca.get_grid()
        
        # Grid should change
        self.assertFalse(np.array_equal(initial, after))
    
    def test_pattern_loading(self):
        """Test pattern loads correctly"""
        ca = MyCA(width=10, height=10, pattern='block')
        grid = ca.get_grid()
        
        # Should have 4 cells alive (2x2 block)
        self.assertEqual(np.count_nonzero(grid), 4)

if __name__ == '__main__':
    unittest.main()
```

### Debug Helpers

```python
def debug_neighborhood(self, x, y):
    """Print neighborhood for debugging"""
    print(f"Cell ({x}, {y}):")
    print(f"  Center: {self.grid[y, x]}")
    print(f"  North:  {self.grid[(y-1) % self.height, x]}")
    print(f"  East:   {self.grid[y, (x+1) % self.width]}")
    print(f"  South:  {self.grid[(y+1) % self.height, x]}")
    print(f"  West:   {self.grid[y, (x-1) % self.width]}")
    print(f"  Neighbors: {self._count_neighbors(x, y)}")

def visualize_step(self):
    """Print ASCII visualization"""
    print("\n" + "="*self.width)
    for row in self.grid:
        print(''.join('█' if cell else '.' for cell in row))
    print("="*self.width + "\n")
```

---

## Part 7: Integration

### Plugin Metadata

```python
# Required metadata for CALab integration
PLUGIN_METADATA = {
    'name': 'My Automaton',
    'version': '1.0.0',
    'author': 'Your Name',
    'description': 'Custom cellular automaton',
    
    # Technical specs
    'num_states': 2,
    'neighborhood': 'moore',  # or 'von_neumann'
    'boundary': 'periodic',   # or 'fixed'
    
    # Patterns
    'patterns': {
        'pattern_name': 'Description'
    },
    
    # Category for organization
    'category': 'custom',  # or 'life-like', 'wave', etc.
    
    # Optional features
    'configurable_states': False,
    'configurable_rules': False,
    'supports_import': True
}
```

### Registration

```python
# In plugins/__init__.py

# Import your plugin
from .my_ca import create_automaton, PLUGIN_METADATA

# Register in plugin dictionary
PLUGINS['my_ca'] = create_automaton

# Register metadata
PLUGIN_INFO['my_ca'] = PLUGIN_METADATA

# Add to category
if PLUGIN_METADATA['category'] not in PLUGIN_CATEGORIES:
    PLUGIN_CATEGORIES[PLUGIN_METADATA['category']] = []
PLUGIN_CATEGORIES[PLUGIN_METADATA['category']].append('my_ca')
```

---

## Part 8: Advanced Examples

### Example 1: Brian's Brain Clone

```python
class BriansBrainClone:
    """
    Three-state automaton:
    0 = Dead, 1 = Alive, 2 = Dying
    """
    
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)
        self.num_states = 3
    
    def step(self):
        new_grid = np.zeros_like(self.grid)
        
        for y in range(self.height):
            for x in range(self.width):
                current = self.grid[y, x]
                
                if current == 1:
                    # Alive → Dying
                    new_grid[y, x] = 2
                
                elif current == 2:
                    # Dying → Dead
                    new_grid[y, x] = 0
                
                else:  # current == 0
                    # Dead → Alive if exactly 2 alive neighbors
                    alive_neighbors = self._count_alive_neighbors(x, y)
                    if alive_neighbors == 2:
                        new_grid[y, x] = 1
        
        self.grid = new_grid
    
    def _count_alive_neighbors(self, x, y):
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.width
                ny = (y + dy) % self.height
                if self.grid[ny, nx] == 1:
                    count += 1
        return count
```

### Example 2: Configurable Life-like

```python
class ConfigurableLife:
    """
    Life-like automaton with configurable B/S rules
    """
    
    def __init__(self, width=100, height=100, 
                 birth=[3], survival=[2, 3]):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)
        self.birth = set(birth)
        self.survival = set(survival)
        self.num_states = 2
    
    def step(self):
        new_grid = self.grid.copy()
        
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self._count_neighbors(x, y)
                
                if self.grid[y, x] == 0:
                    # Birth rule
                    if neighbors in self.birth:
                        new_grid[y, x] = 1
                else:
                    # Survival rule
                    if neighbors not in self.survival:
                        new_grid[y, x] = 0
        
        self.grid = new_grid
    
    def _count_neighbors(self, x, y):
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.width
                ny = (y + dy) % self.height
                if self.grid[ny, nx] == 1:
                    count += 1
        return count
```

---

## Part 9: Best Practices

### Code Style

```python
# Good: Clear, documented
class MyCA:
    """My cellular automaton implementation"""
    
    def __init__(self, width, height):
        """
        Initialize automaton
        
        Args:
            width: Grid width
            height: Grid height
        """
        self.width = width
        self.height = height
    
    def step(self):
        """Execute one evolution step"""
        # Implementation...
        pass

# Bad: Unclear, undocumented
class MCA:
    def __init__(self, w, h):
        self.w = w
        self.h = h
    
    def s(self):
        # ???
        pass
```

### Performance

✅ **Do**:
- Use NumPy arrays
- Vectorize when possible
- Avoid nested loops for large grids
- Profile slow sections
- Cache repeated calculations

❌ **Don't**:
- Use Python lists for grids
- Recalculate same values
- Ignore performance
- Optimize prematurely

### Error Handling

```python
def create_automaton(width, height, pattern=None):
    """Create automaton with validation"""
    
    # Validate inputs
    if width < 10 or width > 1000:
        raise ValueError("Width must be between 10 and 1000")
    
    if height < 10 or height > 1000:
        raise ValueError("Height must be between 10 and 1000")
    
    if pattern and pattern not in PATTERNS:
        raise KeyError(f"Unknown pattern: {pattern}")
    
    # Create automaton
    return MyCA(width, height, pattern)
```

---

## Part 10: Distribution

### Documentation

Create `plugins/my_ca/README.md`:

```markdown
# My Custom CA

## Description
Brief description of your automaton

## Rules
Explain the rules clearly

## Patterns
List available patterns with descriptions

## Usage
```python
from plugins import get_plugin
auto = get_plugin('my_ca')(width=100, height=100)
auto.step()
```

## Examples
Show interesting examples

## Author
Your name and contact
```

### Sharing

```bash
# Create package
cd plugins
tar -czf my_ca_plugin.tar.gz my_ca.py patterns/my_ca/

# Share file
# Users extract to their plugins/ directory
```

---

## Quick Reference

### Minimum Requirements

```python
class MinimalPlugin:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)
        self.num_states = 2
    
    def step(self):
        # Evolution logic
        pass
    
    def get_grid(self):
        return self.grid.copy()

PATTERNS = {
    'default': {
        'grid': np.array([[1]]),
        'description': 'Default pattern'
    }
}

def create_automaton(width=100, height=100, pattern='default'):
    return MinimalPlugin(width, height)
```

---

## Troubleshooting

**Import errors**: Check `__init__.py` registration
**Pattern not loading**: Verify pattern format
**Slow evolution**: Profile and optimize
**Wrong behavior**: Add debug prints

---

## Next Steps

**Study Examples**: Read existing plugins
**Start Simple**: Begin with 2-state CA
**Test Thoroughly**: Write unit tests
**Share**: Contribute to community!

---

**Create the automaton of your dreams!** 🚀✨
