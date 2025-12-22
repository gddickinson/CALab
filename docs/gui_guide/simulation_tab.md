# Simulation Tab Guide

The **Simulation Tab** is where you run cellular automata and watch them evolve!

---

## Interface Overview

### Layout

**Left Side**: Controls and statistics
**Right Side**: Visualization canvas

### Main Components

1. **Automaton Selector** - Choose which CA to run
2. **Pattern Selector** - Choose initial pattern
3. **Playback Controls** - Play, pause, step, reset
4. **Speed Control** - Adjust simulation speed
5. **Grid Settings** - Configure grid size
6. **Statistics Panel** - Live metrics
7. **Visualization Canvas** - See the automaton evolve

---

## Getting Started

### Quick Start

**Step 1**: Select an automaton
- Click "Automaton" dropdown
- Choose from 13 available models
- Example: "Conway's Game of Life"

**Step 2**: Select a pattern
- Click "Pattern" dropdown  
- Choose initial configuration
- Example: "glider"

**Step 3**: Press Play!
- Click ▶️ Play button
- Watch the evolution
- Adjust speed as needed

**Step 4**: Explore
- Try different patterns
- Change automata
- Observe statistics

---

## Automaton Selection

### Dropdown Menu

Shows all 13 available automata:

**Beginner-Friendly**:
- Conway's Game of Life
- Wire World
- Brian's Brain

**Intermediate**:
- Seeds
- Rule 30, 90, 110
- HighLife, Day and Night

**Advanced**:
- Cyclic CA
- Langton's Loop
- Von Neumann Constructor

### Changing Automaton

**Step 1**: Click "Automaton" dropdown
**Step 2**: Select new automaton
**Step 3**: Pattern updates to match
**Step 4**: Click Reset to initialize
**Step 5**: Press Play

**Tip**: Each automaton has unique patterns!

---

## Pattern Selection

### Available Patterns

Each automaton includes multiple patterns:

**Game of Life** (9 patterns):
- glider - Moving pattern
- glider_gun - Creates gliders
- pulsar - Oscillator
- And 6 more...

**Wire World** (4 patterns):
- simple_circuit - Basic demo
- or_gate - Logic gate
- diode - One-way flow
- clock - Oscillator

**Rule 90** (4 patterns):
- single_cell - Sierpinski triangle
- random - Chaotic pattern
- alternating - Striped pattern
- three_cells - Multiple sources

### Pattern Effects

**Symmetric**: Often stable or oscillating
**Asymmetric**: Often moving or growing
**Sparse**: Clean, easy to track
**Dense**: Complex, chaotic

---

## Playback Controls

### ▶️ Play / ⏸️ Pause

**Play**:
- Starts continuous evolution
- Uses speed slider setting
- Updates visualization each step
- Click again to pause

**Shortcuts**: Space bar (future)

### ⏭️ Step

**Purpose**: Advance one generation

**When to use**:
- Studying slow patterns
- Analyzing specific transitions
- Debugging rules
- Educational demonstrations

**Tip**: Great for understanding CA mechanics!

### 🔄 Reset

**Purpose**: Return to initial state

**What it does**:
- Reloads pattern
- Resets generation counter
- Clears history
- Keeps same automaton

**Use when**:
- Want to replay
- Testing different speeds
- Comparing evolution

---

## Speed Control

### Slider

**Range**: 10ms to 500ms per step
- **Fast** (10-50ms): Quick overview
- **Medium** (100-200ms): Comfortable viewing
- **Slow** (300-500ms): Detailed study

### Real-Time FPS

Displays actual frames per second:
- Shows rendering performance
- Indicates if simulation slowing
- Useful for optimization

**Tip**: Slower speeds easier to understand!

---

## Grid Settings

### Grid Size

**Control**: Slider or input box
**Range**: 50 to 300 cells

**Small (50-100)**:
- Fast computation
- Easy to see individual cells
- Good for learning

**Medium (100-200)**:
- Balanced performance
- Most patterns fit well
- Recommended default (150)

**Large (200-300)**:
- Complex patterns
- Slower computation
- Advanced study

### Performance Tips

✅ **Faster**:
- Smaller grids
- Simpler automata (Life, Brian's Brain)
- Lower speed setting

⚠️ **Slower**:
- Larger grids
- Complex automata (Von Neumann)
- High speed setting

---

## Statistics Panel

### Real-Time Metrics

**Generation**: Current time step
- Increments each step
- Resets to 0 on reset
- Shows automaton age

**Active Cells**: Number of non-zero cells
- Total count
- Updates each step
- Shows population

**Density**: Percentage of grid alive
- Formula: (active / total) × 100
- Range: 0% to 100%
- Shows coverage

**Entropy**: Measure of disorder
- Higher = more chaotic
- Lower = more organized
- Range: 0 to log₂(states)

**State Distribution**: Breakdown by state
- Shows count per state
- Useful for multi-state CA
- Example: "State 1: 45, State 2: 12"

**FPS**: Frames per second
- Rendering performance
- Target: 30-60 FPS
- Lower = simulation struggling

---

## Visualization

### Color Scheme

Each automaton has custom colors:

**Game of Life**:
- Black: Dead
- Green: Alive

**Wire World**:
- Black: Empty
- Yellow: Wire
- Blue: Electron head
- Red: Electron tail

**Brian's Brain**:
- Black: Dead
- White: Alive  
- Blue: Dying

**Cyclic CA**:
- Rainbow: 14 different states
- Creates beautiful spirals

### Canvas Interaction

**Currently**: View only
**Future**: Click to edit cells

### Display Options

**Grid Lines**: Currently always on
**Zoom**: Adjust grid size
**Full Screen**: Maximize window

---

## Common Workflows

### Workflow 1: Explore an Automaton

```
1. Select automaton (e.g., Game of Life)
2. Try first pattern (e.g., glider)
3. Press Play, watch evolution
4. Press Reset
5. Try next pattern (e.g., pulsar)
6. Compare behaviors
7. Try all patterns
```

### Workflow 2: Compare Automata

```
1. Select Life, load glider, watch
2. Note behavior (moves diagonally)
3. Select HighLife, load glider
4. Watch and compare
5. Repeat for other CA
```

### Workflow 3: Study Pattern

```
1. Load interesting pattern
2. Set speed to SLOW (400ms)
3. Use Step button
4. Watch each generation carefully
5. Identify stable structures
6. Note emergent patterns
```

### Workflow 4: Performance Testing

```
1. Select automaton
2. Set grid size to 100
3. Note FPS
4. Increase to 200
5. Note FPS change
6. Find optimal size for your system
```

---

## Understanding Statistics

### Generation Count

**What it means**:
- Number of time steps
- Automaton's "age"
- Evolution duration

**Typical values**:
- 0-50: Early evolution
- 50-500: Development phase
- 500+: Mature state

### Active Cells

**What it means**:
- Population size
- Energy in system
- Complexity indicator

**Patterns**:
- **Increasing**: Growth/expansion
- **Decreasing**: Dying/shrinking
- **Stable**: Equilibrium
- **Oscillating**: Periodic behavior

### Density

**What it means**:
- Percentage of grid occupied
- Saturation level
- Space utilization

**Typical ranges**:
- 0-10%: Sparse patterns
- 10-30%: Moderate activity
- 30-50%: Dense activity
- 50%+: Very dense (rare)

### Entropy

**What it means**:
- Disorder/randomness
- Information content
- Predictability

**Interpretation**:
- **Low**: Ordered, predictable
- **Medium**: Balanced complexity
- **High**: Chaotic, random

---

## Tips for Best Results

### Performance Tips

✅ **Do**:
- Start with grid size 150
- Use medium speed (150ms)
- Try simple patterns first
- Close other applications

❌ **Don't**:
- Jump to grid size 300
- Run at minimum speed (10ms)
- Use complex patterns initially
- Run multiple instances

### Learning Tips

✅ **Do**:
- Try all patterns for each automaton
- Use Step to study transitions
- Watch statistics change
- Compare similar automata

❌ **Don't**:
- Rush through patterns
- Ignore statistics
- Stay at one automaton
- Just watch without analyzing

### Discovery Tips

✅ **Do**:
- Look for emergent structures
- Note interesting behaviors
- Try different speeds
- Explore all automata

❌ **Don't**:
- Focus only on final state
- Ignore intermediate stages
- Stay at one speed
- Skip documentation

---

## Troubleshooting

### Problem: Simulation Won't Start

**Solutions**:
- Check automaton selected
- Verify pattern selected
- Try Reset button
- Check Error Console

### Problem: Everything Dies Quickly

**Causes**:
- Pattern too sparse
- Wrong automaton for pattern
- Rules cause death

**Solutions**:
- Try denser pattern
- Check automaton/pattern match
- Try different pattern

### Problem: No Changes/Static

**Causes**:
- Pattern already stable
- Automaton issue
- Grid too small

**Solutions**:
- Try different pattern
- Check automaton (diagnostic)
- Increase grid size

### Problem: Too Fast/Slow

**Solutions**:
- Adjust speed slider
- Change grid size (performance)
- Use Step button for slow analysis

### Problem: Low FPS

**Causes**:
- Grid too large
- Complex automaton
- Computer performance

**Solutions**:
- Reduce grid size
- Try simpler automaton
- Close other applications

---

## Keyboard Shortcuts

**Currently Available**:
- (None yet)

**Planned**:
- Space: Play/Pause
- S: Step
- R: Reset
- +/-: Speed adjustment
- Arrow keys: (Future: pan view)

---

## Advanced Features

### Custom Rules (Future)

Will integrate with Rule Editor:
1. Create rules in Rule Editor
2. Test in Simulation tab
3. Iterate and refine

### Custom Patterns (Future)

Will integrate with Pattern Editor:
1. Design in Pattern Editor
2. Load in Simulation
3. Test and refine

### Export Capabilities (Future)

- Save final state
- Export as image
- Record video
- Export data (CSV)

---

## Next Steps

**Understand the Models**: Read [Models Overview](../models/overview.md)

**Create Rules**: See [Rule Editor Guide](rule_editor.md)

**Design Patterns**: See [Pattern Editor Guide](pattern_editor.md)

**Analyze Behavior**: See [Diagnostics Guide](diagnostics.md)

---

## Quick Reference

### Essential Controls

| Button | Action |
|--------|--------|
| ▶️ Play | Start continuous evolution |
| ⏸️ Pause | Stop evolution |
| ⏭️ Step | Advance one generation |
| 🔄 Reset | Return to initial state |

### Key Statistics

| Metric | Meaning |
|--------|---------|
| Generation | Time step number |
| Active Cells | Population size |
| Density | Percentage occupied |
| Entropy | Chaos/order measure |
| FPS | Rendering performance |

### Recommended Settings

| Purpose | Grid Size | Speed |
|---------|-----------|-------|
| Learning | 100 | 200ms |
| Exploration | 150 | 150ms |
| Analysis | 150 | 400ms |
| Performance | 100 | 100ms |

---

**Happy simulating!** 🎮
