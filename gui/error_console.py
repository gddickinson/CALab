"""
CALab - Error Console
Dockable error logging widget
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QPushButton, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QColor
from datetime import datetime


class ErrorConsole(QWidget):
    """
    Error console for displaying errors and warnings
    """
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self.error_count = 0
        self.warning_count = 0
        
    def _setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header with controls
        header = QHBoxLayout()
        
        self.count_label = QLabel("Errors: 0 | Warnings: 0")
        header.addWidget(self.count_label)
        
        header.addStretch()
        
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear)
        header.addWidget(clear_button)
        
        export_button = QPushButton("Export")
        export_button.clicked.connect(self._export_log)
        header.addWidget(export_button)
        
        layout.addLayout(header)
        
        # Text display
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("Courier", 9))
        layout.addWidget(self.text_edit)
        
    def add_error(self, error_type: str, message: str):
        """Add an error message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format message
        if "error" in error_type.lower():
            prefix = "❌ ERROR"
            self.error_count += 1
            color = "#FF0000"
        elif "warning" in error_type.lower():
            prefix = "⚠️  WARNING"
            self.warning_count += 1
            color = "#FFA500"
        else:
            prefix = "ℹ️  INFO"
            color = "#0000FF"
        
        # Add to display
        html = f"""
        <div style="color: {color}; margin: 5px 0; padding: 5px; border-left: 3px solid {color};">
            <b>[{timestamp}] {prefix}: {error_type}</b><br/>
            <span style="color: #333;">{message}</span>
        </div>
        """
        
        self.text_edit.append(html)
        
        # Scroll to bottom
        self.text_edit.moveCursor(QTextCursor.End)
        
        # Update count
        self.count_label.setText(f"Errors: {self.error_count} | Warnings: {self.warning_count}")
    
    def clear(self):
        """Clear all messages"""
        self.text_edit.clear()
        self.error_count = 0
        self.warning_count = 0
        self.count_label.setText("Errors: 0 | Warnings: 0")
    
    def _export_log(self):
        """Export log to file"""
        from PyQt5.QtWidgets import QFileDialog
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Error Log", "", "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.text_edit.toPlainText())
                self.add_error("Info", f"Log exported to {filename}")
            except Exception as e:
                self.add_error("Error", f"Failed to export: {e}")
