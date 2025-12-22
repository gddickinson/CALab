# Tutorial: Creating Custom Rules

Learn how to design your own cellular automaton rules from scratch!

---

## What You'll Learn

- Understanding rule types
- Creating totalistic rules (Life-like)
- Creating table-based rules
- Testing and refining rules
- Common patterns and techniques

**Time**: 30-45 minutes
**Difficulty**: ⭐⭐ Intermediate

---

## Prerequisites

- Basic understanding of CA (see [Introduction](../introduction.md))
- Familiarity with [Rule Editor](../gui_guide/rule_editor.md)
- CALab GUI running

---

## Part 1: Your First Totalistic Rule

### Step 1: Open Rule Editor

1. Launch CALab
2. Click "Rule Editor" tab
3. Select "Totalistic" from Type dropdown

### Step 2: Create Simple Rule

Let's create a simple majority rule:

**Goal**: Cells follow the majority of their neighbors

**Rule**: B5678/S5678
- Birth if 5+ neighbors alive
- Survive if 5+ neighbors alive

**Enter it**:
1. Birth field: "5678"
2. Survival field: "5678"
3. Click "Add Rule"

### Step 3: Test It

**Create a Test Pattern**:
1. Go to Pattern Editor
2. Draw random pattern (medium density)
3. Save as "majority_test"

**Run Simulation** (once integrated):
1. Go to Simulation tab
2. Load your rule (future feature)
3. Load your pattern
4. Press Play!

**Expected Behavior**:
- Clusters form
- Boundaries smooth out
- Eventually stabilizes

---

## Part 2: Game of Life Variations

### Classic Life: B3/S23

**Behavior**: Balanced, interesting patterns

**Variations to Try**:

**HighLife: B36/S23**
- Add birth condition 6
- Creates replicators!

**Seeds: B2/S**
- Only birth on 2
- No survival (empty S)
- Explosive growth

**Life Without Death: B3/S012345678**
- Same birth (3)
- All survive
- Infinite growth

### Exercise: Find Your Own

**Task**: Create a stable, interesting variant

**Method**:
1. Start with B3/S23
2. Add one birth condition: B34/S23
3. Test - too much? Too little?
4. Adjust survival: B34/S234
5. Keep tweaking!

**Goal**: Find rule that creates:
- Stable structures
- Some oscillators
- Maybe moving patterns

---

## Part 3: Symmetric Rules

### What Are Symmetric Rules?

Rules where birth = survival conditions

**Example**: Day and Night (B3678/S34678)

### Creating Symmetric Rules

**Try these**:

**B12345678/S12345678**
- Almost everything survives
- Very stable

**B012345678/S012345678**
- Everything survives
- Instant fill

**B3/S3**
- Simple symmetric
- Creates mazes

**B4/S4**
- Diamond-like patterns

### Exercise: Symmetric Explorer

**Task**: Find interesting symmetric rule

**Start**: B3/S3
**Modify**: Add one condition at a time
**Try**:
- B34/S34
- B345/S345
- B3456/S3456

**Record**: Which creates best patterns?

---

## Part 4: Table-Based Rules

### When to Use Table Rules

Use when you need:
- Directional behavior
- Multi-state systems
- Precise control
- Asymmetric rules

### Simple Example: Directional Growth

**Goal**: Cells grow only to the North

**Rules**:
```
Pattern: 0,1,0,0,0 → Result: 1
(Dead cell with alive North becomes alive)

Pattern: 1,X,X,X,X → Result: 1
(Alive cells stay alive)

Pattern: 0,0,X,X,X → Result: 0
(Dead stays dead unless North neighbor)
```

**Enter in Rule Editor**:
1. Select "Table-Based"
2. Set States: 2
3. Add Pattern: "0,1,0,0,0" → 1
4. Add Pattern: "1,0,0,0,0" → 1
5. Add Pattern: "1,1,0,0,0" → 1
... (and so on)

### Exercise: Create Simple CA

**Task**: Create "Transmission" CA

**States**: 3
- 0: Empty
- 1: Wire
- 2: Signal

**Rules**:
- Signal moves along wire
- Signal disappears on empty
- Wire stays wire

**Hint**:
```
Pattern: 1,2,0,0,0 → Result: 2
(Wire with signal North gets signal)

Pattern: 2,X,X,X,X → Result: 0
(Signal dies next step)
```

---

## Part 5: Advanced Techniques

### Multi-State Rules

**3-State Example**: Brian's Brain Style

States: 0=Dead, 1=Alive, 2=Dying

**Rules**:
```
0 with 2 neighbors of state 1 → 1 (Birth)
1 → 2 (Alive becomes dying)
2 → 0 (Dying becomes dead)
```

**In Table Format**:
```
Pattern: 1,X,X,X,X → Result: 2
Pattern: 2,X,X,X,X → Result: 0
(Plus birth rules based on counting)
```

### Rotation Invariance

Make rules work regardless of rotation:

**Instead of**:
```
0,1,0,0,0 → 1 (North only)
```

**Do this**:
```
0,1,0,0,0 → 1 (North)
0,0,1,0,0 → 1 (East)
0,0,0,1,0 → 1 (South)
0,0,0,0,1 → 1 (West)
```

### Conditional Rules

Rules that depend on combinations:

```
0,1,1,0,0 → 1 (North AND East)
0,1,0,1,0 → 2 (North AND South - line)
0,0,1,0,1 → 3 (East AND West - line)
```

---

## Part 6: Testing and Refinement

### Testing Checklist

✅ **Initial State**:
- Pattern doesn't immediately die
- Some evolution occurs
- Not instant explosion

✅ **Evolution**:
- Interesting structures form
- Behavior not too chaotic
- Not too boring/stable

✅ **Long-term**:
- Run 500+ steps
- Check for eventual behavior
- Oscillators? Still life? Chaos?

### Common Problems

**Problem**: Everything dies
**Fix**: 
- Increase survival conditions
- Try denser initial pattern
- Add more birth conditions

**Problem**: Everything fills
**Fix**:
- Reduce birth conditions
- Increase death (fewer survival)
- Try sparser pattern

**Problem**: Too chaotic
**Fix**:
- Reduce birth conditions
- Increase survival requirements
- More restrictive rules

**Problem**: Too boring
**Fix**:
- Add birth conditions
- Reduce survival slightly
- Less restrictive rules

### Iterative Process

```
1. Design rule
2. Test with multiple patterns
3. Observe 100+ steps
4. Note problems
5. Adjust ONE parameter
6. Repeat
```

---

## Part 7: Famous Rules to Study

### Analyze These

**Maze (B3/S12345)**
- Why does it make mazes?
- What happens with different patterns?
- Can you modify it?

**Coral (B3/S45678)**
- High survival
- Creates branches
- Study the structure

**2x2 (B36/S125)**
- Special blocks of 2x2
- Complex interactions

### Reverse Engineering

**Exercise**: Recreate Game of Life

**Start**: Empty rules
**Observe**: Life behavior
- Blocks stable (4 cells, each sees 3)
- Blinkers oscillate
- Gliders move

**Deduce**:
- Need birth on 3
- Need survival on 2, 3
- B3/S23

---

## Part 8: Documentation

### Record Your Rules

**What to save**:
```
Rule Name: Majority Rule
Rule String: B5678/S5678
Description: Cells follow majority
Behavior: Forms clusters, smooths
Interesting Patterns: Random 40% density
Created: 2024-12-22
```

### Export and Share

1. Create rule in Rule Editor
2. Click "Export Rules"
3. Save as "my_rule.json"
4. Add README.txt with description
5. Share with others!

### Build a Library

**Organize by**:
- Type (totalistic, table-based)
- Behavior (chaotic, stable, etc)
- States (2-state, multi-state)
- Purpose (learning, art, research)

---

## Part 9: Project Ideas

### Project 1: Custom Life Variant

**Goal**: Create Life-like rule with unique behavior

**Requirements**:
- Totalistic rule
- 2 states
- Must have stable structures
- Must have one moving pattern

**Deliverable**: Rule + 3 example patterns

### Project 2: Multi-State Art

**Goal**: Beautiful visual patterns

**Requirements**:
- 3+ states
- Creates patterns (not random)
- Visually interesting
- Runs 200+ steps

**Deliverable**: Rule + showcase pattern

### Project 3: Signal System

**Goal**: Information transmission

**Requirements**:
- Table-based rules
- 3+ states
- Signals travel
- Signals can interact

**Deliverable**: Rule + demo patterns

---

## Part 10: Next Steps

### Continue Learning

**Advanced Topics**:
- [Creating Plugins](creating_plugins.md) - Code your own
- [Advanced Techniques](advanced.md) - Expert methods
- [Theory](../theory.md) - Deep understanding

### Share Your Work

**Where to share**:
- Export and document
- Create GitHub repository
- Write tutorials
- Teach others!

### Join the Community

**Resources**:
- LifeWiki (Game of Life patterns)
- Cellular Automata subreddit
- Scientific papers
- Research groups

---

## Quick Reference

### Totalistic Rule Format

```
B<birth>/S<survival>

Example: B3/S23
- B3: Birth on 3 neighbors
- S23: Survive on 2 or 3 neighbors
```

### Table Rule Format

```
Pattern: C,N,E,S,W → Result

Example: 0,1,1,1,0 → 1
- Center: 0
- North: 1
- East: 1  
- South: 1
- West: 0
- Becomes: 1
```

### Common Patterns

```
High Birth/Low Survival: Chaotic
Low Birth/High Survival: Stable
Symmetric (B=S): Usually stable
B3/S23 variants: Life-like behavior
```

---

## Practice Exercises

### Exercise 1: Speed Runner

Create a rule where patterns move fast.

**Hint**: Look at asymmetric conditions

### Exercise 2: Crystallizer

Create a rule that forms crystal-like structures.

**Hint**: High survival, moderate birth

### Exercise 3: Replicator

Create a rule with self-copying patterns.

**Hint**: Study HighLife (B36/S23)

### Exercise 4: Oscillator Factory

Create a rule where most patterns oscillate.

**Hint**: Symmetric rules often oscillate

### Exercise 5: Maze Maker

Create a rule that forms maze-like patterns.

**Hint**: B3/S12345 is famous for this

---

**Congratulations!** You're now ready to create your own cellular automaton rules! 🎨

**Remember**: The best learning comes from experimentation. Try crazy ideas! Document interesting discoveries! Have fun! 🚀
