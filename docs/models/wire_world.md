# Wire World - Complete Guide

The cellular automaton for digital circuit simulation!

---

## Overview

**States**: 4
- 0: Empty (black)
- 1: Wire (yellow/conductor)
- 2: Electron Head (blue)
- 3: Electron Tail (red)

**Purpose**: Simulate electronic circuits
**Created**: Brian Silverman (1987)
**Use**: Digital logic, education, circuit design

---

## The Rules

### Simple and Elegant

**Rule 1: Empty stays empty**
```
Empty → Empty (always)
```

**Rule 2: Electron head becomes tail**
```
Head → Tail (always)
```

**Rule 3: Electron tail becomes wire**
```
Tail → Wire (always)
```

**Rule 4: Wire becomes head (conditionally)**
```
Wire + (1 or 2 heads nearby) → Head
Wire + (0, 3, 4, 5, 6, 7, or 8 heads) → Wire
```

**That's it!** Four simple rules create digital electronics.

---

## How It Works

### Electron Propagation

```
Time 0:  ====H=====
         (Wire-Head-Wire)

Time 1:  ====TH====
         (Wire-Tail-Head)

Time 2:  ====WTH===
         (Wire-Wire-Tail-Head)

Time 3:  ====WWTH==
         (Signal moves along wire)
```

**Key Insight**: Head → Tail → Wire cycle prevents backflow!

### Why 1 or 2 Heads?

**Purpose**: Control signal propagation

**If only 1**: Too restrictive
**If 1 or 2**: Perfect for logic gates
**If 3+**: Signals multiply uncontrollably

**This constraint enables**:
- Clean signal flow
- Logic gate design
- No interference
- Predictable behavior

---

## Basic Components

### Straight Wire

```
=================
```

**Purpose**: Conduct signal
**Behavior**: Head travels along
**Speed**: 1 cell per generation
**Use**: Connections

### Corner/Bend

```
====
   |
   |
```

**Purpose**: Change direction
**Behavior**: Head follows path
**Use**: Routing

### Diode (One-Way)

```
    ===
   ||
   ||
====
```

**Purpose**: Allow flow one direction only
**Mechanism**: 3 heads from wrong direction (wire stays wire)
**Use**: Control flow, prevent backflow

### Clock/Oscillator

```
   ===
  |   |
  =====
```

**Purpose**: Generate periodic signal
**Behavior**: Electron loops, emits head each cycle
**Use**: Timing, triggering

---

## Logic Gates

### NOT Gate (Inverter)

```
Input ─┐
       └─┐
         ├─ Output
Clock ───┘
```

**Operation**:
- Input present: Blocks clock signal → Output OFF
- Input absent: Clock reaches output → Output ON
- Inverts input signal

### AND Gate

```
Input A ─┐
         ├─ Output
Input B ─┘
```

**Operation**:
- Both A AND B needed
- One head alone: Wire stays wire
- Two heads together: Wire becomes head
- Perfect for 1-or-2 rule!

### OR Gate

```
Input A ─┐
         ├─ Output
Input B ─┘
         ├─ Output
```

**Operation**:
- Either A OR B triggers
- Any input creates signal
- Simple merge point

### XOR Gate

```
More complex structure
Uses combination of gates
Input A ⊕ Input B
```

**Operation**:
- True if inputs different
- False if inputs same
- Requires NOT + AND + OR

---

## Advanced Components

### Multiplexer (MUX)

**Purpose**: Select between inputs

```
Data A ──┐
         MUX── Output
Data B ──┘
         ↑
      Select
```

**Use**: Data routing, switching

### Demultiplexer (DEMUX)

**Purpose**: Route to multiple outputs

```
           ┌── Output A
Input ─ DEMUX
           └── Output B
           ↑
        Select
```

**Use**: Distribution, addressing

### Flip-Flop (Memory)

**Purpose**: Store one bit

**SR Latch**:
```
Set ──┐
      LATCH── Output
Reset ┘
```

**D Flip-Flop**:
```
Data ──┐
       FF── Output
Clock ─┘
```

**Use**: Memory, state storage

### Counter

**Purpose**: Count pulses

**Structure**: Chain of flip-flops
**Behavior**: Binary counting
**Use**: Timing, sequencing

---

## CALab Patterns

### simple_circuit

**Description**: Basic demonstration
**Contains**:
- Straight wires
- Simple corners
- Single electron

**Purpose**: Learn basics
**Run Time**: Indefinite (loops)

### or_gate

**Description**: OR gate example
**Contains**:
- Two input wires
- Merge point
- Output wire
- Electron on one input

**Purpose**: Demonstrate OR logic
**Run Time**: Watch signal merge

### diode

**Description**: One-way conductor
**Contains**:
- Diode structure
- Test signal
- Blocking mechanism

**Purpose**: Show directional flow
**Run Time**: Watch head blocked one way

### clock

**Description**: Oscillator circuit
**Contains**:
- Loop structure
- Electron circulating
- Periodic emission

**Purpose**: Timing signals
**Run Time**: Continuous oscillation

---

## Design Principles

### Wire Routing

**Guidelines**:
- Minimize crossings (can't cross!)
- Use grid efficiently
- Leave space for expansion
- Document paths

**Tricks**:
- Use empty space as insulation
- Plan layout before building
- Test segments individually

### Signal Timing

**Considerations**:
- Wire length = delay
- Longer wire = more delay
- Match timing for gates
- Use clock to synchronize

**Formula**: Delay = Wire length × 1 generation

### Component Spacing

**Rules**:
- 1 empty cell between wires (minimum)
- 2-3 cells for safety
- More for complex areas
- Less for compact designs

---

## Building Circuits

### Design Process

**Step 1: Plan**
```
1. Define inputs/outputs
2. Choose logic gates needed
3. Sketch layout
4. Estimate space
```

**Step 2: Build**
```
1. Place gates
2. Route wires
3. Add clock if needed
4. Insert test signals
```

**Step 3: Test**
```
1. Run simulation
2. Verify logic
3. Check timing
4. Debug issues
```

**Step 4: Refine**
```
1. Optimize routing
2. Reduce size
3. Improve timing
4. Document final
```

### Common Patterns

**T-Junction** (Split signal):
```
====T====
    |
```

**Merge** (Combine signals):
```
====Y====
    |
```

**Loop** (Storage/delay):
```
   ===
  |   |
  =====
```

---

## Circuit Examples

### Half Adder

**Purpose**: Add two bits
**Inputs**: A, B
**Outputs**: Sum, Carry

**Logic**:
- Sum = A XOR B
- Carry = A AND B

**Uses**: Arithmetic, counting

### Full Adder

**Purpose**: Add three bits (A + B + Carry-in)
**Outputs**: Sum, Carry-out

**Structure**: Two half adders + OR gate

**Uses**: Multi-bit addition

### Shift Register

**Purpose**: Move data left/right
**Structure**: Chain of flip-flops
**Control**: Clock signal

**Uses**: Serial communication, delays

### Binary Counter

**Purpose**: Count pulses
**Structure**: Flip-flops in cascade
**Behavior**: 00, 01, 10, 11, 00...

**Uses**: Timing, addressing, sequencing

---

## Experiments to Try

### Experiment 1: Watch Electron

```
1. Load "simple_circuit"
2. Set speed slow (300ms)
3. Follow single electron
4. Note Head → Tail → Wire cycle
5. Observe continuous flow
```

### Experiment 2: Gate Testing

```
1. Load "or_gate"
2. Watch signal merge
3. Observe OR behavior
4. Modify to test AND (need 2 inputs)
```

### Experiment 3: Clock Analysis

```
1. Load "clock"
2. Count loop length
3. Note period (time for full cycle)
4. Observe regular emission
```

### Experiment 4: Build Your Own

```
1. Pattern Editor: Draw wire
2. Add electron head
3. Add electron tail behind it
4. Test in simulation
5. Watch it propagate!
```

### Experiment 5: Diode Test

```
1. Load "diode"
2. Watch signal blocked
3. Try reverse direction
4. Compare behaviors
```

---

## Troubleshooting Circuits

### Problem: Signal Dies

**Causes**:
- Wire broken (empty cell)
- Wrong head placement
- Tail blocking head
- No continuous path

**Solutions**:
- Check wire continuity
- Verify electron sequence (H-T-W)
- Fix breaks
- Test path

### Problem: Signal Multiplies

**Causes**:
- 3+ heads near wire
- Accidental feedback
- Wrong gate design

**Solutions**:
- Check neighbor counts
- Add diodes
- Fix layout
- Space components

### Problem: Timing Issues

**Causes**:
- Wire lengths unequal
- Gates misaligned
- Clock too fast/slow

**Solutions**:
- Match wire lengths
- Add delay loops
- Adjust paths
- Synchronize inputs

### Problem: Gates Don't Work

**Causes**:
- Wrong spacing
- Missing wires
- Incorrect logic

**Solutions**:
- Verify gate design
- Check all connections
- Test with known patterns
- Debug step by step

---

## Advanced Techniques

### Compact Design

**Goals**:
- Minimize space
- Reduce wire length
- Efficient layout

**Methods**:
- Overlap carefully
- Use all directions
- Multi-layer thinking (can't actually layer!)
- Careful planning

### Modular Construction

**Approach**:
- Build tested modules
- Save as patterns
- Combine modules
- Test interfaces

**Benefits**:
- Reusable components
- Easier debugging
- Scalable designs

### Propagation Delay Management

**Challenge**: Signal timing
**Solution**: Equal path lengths

**Technique**:
```
Add delay loops to shorter paths:
Short: ====A====
Long:  ===∩∩∩A===
         (loop adds delay)
```

---

## Educational Value

### Why Wire World?

**Advantages**:
1. **Visual**: See electrons move
2. **Intuitive**: Wires make sense
3. **Practical**: Real logic gates
4. **Educational**: Learn digital design

### Learning Digital Logic

**Progression**:
```
1. Basic gates (AND, OR, NOT)
2. Combinational logic (adders, MUX)
3. Sequential logic (flip-flops)
4. Complex circuits (counters, registers)
5. Simple computers (possible!)
```

### Compared to Real Electronics

**Similarities**:
- Logic gates work same way
- Timing matters
- Signal propagation
- Circuit design principles

**Differences**:
- Slower (1 cell/gen vs speed of light)
- Visible electrons
- No voltage/current
- Discrete time steps

---

## Tips for Success

### Design

✅ **Do**:
- Plan before building
- Start simple
- Test components individually
- Document layout
- Use symmetry

❌ **Don't**:
- Build without planning
- Make too complex initially
- Skip testing
- Forget spacing
- Cross wires (impossible!)

### Testing

✅ **Do**:
- Test each gate
- Verify timing
- Use step button
- Check all paths
- Save working designs

❌ **Don't**:
- Assume it works
- Skip verification
- Run too fast
- Ignore errors

### Learning

✅ **Do**:
- Build from examples
- Modify working circuits
- Understand before creating
- Read about digital logic
- Experiment freely

❌ **Don't**:
- Copy without understanding
- Skip fundamentals
- Rush complexity
- Give up on errors

---

## Real-World Applications

### Educational

**Teaching**:
- Boolean logic
- Digital circuits
- Computer architecture
- Circuit design

**Benefits**:
- Visual learning
- Interactive
- Immediate feedback
- Fun!

### Computational

**Demonstrated**:
- Turing completeness
- Universal computation
- Can build computer in Wire World!

**Projects**:
- Working CPU designs
- ALU implementations
- Memory systems
- Full computers (theoretically)

---

## Resources

### In CALab

**Patterns**: 4 included circuits
**Tools**: Pattern editor for design
**Analysis**: Diagnostics for testing

### External

**Web**:
- Wire World computer (YouTube)
- Circuit collections
- Logic gate libraries

**Books**:
- Digital design textbooks
- Logic circuit handbooks

---

## Quick Reference

### States

| State | Color | Meaning |
|-------|-------|---------|
| 0 | Black | Empty space |
| 1 | Yellow | Wire/conductor |
| 2 | Blue | Electron head |
| 3 | Red | Electron tail |

### Basic Gates

| Gate | Inputs | Function |
|------|--------|----------|
| NOT | 1 | Inverts |
| AND | 2 | Both true |
| OR | 2 | Either true |
| XOR | 2 | Different |

### Signal Speed

**Propagation**: 1 cell per generation
**Delay**: Length of wire
**Period**: Length of loop

---

## Conclusion

Wire World shows:
- **Simplicity**: 4 states, simple rules
- **Power**: Build real logic circuits
- **Beauty**: Visible electron flow
- **Education**: Learn digital design

**Perfect for understanding digital electronics!**

---

## Next Steps

**Basic**: Try all CALab patterns

**Intermediate**: Build simple gates

**Advanced**: Design complex circuits

**Expert**: Create computer components

---

**Build the circuits of your imagination!** ⚡✨
