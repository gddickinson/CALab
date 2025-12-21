"""CALab GUI Modules"""
from .main_window import CALabMainWindow
from .simulation_tab import SimulationTab
from .rule_editor_tab import RuleEditorTab
from .pattern_editor_tab import PatternEditorTab
from .diagnostics_tab import DiagnosticsTab
from .error_console import ErrorConsole

__all__ = [
    'CALabMainWindow',
    'SimulationTab',
    'RuleEditorTab',
    'PatternEditorTab',
    'DiagnosticsTab',
    'ErrorConsole'
]
