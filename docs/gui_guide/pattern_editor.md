# Pattern Editor Guide

The **Pattern Editor** tab lets you visually design initial patterns for cellular automata!

---

## Overview

The Pattern Editor provides:
- **Visual canvas** for drawing patterns
- **Drawing tools** for manipulation
- **Pattern library** for saving/loading
- **Import/export** capabilities

---

## The Canvas

### Layout

**Left Side**: 30x30 drawing grid
**Right Side**: Tools and pattern library

### Drawing

**Click**: Place a cell
**Click and Drag**: Draw continuously
**State**: Choose which state to place (0-8)

### Grid Display

- **Black grid lines** separate cells
- **Colors** represent different states
- **Cell size**: 15 pixels each

---

## Drawing Controls

### State Selection

**Draw State Dropdown**
- Choose which state to draw
- State 0: Dead/Empty (black)
- State 1: Alive (green)
- State 2-8: Additional states (various colors)

**Number of States**
- Set how many states available (2-8)
- More states = more complex patterns
- Updates state dropdown automatically

**Grid Size**
- Adjust canvas size (10-50 cells)
- Larger = more complex patterns possible
- Smaller = easier to manage

---

## Drawing Tools

### 🗑️ Clear Canvas

**Action**: Erases entire grid
**Use when**: Starting fresh
**Tip**: Save first if you want to keep current pattern!

### ⬌ Mirror Horizontal

**Action**: Flips pattern left-right

**Example**:
```
Before:        After:
. . X .    →   . X . .
. X X .        . X X .
X . . .        . . . X
```

**Use for**:
- Creating symmetric patterns
- Debugging asymmetry
- Artistic effects

### ⬍ Mirror Vertical

**Action**: Flips pattern top-bottom

**Example**:
```
Before:        After:
X . .      →   . . X
. X .          . X .
. . X          X . .
```

**Use for**:
- Vertical symmetry
- Inverting patterns
- Combined with horizontal mirror

### ↻ Rotate 90°

**Action**: Rotates pattern clockwise

**Example**:
```
Before:        After:
X X .      →   X . .
. X .          X X .
. . .          . X .
```

**Use for**:
- Trying different orientations
- Finding stable rotations
- Creating rotating animations

### ◐ Invert

**Action**: Swaps states (max_state - current_state)

**Example (2 states)**:
```
Before (0/1):  After (1/0):
. X .      →   X . X
X X X          . . .
. X .          X . X
```

**Use for**:
- Positive/negative patterns
- Testing complementary patterns
- Artistic effects

---

## Pattern Library

### Saving Patterns

**Step 1**: Click "💾 Save"
**Step 2**: Enter pattern name
**Step 3**: Pattern saved to library

**Tips**:
- Use descriptive names ("glider", "gun", "block")
- Save variations ("glider_v2", "gun_large")
- Save before clearing canvas!

### Loading Patterns

**Step 1**: Select pattern from list
**Step 2**: Click "📂 Load"
**Step 3**: Pattern appears on canvas

**Tips**:
- Load before modifying (preserves original)
- Combine patterns by loading then adding
- Use as templates

### Deleting Patterns

**Step 1**: Select pattern from list
**Step 2**: Click "🗑️ Delete"
**Step 3**: Confirm deletion

**Warning**: Cannot be undone!

---

## Import/Export

### Exporting Patterns

**Purpose**: Save to file, share with others

**Step 1**: Click "📤 Export"
**Step 2**: Choose location
**Step 3**: Save as .npy file

**File Format**: NumPy array (.npy)
- Binary format
- Compact storage
- Easy to load

**Use Cases**:
- Backup important patterns
- Share with collaborators
- Version control
- Cross-platform transfer

### Importing Patterns

**Purpose**: Load patterns from files

**Step 1**: Click "📥 Import"
**Step 2**: Select .npy file
**Step 3**: Pattern loads to canvas

**Tips**:
- Check grid size matches
- Verify state count compatible
- Preview before saving to library

---

## Pattern Design Techniques

### Symmetric Patterns

**Method 1: Quadrant Design**
```
1. Draw upper-left quadrant
2. Mirror horizontal → upper-right
3. Select all and mirror vertical → bottom
```

**Method 2: Axis Design**
```
1. Draw along horizontal axis
2. Mirror vertical → complete pattern
```

**Use for**:
- Stable structures
- Balanced growth
- Aesthetic appeal

### Minimal Patterns

**Goal**: Smallest pattern with desired behavior

**Approach**:
```
1. Start with large pattern
2. Remove cells one by one
3. Test after each removal
4. Keep removing until behavior changes
```

**Examples**:
- Glider: 5 cells minimum
- Blinker: 3 cells
- Block: 4 cells

### Asymmetric Patterns

**Purpose**: Create directional behavior

**Techniques**:
- Weight one side heavier
- Use odd numbers
- Create imbalance

**Examples**:
- Spaceships (move in direction)
- Waves (propagate directionally)
- Growth (expand one way)

### Dense Patterns

**Purpose**: High initial activity

**Method**:
- Fill large areas
- Use checkerboard patterns
- Random-like placement

**Use for**:
- Testing rule behavior
- Creating chaos
- Soup experiments

### Sparse Patterns

**Purpose**: Minimal starting conditions

**Method**:
- Single cells
- Small clusters
- Distant groups

**Use for**:
- Clean evolution
- Tracking growth
- Identifying emergent structures

---

## Pattern Types

### Still Lifes

**Definition**: Patterns that don't change

**Examples**:
```
Block (2x2):
X X
X X

Beehive:
. X X .
X . . X
. X X .

Loaf:
. X X .
X . . X
. X . X
. . X .
```

**Design Tips**:
- Balance all cells
- Each cell sees 2-3 neighbors (Life)
- Test stability

### Oscillators

**Definition**: Patterns that repeat

**Period**: Number of steps to repeat
- Period 2: Blinker
- Period 3: Pulsar
- Period N: Complex oscillators

**Design Tips**:
- Create imbalance that reverses
- Use symmetric base
- Test multiple periods

### Spaceships

**Definition**: Patterns that move

**Examples**:
```
Glider (diagonal):
. X .
. . X
X X X

LWSS (horizontal):
. X . . X
X . . . .
X . . . X
X X X X .
```

**Design Tips**:
- Create thrust in one direction
- Balance to prevent spinning
- Test velocity

### Guns

**Definition**: Patterns that create other patterns

**Complexity**: Usually large and complex

**Design**:
1. Start with oscillators
2. Add reflecting patterns
3. Time collisions
4. Create periodic emissions

---

## Common Patterns to Try

### Game of Life Patterns

**Glider** (5 cells):
```
. X .
. . X
X X X
```

**Blinker** (3 cells):
```
X X X  ←→  . X .
            . X .
            . X .
```

**Toad** (6 cells):
```
. X X X    X X .
X X X .    . X X
```

**Beacon** (6 cells):
```
X X . .
X X . .
. . X X
. . X X
```

### Seeds Patterns

**Serviette** (2x2):
```
X X
X X
```
Creates explosive growth!

**Two Cells**:
```
X X
```
Simple but effective

### Brian's Brain

**Circle**:
```
. X X X .
X . . . X
X . . . X
X . . . X
. X X X .
```

**Cross**:
```
. . X . .
. . X . .
X X X X X
. . X . .
. . X . .
```

---

## Advanced Techniques

### Pattern Arithmetic

**Addition**: Place multiple patterns
- Draw first pattern
- Draw second pattern nearby
- Watch interaction

**Subtraction**: Remove from pattern
- Load pattern
- Use state 0 to "erase"
- Create gaps

### Pattern Libraries

**Organize by Type**:
- `glider_SE` (southeast glider)
- `glider_NW` (northwest glider)
- `osc_p2_blinker` (period 2 oscillator)
- `still_block` (still life)

**Version Control**:
- Save iterations: `gun_v1`, `gun_v2`, `gun_v3`
- Track improvements
- Compare versions

### Testing Patterns

**Systematic Testing**:
1. Create pattern
2. Test in simulation (50 steps)
3. Observe behavior
4. Note: stable/oscillating/moving/dying
5. Refine and repeat

**Iteration Process**:
```
Design → Test → Analyze → Refine → Repeat
```

---

## Workflow Examples

### Workflow 1: Create Spaceship

```
1. Start with symmetric pattern
2. Add asymmetry in one direction
3. Test in simulation
4. Observe: Does it move? Correct direction?
5. Adjust weights
6. Repeat until moves cleanly
7. Save with descriptive name
8. Export for backup
```

### Workflow 2: Build Oscillator

```
1. Create symmetric base pattern
2. Test period (count steps to repeat)
3. If doesn't oscillate: add/remove cells
4. If oscillates: note period
5. Minimize cells (remove unnecessary)
6. Verify still oscillates
7. Save to library
```

### Workflow 3: Design Still Life

```
1. Place cells in cluster
2. Test each cell has 2-3 neighbors (Life)
3. Run simulation
4. If changes: identify unstable cells
5. Adjust until stable
6. Minimize pattern
7. Save and document
```

---

## Tips for Success

**Start Simple**
- ✓ Begin with 2 states
- ✓ Use small patterns (5-10 cells)
- ✓ Test frequently

**Use Symmetry**
- ✓ Mirror tools are your friend
- ✓ Symmetric often = stable
- ✓ Break symmetry for movement

**Save Everything**
- ✓ Save before major changes
- ✓ Save interesting accidents
- ✓ Export important patterns

**Experiment Freely**
- ✓ Try random placements
- ✓ Combine patterns
- ✓ Use all tools

**Document Discoveries**
- ✓ Name patterns descriptively
- ✓ Note interesting behaviors
- ✓ Share with others

---

## Keyboard Shortcuts

Currently: Mouse-driven interface

**Future Enhancements** (not yet implemented):
- Arrow keys: Move selection
- Delete: Clear selected cell
- 1-8: Quick state selection
- Ctrl+Z: Undo
- Ctrl+Y: Redo

---

## Troubleshooting

**Can't Draw**
- ✓ Check state selected
- ✓ Verify grid size set
- ✓ Click within canvas area

**Tools Don't Work**
- ✓ Ensure pattern exists on canvas
- ✓ Check not all empty
- ✓ Try with simple pattern first

**Export Fails**
- ✓ Check file permissions
- ✓ Verify valid filename
- ✓ Try different location

**Import Fails**
- ✓ Verify .npy file
- ✓ Check file not corrupted
- ✓ Ensure compatible format

---

## Next Steps

**Test Your Pattern**: Go to [Simulation Tab](simulation_tab.md)

**Create Rules for It**: See [Rule Editor](rule_editor.md)

**Learn Theory**: Read [Pattern Theory](../theory.md)

**See Examples**: Browse [Models](../models/overview.md)

---

**Happy pattern designing!** 🎨
