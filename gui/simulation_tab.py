"""
CALab - Simulation Tab
Main simulation viewer with live visualization and controls
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QSlider, QComboBox, QSpinBox, QGroupBox,
                             QTextEdit, QGridLayout, QSplitter)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import ListedColormap
import numpy as np

from plugins import PLUGIN_REGISTRY, list_plugins


class SimulationTab(QWidget):
    """
    Main simulation tab with visualization and controls
    """
    
    # Signals
    error_occurred = pyqtSignal(str, str)  # (error_type, message)
    status_update = pyqtSignal(str)  # status message
    
    def __init__(self, simulator, diagnostics):
        super().__init__()
        
        self.simulator = simulator
        self.diagnostics = diagnostics
        self.current_automaton = None
        self.current_plugin = None
        
        # Setup callbacks
        self.simulator.on_step_callback = self._on_simulation_step
        self.simulator.on_error_callback = self._on_simulation_error
        
        self._setup_ui()
        
        # Update timer for live stats
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_display)
        self.update_timer.start(100)  # Update every 100ms
        
    def _setup_ui(self):
        """Setup the user interface"""
        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        # Left side: Visualization
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Matplotlib canvas
        self.figure = Figure(figsize=(8, 8))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.axis('off')
        self.im = None
        
        left_layout.addWidget(self.canvas)
        
        # Right side: Controls
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setAlignment(Qt.AlignTop)
        
        # Automaton selection
        selection_group = self._create_selection_group()
        right_layout.addWidget(selection_group)
        
        # Playback controls
        playback_group = self._create_playback_group()
        right_layout.addWidget(playback_group)
        
        # Parameters
        params_group = self._create_parameters_group()
        right_layout.addWidget(params_group)
        
        # Statistics
        stats_group = self._create_statistics_group()
        right_layout.addWidget(stats_group)
        
        # Add stretch at bottom
        right_layout.addStretch()
        
        # Use splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([800, 300])
        
        main_layout.addWidget(splitter)
        
    def _create_selection_group(self):
        """Create automaton selection group"""
        group = QGroupBox("Automaton Selection")
        layout = QVBoxLayout()
        
        # Plugin selector
        layout.addWidget(QLabel("Automaton Type:"))
        self.plugin_combo = QComboBox()
        
        plugins = list_plugins()
        for plugin_name in plugins:
            plugin = PLUGIN_REGISTRY[plugin_name]
            metadata = plugin.get_metadata()
            self.plugin_combo.addItem(metadata.name, plugin_name)
        
        self.plugin_combo.currentIndexChanged.connect(self._on_plugin_changed)
        layout.addWidget(self.plugin_combo)
        
        # Pattern selector
        layout.addWidget(QLabel("Pattern:"))
        self.pattern_combo = QComboBox()
        self.pattern_combo.currentIndexChanged.connect(self._on_pattern_changed)
        layout.addWidget(self.pattern_combo)
        
        # New button
        self.new_button = QPushButton("🆕 Create New")
        self.new_button.clicked.connect(self.new_simulation)
        layout.addWidget(self.new_button)
        
        group.setLayout(layout)
        return group
    
    def _create_playback_group(self):
        """Create playback controls group"""
        group = QGroupBox("Playback Controls")
        layout = QVBoxLayout()
        
        # Buttons row
        button_layout = QHBoxLayout()
        
        self.play_button = QPushButton("▶ Play")
        self.play_button.clicked.connect(self._toggle_play)
        button_layout.addWidget(self.play_button)
        
        self.step_button = QPushButton("⏭ Step")
        self.step_button.clicked.connect(self._step_once)
        button_layout.addWidget(self.step_button)
        
        self.reset_button = QPushButton("🔄 Reset")
        self.reset_button.clicked.connect(self.new_simulation)
        button_layout.addWidget(self.reset_button)
        
        layout.addLayout(button_layout)
        
        group.setLayout(layout)
        return group
    
    def _create_parameters_group(self):
        """Create parameters group"""
        group = QGroupBox("Parameters")
        layout = QGridLayout()
        
        # Speed control
        layout.addWidget(QLabel("Speed (ms):"), 0, 0)
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(10)
        self.speed_slider.setMaximum(500)
        self.speed_slider.setValue(100)
        self.speed_slider.valueChanged.connect(self._on_speed_changed)
        layout.addWidget(self.speed_slider, 0, 1)
        
        self.speed_label = QLabel("100 ms")
        layout.addWidget(self.speed_label, 0, 2)
        
        # Grid size
        layout.addWidget(QLabel("Grid Size:"), 1, 0)
        self.grid_size_spin = QSpinBox()
        self.grid_size_spin.setMinimum(50)
        self.grid_size_spin.setMaximum(300)
        self.grid_size_spin.setValue(150)
        self.grid_size_spin.setSingleStep(10)
        layout.addWidget(self.grid_size_spin, 1, 1, 1, 2)
        
        group.setLayout(layout)
        return group
    
    def _create_statistics_group(self):
        """Create statistics display group"""
        group = QGroupBox("Statistics")
        layout = QVBoxLayout()
        
        # Stats display
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setMaximumHeight(150)
        self.stats_text.setFont(QFont("Courier", 10))
        layout.addWidget(self.stats_text)
        
        group.setLayout(layout)
        return group
    
    def _on_plugin_changed(self, index):
        """Handle plugin selection change"""
        if index < 0:
            return
        
        plugin_name = self.plugin_combo.itemData(index)
        self.current_plugin = PLUGIN_REGISTRY[plugin_name]
        
        # Update pattern combo
        self.pattern_combo.clear()
        patterns = self.current_plugin.get_default_patterns()
        
        for pattern_name, pattern_info in patterns.items():
            desc = pattern_info.get('description', pattern_name)
            self.pattern_combo.addItem(f"{pattern_name}: {desc}", pattern_name)
    
    def _on_pattern_changed(self, index):
        """Handle pattern selection change"""
        # Pattern will be used when creating new automaton
        pass
    
    def _on_speed_changed(self, value):
        """Handle speed slider change"""
        self.speed_label.setText(f"{value} ms")
        self.simulator.set_speed(value)
    
    def _toggle_play(self):
        """Toggle play/pause"""
        if self.simulator.running:
            self.simulator.pause()
            self.play_button.setText("▶ Play")
            self.status_update.emit("Paused")
        else:
            if self.current_automaton is None:
                self.new_simulation()
            
            if not self.simulator.running:
                self.simulator.start()
            else:
                self.simulator.resume()
            
            self.play_button.setText("⏸ Pause")
            self.status_update.emit("Running")
    
    def _step_once(self):
        """Execute single step"""
        if self.current_automaton is None:
            self.new_simulation()
        
        if self.simulator.running:
            self.simulator.pause()
            self.play_button.setText("▶ Play")
        
        self.simulator.step_once()
        self._update_display()
        self.status_update.emit(f"Stepped to generation {self.current_automaton.generation}")
    
    def new_simulation(self):
        """Create new simulation"""
        try:
            # Stop current simulation
            if self.simulator.running:
                self.simulator.stop()
                self.play_button.setText("▶ Play")
            
            # Get current selections
            plugin_name = self.plugin_combo.currentData()
            pattern_name = self.pattern_combo.currentData()
            grid_size = self.grid_size_spin.value()
            
            if not plugin_name or not pattern_name:
                self.error_occurred.emit("Warning", "Please select automaton and pattern")
                return
            
            # Create automaton
            plugin = PLUGIN_REGISTRY[plugin_name]
            self.current_plugin = plugin
            
            self.current_automaton = plugin.create_automaton(
                grid_size, grid_size, pattern=pattern_name
            )
            
            self.simulator.set_automaton(self.current_automaton)
            
            # Update display
            self._update_display()
            
            metadata = plugin.get_metadata()
            self.status_update.emit(f"Created {metadata.name} with {pattern_name} pattern")
            
            # Log to diagnostics
            self.diagnostics.log_event(
                "simulation_created",
                f"Created {metadata.name}",
                pattern=pattern_name,
                size=grid_size
            )
            
        except Exception as e:
            self.error_occurred.emit("Error", f"Failed to create simulation: {e}")
            import traceback
            traceback.print_exc()
    
    def _on_simulation_step(self, automaton):
        """Callback when simulation steps"""
        # Update will happen in timer
        pass
    
    def _on_simulation_error(self, error):
        """Callback when simulation error occurs"""
        self.error_occurred.emit("Simulation Error", str(error))
        self.diagnostics.log_error(error, "simulation")
    
    def _update_display(self):
        """Update the visualization"""
        if self.current_automaton is None:
            return
        
        try:
            # Update grid visualization
            if self.im is None:
                # First time - create image
                colormap = self.current_plugin.get_colormap()
                cmap = ListedColormap(colormap)
                
                self.im = self.ax.imshow(
                    self.current_automaton.grid,
                    cmap=cmap,
                    interpolation='nearest',
                    vmin=0,
                    vmax=self.current_automaton.metadata.num_states - 1
                )
                self.ax.set_title(self.current_automaton.metadata.name, fontsize=14, fontweight='bold')
            else:
                # Update existing image
                self.im.set_array(self.current_automaton.grid)
            
            self.canvas.draw_idle()
            
            # Update statistics
            stats = self.current_automaton.compute_statistics()
            
            stats_text = f"""
Generation: {stats['generation']}
Total Cells: {stats['total_cells']:,}
Active Cells: {stats['active_cells']:,}
Density: {stats['density']:.2f}%
Entropy: {stats['entropy']:.3f}
Unique States: {stats['unique_states']}

State Distribution:
"""
            
            for state, count in sorted(stats['state_counts'].items()):
                pct = (count / stats['total_cells']) * 100
                stats_text += f"  State {state}: {count:,} ({pct:.2f}%)\n"
            
            if self.simulator.running:
                status = self.simulator.get_status()
                stats_text += f"\nFPS: {status['fps']:.1f}"
            
            self.stats_text.setText(stats_text.strip())
            
        except Exception as e:
            print(f"Display update error: {e}")
    
    def save_file(self, filename):
        """Save current state"""
        # TODO: Implement save
        self.status_update.emit(f"Save to {filename} not yet implemented")
    
    def load_file(self, filename):
        """Load saved state"""
        # TODO: Implement load
        self.status_update.emit(f"Load from {filename} not yet implemented")
