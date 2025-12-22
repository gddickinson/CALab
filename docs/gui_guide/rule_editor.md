# Rule Editor Guide

The **Rule Editor** tab lets you create custom cellular automaton rules without programming!

---

## Overview

The Rule Editor supports two types of rules:

1. **Table-Based Rules** - Explicit pattern matching (like Langton's Loop)
2. **Totalistic Rules** - Neighbor counting (like Game of Life)

---

## Table-Based Rules

### What Are They?

Rules where you specify **exact patterns** and their results.

**Pattern Format**: `C,N,E,S,W` (Center, North, East, South, West)

**Example Rule**:
```
Pattern: 0,1,1,1,0 → Result: 1
Meaning: "Dead cell (0) with alive cells to N, E, S becomes alive (1)"
```

### Creating Table Rules

**Step 1: Set Rule Type**
- Select "Table-Based" from Type dropdown
- Set number of states (2-10)

**Step 2: Define Patterns**
- Enter pattern in format: `C,N,E,S,W`
- Each number is a state (0 to num_states-1)
- Set result state (what cell becomes)
- Click "Add Rule"

**Step 3: Build Complete Rule Set**
- Add as many rules as needed
- Each unique pattern needs a rule
- Patterns not defined will use default behavior

### Table Rule Examples

**Example 1: Simple Growth**
```
Pattern: 0,1,0,0,0 → Result: 1
(Dead cell with alive neighbor to North becomes alive)

Pattern: 0,0,1,0,0 → Result: 1
(Dead cell with alive neighbor to East becomes alive)

Pattern: 0,0,0,1,0 → Result: 1
(Dead cell with alive neighbor to South becomes alive)

Pattern: 0,0,0,0,1 → Result: 1
(Dead cell with alive neighbor to West becomes alive)

Pattern: 1,X,X,X,X → Result: 1
(Alive cells stay alive - X means any state)
```

**Example 2: Signal Transmission**
```
Pattern: 2,0,0,0,0 → Result: 2
(Signal state (2) persists)

Pattern: 0,2,0,0,0 → Result: 2
(Signal propagates from North)

Pattern: 0,0,2,0,0 → Result: 2
(Signal propagates from East)
```

**Example 3: Langton's Loop Style**
```
Pattern: 0,1,1,1,0 → Result: 2
Pattern: 2,1,0,1,0 → Result: 1
Pattern: 1,2,2,2,0 → Result: 3
... (many more rules for complete system)
```

### Tips for Table Rules

✅ **Start Simple**
- Begin with 2 states
- Add complexity gradually

✅ **Test Incrementally**
- Add a few rules
- Test in simulation
- Add more rules

✅ **Document Your Rules**
- Use Export to save
- Add comments to JSON file

✅ **Common Patterns**
- Identity: `X,X,X,X,X → X` (stays same)
- Death: `1,X,X,X,X → 0` (always dies)
- Propagation: `0,1,0,0,0 → 1` (spreads)

❌ **Avoid**
- Too many rules at once
- Contradictory rules
- Undefined default behavior

---

## Totalistic Rules

### What Are They?

Rules based on **counting neighbors** (like Game of Life).

**Format**: `B<birth>/S<survival>`
- **B** = Birth conditions (dead → alive)
- **S** = Survival conditions (alive → alive)

**Example**: `B3/S23` (Game of Life)
- Dead cell with **3** neighbors becomes alive
- Alive cell with **2 or 3** neighbors survives
- All other cells die

### Creating Totalistic Rules

**Step 1: Set Rule Type**
- Select "Totalistic" from Type dropdown
- States automatically set to 2 (alive/dead)

**Step 2: Enter Birth Conditions**
- Enter neighbor counts that cause birth
- Example: "3" means "3 neighbors"
- Example: "36" means "3 or 6 neighbors"

**Step 3: Enter Survival Conditions**
- Enter neighbor counts for survival
- Example: "23" means "2 or 3 neighbors"
- Example: "34678" means "3,4,6,7, or 8 neighbors"

**Step 4: Test**
- Click "Set Rule"
- Rule is ready to test

### Famous Totalistic Rules

**Game of Life** - `B3/S23`
```
Birth: 3 neighbors
Survival: 2 or 3 neighbors
```
Most famous CA! Complex patterns, gliders, guns.

**HighLife** - `B36/S23`
```
Birth: 3 or 6 neighbors
Survival: 2 or 3 neighbors
```
Like Life but has replicator patterns.

**Day and Night** - `B3678/S34678`
```
Birth: 3, 6, 7, or 8 neighbors
Survival: 3, 4, 6, 7, or 8 neighbors
```
Symmetric rules, stable patterns.

**Seeds** - `B2/S`
```
Birth: 2 neighbors
Survival: None (all die)
```
Explosive growth, beautiful patterns.

**Maze** - `B3/S12345`
```
Birth: 3 neighbors
Survival: 1, 2, 3, 4, or 5 neighbors
```
Creates maze-like structures.

**Coral** - `B3/S45678`
```
Birth: 3 neighbors
Survival: 4, 5, 6, 7, or 8 neighbors
```
Grows coral-like structures.

### Experimenting with Totalistic Rules

Try these combinations:

**High Birth**
- `B012345/S01234` - Everything becomes alive
- `B3456/S012345678` - Dense, complex patterns

**Low Birth**
- `B1/S` - Minimal growth
- `B3/S` - Life-like but no survival

**Symmetric**
- Same counts for birth and survival
- Often creates stable patterns

**Asymmetric**
- Different birth/survival
- Usually more interesting dynamics

---

## Working with Rules

### Viewing Current Rules

The **Current Rules** table shows:
- Pattern or condition
- Result state
- Delete button for each rule

### Managing Rules

**Import Rules**
- Click "Import Rules"
- Select JSON file
- Rules load into table

**Export Rules**
- Click "Export Rules"
- Choose save location
- Creates JSON file with all rules

**Clear All**
- Click "Clear All"
- Confirms before deleting
- Removes all rules

### Testing Rules

**Test Button** (Future feature)
- Will test rules in simulation
- Check for completeness
- Identify issues

For now, test by:
1. Export rules
2. Go to Simulation tab
3. (Would need plugin integration)

---

## Rule File Format

Rules export as JSON:

```json
{
  "metadata": {
    "num_states": 2,
    "rule_type": "totalistic"
  },
  "rules": [
    {
      "pattern": [0, 1, 1, 1, 0],
      "result": 1
    },
    {
      "pattern": [1, 0, 0, 0, 0],
      "result": 1
    }
  ]
}
```

Or for totalistic:

```json
{
  "metadata": {
    "num_states": 2,
    "rule_type": "totalistic",
    "birth": "3",
    "survival": "23"
  }
}
```

---

## Advanced Techniques

### Multi-State Rules

Use 3+ states for richer behavior:

**3 States** (Brian's Brain style)
```
State 0: Dead
State 1: Alive
State 2: Dying

Rules:
- 1,X,X,X,X → 2 (Alive becomes dying)
- 2,X,X,X,X → 0 (Dying becomes dead)
- 0 with 2 neighbors of state 1 → 1 (Birth)
```

**4 States** (Wire World style)
```
State 0: Empty
State 1: Wire
State 2: Electron Head
State 3: Electron Tail

Rules for electron propagation...
```

### Directional Rules

Make rules depend on direction:

```
Pattern: 0,1,0,0,0 → 2 (North activation)
Pattern: 0,0,1,0,0 → 3 (East activation)
Pattern: 0,0,0,1,0 → 4 (South activation)
Pattern: 0,0,0,0,1 → 5 (West activation)
```

### Conditional Rules

Create rules that depend on combinations:

```
Pattern: 0,1,1,0,0 → 1 (N+E corner)
Pattern: 0,1,0,1,0 → 2 (N+S line)
Pattern: 0,0,1,0,1 → 3 (E+W line)
```

---

## Common Patterns

### Growth Rules
```
B3/S23   - Balanced growth (Life)
B3/S012345678 - Everything survives
B2/S - Explosive growth (Seeds)
```

### Stable Rules
```
B1/S012345678 - Very stable
B3/S12345678 - High survival
```

### Crystalline Rules
```
B3/S234 - Crystal growth
B3678/S34678 - Day and Night
```

### Wave Rules
```
B2/S0 - Brian's Brain style
B2/S2 - Persistent waves
```

---

## Troubleshooting

**Nothing Happens**
- ✓ Check birth conditions set
- ✓ Verify pattern syntax correct
- ✓ Ensure initial pattern matches rules

**Everything Dies**
- ✓ Add survival conditions
- ✓ Check S values
- ✓ Test with denser initial pattern

**Everything Becomes Alive**
- ✓ Reduce birth conditions
- ✓ Add death rules
- ✓ Check for contradictions

**Rules Don't Apply**
- ✓ Verify pattern format (comma-separated)
- ✓ Check state numbers valid
- ✓ Ensure no typos

---

## Examples to Try

### Example 1: Simple Majority Rule
```
Type: Totalistic
Birth: 5678 (becomes alive if 5+ neighbors)
Survival: 5678 (survives if 5+ neighbors)

Result: Cells follow majority of neighbors
```

### Example 2: Replicator
```
Type: Totalistic
Birth: 1357 (odd neighbors)
Survival: 1357 (odd neighbors)

Result: Creates replicating patterns
```

### Example 3: Diamoeba
```
Type: Totalistic  
Birth: 35678
Survival: 5678

Result: Amoeba-like growth
```

---

## Next Steps

**Create a Pattern**: See [Pattern Editor Guide](pattern_editor.md)

**Test Your Rules**: See [Simulation Tab Guide](simulation_tab.md)

**Advanced**: See [Creating Plugins Tutorial](../tutorials/creating_plugins.md)

---

## Tips for Success

1. **Start with known rules** (B3/S23)
2. **Modify one parameter** at a time
3. **Test immediately** after changes
4. **Save interesting rules** (export!)
5. **Document what works** (add notes)
6. **Share discoveries** (export and share files)

**Happy rule creating!** 🎨
