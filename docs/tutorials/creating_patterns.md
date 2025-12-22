# Tutorial: Creating Custom Patterns

Learn how to design effective initial patterns for cellular automata!

---

## What You'll Learn

- Using the Pattern Editor effectively
- Design principles
- Pattern types and purposes
- Testing and refinement
- Common techniques

**Time**: 30-40 minutes
**Difficulty**: ⭐⭐ Intermediate

---

## Prerequisites

- Basic CA understanding ([Introduction](../introduction.md))
- Familiarity with [Pattern Editor](../gui_guide/pattern_editor.md)
- CALab GUI running

---

## Part 1: Interface Mastery

### Step 1: Open Pattern Editor

1. Launch CALab
2. Click "Pattern Editor" tab
3. Familiarize with layout:
   - Left: 30×30 canvas
   - Right: Tools and library

### Step 2: Basic Drawing

**Exercise**: Draw a simple block

```
1. Click on a cell → draws state 1
2. Click adjacent cells
3. Create 2×2 square
4. See it colored (default: green)
```

**Controls**:
- **Click**: Place cell
- **Drag**: Draw continuously
- **State dropdown**: Change which state to draw

### Step 3: Try Each Tool

**Clear**: Click button → grid empties

**Mirror H**: Draw pattern, click → flips left-right

**Mirror V**: Draw pattern, click → flips top-bottom

**Rotate**: Draw L-shape, click → rotates 90°

**Invert**: Draw pattern, click → swaps states

---

## Part 2: Design Principles

### Symmetry

**Why**: Symmetric patterns often create stable or oscillating structures

**Types**:

**Horizontal Symmetry**:
```
X X X
 X X
X X X
```

**Vertical Symmetry**:
```
X   X
X X X
X   X
```

**Rotational Symmetry**:
```
X   X
  X
X   X
```

**4-Way Symmetry**:
```
  X
X X X
  X
```

### Density

**Sparse** (< 20% filled):
- Clean evolution
- Easy to track
- Often stable
- Good for learning

**Medium** (20-50% filled):
- Balanced
- Interesting dynamics
- Common patterns
- Good starting point

**Dense** (> 50% filled):
- Complex interactions
- Often chaotic
- Hard to predict
- Advanced study

### Size

**Small** (3-10 cells):
- Minimal patterns
- Clean behavior
- Easy to understand
- Quick to test

**Medium** (10-30 cells):
- More complexity
- Interesting behavior
- Standard size
- Most patterns

**Large** (30+ cells):
- Complex structures
- Long evolution
- Advanced patterns
- Research level

---

## Part 3: Pattern Types

### Type 1: Still Lifes

**Goal**: Create stable, non-changing pattern

**For Game of Life**:

**Exercise**: Design a block
```
1. Draw 2×2 square: ██
                      ██
2. Each cell sees 3 neighbors
3. Save as "my_block"
4. Test: Should never change
```

**Challenge**: Create a beehive
```
Hint:  ██
      █  █
       ██
```

### Type 2: Oscillators

**Goal**: Create repeating pattern

**For Game of Life**:

**Exercise**: Design a blinker
```
1. Draw horizontal: ███
2. Save as "my_blinker"
3. Test: Should alternate horizontal/vertical
```

**Challenge**: Create a toad
```
Hint: Offset rows
```

### Type 3: Spaceships

**Goal**: Create moving pattern

**For Game of Life**:

**Exercise**: Draw a glider
```
1. Pattern:  █
             █
            ███
2. Explanation:
   - Asymmetric
   - Weighted toward one corner
   - Should move diagonally
3. Test: Watch it travel!
```

### Type 4: Growth Patterns

**Goal**: Create expanding pattern

**For Seeds**:

**Exercise**: Serviette (2×2)
```
1. Draw: ██
         ██
2. Test in Seeds
3. Watch explosive growth!
```

### Type 5: Random Patterns

**Goal**: Testing rule behavior

**Exercise**: Controlled randomness
```
1. Draw scattered cells (~30% density)
2. Not too sparse (nothing happens)
3. Not too dense (instant chaos)
4. Just right for testing
```

---

## Part 4: Automaton-Specific Patterns

### Game of Life Patterns

**Glider Gun Setup**:
```
Complex but rewarding:
1. Draw stable base
2. Add emitter mechanism
3. Test emission timing
4. Adjust until working
```

**R-Pentomino**:
```
Simple methuselah:
 ██
██
 █

Takes 1103 steps!
```

### Seeds Patterns

**Explosive Starts**:
```
Serviette: ██
           ██

Two cells: ██

Cross:  █
       ███
        █
```

**Tip**: Seeds needs neighbors, so clustering helps!

### Brian's Brain Patterns

**Circle**:
```
Draw hollow circle
Watch waves propagate outward
Beautiful patterns!
```

**Lines**:
```
Draw parallel lines
Watch interference
Create standing waves
```

### Wire World Patterns

**Simple Wire**:
```
═══H═══
(Wire with electron head)
```

**Clock**:
```
Loop of wire
One electron circulating
Periodic output
```

---

## Part 5: Design Techniques

### Technique 1: Symmetry Construction

**Method**:
```
1. Draw upper-left quadrant
2. Mirror horizontal
3. Mirror vertical (whole pattern)
4. Result: 4-way symmetric
```

**Exercise**: Create symmetric cross
```
1. Draw:   █
          ███
           █
2. Should already be symmetric!
```

### Technique 2: Iterative Refinement

**Process**:
```
1. Design initial pattern
2. Test in simulation
3. Observe behavior
4. Identify issues
5. Modify pattern
6. Repeat until satisfied
```

**Exercise**: Perfect a blinker
```
1. Draw ████ (4 cells)
2. Test → oscillates but messy
3. Remove one → ███
4. Test → clean oscillation!
5. Save final version
```

### Technique 3: Building Blocks

**Method**:
```
1. Create library of tested components
2. Combine in new patterns
3. Test combinations
4. Build complexity gradually
```

**Exercise**: Glider fleet
```
1. Draw one glider
2. Copy pattern to corners
3. Four gliders moving inward
4. Watch collisions!
```

### Technique 4: Minimal Design

**Method**:
```
1. Start with large pattern
2. Remove cells one at a time
3. Test after each removal
4. Keep removing until behavior changes
5. Add back last cell removed
6. Result: Minimal pattern
```

**Exercise**: Minimize oscillator
```
1. Draw large oscillating pattern
2. Remove edge cells
3. Test still oscillates?
4. Continue until minimal
```

---

## Part 6: Testing Patterns

### Test Protocol

**Step 1: Visual Test**
```
1. Load pattern in Pattern Editor
2. Check symmetry
3. Verify density
4. Count cells
5. Document
```

**Step 2: Quick Simulation**
```
1. Test in Simulation tab
2. Run 50 steps
3. Check: Still alive? Changes?
4. Initial assessment
```

**Step 3: Long-Term Test**
```
1. Run 200+ steps
2. Watch evolution
3. Note behavior type
4. Classify result
```

**Step 4: Diagnostics**
```
1. Go to Diagnostics tab
2. Check classification
3. Review metrics
4. Analyze statistics
```

### Test Questions

**Does it**:
- Stay alive?
- Change at all?
- Settle down?
- Oscillate?
- Move?
- Grow?
- Die?

**How long**:
- Until stable?
- Until periodic?
- Until death?

**What's the result**:
- Still life?
- Oscillator (what period)?
- Spaceship (what velocity)?
- Ash/debris?

---

## Part 7: Common Patterns Library

### Life Patterns to Create

**Still Lifes**:
```
Block: ██    Boat: ██    Tub:  █
       ██          █ █         █ █
                    █           █
```

**Oscillators**:
```
Blinker: ███

Toad:  ███
      ███

Beacon: ██
        ██
          ██
          ██
```

**Spaceships**:
```
Glider:   █
         █
        ███

LWSS:  █  █
      █
      █   █
      ████
```

### Seeds Patterns

**Starters**:
```
Serviette: ██
           ██

Line: ████████

Cross:    █
        █████
          █
```

### Brian's Brain

**Initiators**:
```
Circle: Draw hollow circle
Lines: Parallel lines
Random: Scattered cells
```

---

## Part 8: Advanced Projects

### Project 1: Glider Gun

**Goal**: Create pattern that emits gliders

**Difficulty**: ⭐⭐⭐⭐ Very Hard

**Steps**:
```
1. Research Gosper gun design
2. Draw stable base
3. Add emitter sections
4. Test timing
5. Adjust until working
6. Save and document
```

### Project 2: Spaceship Fleet

**Goal**: Multiple moving patterns

**Difficulty**: ⭐⭐⭐ Moderate

**Steps**:
```
1. Create one glider
2. Position second glider
3. Ensure they don't collide
4. Add more spaceships
5. Create formation
6. Save fleet pattern
```

### Project 3: Methuselah Collection

**Goal**: Small patterns, long evolution

**Difficulty**: ⭐⭐⭐⭐ Hard

**Steps**:
```
1. Try random 5-10 cell patterns
2. Test each 1000+ steps
3. Find long-lived ones
4. Document lifespans
5. Build collection
6. Share discoveries
```

### Project 4: Symmetric Art

**Goal**: Beautiful symmetric patterns

**Difficulty**: ⭐⭐ Easy

**Steps**:
```
1. Draw quarter pattern
2. Mirror to full
3. Test for interest
4. Refine aesthetics
5. Save art pieces
6. Create gallery
```

---

## Part 9: Troubleshooting

### Pattern Dies Immediately

**Causes**:
- Too sparse
- Wrong for automaton
- Unstable configuration

**Solutions**:
- Add more cells
- Check rule requirements
- Test different densities
- Try different positions

### Pattern Explodes

**Causes**:
- Too dense
- Wrong automaton (Seeds?)
- Unstable initial state

**Solutions**:
- Reduce density
- Spread cells out
- Test in correct CA
- Start smaller

### Pattern Boring

**Causes**:
- Too simple
- Too symmetric
- Wrong automaton

**Solutions**:
- Add asymmetry
- Increase complexity
- Try different CA
- Combine patterns

### Can't Save Pattern

**Causes**:
- No name entered
- File permissions
- Grid empty

**Solutions**:
- Enter descriptive name
- Check save location
- Verify pattern exists
- Try again

---

## Part 10: Best Practices

### Organization

✅ **Do**:
- Use descriptive names
- Organize by type
- Document behavior
- Save variations
- Keep backups

❌ **Don't**:
- Use "test1", "test2"
- Mix all types
- Forget details
- Overwrite originals
- Lose work

### Documentation

**Record**:
```
Name: glider_northeast
Type: Spaceship
Automaton: Life
Cells: 5
Velocity: c/4 diagonal
Behavior: Moves northeast
Created: 2024-12-22
Notes: Classic pattern
```

### Experimentation

✅ **Do**:
- Try crazy ideas
- Test everything
- Save interesting fails
- Learn from mistakes
- Share discoveries

❌ **Don't**:
- Fear failure
- Stick to known patterns
- Delete experiments
- Give up easily
- Keep secrets

---

## Resources

### In CALab

**Tools**: Pattern Editor
**Testing**: Simulation tab
**Analysis**: Diagnostics

### External

**Websites**:
- LifeWiki (Life patterns)
- Pattern collections
- CA repositories

**Books**:
- Pattern catalogs
- Design guides

---

## Quick Reference

### Design Checklist

- [ ] Appropriate density?
- [ ] Correct automaton?
- [ ] Tested 50+ steps?
- [ ] Documented behavior?
- [ ] Saved with good name?
- [ ] Backed up?

### Common Sizes

| Size | Cells | Use |
|------|-------|-----|
| Tiny | 3-5 | Minimal |
| Small | 5-10 | Common |
| Medium | 10-30 | Standard |
| Large | 30+ | Complex |

### Testing Duration

| Purpose | Steps |
|---------|-------|
| Quick check | 50 |
| Basic test | 100 |
| Full test | 200 |
| Long-term | 500+ |

---

## Conclusion

Pattern design is:
- **Creative**: Express yourself
- **Scientific**: Test hypotheses
- **Educational**: Learn CA behavior
- **Fun**: Endless possibilities

**Start designing today!**

---

## Next Steps

**Master Tools**: Practice with [Pattern Editor](../gui_guide/pattern_editor.md)

**Create Rules**: Design rules for your patterns

**Advanced**: Study [Advanced Techniques](advanced.md)

**Share**: Export and document discoveries!

---

**Design the patterns of tomorrow!** 🎨✨
