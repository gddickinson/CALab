# Models Overview

CALab includes **13 cellular automata models** spanning historical classics to modern discoveries.

---

## Complete Model List

| Model | States | Type | Patterns | Difficulty |
|-------|--------|------|----------|------------|
| Game of Life | 2 | Life-like | 9 | ⭐ Beginner |
| Wire World | 4 | Circuit | 4 | ⭐ Beginner |
| Brian's Brain | 3 | Wave | 7 | ⭐ Beginner |
| Seeds | 2 | Explosive | 6 | ⭐⭐ Easy |
| Rule 30 | 2 | Elementary | 4 | ⭐⭐ Easy |
| Rule 90 | 2 | Elementary | 4 | ⭐⭐ Easy |
| Rule 110 | 2 | Elementary | 4 | ⭐⭐⭐ Moderate |
| HighLife | 2 | Life-like | 3 | ⭐⭐ Easy |
| Day and Night | 2 | Life-like | 3 | ⭐⭐⭐ Moderate |
| Cyclic CA | 14 | Self-organizing | 4 | ⭐⭐⭐ Moderate |
| Langton's Loop | 8 | Self-replicating | 2 | ⭐⭐⭐⭐ Advanced |
| Von Neumann (Simple) | 29 | Self-replicating | 3 | ⭐⭐⭐⭐ Advanced |
| Von Neumann (Full) | 29 | Self-replicating | 4 | ⭐⭐⭐⭐⭐ Expert |

---

## By Category

### Life-Like Automata

**Game of Life** (`game_of_life`)
- **Rule**: B3/S23
- **Features**: Gliders, guns, spaceships
- **Best for**: Learning CA basics
- **Highlight**: Most famous CA!

**HighLife** (`highlife`)
- **Rule**: B36/S23
- **Features**: Replicator patterns
- **Best for**: Self-replication study
- **Highlight**: Contains self-replicating pattern!

**Day and Night** (`day_and_night`)
- **Rule**: B3678/S34678
- **Features**: Symmetric behavior
- **Best for**: Studying symmetry
- **Highlight**: Live/dead roles symmetric

### Wave & Propagation

**Brian's Brain** (`brians_brain`)
- **States**: 3 (dead, alive, dying)
- **Features**: Beautiful waves
- **Best for**: Visual effects
- **Highlight**: Persistent wave patterns

**Seeds** (`seeds`)
- **Rule**: B2/S (no survival)
- **Features**: Explosive growth
- **Best for**: Fractal patterns
- **Highlight**: Every cell dies immediately!

### Elementary CA

**Rule 30** (`rule_30`)
- **Type**: Chaotic
- **Features**: Random-looking output
- **Best for**: Studying chaos
- **Highlight**: Used in Mathematica RNG!

**Rule 90** (`rule_90`)
- **Type**: Fractal
- **Features**: Sierpinski triangle
- **Best for**: Fractal study
- **Highlight**: Perfect mathematical pattern

**Rule 110** (`rule_110`)
- **Type**: Universal
- **Features**: Turing complete
- **Best for**: Computation theory
- **Highlight**: Can compute anything!

### Circuit Simulation

**Wire World** (`wireworld`)
- **States**: 4 (empty, wire, head, tail)
- **Features**: Digital circuits
- **Best for**: Learning digital logic
- **Highlight**: Simulate AND, OR, NOT gates!

### Self-Organizing

**Cyclic CA** (`cyclic_ca`)
- **States**: 14 (configurable)
- **Features**: Rainbow spirals
- **Best for**: Visual beauty
- **Highlight**: Self-organizing spirals!

### Self-Replicating

**Langton's Loop** (`langton_loop`)
- **States**: 8
- **Features**: Self-copies
- **Best for**: Replication study
- **Highlight**: Simplified von Neumann

**Von Neumann (Simple)** (`von_neumann`)
- **States**: 29
- **Features**: Educational demo
- **Best for**: Learning concepts
- **Highlight**: Historical significance

**Von Neumann (Full)** (`von_neumann_full`)
- **States**: 29
- **Features**: 7,070 rules
- **Best for**: Serious research
- **Highlight**: Full working implementation!

---

## Quick Selection Guide

### I Want...

**...to learn CA basics**
→ Start with **Game of Life**

**...beautiful visuals**
→ Try **Cyclic CA** or **Brian's Brain**

**...to understand computation**
→ Study **Rule 110** or **Game of Life**

**...to see self-replication**
→ Explore **HighLife** or **Langton's Loop**

**...to build circuits**
→ Use **Wire World**

**...mathematical patterns**
→ Try **Rule 90** (Sierpinski)

**...chaos and randomness**
→ Run **Rule 30** or **Seeds**

**...historical perspective**
→ Study **Von Neumann Constructor**

---

## Detailed Guides

Each model has a detailed guide:

- [Game of Life](game_of_life.md)
- [Von Neumann Constructor](von_neumann.md)
- [Wire World](wire_world.md)
- [Elementary CA](elementary_ca.md)
- [And more...](#)

---

## Comparison Charts

### Complexity

```
Simple  ─────────────────────────────  Complex
Game of Life        Langton's Loop        Von Neumann
Rule 90             Wire World            Rule 110
```

### Activity Level

```
Static  ─────────────────────────────  Chaotic
Von Neumann    Game of Life    Seeds
Cyclic CA      Brian's Brain   Rule 30
```

### Pattern Diversity

```
Few     ─────────────────────────────  Many
Seeds              Wire World         Game of Life
Rule 90            HighLife           Rule 110
```

---

## Beginner Recommendations

**Start Here** (⭐ difficulty):
1. **Game of Life** - Classic, well-documented
2. **Wire World** - Visual, intuitive
3. **Brian's Brain** - Beautiful, simple rules

**Next Try** (⭐⭐ difficulty):
4. **Rule 90** - Mathematical beauty
5. **Seeds** - Interesting despite simplicity
6. **HighLife** - Build on Life knowledge

**Then Explore** (⭐⭐⭐ difficulty):
7. **Rule 110** - Universal computation
8. **Cyclic CA** - Self-organization
9. **Day and Night** - Symmetric systems

**Advanced Study** (⭐⭐⭐⭐ difficulty):
10. **Langton's Loop** - Self-replication
11. **Von Neumann** - Historical depth

---

## Research Paths

### Path 1: Computation
```
Game of Life → Rule 110 → Wire World → Von Neumann
(Universal computation and construction)
```

### Path 2: Self-Organization
```
Game of Life → Cyclic CA → Brian's Brain → Seeds
(Emergent patterns)
```

### Path 3: Self-Replication
```
HighLife → Langton's Loop → Von Neumann
(Self-copying systems)
```

### Path 4: Chaos Theory
```
Rule 90 → Rule 30 → Seeds
(Order to chaos spectrum)
```

---

## Fun Facts

**Most Famous**: Game of Life (1970)
**Oldest**: Von Neumann Constructor (1940s)
**Simplest**: Rule 90 (XOR operation)
**Most Complex**: Von Neumann Full (7,070 rules)
**Most Beautiful**: Cyclic CA (rainbow spirals)
**Most Surprising**: Rule 110 (Turing complete!)
**Most Active**: Day and Night (2000+ changes/step)
**Most Explosive**: Seeds (instant death)

---

## Next Steps

- **Try them all**: Use [Simulation Tab](../gui_guide/simulation_tab.md)
- **Compare behavior**: Run diagnostic tests
- **Create variations**: Use [Rule Editor](../gui_guide/rule_editor.md)
- **Design patterns**: Use [Pattern Editor](../gui_guide/pattern_editor.md)

**Happy exploring!** 🔬
