# File Formats Reference

Complete specification of all file formats used in CALab.

---

## Pattern Files (.npy)

### Format

NumPy binary format for 2D arrays.

**Extension**: `.npy`

**Structure**:
```
NumPy array of shape (height, width)
dtype: uint8
Values: State numbers (0 to num_states-1)
```

### Creating Pattern Files

```python
import numpy as np

# Create pattern
pattern = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1]
], dtype=np.uint8)

# Save
np.save('glider.npy', pattern)
```

### Loading Pattern Files

```python
import numpy as np

# Load
pattern = np.load('glider.npy')

print(pattern.shape)  # (3, 3)
print(pattern.dtype)  # uint8
```

### Directory Structure

```
plugins/patterns/
├── game_of_life/
│   ├── glider.npy
│   ├── blinker.npy
│   └── pulsar.npy
├── wireworld/
│   ├── simple_circuit.npy
│   └── or_gate.npy
└── ...
```

---

## Rule Files (.json)

### Format

JSON format for custom rules.

**Extension**: `.json`

**Schema**:
```json
{
  "metadata": {
    "name": "My Rule",
    "author": "Your Name",
    "version": "1.0",
    "num_states": 2,
    "rule_type": "totalistic | table-based"
  },
  "rules": [
    {
      "pattern": [0, 1, 1, 1, 0],
      "result": 1
    }
  ]
}
```

### Totalistic Rule Format

```json
{
  "metadata": {
    "name": "Game of Life",
    "num_states": 2,
    "rule_type": "totalistic",
    "birth": "3",
    "survival": "23"
  }
}
```

**Fields**:
- `birth`: String of neighbor counts for birth
- `survival`: String of neighbor counts for survival

**Example**: B3/S23 → `"birth": "3", "survival": "23"`

### Table-Based Rule Format

```json
{
  "metadata": {
    "name": "Custom Rules",
    "num_states": 3,
    "rule_type": "table-based"
  },
  "rules": [
    {
      "pattern": [0, 1, 0, 0, 0],
      "result": 1,
      "description": "Dead with north neighbor becomes alive"
    },
    {
      "pattern": [1, 0, 0, 0, 0],
      "result": 1,
      "description": "Alive stays alive"
    }
  ]
}
```

**Pattern Format**: `[center, north, east, south, west]`

### Creating Rule Files

```python
import json

rule_data = {
    "metadata": {
        "name": "My Custom Rule",
        "author": "Me",
        "version": "1.0",
        "num_states": 2,
        "rule_type": "totalistic",
        "birth": "3",
        "survival": "23"
    }
}

with open('my_rule.json', 'w') as f:
    json.dump(rule_data, f, indent=2)
```

### Loading Rule Files

```python
import json

with open('my_rule.json', 'r') as f:
    rule_data = json.load(f)

birth = rule_data['metadata']['birth']
survival = rule_data['metadata']['survival']
```

---

## Simulation State Files (.pkl)

### Format

Python pickle format for complete state.

**Extension**: `.pkl`

**Contents**:
```python
{
    'automaton_type': str,      # Plugin name
    'grid': np.ndarray,         # Current state
    'width': int,
    'height': int,
    'num_states': int,
    'generation': int,          # Current step
    'pattern_name': str,        # Initial pattern
    'metadata': dict            # Additional info
}
```

### Saving Simulation

```python
import pickle

state = {
    'automaton_type': 'game_of_life',
    'grid': automaton.get_grid(),
    'width': 150,
    'height': 150,
    'num_states': 2,
    'generation': 347,
    'pattern_name': 'glider',
    'metadata': {
        'created': '2024-12-22',
        'notes': 'Interesting pattern'
    }
}

with open('simulation.pkl', 'wb') as f:
    pickle.dump(state, f)
```

### Loading Simulation

```python
import pickle

with open('simulation.pkl', 'rb') as f:
    state = pickle.load(f)

# Reconstruct automaton
from plugins import get_plugin
plugin = get_plugin(state['automaton_type'])
auto = plugin(state['width'], state['height'])
auto.grid = state['grid']
```

---

## Diagnostic Reports (.json)

### Format

JSON format for analysis results.

**Extension**: `.json` or `.txt` (formatted)

**Schema**:
```json
{
  "timestamp": "2024-12-22T15:30:45",
  "automaton": {
    "name": "Conway's Game of Life",
    "states": 2,
    "neighborhood": "moore"
  },
  "pattern": {
    "name": "glider",
    "initial_density": 1.2
  },
  "metrics": {
    "generation": 347,
    "runtime_seconds": 5.2,
    "classification": "COMPLEX",
    "current_density": 23.4,
    "average_density": 18.7,
    "current_entropy": 0.84,
    "average_entropy": 0.76,
    "state_distribution": {
      "0": 18234,
      "1": 4266
    }
  },
  "events": [
    {
      "timestamp": "12:34:56",
      "type": "INFO",
      "message": "Simulation started"
    },
    {
      "timestamp": "12:35:02",
      "type": "INFO",
      "message": "Generation 100 reached"
    }
  ]
}
```

### Creating Diagnostic Report

```python
import json
from datetime import datetime

report = {
    "timestamp": datetime.now().isoformat(),
    "automaton": {
        "name": "Game of Life",
        "states": 2,
        "neighborhood": "moore"
    },
    "metrics": {
        "generation": generation,
        "classification": classification,
        "current_density": density,
        # ... more metrics
    },
    "events": events_list
}

with open('diagnostic.json', 'w') as f:
    json.dump(report, f, indent=2)
```

---

## Configuration Files (.ini)

### Format

INI format for application settings.

**Extension**: `.ini`

**Structure**:
```ini
[display]
grid_size = 150
speed = 150
show_grid_lines = true
theme = light

[simulation]
default_automaton = game_of_life
default_pattern = glider
auto_start = false

[performance]
use_gpu = false
max_fps = 60
cache_size = 100

[paths]
pattern_dir = plugins/patterns
save_dir = saves
export_dir = exports
```

### Reading Configuration

```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

grid_size = config.getint('display', 'grid_size')
speed = config.getint('display', 'speed')
default_auto = config.get('simulation', 'default_automaton')
```

### Writing Configuration

```python
import configparser

config = configparser.ConfigParser()

config['display'] = {
    'grid_size': '150',
    'speed': '150',
    'show_grid_lines': 'true'
}

config['simulation'] = {
    'default_automaton': 'game_of_life',
    'default_pattern': 'glider'
}

with open('config.ini', 'w') as f:
    config.write(f)
```

---

## Export Formats

### PNG Images

**Format**: Standard PNG
**Usage**: Export visualizations

```python
import matplotlib.pyplot as plt

# Visualize grid
plt.figure(figsize=(10, 10))
plt.imshow(grid, cmap='binary', interpolation='nearest')
plt.axis('off')
plt.savefig('state.png', dpi=300, bbox_inches='tight')
```

### GIF Animations

**Format**: Animated GIF
**Usage**: Export evolution

```python
from PIL import Image

frames = []
for i in range(100):
    automaton.step()
    # Convert grid to image
    img = grid_to_image(automaton.get_grid())
    frames.append(img)

frames[0].save('evolution.gif',
              save_all=True,
              append_images=frames[1:],
              duration=100,
              loop=0)
```

### CSV Data

**Format**: Comma-separated values
**Usage**: Export metrics

```csv
generation,density,entropy,active_cells
0,1.2,0.34,180
1,2.5,0.52,375
2,3.8,0.67,570
...
```

```python
import csv

with open('metrics.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['generation', 'density', 'entropy', 'active_cells'])
    
    for i in range(100):
        automaton.step()
        density = calculate_density(automaton.get_grid())
        entropy = calculate_entropy(automaton.get_grid())
        active = np.count_nonzero(automaton.get_grid())
        
        writer.writerow([i, density, entropy, active])
```

---

## Plugin Definition Files

### Plugin Python File

**Format**: Python module
**Location**: `plugins/plugin_name.py`

**Required Elements**:
```python
# Automaton class
class MyAutomaton:
    def __init__(self, width, height):
        pass
    
    def step(self):
        pass
    
    def get_grid(self):
        pass

# Patterns dictionary
PATTERNS = {
    'pattern_name': {
        'grid': np.array(...),
        'description': 'Description'
    }
}

# Metadata
PLUGIN_INFO = {
    'name': 'My Automaton',
    'author': 'Your Name',
    'version': '1.0.0',
    'description': 'Description',
    'num_states': 2
}

# Factory function
def create_automaton(width, height, pattern):
    return MyAutomaton(width, height)
```

### Plugin Metadata

**Location**: `plugins/__init__.py`

```python
PLUGINS['my_automaton'] = create_automaton

PLUGIN_INFO['my_automaton'] = {
    'name': 'My Automaton',
    'description': 'Brief description',
    'category': 'custom'
}

PLUGIN_CATEGORIES['custom'].append('my_automaton')
```

---

## File Naming Conventions

### Patterns

**Format**: `descriptive_name.npy`

**Examples**:
- `glider.npy`
- `glider_gun.npy`
- `pulsar_p3.npy`
- `lwss_east.npy`

**Guidelines**:
- Lowercase with underscores
- Descriptive names
- Include period if oscillator (e.g., `_p3`)
- Include direction if spaceship (e.g., `_east`)

### Rules

**Format**: `rule_description.json`

**Examples**:
- `life_b3s23.json`
- `highlife_b36s23.json`
- `custom_growth.json`

### Simulations

**Format**: `description_YYYYMMDD_HHMMSS.pkl`

**Examples**:
- `glider_test_20241222_153045.pkl`
- `experiment_1_20241222_160000.pkl`

### Exports

**Images**: `state_gen_0347.png`
**Animations**: `evolution_100steps.gif`
**Data**: `metrics_20241222.csv`

---

## Data Types and Sizes

### Grid Arrays

```python
# Small (50x50)
grid = np.zeros((50, 50), dtype=np.uint8)
# Size: 2.5 KB

# Medium (150x150)
grid = np.zeros((150, 150), dtype=np.uint8)
# Size: 22.5 KB

# Large (500x500)
grid = np.zeros((500, 500), dtype=np.uint8)
# Size: 250 KB
```

### State Types

```python
# 2 states: uint8 (0-1)
grid = np.zeros((h, w), dtype=np.uint8)

# 3-8 states: uint8 (0-7)
grid = np.zeros((h, w), dtype=np.uint8)

# 9-29 states: uint8 (0-28)
grid = np.zeros((h, w), dtype=np.uint8)

# Never use: int32, int64, float64
# (wastes 4-8x memory!)
```

---

## Compatibility

### Cross-Platform

All formats are cross-platform compatible:
- NumPy `.npy`: Binary but platform-independent
- JSON: Text format, universal
- Pickle: Python-specific but cross-platform
- PNG/GIF: Standard image formats
- CSV: Universal text format

### Version Compatibility

**NumPy**: Versions 1.18+ for `.npy` files
**Python**: 3.7+ for pickle protocol 4+
**JSON**: Universal (any JSON parser)

---

## Best Practices

### Patterns

✅ **Do**:
- Use `dtype=np.uint8` for states
- Keep patterns minimal (trim empty borders)
- Include description in metadata
- Use descriptive filenames

❌ **Don't**:
- Use float types for discrete states
- Include large empty borders
- Use generic names like "pattern1"
- Mix different automaton patterns

### Rules

✅ **Do**:
- Include full metadata
- Document each rule
- Use consistent formatting
- Validate before saving

❌ **Don't**:
- Omit metadata
- Leave rules undocumented
- Use inconsistent formats
- Skip validation

### Simulations

✅ **Do**:
- Include timestamp
- Save metadata
- Use compression for large files
- Regular backups

❌ **Don't**:
- Overwrite important saves
- Skip metadata
- Keep unnecessary history
- Forget to backup

---

## File Size Optimization

### Patterns

```python
# Remove empty borders
def trim_pattern(pattern):
    """Remove empty rows/columns"""
    # Find non-zero bounds
    rows = np.any(pattern, axis=1)
    cols = np.any(pattern, axis=0)
    
    # Trim
    return pattern[rows][:, cols]

# Before: 100x100 (10 KB)
# After: 10x10 (100 bytes)
```

### Simulations

```python
# Use compression
import gzip
import pickle

with gzip.open('sim.pkl.gz', 'wb') as f:
    pickle.dump(state, f)

# Can reduce size by 5-10x
```

---

## Validation

### Pattern Validation

```python
def validate_pattern(pattern):
    """Validate pattern array"""
    assert isinstance(pattern, np.ndarray)
    assert pattern.dtype == np.uint8
    assert len(pattern.shape) == 2
    assert pattern.shape[0] > 0
    assert pattern.shape[1] > 0
    assert np.min(pattern) >= 0
    assert np.max(pattern) < 256
```

### Rule Validation

```python
def validate_rule(rule_data):
    """Validate rule JSON"""
    assert 'metadata' in rule_data
    assert 'num_states' in rule_data['metadata']
    assert 'rule_type' in rule_data['metadata']
    
    if rule_data['metadata']['rule_type'] == 'totalistic':
        assert 'birth' in rule_data['metadata']
        assert 'survival' in rule_data['metadata']
```

---

## Quick Reference

### Common Operations

```python
# Save pattern
np.save('pattern.npy', grid)

# Load pattern
grid = np.load('pattern.npy')

# Save simulation
with open('sim.pkl', 'wb') as f:
    pickle.dump(state, f)

# Load simulation
with open('sim.pkl', 'rb') as f:
    state = pickle.load(f)

# Export image
plt.imsave('state.png', grid, cmap='binary')

# Export data
np.savetxt('data.csv', grid, delimiter=',')
```

---

## Further Reading

- [API Reference](api.md) - Function details
- [Plugin System](plugin_system.md) - Architecture
- [Creating Plugins](../tutorials/creating_plugins.md) - Tutorial

---

**Master all CALab file formats!** 📁
