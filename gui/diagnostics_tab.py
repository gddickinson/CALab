"""
CALab - Diagnostics Tab
View and analyze simulation diagnostics
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTextEdit, QGroupBox, QTableWidget,
                             QTableWidgetItem, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.diagnostics import AutomatonAnalyzer


class DiagnosticsTab(QWidget):
    """
    Diagnostics viewer for analyzing automaton behavior
    """
    
    def __init__(self, diagnostics):
        super().__init__()
        self.diagnostics = diagnostics
        self.current_automaton = None
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel("Diagnostics & Analysis")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Summary
        summary_group = self._create_summary_group()
        layout.addWidget(summary_group)
        
        # Event log
        log_group = self._create_log_group()
        layout.addWidget(log_group)
        
        # Analysis
        analysis_group = self._create_analysis_group()
        layout.addWidget(analysis_group)
        
        # Actions
        actions = self._create_actions()
        layout.addLayout(actions)
        
    def _create_summary_group(self):
        """Create summary display"""
        group = QGroupBox("Summary")
        layout = QVBoxLayout()
        
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMaximumHeight(120)
        self.summary_text.setFont(QFont("Courier", 10))
        layout.addWidget(self.summary_text)
        
        refresh_btn = QPushButton("🔄 Refresh Summary")
        refresh_btn.clicked.connect(self._refresh_summary)
        layout.addWidget(refresh_btn)
        
        group.setLayout(layout)
        return group
    
    def _create_log_group(self):
        """Create event log display"""
        group = QGroupBox("Event Log")
        layout = QVBoxLayout()
        
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(3)
        self.log_table.setHorizontalHeaderLabels(["Time", "Type", "Message"])
        self.log_table.setColumnWidth(0, 150)
        self.log_table.setColumnWidth(1, 120)
        layout.addWidget(self.log_table)
        
        button_layout = QHBoxLayout()
        
        refresh_log_btn = QPushButton("🔄 Refresh Log")
        refresh_log_btn.clicked.connect(self._refresh_log)
        button_layout.addWidget(refresh_log_btn)
        
        clear_log_btn = QPushButton("🗑️ Clear Log")
        clear_log_btn.clicked.connect(self._clear_log)
        button_layout.addWidget(clear_log_btn)
        
        layout.addLayout(button_layout)
        
        group.setLayout(layout)
        return group
    
    def _create_analysis_group(self):
        """Create analysis display"""
        group = QGroupBox("Behavior Analysis")
        layout = QVBoxLayout()
        
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setFont(QFont("Courier", 10))
        self.analysis_text.setPlaceholderText(
            "Load an automaton to perform behavior analysis..."
        )
        layout.addWidget(self.analysis_text)
        
        analyze_btn = QPushButton("🔬 Analyze Current Automaton")
        analyze_btn.clicked.connect(self._analyze_current)
        layout.addWidget(analyze_btn)
        
        group.setLayout(layout)
        return group
    
    def _create_actions(self):
        """Create action buttons"""
        layout = QHBoxLayout()
        
        export_btn = QPushButton("📤 Export Diagnostics")
        export_btn.clicked.connect(self._export_diagnostics)
        layout.addWidget(export_btn)
        
        system_info_btn = QPushButton("ℹ️ System Info")
        system_info_btn.clicked.connect(self._show_system_info)
        layout.addWidget(system_info_btn)
        
        layout.addStretch()
        
        return layout
    
    def _refresh_summary(self):
        """Refresh summary display"""
        try:
            summary = self.diagnostics.get_summary()
            self.summary_text.setText(summary)
        except Exception as e:
            self.summary_text.setText(f"Error getting summary: {e}")
    
    def _refresh_log(self):
        """Refresh event log"""
        self.log_table.setRowCount(0)
        
        for log_entry in self.diagnostics.logs:
            row = self.log_table.rowCount()
            self.log_table.insertRow(row)
            
            self.log_table.setItem(row, 0, QTableWidgetItem(log_entry['timestamp']))
            self.log_table.setItem(row, 1, QTableWidgetItem(log_entry['type']))
            self.log_table.setItem(row, 2, QTableWidgetItem(log_entry['message']))
        
        # Scroll to bottom
        self.log_table.scrollToBottom()
    
    def _clear_log(self):
        """Clear event log"""
        reply = QMessageBox.question(
            self, "Confirm", "Clear all diagnostic logs?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.diagnostics.logs.clear()
            self.diagnostics.errors.clear()
            self.log_table.setRowCount(0)
            self._refresh_summary()
    
    def analyze_automaton(self, automaton):
        """Analyze an automaton"""
        self.current_automaton = automaton
        self._analyze_current()
    
    def _analyze_current(self):
        """Analyze current automaton"""
        if self.current_automaton is None:
            QMessageBox.warning(
                self, "Warning",
                "No automaton loaded. Please create a simulation first."
            )
            return
        
        try:
            self.analysis_text.setText("Analyzing... please wait...")
            
            # Perform analysis
            analysis = AutomatonAnalyzer.analyze_evolution(
                self.current_automaton,
                num_steps=100
            )
            
            # Format results
            result_text = f"""
Behavior Analysis
================

Classification: {analysis['classification'].upper()}

Density Metrics:
  Initial: {analysis['initial_density']:.2f}%
  Final: {analysis['final_density']:.2f}%
  Change: {analysis['density_change']:+.2f}%
  Maximum: {analysis['max_density']:.2f}%
  Minimum: {analysis['min_density']:.2f}%
  Average: {analysis['avg_density']:.2f}%
  Std Dev: {analysis['density_std']:.2f}

Entropy Metrics:
  Initial: {analysis['initial_entropy']:.3f}
  Final: {analysis['final_entropy']:.3f}
  Change: {analysis['entropy_change']:+.3f}

Interpretation:
"""
            
            # Add interpretation
            classification = analysis['classification']
            if classification == 'static':
                result_text += "  The automaton reaches a stable state with no further changes."
            elif classification == 'growing':
                result_text += "  The automaton shows expansion with increasing active cells."
            elif classification == 'dying':
                result_text += "  The automaton shows decline with decreasing active cells."
            elif classification == 'chaotic':
                result_text += "  The automaton shows chaotic behavior with high variability."
            elif classification == 'oscillating':
                result_text += "  The automaton shows periodic or oscillating patterns."
            else:
                result_text += "  The automaton shows stable behavior with consistent dynamics."
            
            self.analysis_text.setText(result_text.strip())
            
            # Log analysis
            self.diagnostics.log_event(
                "analysis_complete",
                f"Analyzed automaton: {classification}",
                **analysis
            )
            
        except Exception as e:
            error_msg = f"Analysis failed: {e}"
            self.analysis_text.setText(error_msg)
            self.diagnostics.log_error(e, "analysis")
            QMessageBox.critical(self, "Error", error_msg)
    
    def _export_diagnostics(self):
        """Export diagnostics to file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Diagnostics", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if filename:
            try:
                self.diagnostics.export_report(filename)
                QMessageBox.information(
                    self, "Success",
                    f"Diagnostics exported to:\n{filename}"
                )
                
                self.diagnostics.log_event(
                    "export_complete",
                    f"Diagnostics exported to {filename}"
                )
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {e}")
    
    def _show_system_info(self):
        """Show system information"""
        info = self.diagnostics.get_system_info()
        
        info_text = f"""
System Information
==================

Platform: {info['platform']}
Python Version: {info['python_version']}
NumPy Version: {info['numpy_version']}
Timestamp: {info['timestamp']}
        """.strip()
        
        QMessageBox.information(self, "System Information", info_text)
