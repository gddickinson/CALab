# CALab Plugin Reference Guide

Complete guide to all available cellular automata plugins.

---

## 🔬 Available Plugins

### 1. Langton's Loop
**File**: `plugins/langton_loop.py`

**Description**: Self-replicating cellular automaton based on Chris Langton's simplified version of von Neumann's universal constructor.

**States**: 8 states
- 0: Background (empty)
- 1: Sheath (structural)
- 2: Core (data carrier)
- 3-7: Construction states

**Neighborhood**: von Neumann (4-connected)

**Rules**: 63 transition rules (subset of original 219)

**Patterns**:
- `basic_loop`: Basic 9x9 loop structure
- `extended_loop`: Loop with construction arm

**Best For**: Understanding self-replication, computational theory

**Typical Behavior**: Growing (extends and attempts replication)

**Example**:
```python
from plugins.langton_loop import LangtonLoopPlugin

automaton = LangtonLoopPlugin.create_automaton(150, 150, pattern='basic_loop')
for _ in range(100):
    automaton.step()
```

---

### 2. Wire World
**File**: `plugins/wireworld.py`

**Description**: Circuit simulation automaton perfect for demonstrating electronic logic and signal propagation.

**States**: 4 states
- 0: Empty
- 1: Wire (conductor)
- 2: Electron head
- 3: Electron tail

**Neighborhood**: Moore (8-connected)

**Rules**: 
- Empty → Empty
- Head → Tail
- Tail → Wire  
- Wire → Head (if 1-2 heads nearby)

**Patterns**:
- `simple_circuit`: Circular wire with electrons
- `or_gate`: OR logic gate
- `diode`: One-way conductor
- `clock`: Clock signal generator

**Best For**: Circuit simulation, logic gates, education

**Typical Behavior**: Stable oscillation (electrons circulate)

**Example**:
```python
from plugins.wireworld import WireWorldPlugin

automaton = WireWorldPlugin.create_automaton(150, 150, pattern='simple_circuit')
for _ in range(100):
    automaton.step()
```

---

### 3. Conway's Game of Life
**File**: `plugins/game_of_life.py`

**Description**: The most famous cellular automaton, demonstrating emergence and complexity from simple rules.

**States**: 2 states (alive/dead)

**Neighborhood**: Moore (8-connected)

**Rules** (B3/S23):
- Birth: dead cell with exactly 3 neighbors becomes alive
- Survival: live cell with 2-3 neighbors survives
- Death: all other cases

**Patterns**:
- `glider_gun`: Gosper's Glider Gun (creates gliders)
- `glider`: Simple traveling pattern
- `pulsar`: Period-3 oscillator
- `pentadecathlon`: Period-15 oscillator
- `lightweight_spaceship`: LWSS (faster spaceship)
- `r_pentomino`: Chaotic methuselah (stabilizes at gen 1103)
- `diehard`: Dies after 130 generations
- `acorn`: Stabilizes after 5206 generations
- `random`: Random soup

**Best For**: Understanding emergence, pattern formation, computational universality

**Typical Behavior**: Varies by pattern (oscillating, growing, chaotic, stable)

**Example**:
```python
from plugins.game_of_life import GameOfLifePlugin

# Create glider gun
automaton = GameOfLifePlugin.create_automaton(150, 150, pattern='glider_gun')
for _ in range(100):
    automaton.step()
    
# Watch gliders spawn and travel
```

---

### 4. Brian's Brain
**File**: `plugins/brians_brain.py`

**Description**: Beautiful three-state automaton creating propagating wave patterns. Named after Brian Silverman.

**States**: 3 states
- 0: Dead (off)
- 1: Alive (on)
- 2: Dying (refractory)

**Neighborhood**: Moore (8-connected)

**Rules**:
- Dead + 2 alive neighbors → Alive
- Alive → Always dying
- Dying → Always dead

**Patterns**:
- `random`: Random soup (creates beautiful waves)
- `circle`: Expanding circle wave
- `lines`: Parallel wave sources
- `cross`: Cross pattern
- `glider`: Moving pattern
- `gun`: Wave generator
- `spiral`: Spiral wave source

**Best For**: Visual appeal, wave dynamics, aesthetics

**Typical Behavior**: Oscillating/chaotic (propagating waves)

**Example**:
```python
from plugins.brians_brain import BriansBrainPlugin

# Create beautiful wave patterns
automaton = BriansBrainPlugin.create_automaton(150, 150, pattern='spiral')
for _ in range(100):
    automaton.step()
```

---

### 5. Seeds
**File**: `plugins/seeds.py`

**Description**: Explosive automaton (B2/S) where every pattern dies immediately after birth, creating fractal-like structures.

**States**: 2 states (alive/dead)

**Neighborhood**: Moore (8-connected)

**Rules** (B2/S):
- Birth: dead cell with exactly 2 neighbors becomes alive
- Death: ALL alive cells die (no survival)

**Patterns**:
- `single_cell`: Single cell explosion
- `line`: Line explosion
- `cross`: Cross explosion
- `random`: Random seed pattern
- `serviette`: Famous 2x2 pattern
- `two_cells`: Two adjacent cells

**Best For**: Understanding explosive growth, fractals, ephemeral patterns

**Typical Behavior**: Growing (explosive expansion)

**Example**:
```python
from plugins.seeds import SeedsPlugin

# Watch explosive fractal growth
automaton = SeedsPlugin.create_automaton(150, 150, pattern='serviette')
for _ in range(30):  # Fast explosion!
    automaton.step()
```

---

## 🎯 Quick Comparison

| Automaton | States | Neighborhood | Typical Behavior | Visual Appeal | Complexity |
|-----------|--------|--------------|------------------|---------------|------------|
| Langton's Loop | 8 | von Neumann | Growing | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Wire World | 4 | Moore | Stable | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Game of Life | 2 | Moore | Varies | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Brian's Brain | 3 | Moore | Chaotic | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Seeds | 2 | Moore | Growing | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 📊 Usage Patterns

### For Education
1. **Game of Life**: Classic introduction to CA
2. **Wire World**: Demonstrate logic and computation
3. **Langton's Loop**: Self-replication and complexity

### For Visual Art
1. **Brian's Brain**: Beautiful wave patterns
2. **Seeds**: Fractal explosions
3. **Wire World**: Circuit aesthetics

### For Research
1. **Langton's Loop**: Self-replication studies
2. **Game of Life**: Computational universality
3. **Custom plugins**: Implement your own rules

---

## 🚀 Running the Demos

### Test Single Plugin
```bash
python demo.py  # Langton's Loop demo
```

### Test All Plugins
```bash
python demo_all.py  # Interactive showcase
```

### In Your Code
```python
from plugins import PLUGIN_REGISTRY

# Get a plugin
plugin = PLUGIN_REGISTRY['wireworld']

# Create automaton
automaton = plugin.create_automaton(150, 150)

# Run simulation
for _ in range(100):
    automaton.step()
    stats = automaton.compute_statistics()
    print(f"Gen {automaton.generation}: {stats['density']:.2f}% density")
```

---

## 🎨 Color Schemes

Each plugin has a custom colormap:

**Langton's Loop**:
- Black (background), White (sheath), Red (core), Green (arm), Blue+ (special states)

**Wire World**:
- Black (empty), Yellow (wire), Blue (electron head), Red (electron tail)

**Game of Life**:
- Black (dead), Green (alive)

**Brian's Brain**:
- Black (dead), Green (alive), Blue (dying)

**Seeds**:
- Black (dead), Orange (alive)

---

## 🔧 Creating Your Own Plugin

1. Copy a similar plugin as template
2. Implement the rules in `step()`
3. Add patterns in `initialize_pattern()`
4. Define colormap in `get_colormap()`
5. Add to `plugins/__init__.py`

Example minimal plugin:
```python
from core.automaton_base import CellularAutomaton, PluginInterface, AutomatonMetadata, NeighborhoodType

class MyAutomaton(CellularAutomaton):
    def __init__(self, width, height):
        metadata = AutomatonMetadata(
            name="My Automaton",
            description="My custom rules",
            author="You",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.MOORE
        )
        super().__init__(width, height, metadata)
    
    def step(self):
        # Implement your rules here
        pass
    
    def initialize_pattern(self, pattern_name, **kwargs):
        # Initialize grid
        pass

class MyPlugin(PluginInterface):
    @staticmethod
    def get_metadata():
        return MyAutomaton(1, 1).metadata
    
    @staticmethod
    def create_automaton(width, height, **kwargs):
        automaton = MyAutomaton(width, height)
        automaton.initialize_pattern(kwargs.get('pattern', 'default'))
        return automaton
    
    @staticmethod
    def get_default_patterns():
        return {'default': {'description': 'Default pattern'}}
    
    @staticmethod
    def get_colormap():
        return ['#000000', '#00FF00']
```

---

## 📚 Further Reading

- **Langton's Loop**: Langton, C. (1984). "Self-reproduction in cellular automata"
- **Wire World**: Brian Silverman's original description
- **Game of Life**: Gardner, M. (1970). "Mathematical Games" column
- **Brian's Brain**: Brian Silverman's creation
- **Seeds**: Part of the larger B/S automata family

---

## ✅ Plugin Checklist

When implementing a new plugin:

- [ ] Implements `CellularAutomaton` or `RuleBasedAutomaton`
- [ ] Implements `PluginInterface`
- [ ] Has proper `step()` method
- [ ] Has `initialize_pattern()` method
- [ ] Has custom `get_colormap()`
- [ ] Includes multiple patterns
- [ ] Has comprehensive docstrings
- [ ] Added to `PLUGIN_REGISTRY`
- [ ] Tested with demo script
- [ ] Documented in this guide

---

**All plugins are production-ready and fully functional! 🎉**
