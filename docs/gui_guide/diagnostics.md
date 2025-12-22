# Diagnostics Tab Guide

The **Diagnostics Tab** provides powerful analysis tools for understanding cellular automaton behavior.

---

## Overview

The Diagnostics tab offers:

1. **System Summary** - Current simulation status
2. **Behavior Analysis** - Classification and metrics
3. **Event Log** - Detailed activity tracking
4. **Export Capabilities** - Save analysis data

---

## Interface Layout

### Top Section: Summary Panel

Shows current simulation state:
- Selected automaton
- Current pattern
- Generation count
- Grid dimensions
- Performance metrics

### Middle Section: Behavior Analysis

Detailed behavioral classification:
- **Classification** - Pattern type identified
- **Density Metrics** - Population statistics
- **Entropy Metrics** - Disorder measurements
- **State Distribution** - Breakdown by state

### Bottom Section: Event Log

Scrollable table showing:
- **Timestamp** - When event occurred
- **Event Type** - Category (info/warning/error)
- **Message** - Event description

### Control Buttons

**Refresh** - Update all metrics
**Export Diagnostics** - Save to JSON file
**Clear Log** - Remove all events

---

## Summary Display

### Information Shown

**Automaton Info**:
```
Automaton: Conway's Game of Life
Pattern: glider
States: 2
Neighborhood: Moore (8 neighbors)
```

**Grid Info**:
```
Grid Size: 150 x 150 (22,500 cells)
Generation: 347
Runtime: 5.2 seconds
```

**Performance**:
```
Average FPS: 58.3
Steps per second: 58.3
Memory usage: 1.2 MB
```

### How to Use

1. **Run a simulation** in Simulation tab
2. **Switch to Diagnostics** tab
3. **Click Refresh** to update metrics
4. **Review analysis** below

---

## Behavior Analysis

### Classification Types

**STATIC**
- No changes occurring
- Stable configuration
- May be still life pattern

**GROWING**
- Population increasing
- Density rising over time
- May be unbounded growth

**DYING**
- Population decreasing
- Density falling
- Approaching extinction

**OSCILLATING**
- Periodic behavior detected
- Returns to previous states
- Shows period if detected

**CHAOTIC**
- Unpredictable changes
- High entropy
- No clear pattern

**STABLE**
- Reached equilibrium
- Mix of static/oscillating
- Long-term stability

**COMPLEX**
- Mix of behaviors
- Local patterns
- Class 4 automata

### Density Metrics

**Current Density**: Percentage of active cells now
```
Current: 23.4%
```

**Average Density**: Mean over run
```
Average: 18.7%
Range: 5.2% - 34.1%
```

**Density Trend**: Change over time
```
Trend: ↗ Increasing
Rate: +0.3% per 100 steps
```

**Interpretation**:
- <5%: Sparse
- 5-20%: Low
- 20-40%: Medium
- 40-60%: High
- >60%: Dense

### Entropy Metrics

**Current Entropy**: Disorder level now
```
Current: 0.84
```

**Average Entropy**: Mean over run
```
Average: 0.76
Range: 0.21 - 0.95
```

**Entropy Trend**: Change pattern
```
Trend: ↘ Decreasing (becoming ordered)
```

**Interpretation**:
- 0.0-0.3: Highly ordered
- 0.3-0.6: Moderately ordered
- 0.6-0.8: Moderately chaotic
- 0.8-1.0: Highly chaotic

### State Distribution

**Breakdown by State**:
```
State 0 (Dead):  18,234 cells (81.0%)
State 1 (Alive):  4,266 cells (19.0%)
```

**Multi-State Example** (Wire World):
```
State 0 (Empty):   19,450 cells (86.4%)
State 1 (Wire):     2,850 cells (12.7%)
State 2 (Head):        15 cells (0.07%)
State 3 (Tail):       185 cells (0.82%)
```

---

## Event Log

### Event Types

**INFO** (Blue)
- Normal operations
- Milestones reached
- Pattern changes

**WARNING** (Yellow)
- Potential issues
- Performance degradation
- Unusual behavior

**ERROR** (Red)
- Failures
- Invalid operations
- Critical issues

### Common Events

**Simulation Events**:
```
[12:34:56] INFO: Simulation started (Game of Life, glider)
[12:35:02] INFO: Generation 100 reached
[12:35:45] INFO: Pattern stabilized (still life detected)
[12:36:12] INFO: Simulation paused
```

**Pattern Events**:
```
[12:34:58] INFO: Initial density: 1.2%
[12:35:30] INFO: Glider collision detected
[12:35:45] INFO: Stable configuration achieved
```

**Performance Events**:
```
[12:35:15] WARNING: FPS dropped to 25
[12:35:50] INFO: Performance recovered (58 FPS)
```

**Error Events**:
```
[12:36:30] ERROR: Invalid pattern data
[12:36:45] ERROR: Memory limit reached
```

### Log Management

**View Log**:
- Scroll through events
- Filter by type (future)
- Search for keywords (future)

**Clear Log**:
1. Click "Clear Log" button
2. Confirm action
3. Log is emptied

**Export Log**:
1. Click "Export Diagnostics"
2. Choose save location
3. Saves as JSON with full log

---

## Using Diagnostics

### Workflow 1: Understand Behavior

```
1. Run simulation for 200+ steps
2. Switch to Diagnostics tab
3. Click Refresh
4. Check Classification
5. Review density/entropy trends
6. Read conclusions
```

### Workflow 2: Performance Analysis

```
1. Run large grid simulation
2. Monitor FPS in status bar
3. Check Diagnostics for warnings
4. Review performance metrics
5. Adjust grid size if needed
```

### Workflow 3: Pattern Analysis

```
1. Load interesting pattern
2. Let evolve
3. Check Diagnostics classification
4. Is it oscillating? What period?
5. Is it growing? How fast?
6. Export data for record
```

### Workflow 4: Comparison Study

```
1. Run automaton A
2. Export diagnostics
3. Run automaton B (same pattern)
4. Export diagnostics
5. Compare JSON files
6. Identify differences
```

---

## Interpreting Results

### Static Classification

**Characteristics**:
- Density stable (±0.1%)
- Entropy low and stable
- No changes for 50+ steps

**Meaning**:
- Pattern is still life
- Or died completely
- No further evolution

**Examples**:
- Block in Life
- Beehive
- Empty grid

### Growing Classification

**Characteristics**:
- Density increasing >0.5%/step
- Entropy variable
- Population expanding

**Meaning**:
- Pattern not contained
- May be replicator
- Or unbounded growth

**Examples**:
- Seeds with any pattern
- Life with R-pentomino (early)
- Day & Night random starts

### Oscillating Classification

**Characteristics**:
- Density oscillates
- Period detected
- Returns to previous state

**Meaning**:
- Periodic behavior
- Stable oscillator
- Predictable pattern

**Examples**:
- Blinker (period 2)
- Pulsar (period 3)
- Toad (period 2)

### Chaotic Classification

**Characteristics**:
- High entropy (>0.7)
- Unpredictable changes
- No clear pattern

**Meaning**:
- Complex dynamics
- Sensitive to conditions
- Class 3 automaton

**Examples**:
- Rule 30 with single cell
- Seeds with serviette
- Random Life patterns

### Complex Classification

**Characteristics**:
- Medium entropy (0.4-0.7)
- Mix of structures
- Long-lived patterns

**Meaning**:
- Class 4 behavior
- Edge of chaos
- Most interesting!

**Examples**:
- Rule 110
- Life with many patterns
- Wire World circuits

---

## Export Format

### JSON Structure

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
    }
  ]
}
```

### Using Exported Data

**Python Analysis**:
```python
import json

with open('diagnostics.json') as f:
    data = json.load(f)

print(f"Classification: {data['metrics']['classification']}")
print(f"Avg Density: {data['metrics']['average_density']}%")
```

**Comparison Script**:
```python
# Compare two runs
with open('run1.json') as f1, open('run2.json') as f2:
    d1 = json.load(f1)
    d2 = json.load(f2)
    
print(f"Run 1 entropy: {d1['metrics']['average_entropy']}")
print(f"Run 2 entropy: {d2['metrics']['average_entropy']}")
```

---

## Tips and Tricks

### Accurate Classification

✅ **Do**:
- Run 200+ steps before checking
- Use Refresh button
- Let patterns stabilize
- Test multiple times

❌ **Don't**:
- Check too early (<50 steps)
- Expect instant classification
- Assume first result final

### Performance Monitoring

✅ **Do**:
- Check FPS regularly
- Note warnings
- Export before changes
- Track over time

❌ **Don't**:
- Ignore warnings
- Run too large grids
- Forget to export

### Data Collection

✅ **Do**:
- Export after each run
- Use descriptive filenames
- Keep organized records
- Document findings

❌ **Don't**:
- Overwrite exports
- Use generic names
- Lose data
- Skip documentation

---

## Troubleshooting

### Problem: No Classification Shown

**Causes**:
- Simulation not run
- Too few steps
- No data yet

**Solutions**:
- Run simulation first
- Let evolve 50+ steps
- Click Refresh button

### Problem: Wrong Classification

**Causes**:
- Not enough steps
- Transitional behavior
- Complex pattern

**Solutions**:
- Run longer (200+ steps)
- Observe actual behavior
- Check multiple times

### Problem: Can't Export

**Causes**:
- No data collected
- File permissions
- Invalid path

**Solutions**:
- Run simulation first
- Check save location
- Verify permissions

---

## Advanced Usage

### Systematic Testing

**Test Protocol**:
```
1. Select automaton
2. Run pattern A
3. Export diagnostics as "auto_patternA.json"
4. Run pattern B
5. Export diagnostics as "auto_patternB.json"
6. Compare results
7. Document findings
```

### Batch Analysis

**Python Script**:
```python
import json
import os

results = {}
for file in os.listdir('diagnostics/'):
    if file.endswith('.json'):
        with open(f'diagnostics/{file}') as f:
            data = json.load(f)
            results[file] = {
                'class': data['metrics']['classification'],
                'entropy': data['metrics']['average_entropy']
            }

# Analyze patterns
for name, metrics in results.items():
    print(f"{name}: {metrics['class']} (entropy: {metrics['entropy']:.2f})")
```

### Research Applications

**Use diagnostics for**:
- Pattern classification studies
- Rule comparison research
- Performance benchmarking
- Behavior prediction
- Academic papers

---

## Integration with Other Tabs

### With Simulation Tab

**Flow**:
```
Simulation → Run pattern → Observe
     ↓
Diagnostics → Analyze → Classification
     ↓
Simulation → Adjust and test again
```

### With Pattern Editor

**Flow**:
```
Pattern Editor → Design pattern
     ↓
Simulation → Test pattern
     ↓
Diagnostics → Analyze behavior
     ↓
Pattern Editor → Refine based on results
```

### With Rule Editor

**Flow**:
```
Rule Editor → Create rule
     ↓
Simulation → Test with patterns
     ↓
Diagnostics → Check classification
     ↓
Rule Editor → Adjust rules if needed
```

---

## Quick Reference

### Refresh Button
**Purpose**: Update all metrics
**When**: After simulation changes

### Export Button
**Purpose**: Save analysis data
**Format**: JSON file
**Contains**: All metrics + event log

### Clear Log Button
**Purpose**: Empty event log
**Note**: Can't be undone

### Classification Types
| Type | Meaning |
|------|---------|
| STATIC | No changes |
| GROWING | Expanding |
| DYING | Shrinking |
| OSCILLATING | Periodic |
| CHAOTIC | Random |
| STABLE | Equilibrium |
| COMPLEX | Mixed |

---

## Next Steps

**Learn More**:
- [Simulation Tab](simulation_tab.md) - Run automata
- [Pattern Editor](pattern_editor.md) - Design patterns
- [Theory](../theory.md) - Understanding classification

**Advanced**:
- [API Reference](../reference/api.md) - Automate analysis
- [Advanced Techniques](../tutorials/advanced.md) - Expert methods

---

**Master the Diagnostics tab to deeply understand CA behavior!** 📊
