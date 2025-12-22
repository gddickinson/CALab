"""
CALab - Main GUI Window
Comprehensive PyQt-based interface for cellular automata simulation
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QMenuBar, QMenu, QAction, QStatusBar,
                             QMessageBox, QFileDialog, QDockWidget)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon
import sys
import os

# Import tabs
from gui.simulation_tab import SimulationTab
from gui.rule_editor_tab import RuleEditorTab
from gui.pattern_editor_tab import PatternEditorTab
from gui.diagnostics_tab import DiagnosticsTab
from gui.documentation_tab import DocumentationTab
from gui.error_console import ErrorConsole

from core.simulator import SimulationEngine
from utils.diagnostics import DiagnosticCollector


class CALabMainWindow(QMainWindow):
    """
    Main application window for CALab

    Features:
    - Tabbed interface for different tools
    - Menubar with file/edit/view/help menus
    - Status bar with statistics
    - Error console (dock widget)
    - Plugin system integration
    """

    # Signals
    error_occurred = pyqtSignal(str, str)  # (error_type, message)
    status_update = pyqtSignal(str)  # status message

    def __init__(self):
        super().__init__()

        # Core components
        self.simulator = SimulationEngine()
        self.diagnostics = DiagnosticCollector()
        self.current_automaton = None

        # Setup UI
        self.setWindowTitle("CALab - Cellular Automata Laboratory")
        self.setGeometry(100, 100, 1400, 900)

        self._setup_ui()
        self._create_menus()
        self._create_status_bar()
        self._connect_signals()

        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_status_bar)
        self.update_timer.start(100)  # Update every 100ms

    def _setup_ui(self):
        """Setup main user interface"""
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Create tabs
        self.simulation_tab = SimulationTab(self.simulator, self.diagnostics)
        self.rule_editor_tab = RuleEditorTab()
        self.pattern_editor_tab = PatternEditorTab()
        self.diagnostics_tab = DiagnosticsTab(self.diagnostics)
        self.documentation_tab = DocumentationTab()

        self.tab_widget.addTab(self.simulation_tab, "Simulation")
        self.tab_widget.addTab(self.rule_editor_tab, "Rule Editor")
        self.tab_widget.addTab(self.pattern_editor_tab, "Pattern Editor")
        self.tab_widget.addTab(self.diagnostics_tab, "Diagnostics")
        self.tab_widget.addTab(self.documentation_tab, "📚 Documentation")

        # Error console (dockable)
        self.error_console = ErrorConsole()
        error_dock = QDockWidget("Error Console", self)
        error_dock.setWidget(self.error_console)
        error_dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, error_dock)
        error_dock.hide()  # Hidden by default

        self.error_dock = error_dock

    def _create_menus(self):
        """Create menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        new_action = QAction("&New Simulation", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._new_simulation)
        file_menu.addAction(new_action)

        open_action = QAction("&Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        export_action = QAction("&Export Diagnostics...", self)
        export_action.triggered.connect(self._export_diagnostics)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")

        preferences_action = QAction("&Preferences...", self)
        preferences_action.triggered.connect(self._show_preferences)
        edit_menu.addAction(preferences_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        toggle_console_action = QAction("&Error Console", self)
        toggle_console_action.setCheckable(True)
        toggle_console_action.triggered.connect(self._toggle_error_console)
        view_menu.addAction(toggle_console_action)

        # Tools menu
        tools_menu = menubar.addMenu("&Tools")

        analyze_action = QAction("&Analyze Current Simulation", self)
        analyze_action.triggered.connect(self._analyze_simulation)
        tools_menu.addAction(analyze_action)

        batch_action = QAction("&Run Batch Simulations...", self)
        batch_action.triggered.connect(self._run_batch)
        tools_menu.addAction(batch_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        docs_action = QAction("&Documentation", self)
        docs_action.setShortcut("F1")
        docs_action.triggered.connect(self._show_documentation)
        help_menu.addAction(docs_action)

        about_action = QAction("&About CALab", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def _connect_signals(self):
        """Connect internal signals"""
        self.error_occurred.connect(self._handle_error)
        self.status_update.connect(self._update_status_message)

        # Connect tab signals
        self.simulation_tab.error_occurred.connect(self._handle_error)
        self.simulation_tab.status_update.connect(self._update_status_message)

        # Track current automaton
        self.simulator.on_step_callback = self._update_current_automaton

    def _update_current_automaton(self, automaton):
        """Update current automaton reference"""
        self.current_automaton = automaton
        self.diagnostics_tab.current_automaton = automaton

    def _update_status_bar(self):
        """Update status bar with current simulation info"""
        if self.simulator.running:
            status = self.simulator.get_status()
            message = (f"Running | Gen: {status['generation']} | "
                      f"FPS: {status['fps']:.1f} | "
                      f"Time: {status['elapsed_seconds']:.1f}s")
            self.status_bar.showMessage(message)
        elif self.simulator.paused:
            self.status_bar.showMessage("Paused")

    def _update_status_message(self, message: str):
        """Update status bar message"""
        self.status_bar.showMessage(message, 3000)  # Show for 3 seconds

    def _handle_error(self, error_type: str, message: str):
        """Handle error"""
        self.error_console.add_error(error_type, message)
        self.error_dock.show()
        self.diagnostics.log_event("error", message, error_type=error_type)

    # Menu actions
    def _new_simulation(self):
        """Create new simulation"""
        self.simulation_tab.new_simulation()

    def _open_file(self):
        """Open file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "CALab Files (*.calab);;All Files (*)"
        )
        if filename:
            self.simulation_tab.load_file(filename)

    def _save_file(self):
        """Save file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "CALab Files (*.calab);;All Files (*)"
        )
        if filename:
            self.simulation_tab.save_file(filename)

    def _export_diagnostics(self):
        """Export diagnostics"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Diagnostics", "", "JSON Files (*.json);;All Files (*)"
        )
        if filename:
            self.diagnostics.export_report(filename)
            self.status_update.emit(f"Diagnostics exported to {filename}")

    def _show_preferences(self):
        """Show preferences dialog"""
        QMessageBox.information(self, "Preferences", "Preferences dialog not yet implemented")

    def _toggle_error_console(self, checked: bool):
        """Toggle error console visibility"""
        if checked:
            self.error_dock.show()
        else:
            self.error_dock.hide()

    def _analyze_simulation(self):
        """Analyze current simulation"""
        if self.current_automaton:
            self.diagnostics_tab.analyze_automaton(self.current_automaton)
            self.tab_widget.setCurrentWidget(self.diagnostics_tab)
        else:
            QMessageBox.warning(self, "No Simulation", "No simulation loaded")

    def _run_batch(self):
        """Run batch simulations"""
        QMessageBox.information(self, "Batch Mode", "Batch simulation dialog not yet implemented")

    def _show_documentation(self):
        """Show documentation"""
        docs = """
        CALab - Cellular Automata Laboratory

        Quick Start:
        1. Go to Simulation tab
        2. Select an automaton type
        3. Click Play to start

        Tabs:
        - Simulation: Run and visualize automata
        - Rule Editor: Create custom transition rules
        - Pattern Editor: Design initial patterns
        - Diagnostics: View detailed analysis

        Keyboard Shortcuts:
        Ctrl+N: New simulation
        Ctrl+O: Open file
        Ctrl+S: Save file
        Ctrl+Q: Quit
        Space: Play/Pause (in simulation tab)
        """
        QMessageBox.information(self, "Documentation", docs)

    def _show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>CALab - Cellular Automata Laboratory</h2>
        <p><b>Version:</b> 1.0.0</p>
        <p><b>Author:</b> George Dickinson's Lab</p>
        <p>A comprehensive framework for exploring cellular automata.</p>
        <p>Built with Python, PyQt5, NumPy, and Matplotlib.</p>
        """
        QMessageBox.about(self, "About CALab", about_text)

    def closeEvent(self, event):
        """Handle window close"""
        # Stop simulation
        if self.simulator.running:
            self.simulator.stop()

        # Ask for confirmation
        reply = QMessageBox.question(
            self, 'Quit CALab',
            'Are you sure you want to quit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    """Main entry point"""
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setApplicationName("CALab")

    window = CALabMainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
