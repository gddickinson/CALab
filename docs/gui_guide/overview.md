# GUI Overview

Welcome to the CALab graphical user interface!

---

## Interface Layout

CALab uses a **tabbed interface** with 5 main tabs:

1. **Simulation** - Run and visualize automata
2. **Rule Editor** - Create custom rules
3. **Pattern Editor** - Design initial patterns
4. **Diagnostics** - Analyze behavior
5. **Documentation** - Access help (you're here!)

---

## Tab Navigation

### Switching Tabs

Click tab names at the top to switch between modes.

**Keyboard shortcuts** (future):
- Ctrl+1: Simulation
- Ctrl+2: Rule Editor
- Ctrl+3: Pattern Editor
- Ctrl+4: Diagnostics
- Ctrl+5: Documentation (F1)

### Tab Purposes

**Simulation Tab**: The main workspace
- Select automaton and pattern
- Run simulations
- Watch evolution
- View live statistics

**Rule Editor**: For creators
- Design custom rules
- Totalistic (Life-like) rules
- Table-based rules
- Import/export rules

**Pattern Editor**: For designers
- Draw patterns visually
- 30x30 canvas
- Drawing tools (mirror, rotate, etc)
- Pattern library

**Diagnostics**: For analysis
- Behavior classification
- Statistical analysis
- Event logging
- Export data

**Documentation**: For learning
- Complete user guides
- Model references
- Tutorials
- API documentation

---

## Menu Bar

### File Menu

**New Simulation** (Ctrl+N)
- Reset to fresh start
- Clear current state

**Open...** (Ctrl+O)
- Load saved simulation
- Import patterns/rules

**Save** (Ctrl+S) / **Save As...**
- Save current state
- Export configurations

**Export Image**
- Save current visualization
- PNG format

**Exit** (Ctrl+Q)
- Close application
- Confirm unsaved work

### Edit Menu

**Undo** (Ctrl+Z) - Future feature
**Redo** (Ctrl+Y) - Future feature
**Preferences** - Application settings

### View Menu

**Show Error Console** (Ctrl+E)
- Toggle error console
- View warnings/errors
- Debugging information

**Full Screen** (F11)
- Maximize workspace
- Hide OS elements

**Reset Layout**
- Return to default layout
- Fix broken windows

### Tools Menu

**Run Diagnostic Test**
- Test all plugins
- Verify functionality
- Performance check

**Clear Error Log**
- Remove all errors
- Fresh start

**Generate Report**
- Export diagnostic data
- System information

### Help Menu

**Documentation** (F1)
- Jump to docs tab
- Context-sensitive help

**About CALab**
- Version information
- Credits
- License

**Check for Updates**
- Latest version check
- Download updates

---

## Status Bar

Located at bottom of window.

Shows real-time information:
- Current automaton
- Current pattern
- Generation count
- Active cells
- FPS (performance)

---

## Error Console

Dockable panel at bottom (toggle: Ctrl+E).

### Features

**Color-Coded Messages**:
- 🔴 Red: Errors
- 🟡 Yellow: Warnings
- 🔵 Blue: Info

**Counters**:
- Total errors
- Total warnings
- Total messages

**Actions**:
- Clear log
- Export log
- Copy selected

### When to Check

Check if:
- Unexpected behavior
- Simulation won't start
- Features not working
- Performance issues

---

## Keyboard Shortcuts

### Global

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New simulation |
| Ctrl+O | Open file |
| Ctrl+S | Save |
| Ctrl+Q | Quit |
| F1 | Documentation |
| F11 | Full screen |
| Ctrl+E | Toggle error console |

### Simulation (Future)

| Shortcut | Action |
|----------|--------|
| Space | Play/Pause |
| S | Step forward |
| R | Reset |
| +/- | Speed adjust |

### Editing (Future)

| Shortcut | Action |
|----------|--------|
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Ctrl+C | Copy |
| Ctrl+V | Paste |

---

## Common Workflows

### Workflow 1: Quick Exploration

```
1. Start CALab
2. Simulation tab (default)
3. Select automaton
4. Select pattern
5. Press Play
6. Adjust speed
7. Try different patterns
```

### Workflow 2: Create Custom Rule

```
1. Simulation tab: Test existing rules
2. Rule Editor tab: Create new rule
3. (Future) Simulation tab: Test rule
4. Rule Editor: Refine
5. Export rule when satisfied
```

### Workflow 3: Design Pattern

```
1. Pattern Editor tab
2. Draw pattern on canvas
3. Use tools (mirror, rotate)
4. Save to library
5. (Future) Simulation tab: Test
6. Refine in Pattern Editor
7. Export final version
```

### Workflow 4: Analysis

```
1. Simulation tab: Run automaton
2. Let evolve 200+ steps
3. Diagnostics tab: View analysis
4. Check classification
5. Review metrics
6. Export data
```

### Workflow 5: Learning

```
1. Documentation tab
2. Read Introduction
3. Follow Quick Start
4. Try in Simulation tab
5. Read specific model docs
6. Explore tutorials
```

---

## Tips for Efficiency

### Organization

✅ **Do**:
- Use descriptive names for patterns/rules
- Export important work regularly
- Keep patterns organized in library
- Document interesting discoveries

❌ **Don't**:
- Use generic names ("test1", "pattern2")
- Forget to save work
- Mix unrelated patterns
- Ignore documentation

### Performance

✅ **Do**:
- Start with smaller grid sizes
- Use medium speed settings
- Close error console when not needed
- Test with simple patterns first

❌ **Don't**:
- Max out grid size immediately
- Run at highest speed
- Keep error console open always
- Jump to complex patterns

### Learning

✅ **Do**:
- Read documentation first
- Follow tutorials step-by-step
- Experiment freely
- Ask for help (check docs)

❌ **Don't**:
- Skip documentation
- Rush through tutorials
- Fear making mistakes
- Ignore error messages

---

## Customization

### Preferences (Future Feature)

**Appearance**:
- Theme (light/dark)
- Font size
- Color schemes
- Grid appearance

**Behavior**:
- Default grid size
- Default speed
- Auto-play on load
- Confirmation dialogs

**Performance**:
- FPS limit
- Memory limit
- Thread count

### Layout

**Rearrange** (future):
- Drag tabs to reorder
- Detach tabs to windows
- Save custom layouts

**Docking**:
- Error console dockable
- Future: Other dockable panels

---

## Accessibility

### Current Features

- Clear tab labels
- Color-coded status
- Readable fonts
- Error console for messages

### Future Features

- High contrast mode
- Screen reader support
- Keyboard-only navigation
- Adjustable UI scale

---

## Troubleshooting

### GUI Won't Start

**Solutions**:
- Check Python version (3.7+)
- Verify PyQt5 installed
- Check error messages
- Try from command line

### Tabs Not Showing

**Solutions**:
- Maximize window
- Check View → Reset Layout
- Restart application

### Controls Not Responding

**Solutions**:
- Check Error Console
- Try different tab
- Restart simulation
- Restart application

### Performance Issues

**Solutions**:
- Reduce grid size
- Lower speed setting
- Close other applications
- Check system resources

---

## Best Practices

### Before You Start

1. Read [Quick Start Guide](../QUICKSTART.md)
2. Understand [CA Basics](../introduction.md)
3. Familiarize with interface
4. Try simple examples

### While Working

1. Save work frequently
2. Use descriptive names
3. Test incrementally
4. Document discoveries

### When Finished

1. Export important work
2. Clear temporary data
3. Document learnings
4. Share discoveries

---

## Next Steps

**New Users**:
1. Read [Introduction](../introduction.md)
2. Follow [Quick Start](../QUICKSTART.md)
3. Try [Simulation Tab](simulation_tab.md)

**Creating Content**:
1. Learn [Rule Editor](rule_editor.md)
2. Learn [Pattern Editor](pattern_editor.md)
3. Follow [Tutorials](../tutorials/creating_rules.md)

**Advanced Users**:
1. Review [Diagnostics](diagnostics.md)
2. Study [API Reference](../reference/api.md)
3. Create [Plugins](../tutorials/creating_plugins.md)

---

## Quick Reference

### Tab Summary

| Tab | Purpose | Use When |
|-----|---------|----------|
| Simulation | Run CA | Exploring, testing |
| Rule Editor | Make rules | Creating, customizing |
| Pattern Editor | Draw patterns | Designing, editing |
| Diagnostics | Analyze | Studying, research |
| Documentation | Learn | Stuck, learning |

### Essential Actions

| Task | Where | How |
|------|-------|-----|
| Run automaton | Simulation | Select + Play |
| Create rule | Rule Editor | Enter + Add |
| Draw pattern | Pattern Editor | Click + Draw |
| Get help | Documentation | Click tab |

---

**Welcome to CALab!** Explore, create, discover! 🚀
