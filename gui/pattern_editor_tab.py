"""
CALab - Pattern Editor Tab
Create and edit initial patterns for cellular automata
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QGroupBox, QSpinBox, QListWidget,
                             QFileDialog, QMessageBox, QGridLayout, QComboBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QColor, QPen
import numpy as np


class PatternCanvas(QWidget):
    """
    Canvas for drawing patterns
    """
    
    def __init__(self, size=30):
        super().__init__()
        self.grid_size = size
        self.cell_size = 15
        self.grid = np.zeros((size, size), dtype=np.int32)
        self.current_state = 1
        self.num_states = 2
        
        self.setMinimumSize(size * self.cell_size, size * self.cell_size)
        
    def paintEvent(self, event):
        """Paint the grid"""
        painter = QPainter(self)
        
        # Colors for different states
        colors = [
            QColor(0, 0, 0),      # State 0: Black
            QColor(0, 255, 0),    # State 1: Green
            QColor(255, 0, 0),    # State 2: Red
            QColor(0, 0, 255),    # State 3: Blue
            QColor(255, 255, 0),  # State 4: Yellow
        ]
        
        # Draw cells
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                state = self.grid[y, x]
                
                if state < len(colors):
                    painter.fillRect(
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                        colors[state]
                    )
        
        # Draw grid lines
        painter.setPen(QPen(QColor(128, 128, 128), 1))
        for i in range(self.grid_size + 1):
            # Vertical lines
            painter.drawLine(
                i * self.cell_size, 0,
                i * self.cell_size, self.grid_size * self.cell_size
            )
            # Horizontal lines
            painter.drawLine(
                0, i * self.cell_size,
                self.grid_size * self.cell_size, i * self.cell_size
            )
    
    def mousePressEvent(self, event):
        """Handle mouse clicks"""
        x = event.x() // self.cell_size
        y = event.y() // self.cell_size
        
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            self.grid[y, x] = self.current_state
            self.update()
    
    def mouseMoveEvent(self, event):
        """Handle mouse dragging"""
        if event.buttons() & Qt.LeftButton:
            self.mousePressEvent(event)
    
    def clear(self):
        """Clear the grid"""
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        self.update()
    
    def set_state(self, state):
        """Set the current drawing state"""
        self.current_state = state
    
    def set_num_states(self, num_states):
        """Set number of states"""
        self.num_states = num_states


class PatternEditorTab(QWidget):
    """
    Pattern editor for creating initial configurations
    """
    
    def __init__(self):
        super().__init__()
        self.patterns = {}
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the user interface"""
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        # Left: Canvas
        left_layout = QVBoxLayout()
        
        title = QLabel("Pattern Editor")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        left_layout.addWidget(title)
        
        # Canvas
        self.canvas = PatternCanvas(30)
        left_layout.addWidget(self.canvas, alignment=Qt.AlignCenter)
        
        # Drawing controls
        draw_controls = self._create_drawing_controls()
        left_layout.addWidget(draw_controls)
        
        layout.addLayout(left_layout)
        
        # Right: Tools and library
        right_layout = QVBoxLayout()
        
        # Tools
        tools_group = self._create_tools_group()
        right_layout.addWidget(tools_group)
        
        # Pattern library
        library_group = self._create_library_group()
        right_layout.addWidget(library_group)
        
        right_layout.addStretch()
        
        layout.addLayout(right_layout)
        
    def _create_drawing_controls(self):
        """Create drawing controls"""
        group = QGroupBox("Drawing Controls")
        layout = QGridLayout()
        
        # State selector
        layout.addWidget(QLabel("Draw State:"), 0, 0)
        self.state_combo = QComboBox()
        self.state_combo.addItem("State 0 (Dead)", 0)
        self.state_combo.addItem("State 1 (Alive)", 1)
        self.state_combo.currentIndexChanged.connect(self._on_state_changed)
        layout.addWidget(self.state_combo, 0, 1)
        
        # Number of states
        layout.addWidget(QLabel("Total States:"), 1, 0)
        self.num_states_spin = QSpinBox()
        self.num_states_spin.setMinimum(2)
        self.num_states_spin.setMaximum(8)
        self.num_states_spin.setValue(2)
        self.num_states_spin.valueChanged.connect(self._on_num_states_changed)
        layout.addWidget(self.num_states_spin, 1, 1)
        
        # Grid size
        layout.addWidget(QLabel("Grid Size:"), 2, 0)
        self.grid_size_spin = QSpinBox()
        self.grid_size_spin.setMinimum(10)
        self.grid_size_spin.setMaximum(50)
        self.grid_size_spin.setValue(30)
        layout.addWidget(self.grid_size_spin, 2, 1)
        
        group.setLayout(layout)
        return group
    
    def _create_tools_group(self):
        """Create tools group"""
        group = QGroupBox("Tools")
        layout = QVBoxLayout()
        
        clear_btn = QPushButton("🗑️ Clear Canvas")
        clear_btn.clicked.connect(self.canvas.clear)
        layout.addWidget(clear_btn)
        
        mirror_h_btn = QPushButton("⬌ Mirror Horizontal")
        mirror_h_btn.clicked.connect(self._mirror_horizontal)
        layout.addWidget(mirror_h_btn)
        
        mirror_v_btn = QPushButton("⬍ Mirror Vertical")
        mirror_v_btn.clicked.connect(self._mirror_vertical)
        layout.addWidget(mirror_v_btn)
        
        rotate_btn = QPushButton("↻ Rotate 90°")
        rotate_btn.clicked.connect(self._rotate_90)
        layout.addWidget(rotate_btn)
        
        invert_btn = QPushButton("◐ Invert")
        invert_btn.clicked.connect(self._invert)
        layout.addWidget(invert_btn)
        
        group.setLayout(layout)
        return group
    
    def _create_library_group(self):
        """Create pattern library group"""
        group = QGroupBox("Pattern Library")
        layout = QVBoxLayout()
        
        # Pattern list
        self.pattern_list = QListWidget()
        layout.addWidget(self.pattern_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save")
        save_btn.clicked.connect(self._save_pattern)
        button_layout.addWidget(save_btn)
        
        load_btn = QPushButton("📂 Load")
        load_btn.clicked.connect(self._load_pattern)
        button_layout.addWidget(load_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.clicked.connect(self._delete_pattern)
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
        
        # Export
        export_layout = QHBoxLayout()
        
        export_btn = QPushButton("📤 Export")
        export_btn.clicked.connect(self._export_pattern)
        export_layout.addWidget(export_btn)
        
        import_btn = QPushButton("📥 Import")
        import_btn.clicked.connect(self._import_pattern)
        export_layout.addWidget(import_btn)
        
        layout.addLayout(export_layout)
        
        group.setLayout(layout)
        return group
    
    def _on_state_changed(self, index):
        """Handle state selection change"""
        state = self.state_combo.currentData()
        self.canvas.set_state(state)
    
    def _on_num_states_changed(self, value):
        """Handle number of states change"""
        self.canvas.set_num_states(value)
        
        # Update state combo
        self.state_combo.clear()
        for i in range(value):
            self.state_combo.addItem(f"State {i}", i)
    
    def _mirror_horizontal(self):
        """Mirror pattern horizontally"""
        self.canvas.grid = np.fliplr(self.canvas.grid)
        self.canvas.update()
    
    def _mirror_vertical(self):
        """Mirror pattern vertically"""
        self.canvas.grid = np.flipud(self.canvas.grid)
        self.canvas.update()
    
    def _rotate_90(self):
        """Rotate pattern 90 degrees"""
        self.canvas.grid = np.rot90(self.canvas.grid)
        self.canvas.update()
    
    def _invert(self):
        """Invert pattern"""
        max_state = self.num_states_spin.value() - 1
        self.canvas.grid = max_state - self.canvas.grid
        self.canvas.update()
    
    def _save_pattern(self):
        """Save current pattern to library"""
        from PyQt5.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, "Save Pattern", "Pattern name:")
        
        if ok and name:
            self.patterns[name] = self.canvas.grid.copy()
            self.pattern_list.addItem(name)
            QMessageBox.information(self, "Success", f"Pattern '{name}' saved")
    
    def _load_pattern(self):
        """Load pattern from library"""
        current_item = self.pattern_list.currentItem()
        
        if current_item:
            name = current_item.text()
            if name in self.patterns:
                self.canvas.grid = self.patterns[name].copy()
                self.canvas.update()
        else:
            QMessageBox.warning(self, "Warning", "Please select a pattern")
    
    def _delete_pattern(self):
        """Delete pattern from library"""
        current_item = self.pattern_list.currentItem()
        
        if current_item:
            name = current_item.text()
            
            reply = QMessageBox.question(
                self, "Confirm", f"Delete pattern '{name}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                del self.patterns[name]
                self.pattern_list.takeItem(self.pattern_list.currentRow())
        else:
            QMessageBox.warning(self, "Warning", "Please select a pattern")
    
    def _export_pattern(self):
        """Export pattern to file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Pattern", "", "NumPy Files (*.npy);;All Files (*)"
        )
        
        if filename:
            try:
                np.save(filename, self.canvas.grid)
                QMessageBox.information(self, "Success", f"Exported to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {e}")
    
    def _import_pattern(self):
        """Import pattern from file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Import Pattern", "", "NumPy Files (*.npy);;All Files (*)"
        )
        
        if filename:
            try:
                grid = np.load(filename)
                self.canvas.grid = grid
                self.canvas.update()
                QMessageBox.information(self, "Success", "Pattern imported")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import: {e}")
