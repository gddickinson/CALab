# Sonification Tab Guide

The **Sonification Tab** transforms cellular automaton patterns into music and sound, giving you a whole new way to experience and understand CA behavior!

---

## Overview

**Sonification** = Converting visual patterns into audio

The Sonification tab offers:
- **7 different sound modes**
- **Musical scale selection**
- **Real-time audio generation**
- **Interactive visualization**
- **Stereo effects**

**Goal**: Hear your cellular automata!

---

## Getting Started

### Prerequisites

**Required**: `sounddevice` library

Install with:
```bash
pip install sounddevice
```

If not installed, you'll see a warning in the tab.

### Quick Start

```
1. Run a simulation in Simulation tab
2. Switch to Sonification tab
3. Choose a mode (e.g., "Row Scanner")
4. Click "▶️ Play Sound"
5. Listen to your CA!
```

---

## Interface Overview

### Top: Playback Controls

**Play/Stop Button**:
- ▶️ Play Sound - Start audio generation
- ⏸️ Stop Sound - Stop playback

**Volume Slider**:
- Range: 0-100%
- Real-time adjustment
- Default: 50%

### Left: Sonification Mode

**Mode Selection**:
- 7 different modes
- Each creates unique sounds
- Description updates when changed

**Scan Speed**:
- 1-20 Hz (times per second)
- Faster = more rapid scanning
- Default: 5 Hz

### Right: Musical Settings

**Scale**: Choose musical scale
**Root Note**: Base pitch (MIDI)
**Octave Range**: Pitch spread
**Waveform**: Sound character
**Note Duration**: Length of each note
**Reverb**: Add spaciousness

### Bottom: Visualization

**Current Note**: Note being played
**Activity**: Pattern activity level
**Frequency**: Pitch in Hertz

---

## Sonification Modes

### 1. Row Scanner

**How it works**:
- Scans grid row by row (top to bottom)
- Active cells in each row create notes
- Density determines pitch

**Sound**:
- More active cells = higher pitch
- Creates melodic sweeping patterns
- Good for seeing vertical structures

**Best for**:
- Game of Life gliders
- Horizontal patterns
- General exploration

**Example**:
```
Grid:
. . X X .   → Medium note
. . . . .   → Silence
X X X X X   → High note
```

### 2. Column Scanner

**How it works**:
- Scans left to right
- Active cells create notes
- Left/right position = stereo panning

**Sound**:
- Spatial audio (stereo)
- Left column = left speaker
- Right column = right speaker

**Best for**:
- Vertical patterns
- Spaceships
- Brian's Brain waves

**Unique**:
- Only mode with stereo panning!

### 3. Density Wave

**How it works**:
- Monitors overall cell density
- High density = high pitch
- Creates ambient soundscape

**Sound**:
- Smooth, sustained tones
- Evolves with pattern
- Drone-like quality

**Best for**:
- Seeds (explosive growth)
- Rule 30 (chaos)
- Watching evolution over time

**Feel**:
- Meditative
- Ambient music

### 4. State Percussion

**How it works**:
- Each state triggers different sound
- Multiple states = layered percussion
- Quick rhythmic hits

**Sound**:
- Percussive, rhythmic
- Multi-state patterns sound complex
- Like drums for each state

**Best for**:
- Wire World (4 states)
- Brian's Brain (3 states)
- Von Neumann (many states)

**Pattern**:
```
State 1 → Low drum
State 2 → Mid drum
State 3 → High drum
All together → Rhythm!
```

### 5. Cellular Melody

**How it works**:
- Picks random active cells
- X position = note in scale
- Y position = octave

**Sound**:
- Melodic, musical
- Uses selected scale
- Random but harmonious

**Best for**:
- Game of Life patterns
- Any active CA
- Musical exploration

**Mapping**:
```
Top rows → High octaves
Bottom rows → Low octaves
Left columns → First notes of scale
Right columns → Last notes of scale
```

### 6. Chaos Rhythm

**How it works**:
- Monitors state CHANGES
- More changes = more sound
- Drives simulation forward

**Sound**:
- Rhythmic pulses
- Intensity varies
- Tracks dynamics

**Best for**:
- Rule 30 (chaotic)
- Seeds (explosive)
- Day and Night

**Special**:
- Advances simulation automatically!
- Hear the rate of change

### 7. Ambient Drone

**How it works**:
- Creates chord (root + fifth + octave)
- Sustained tones
- Based on overall complexity

**Sound**:
- Rich, harmonic
- Continuous drone
- Meditative quality

**Best for**:
- Background ambience
- Meditation
- Long-running patterns

**Character**:
- Peaceful
- Immersive
- Contemplative

---

## Musical Settings

### Scale Selection

**Major**: Happy, bright
```
C D E F G A B
Do Re Mi Fa Sol La Ti
```

**Minor**: Sad, dark
```
C D Eb F G Ab Bb
More emotional feel
```

**Pentatonic**: Asian, simple
```
C D E G A
Very harmonious
No "bad" notes
```

**Blues**: Expressive, soulful
```
C Eb F F# G Bb
Blues feeling
```

**Chromatic**: All notes
```
C C# D D# E F F# G G# A A# B
Every semitone
Dissonant possibilities
```

**Whole Tone**: Dreamy
```
C D E F# G# A#
Debussy-like
Floating quality
```

**Harmonic Minor**: Exotic
```
C D Eb F G Ab B
Middle Eastern flavor
Dramatic
```

### Root Note

**MIDI number** of base pitch:
- 60 = Middle C (default)
- 48 = C one octave below
- 72 = C one octave above

**Range**: 36 (C2) to 84 (C6)

**Lower** = Deeper, bass-like
**Higher** = Brighter, treble-like

### Octave Range

**How many octaves** to spread across:
- 1 octave = Narrow range
- 2 octaves = Medium range (default)
- 3-4 octaves = Wide range

**Larger range** = More pitch variation

### Waveform

Different **tone colors**:

**Sine**: Pure, smooth
- Flute-like
- Clean tone
- No harmonics

**Square**: Buzzy, retro
- 8-bit game sound
- Hollow quality
- Odd harmonics

**Sawtooth**: Bright, sharp
- Brassy
- Rich in harmonics
- Cutting sound

**Triangle**: Soft, mellow
- Between sine and square
- Gentle
- Few harmonics

### Note Duration

**How long** each note plays:
- 0.01 sec = Very short, percussive
- 0.1 sec = Short note (default)
- 0.5 sec = Medium sustain
- 2.0 sec = Long, sustained

**Shorter** = More rhythmic
**Longer** = More flowing

### Reverb

**Add reverb** checkbox:
- ☐ Off = Dry, direct
- ☑ On = Spacious, echoey

**Effect**:
- Simulates room acoustics
- Adds depth
- More pleasant

---

## Experiments to Try

### Experiment 1: Glider Song

```
1. Simulation tab: Load Game of Life glider
2. Sonification tab
3. Mode: Row Scanner
4. Scale: Pentatonic
5. Play
6. Result: Descending melody as glider moves down!
```

### Experiment 2: Chaos Percussion

```
1. Load Rule 30, single cell
2. Mode: State Percussion
3. Waveform: Square
4. Duration: 0.05 sec
5. Play
6. Result: Chaotic rhythm!
```

### Experiment 3: Ambient Life

```
1. Load Life random pattern
2. Mode: Ambient Drone
3. Scale: Minor
4. Reverb: ON
5. Play
6. Result: Evolving ambient music
```

### Experiment 4: Seeds Explosion

```
1. Load Seeds serviette pattern
2. Mode: Density Wave
3. Scan Speed: 10 Hz
4. Play
5. Result: Rising pitch as pattern explodes!
```

### Experiment 5: Wire World Circuit

```
1. Load Wire World clock
2. Mode: State Percussion
3. All 4 states create different sounds
4. Play
5. Result: Rhythmic electronic pattern!
```

### Experiment 6: Stereo Waves

```
1. Load Brian's Brain circle
2. Mode: Column Scanner
3. Play
4. Result: Waves sweep left to right in stereo!
```

### Experiment 7: Scale Comparison

```
Same pattern, different scales:
1. Major - Happy feel
2. Minor - Sad feel
3. Blues - Soulful
4. Compare the emotion!
```

---

## Tips for Best Results

### General

✅ **Do**:
- Start with medium volume (50%)
- Use headphones for stereo effects
- Try different modes
- Experiment with scales
- Adjust scan speed
- Listen for patterns

❌ **Don't**:
- Max volume immediately
- Ignore stereo (use both ears!)
- Stick to one mode
- Forget to try scales
- Rush through

### Mode Selection

**Active patterns** → Row/Column Scanner
**Multi-state** → State Percussion
**Chaotic** → Chaos Rhythm or Density Wave
**Peaceful** → Ambient Drone
**Musical** → Cellular Melody

### Musical Settings

**Harmonious** → Pentatonic, Major
**Experimental** → Chromatic, Whole Tone
**Emotional** → Minor, Blues
**Exotic** → Harmonic Minor

**Short notes** → Percussive, rhythmic
**Long notes** → Flowing, ambient

### Performance

If **choppy audio**:
- Reduce scan speed
- Increase note duration
- Simplify mode
- Close other programs

If **too quiet**:
- Increase volume slider
- Check system volume
- Verify audio device

---

## Understanding the Sound

### What You're Hearing

**Pitch** (high/low):
- Density of active cells
- Position in grid
- State values

**Rhythm** (timing):
- Scan speed
- Pattern changes
- State transitions

**Timbre** (tone color):
- Waveform selection
- Number of states
- Reverb setting

**Spatial** (stereo):
- Column Scanner mode
- Left/right position
- Panning

### Pattern Recognition

**Oscillator** (Life blinker):
- Alternating pitches
- Regular rhythm
- Predictable

**Spaceship** (glider):
- Moving pitch pattern
- Directional sweep
- Continuous motion

**Chaos** (Rule 30):
- Random pitches
- Unpredictable
- Never repeats

**Growth** (Seeds):
- Rising pitches
- Increasing density
- Accelerating

**Stable** (still life):
- Constant pitch
- No change
- Peaceful

---

## Technical Details

### Audio Specifications

**Sample Rate**: 44,100 Hz (CD quality)
**Channels**: 2 (stereo)
**Bit Depth**: 16-bit
**Latency**: ~50ms

### MIDI Notes

**Range**: 36-84 (C2 to C6)
**Middle C**: MIDI 60
**Concert A**: MIDI 69 = 440 Hz

**Formula**: 
```
Frequency = 440 * 2^((MIDI - 69) / 12)
```

### Waveform Math

**Sine**: sin(2πft)
**Square**: sign(sin(2πft))
**Sawtooth**: 2(ft - floor(ft + 0.5))
**Triangle**: 2|2(ft - floor(ft + 0.5))| - 1

Where:
- f = frequency
- t = time

---

## Troubleshooting

### No Sound

**Check**:
- Volume slider not at 0?
- System audio on?
- Correct audio device?
- Simulation running?
- sounddevice installed?

**Solutions**:
- Adjust volume
- Check system settings
- Verify installation
- Load automaton first

### Audio Crackling

**Causes**:
- CPU overload
- Scan speed too high
- Buffer underrun

**Solutions**:
- Reduce scan speed
- Close other programs
- Increase note duration
- Simplify grid size

### Wrong Notes

**Causes**:
- Scale mismatch
- Root note wrong
- Octave range off

**Solutions**:
- Check scale selection
- Verify root note
- Adjust octave range
- Try different mode

### Too Chaotic

**Solutions**:
- Use Pentatonic scale (always sounds good)
- Reduce octave range to 1
- Try Ambient Drone mode
- Lower scan speed

### Too Boring

**Solutions**:
- Increase scan speed
- Try Chaos Rhythm mode
- Use more active pattern
- Experiment with scales

---

## Creative Applications

### Composition

**Use CA as**:
- Melody generator
- Rhythm source
- Ambient backing
- Experimental instrument

**Record** with:
- Audio recording software
- System audio capture
- DAW integration

### Live Performance

**Combine**:
- Multiple CAs
- Different modes
- Various scales
- Pattern switching

**Control**:
- Real-time parameter changes
- Mode switching
- Scale modulation
- Volume dynamics

### Meditation

**Settings**:
- Ambient Drone mode
- Minor or Pentatonic scale
- Reverb ON
- Long note duration
- Low volume

**Patterns**:
- Stable Life patterns
- Cyclic CA spirals
- Slow evolution

### Education

**Demonstrate**:
- Pattern types through sound
- Chaos vs order
- State changes
- Spatial relationships

**Compare**:
- Life vs Seeds (order vs chaos)
- Rule 90 vs Rule 30 (fractal vs random)
- Different states (Wire World)

---

## Advanced Techniques

### Mode Combinations

**Try changing modes** while playing:
- Shift between perspectives
- Hear different aspects
- Find interesting combinations

### Parameter Modulation

**Adjust during playback**:
- Scan speed (tempo changes)
- Volume (dynamics)
- Scale (key changes)
- Waveform (timbre changes)

### Pattern Design for Sound

**Create patterns** specifically for sonification:
- Vertical patterns → Row Scanner
- Horizontal patterns → Column Scanner
- Dense patterns → Density Wave
- Multi-state → State Percussion

---

## Fun Facts

**Unusual sounds**:
- Langton's Loop makes weird chirps
- Seeds creates rising screams
- Cyclic CA makes swirling sounds
- Wire World sounds electronic

**Musical CAs**:
- Some Life patterns are "musical"
- Gliders create descending melodies
- Oscillators make rhythms
- Guns create repeating phrases

**Synesthesia**:
- Some people "see sounds"
- Sonification helps everyone experience this
- Colors → Pitches
- Patterns → Rhythms

---

## Quick Reference

### Modes Summary

| Mode | Best For | Sound Type |
|------|----------|------------|
| Row Scanner | General | Melodic |
| Column Scanner | Waves | Stereo melodic |
| Density Wave | Growth | Ambient |
| State Percussion | Multi-state | Rhythmic |
| Cellular Melody | Life | Musical |
| Chaos Rhythm | Chaos | Percussive |
| Ambient Drone | Background | Harmonic |

### Scale Feelings

| Scale | Mood |
|-------|------|
| Major | Happy |
| Minor | Sad |
| Pentatonic | Pleasant |
| Blues | Soulful |
| Chromatic | Experimental |
| Whole Tone | Dreamy |

### Waveforms

| Waveform | Character |
|----------|-----------|
| Sine | Pure, smooth |
| Square | Buzzy, retro |
| Sawtooth | Bright, sharp |
| Triangle | Soft, mellow |

---

## Integration with Other Tabs

### With Simulation

**Flow**:
```
Simulation → Load pattern → Run
     ↓
Sonification → Select mode → Play
     ↓
Listen while watching visualization
```

### With Diagnostics

**Analysis**:
```
Run pattern
Check classification (Diagnostics)
Choose appropriate mode (Sonification)
Hear the behavior!
```

### With Pattern Editor

**Design**:
```
Create pattern for sound
Test in Sonification
Refine based on audio
Perfect the pattern
```

---

## Conclusion

Sonification provides:
- **New perspective** on CA behavior
- **Musical creativity** from patterns
- **Educational tool** for understanding
- **Artistic expression** through code
- **Fun experimentation** with sound

**Listen to the mathematics!** 🎵✨

---

## Next Steps

**Explore**: Try all 7 modes

**Compare**: Same pattern, different modes

**Create**: Design patterns for sound

**Share**: Record and share your CA music!

---

**Turn patterns into melodies!** 🎶🔬
