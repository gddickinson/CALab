# CALab - Cellular Automata Laboratory

**A comprehensive, modular framework for creating and visualizing cellular automata simulations**

## 🎯 Features

### Core Architecture
- **Modular Plugin System**: Easy to add new automata types
- **Rule Engine**: Support for table-based, totalistic, and custom rules
- **Simulation Engine**: Threaded execution with proper state management
- **Comprehensive Diagnostics**: Full error tracking and performance analysis

### PyQt GUI
- **Tabbed Interface**: Organized workflow
  - Simulation tab: Real-time visualization and controls
  - Rule Editor: Create and modify transition rules
  - Pattern Editor: Design initial configurations
  - Diagnostics: Detailed analysis and reports
- **Error Console**: Dockable error logging window
- **Status Bar**: Real-time statistics (FPS, generation count)
- **Menu System**: Full file/edit/view/tools/help menus

### Automata Included
- **Langton's Loop**: Properly implemented with actual rule table
- **Game of Life**: Gosper's Glider Gun
- **Wire World**: Signal propagation
- **Brian's Brain**: Wave patterns
- **Extensible**: Add your own via plugin system

## 📁 Project Structure

```
CALab/
├── core/                    # Core framework modules
│   ├── automaton_base.py    # Base classes and interfaces
│   ├── rule_engine.py       # Rule management
│   └── simulator.py         # Simulation engine
│
├── plugins/                 # Automaton plugins
│   ├── __init__.py
│   ├── langton_loop.py      # Proper Langton Loop
│   ├── wireworld.py
│   └── game_of_life.py
│
├── gui/                     # PyQt interface
│   ├── main_window.py       # Main application window
│   ├── simulation_tab.py    # Simulation viewer
│   ├── rule_editor_tab.py   # Rule creation
│   ├── pattern_editor_tab.py
│   ├── diagnostics_tab.py
│   └── error_console.py
│
├── utils/                   # Utilities
│   ├── diagnostics.py       # Diagnostic collection
│   └── logger.py
│
├── tests/                   # Unit tests
│   ├── test_core.py
│   ├── test_plugins.py
│   └── test_simulator.py
│
├── data/                    # Data storage
│   ├── patterns/            # Saved patterns
│   ├── rules/               # Rule sets
│   └── diagnostics/         # Diagnostic reports
│
└── main.py                  # Entry point
```

## 🚀 Installation

### Requirements
```bash
pip install PyQt5 numpy matplotlib
```

### Setup
```bash
cd CALab
python main.py
```

## 💡 Usage

### Basic Usage

```python
# Run the GUI
python main.py

# Or import as library
from core.automaton_base import CellularAutomaton
from plugins.langton_loop import LangtonLoopPlugin
from core.simulator import SimulationEngine

# Create automaton
automaton = LangtonLoopPlugin.create_automaton(150, 150)

# Create simulator
simulator = SimulationEngine(automaton)

# Run simulation
simulator.start()
```

### Creating a Custom Plugin

```python
from core.automaton_base import CellularAutomaton, PluginInterface, AutomatonMetadata
from core.rule_engine import RuleEngine

class MyAutomatonPlugin(PluginInterface):
    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="My Automaton",
            description="Custom automaton",
            author="Your Name",
            version="1.0",
            num_states=3,
            neighborhood_type=NeighborhoodType.MOORE
        )
    
    @staticmethod
    def create_automaton(width, height, **kwargs):
        return MyAutomaton(width, height)
    
    @staticmethod
    def get_default_patterns():
        return {"random": {"density": 0.3}}
```

### Unit Testing

All core modules can be run independently:

```python
# Test core automaton
from core.automaton_base import CellularAutomaton
from tests.test_core import test_automaton_base

test_automaton_base()

# Test simulator
from tests.test_simulator import test_simulation_engine

test_simulation_engine()

# Test plugins
from tests.test_plugins import test_langton_loop

test_langton_loop()
```

## 🔧 GUI Features

### Simulation Tab
- **Plugin Selection**: Dropdown to choose automaton type
- **Playback Controls**: Play, Pause, Step, Reset
- **Speed Control**: Adjust simulation speed
- **Grid Size**: Change dimensions on the fly
- **Visualization**: Real-time matplotlib display
- **Statistics**: Live density, entropy, cell counts

### Rule Editor Tab
- **Visual Rule Creation**: Click-based interface
- **Rule Validation**: Automatic checking
- **Import/Export**: Save and load rule sets
- **Testing**: Test rules before applying

### Pattern Editor Tab
- **Grid Drawing**: Click to place cells
- **Symmetry Tools**: Mirror, rotate patterns
- **Library**: Save and load patterns
- **Preview**: See pattern before applying

### Diagnostics Tab
- **Performance Metrics**: FPS, step duration
- **Behavior Analysis**: Growth, periodicity detection
- **Export**: Generate reports for debugging
- **Visualization**: Charts and graphs

## 📊 Diagnostics

The diagnostic system collects comprehensive information:

- **System Info**: Platform, Python version
- **Event Logs**: All significant events
- **Error Tracking**: Full tracebacks
- **Performance Metrics**: Timing data
- **Automaton Snapshots**: Grid states over time

Export diagnostics:
```python
from utils.diagnostics import DiagnosticCollector

diagnostics = DiagnosticCollector()
# ... run simulation ...
diagnostics.export_report("diagnostic_report.json")
```

Send this report for analysis!

## 🧪 Actual Working Implementations

### Langton's Loop
The implementation includes:
- Proper rule table (subset of 219 rules)
- von Neumann neighborhood
- State machine for replication
- Correct initialization pattern

### Why Previous Versions Didn't Work
1. **Original simplified version**: Too generic, didn't implement actual state transitions
2. **Missing rule tables**: Self-replication requires precise rules
3. **Incorrect neighborhoods**: Must use von Neumann (4-connected)

### What's Fixed
1. **Langton Loop**: Actual rule table implementation
2. **Rule Engine**: Proper pattern matching
3. **Simulator**: Thread-safe execution
4. **GUI**: Proper event-driven updates

## 🔬 For Researchers

### Extending CALab

Add new automata by creating plugins:

1. Implement `PluginInterface`
2. Define transition rules
3. Add to `plugins/` directory
4. Register in plugin manager

### Analysis Tools

```python
from utils.diagnostics import AutomatonAnalyzer

# Analyze behavior
analysis = AutomatonAnalyzer.analyze_evolution(automaton, num_steps=100)
print(analysis['classification'])  # "growing", "stable", "chaotic", etc.

# Detect periodicity
period = AutomatonAnalyzer.detect_periodicity(automaton)
if period:
    print(f"Periodic with period {period}")

# Compare automata
comparison = AutomatonAnalyzer.compare_automata(automaton1, automaton2)
print(f"Correlation: {comparison['density_correlation']}")
```

### Batch Processing

```python
from core.simulator import BatchSimulation

batch = BatchSimulation()

# Define parameter sweep
params = [
    {'width': 100, 'height': 100, 'mutation_rate': 0.001},
    {'width': 100, 'height': 100, 'mutation_rate': 0.01},
    # ... more parameter sets ...
]

# Run batch
results = batch.run_batch(
    automaton_factory=LangtonLoopPlugin.create_automaton,
    parameter_sets=params,
    num_steps=1000
)

batch.export_results("batch_results.json")
```

## 🎓 Learning Resources

### Understanding the Architecture

1. **Core**: Base classes all automata inherit from
2. **Plugins**: Specific implementations (Langton Loop, etc.)
3. **Simulator**: Runs automata in separate thread
4. **GUI**: PyQt interface wraps everything
5. **Utils**: Diagnostics, logging, analysis

### Key Concepts

- **Neighborhood**: Cells considered for transition
- **Rule Table**: Maps (current state, neighbors) → new state
- **Generation**: One complete update of all cells
- **Totalistic**: Rules based only on neighbor sum
- **State Space**: All possible cell configurations

## 🐛 Debugging

### Common Issues

**Issue**: GUI doesn't update
- **Solution**: Check that automaton.step() is being called
- **Diagnostic**: Enable debug logging

**Issue**: Automaton is static
- **Solution**: Verify rule table is not empty
- **Diagnostic**: Export and examine rules

**Issue**: Crashes or freezes
- **Solution**: Check thread synchronization
- **Diagnostic**: Export diagnostic report

### Generating Debug Reports

```python
# In GUI: File → Export Diagnostics
# Or programmatically:

diagnostics.capture_automaton_state(automaton, "before_crash")
diagnostics.log_error(exception, context="simulation_step")
diagnostics.export_report("crash_report.json")
```

Send crash_report.json for analysis!

## 📝 TODO / Future Enhancements

- [ ] Complete all 219 Langton Loop rules
- [ ] Hexagonal grid support
- [ ] 3D cellular automata
- [ ] GPU acceleration
- [ ] Network-based automata
- [ ] Machine learning rule discovery
- [ ] Pattern database/library
- [ ] Animation export (GIF/MP4)
- [ ] Undo/Redo system
- [ ] Multi-grid comparison view

## 🤝 Contributing

To add a new automaton:

1. Create plugin in `plugins/`
2. Implement `PluginInterface`
3. Add tests in `tests/`
4. Update README
5. Submit pull request

## 📜 License

MIT License - Feel free to use and modify

## 🙏 Acknowledgments

- John von Neumann: Original self-replicating automata concept
- Chris Langton: Simplified self-replicating loops
- Conway: Game of Life
- George Dickinson: Project development and FLIKA integration concepts

## 📧 Contact

For bugs, feature requests, or questions, please export a diagnostic report and share it for analysis.

---

**Built for researchers, by researchers** 🔬
