# Theory and Mathematics of Cellular Automata

Understanding the mathematical foundations of CA.

---

## Mathematical Definition

A cellular automaton is a 4-tuple: **CA = (L, S, N, f)**

### L: Lattice
The grid structure (usually ℤ² for 2D)
- **1D**: Line of cells
- **2D**: Grid of cells  
- **3D**: Volume of cells

### S: States
Finite set of possible states
- S = {0, 1} for 2-state CA
- S = {0, 1, 2, ..., n-1} for n-state CA
- Examples: {dead, alive}, {empty, wire, head, tail}

### N: Neighborhood
Function defining which cells influence each other
- **Von Neumann**: {N, E, S, W}
- **Moore**: {NW, N, NE, E, SE, S, SW, W}
- **Radius-r**: All cells within distance r

### f: Transition Function
Rule that determines next state
- f: S^|N| → S
- Takes neighborhood states → new center state
- Example: f({alive, dead, alive, ...}) = alive

---

## State Space

### Configuration Space
Set of all possible grid configurations
- For n states and w×h grid: n^(w×h) configurations
- Example: 100×100 Life grid = 2^10,000 ≈ 10^3,010 configurations
- Impossibly large to enumerate!

### Dynamics
Evolution function φ: C → C
- Maps configuration to next configuration
- Applied repeatedly: φ, φ², φ³, ...
- Creates trajectory through state space

### Orbits
Sequence of configurations under repeated application
- **Fixed Point**: φ(c) = c (still life)
- **Period-n**: φⁿ(c) = c (oscillator)
- **Eventually Periodic**: Reaches cycle
- **Chaotic**: Never repeats

---

## Neighborhood Functions

### Von Neumann Neighborhood

```
Distance 1:
      N
      |
  W - C - E
      |
      S

Size: 4 neighbors
```

**Properties**:
- Manhattan distance ≤ 1
- |N| = 4
- 5 cells total (including center)

**Used by**:
- Von Neumann Constructor
- Many historical CA

### Moore Neighborhood

```
Distance 1:
  NW  N  NE
   |  |  |
  W - C - E
   |  |  |
  SW  S  SE

Size: 8 neighbors
```

**Properties**:
- Chebyshev distance ≤ 1
- |N| = 8
- 9 cells total

**Used by**:
- Game of Life
- Most popular CA

### Extended Neighborhoods

**Von Neumann Radius-2**:
```
        N2
         |
     NW N NE
      | | |
  W2 W C E E2
      | | |
     SW S SE
         |
        S2

Size: 12 neighbors
```

**Moore Radius-2**:
All cells within Chebyshev distance 2
Size: 24 neighbors

---

## Rule Classifications

### Totalistic Rules

Next state depends only on **sum** of neighbor states.

**Mathematical Form**:
```
f(c, n₁, n₂, ..., nₖ) = g(c, Σnᵢ)
```

**Example**: Game of Life (B3/S23)
```
If c = 0 and Σnᵢ = 3: next = 1
If c = 1 and Σnᵢ ∈ {2,3}: next = 1
Otherwise: next = 0
```

**Advantages**:
- Simple to specify
- Easy to understand
- Often interesting

**Limitations**:
- Cannot distinguish patterns
- No directional information

### Outer Totalistic

Depends on sum + center state separately.

**More expressive** than pure totalistic.

### Table-Based Rules

Explicit lookup for each pattern.

**Mathematical Form**:
```
f(c, n₁, n₂, ..., nₖ) = lookup[(c, n₁, n₂, ..., nₖ)]
```

**Example**: Langton's Loop
- 219 explicit rules
- Each pattern specified

**Advantages**:
- Maximum flexibility
- Directional control
- Asymmetric behavior

**Limitations**:
- Large tables
- Hard to design
- Not intuitive

---

## Important Properties

### Reversibility

**Definition**: Injective evolution function
- φ(c₁) = φ(c₂) ⟹ c₁ = c₂
- Can reconstruct previous state
- Information preserved

**Examples**:
- Most CA are **irreversible**
- Life is irreversible
- Special CA can be reversible (Margolus neighborhood)

**Implications**:
- Entropy increases (2nd law thermodynamics)
- Garden of Eden patterns
- Predecessor problem

### Garden of Eden

**Definition**: Configuration with no predecessor
- Cannot be reached from any previous state
- Can only exist at t = 0
- Exists in most CA

**Example in Life**:
- Certain patterns have no predecessor
- Proved to exist (Moore, Myhill)

### Universality

**Definition**: Can simulate any computation
- Turing complete
- Can build logic gates
- Can implement any algorithm

**Examples**:
- Rule 110 (elementary CA)
- Game of Life
- Von Neumann Constructor

**Proof Methods**:
- Build logic gates (AND, OR, NOT)
- Construct wires for signals
- Create memory elements
- Show can simulate Turing machine

---

## Elementary Cellular Automata

### Definition

**Simplest possible CA**:
- 1D lattice
- 2 states: {0, 1}
- Neighborhood: {left, center, right}

### Rule Numbering

**Total possible rules**: 2^8 = 256

**Rule number** from truth table:
```
LCR → New
111 → b₇
110 → b₆
101 → b₅
100 → b₄
011 → b₃
010 → b₂
001 → b₁
000 → b₀

Rule number = Σ bᵢ × 2^i
```

**Example**: Rule 110
```
111→0, 110→1, 101→1, 100→0
011→1, 010→1, 001→1, 000→0

Binary: 01101110
Decimal: 110
```

### Wolfram Classification

**Class 1**: Uniform
- Evolves to homogeneous state
- Example: Rule 0

**Class 2**: Periodic
- Simple repeating structures
- Example: Rule 54

**Class 3**: Chaotic
- Random, unpredictable
- Example: Rule 30

**Class 4**: Complex
- Long-lived structures
- Edge of chaos
- Example: Rule 110

---

## Computational Complexity

### Time Complexity

**Naive simulation**:
```
For each step:
  For each cell:
    Check neighbors
    Apply rule
    
Time: O(n × g)
- n = number of cells
- g = number of generations
```

### Space Complexity

**Grid storage**:
```
Space: O(w × h × s)
- w = width
- h = height  
- s = bytes per state
```

**Optimization**:
- Sparse grids (hashlife)
- Only store active regions
- Compress periodic patterns

### Hashlife Algorithm

**Revolutionary optimization**:
- Exponential speedup
- Hashes repeated patterns
- Jumps forward in time
- Practical for 10^9+ generations

---

## Pattern Theory

### Still Lifes

**Mathematical Definition**:
Fixed points of evolution function
```
φ(P) = P
```

**Properties**:
- Zero velocity
- Stable configuration
- Local equilibrium

**Examples in Life**:
- Block (2×2)
- Beehive
- Loaf

### Oscillators

**Definition**: Period-n patterns
```
φⁿ(P) = P
φᵏ(P) ≠ P for 0 < k < n
```

**Properties**:
- Return to original state
- Period n (minimal)
- Periodic orbit

**Examples**:
- Blinker (period 2)
- Pulsar (period 3)
- Pentadecathlon (period 15)

### Spaceships

**Definition**: Translating patterns
```
φⁿ(P) = translate(P, Δx, Δy)
```

**Velocity**: v = Δ / n
- Δ = translation distance
- n = period
- Usually expressed as "c/n"

**Speed Limit**:
- Life: c/2 (light speed / 2)
- Diagonal: c (light speed)
- Depends on CA rules

### Guns

**Definition**: Patterns that emit spaceships
```
φⁿ(P) = P + spaceship
```

**Requirements**:
- Periodic core
- Emission mechanism
- Clean separation

**Famous Example**:
- Gosper Glider Gun (period 30)

---

## Entropy and Information

### Shannon Entropy

**Definition**:
```
H = -Σ pᵢ log₂(pᵢ)
```
- pᵢ = probability of state i
- Measures uncertainty
- Maximum when uniform

**In CA**:
- Class 1: Low entropy (uniform)
- Class 3: High entropy (chaotic)
- Class 4: Medium entropy (complex)

### Mutual Information

**Measures correlation**:
```
I(X;Y) = H(X) + H(Y) - H(X,Y)
```

**In CA**:
- How much one cell tells about another
- Decreases with distance
- Varies with rule class

### Lyapunov Exponents

**Measures sensitivity**:
- λ > 0: Chaotic (diverge)
- λ = 0: Neutral (borderline)
- λ < 0: Stable (converge)

---

## Emergent Computation

### Logic Gates

**AND Gate**:
```
Input A ─┐
         └─ AND ─ Output
Input B ─┘
```
Can be built in Life, Wire World

**OR Gate**:
```
Input A ─┐
         └─ OR ─ Output
Input B ─┘
```

**NOT Gate**:
```
Input ─ NOT ─ Output
```

### Universal Computation

**Requirements**:
1. Logic gates (AND, OR, NOT)
2. Wires (signal transmission)
3. Memory (state storage)
4. Control (conditional execution)

**Implication**:
- Can compute any computable function
- Can simulate any computer
- Turing complete

---

## Self-Replication Theory

### Von Neumann's Approach

**Components**:
1. **Universal Constructor**: Builds anything
2. **Universal Computer**: Executes instructions
3. **Tape Reader**: Reads construction plan
4. **Instructions**: Self-description

**Process**:
1. Read instructions
2. Build copy of machine
3. Copy instructions to new machine
4. Separate

### Langton's Simplification

**Reduced complexity**:
- 8 states (vs 29)
- Simpler rules
- Loop structure
- Same principle

---

## Open Problems

### Undecidable Problems

**Halting Problem**:
- Given initial pattern, will it halt?
- Undecidable in general
- Equivalent to Turing halting problem

**Garden of Eden Problem**:
- Does a specific pattern have predecessor?
- Undecidable in general

### Open Questions

**Life Patterns**:
- Smallest spaceship at each velocity?
- All possible oscillator periods?
- Optimal glider guns?

**General CA**:
- Classification completeness?
- Complexity measures?
- Prediction methods?

---

## Further Reading

**Classic Papers**:
- Von Neumann (1966) - Self-replication
- Wolfram (1983) - Classification
- Cook (2004) - Rule 110 proof

**Books**:
- "A New Kind of Science" - Wolfram
- "Cellular Automata Machines" - Toffoli & Margolus
- "The Recursive Universe" - Poundstone

**Online**:
- LifeWiki
- Wolfram MathWorld
- Complex Systems journal

---

## Summary

CA are:
- **Simple**: Few rules
- **Rich**: Complex behavior
- **Universal**: Can compute anything
- **Emergent**: Whole > parts
- **Mathematical**: Rigorous framework

Study CA to understand:
- Complexity from simplicity
- Emergence and self-organization
- Computation and information
- Pattern formation
- Artificial life

---

**Next**: [Models Overview](models/overview.md) to see theory in practice!
