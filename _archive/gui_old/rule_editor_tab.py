"""
CALab - Rule Editor Tab
Create and modify cellular automaton rules
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTableWidget, QTableWidgetItem, QGroupBox,
                             QComboBox, QSpinBox, QLineEdit, QTextEdit,
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt


class RuleEditorTab(QWidget):
    """
    Rule editor for creating custom transition rules
    """
    
    def __init__(self):
        super().__init__()
        self.rules = {}
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel("Rule Editor")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Rule type selection
        type_group = self._create_type_group()
        layout.addWidget(type_group)
        
        # Rule input
        input_group = self._create_input_group()
        layout.addWidget(input_group)
        
        # Rule table
        table_group = self._create_table_group()
        layout.addWidget(table_group)
        
        # Actions
        actions = self._create_actions()
        layout.addLayout(actions)
        
    def _create_type_group(self):
        """Create rule type selection"""
        group = QGroupBox("Rule Type")
        layout = QHBoxLayout()
        
        layout.addWidget(QLabel("Type:"))
        
        self.type_combo = QComboBox()
        self.type_combo.addItem("Table-Based (e.g., Langton Loop)", "table")
        self.type_combo.addItem("Totalistic (e.g., Game of Life)", "totalistic")
        self.type_combo.currentIndexChanged.connect(self._on_type_changed)
        layout.addWidget(self.type_combo)
        
        layout.addWidget(QLabel("States:"))
        self.states_spin = QSpinBox()
        self.states_spin.setMinimum(2)
        self.states_spin.setMaximum(10)
        self.states_spin.setValue(2)
        layout.addWidget(self.states_spin)
        
        layout.addStretch()
        
        group.setLayout(layout)
        return group
    
    def _create_input_group(self):
        """Create rule input group"""
        group = QGroupBox("Add Rule")
        layout = QVBoxLayout()
        
        # Table-based input
        self.table_widget = QWidget()
        table_layout = QHBoxLayout(self.table_widget)
        
        table_layout.addWidget(QLabel("Pattern (C,N,E,S,W):"))
        self.pattern_edit = QLineEdit()
        self.pattern_edit.setPlaceholderText("e.g., 0,1,1,1,0")
        table_layout.addWidget(self.pattern_edit)
        
        table_layout.addWidget(QLabel("→ Result:"))
        self.result_spin = QSpinBox()
        self.result_spin.setMinimum(0)
        self.result_spin.setMaximum(9)
        table_layout.addWidget(self.result_spin)
        
        add_table_btn = QPushButton("Add Rule")
        add_table_btn.clicked.connect(self._add_table_rule)
        table_layout.addWidget(add_table_btn)
        
        layout.addWidget(self.table_widget)
        
        # Totalistic input
        self.totalistic_widget = QWidget()
        totalistic_layout = QHBoxLayout(self.totalistic_widget)
        
        totalistic_layout.addWidget(QLabel("Birth:"))
        self.birth_edit = QLineEdit()
        self.birth_edit.setPlaceholderText("e.g., 3")
        totalistic_layout.addWidget(self.birth_edit)
        
        totalistic_layout.addWidget(QLabel("Survive:"))
        self.survive_edit = QLineEdit()
        self.survive_edit.setPlaceholderText("e.g., 23")
        totalistic_layout.addWidget(self.survive_edit)
        
        add_totalistic_btn = QPushButton("Set Rule")
        add_totalistic_btn.clicked.connect(self._add_totalistic_rule)
        totalistic_layout.addWidget(add_totalistic_btn)
        
        layout.addWidget(self.totalistic_widget)
        self.totalistic_widget.hide()
        
        group.setLayout(layout)
        return group
    
    def _create_table_group(self):
        """Create rule table display"""
        group = QGroupBox("Current Rules")
        layout = QVBoxLayout()
        
        self.rule_table = QTableWidget()
        self.rule_table.setColumnCount(3)
        self.rule_table.setHorizontalHeaderLabels(["Pattern", "Result", "Actions"])
        layout.addWidget(self.rule_table)
        
        # Rule description
        self.rule_description = QTextEdit()
        self.rule_description.setMaximumHeight(100)
        self.rule_description.setReadOnly(True)
        self.rule_description.setPlaceholderText("Rule description will appear here...")
        layout.addWidget(self.rule_description)
        
        group.setLayout(layout)
        return group
    
    def _create_actions(self):
        """Create action buttons"""
        layout = QHBoxLayout()
        
        import_btn = QPushButton("📂 Import Rules")
        import_btn.clicked.connect(self._import_rules)
        layout.addWidget(import_btn)
        
        export_btn = QPushButton("💾 Export Rules")
        export_btn.clicked.connect(self._export_rules)
        layout.addWidget(export_btn)
        
        clear_btn = QPushButton("🗑️ Clear All")
        clear_btn.clicked.connect(self._clear_rules)
        layout.addWidget(clear_btn)
        
        layout.addStretch()
        
        test_btn = QPushButton("🧪 Test Rules")
        test_btn.clicked.connect(self._test_rules)
        layout.addWidget(test_btn)
        
        return layout
    
    def _on_type_changed(self, index):
        """Handle rule type change"""
        rule_type = self.type_combo.currentData()
        
        if rule_type == "table":
            self.table_widget.show()
            self.totalistic_widget.hide()
        else:
            self.table_widget.hide()
            self.totalistic_widget.show()
    
    def _add_table_rule(self):
        """Add a table-based rule"""
        pattern_text = self.pattern_edit.text().strip()
        result = self.result_spin.value()
        
        if not pattern_text:
            QMessageBox.warning(self, "Warning", "Please enter a pattern")
            return
        
        try:
            # Parse pattern
            pattern = tuple(map(int, pattern_text.split(',')))
            
            # Add to rules
            self.rules[pattern] = result
            
            # Add to table
            row = self.rule_table.rowCount()
            self.rule_table.insertRow(row)
            
            self.rule_table.setItem(row, 0, QTableWidgetItem(str(pattern)))
            self.rule_table.setItem(row, 1, QTableWidgetItem(str(result)))
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda: self._delete_rule(row))
            self.rule_table.setCellWidget(row, 2, delete_btn)
            
            # Clear input
            self.pattern_edit.clear()
            
            self._update_description()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid pattern: {e}")
    
    def _add_totalistic_rule(self):
        """Add totalistic rule (B/S notation)"""
        birth = self.birth_edit.text().strip()
        survive = self.survive_edit.text().strip()
        
        rule_text = f"B{birth}/S{survive}"
        
        self.rule_description.setText(f"""
Totalistic Rule: {rule_text}

Birth conditions: {birth}
(Dead cell becomes alive if it has exactly this many neighbors)

Survival conditions: {survive}
(Live cell survives if it has this many neighbors)

Examples:
- B3/S23 = Conway's Game of Life
- B2/S = Seeds (no survival)
- B36/S23 = HighLife
        """.strip())
    
    def _delete_rule(self, row):
        """Delete a rule"""
        pattern_item = self.rule_table.item(row, 0)
        if pattern_item:
            pattern_text = pattern_item.text()
            # Remove from rules dict
            # (simplified - would need to parse pattern)
            self.rule_table.removeRow(row)
            self._update_description()
    
    def _update_description(self):
        """Update rule description"""
        count = len(self.rules)
        
        desc = f"Total Rules: {count}\n\n"
        
        if count > 0:
            desc += "Sample rules:\n"
            for i, (pattern, result) in enumerate(list(self.rules.items())[:5]):
                desc += f"  {pattern} → {result}\n"
            
            if count > 5:
                desc += f"  ... and {count - 5} more"
        else:
            desc += "No rules defined yet."
        
        self.rule_description.setText(desc)
    
    def _import_rules(self):
        """Import rules from file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Import Rules", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if filename:
            try:
                import json
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                # Load rules
                if 'rules' in data:
                    for rule in data['rules']:
                        pattern = tuple(rule['pattern'])
                        result = rule['result']
                        self.rules[pattern] = result
                
                self._refresh_table()
                QMessageBox.information(self, "Success", f"Imported {len(self.rules)} rules")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import: {e}")
    
    def _export_rules(self):
        """Export rules to file"""
        if not self.rules:
            QMessageBox.warning(self, "Warning", "No rules to export")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Rules", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if filename:
            try:
                import json
                data = {
                    'metadata': {
                        'num_states': self.states_spin.value(),
                        'rule_type': self.type_combo.currentData()
                    },
                    'rules': [
                        {'pattern': list(pattern), 'result': result}
                        for pattern, result in self.rules.items()
                    ]
                }
                
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                
                QMessageBox.information(self, "Success", f"Exported to {filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {e}")
    
    def _clear_rules(self):
        """Clear all rules"""
        reply = QMessageBox.question(
            self, "Confirm", "Clear all rules?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.rules.clear()
            self.rule_table.setRowCount(0)
            self._update_description()
    
    def _test_rules(self):
        """Test the rules"""
        QMessageBox.information(
            self, "Test Rules",
            "Rule testing will be implemented with simulation integration"
        )
    
    def _refresh_table(self):
        """Refresh the rule table"""
        self.rule_table.setRowCount(0)
        
        for pattern, result in self.rules.items():
            row = self.rule_table.rowCount()
            self.rule_table.insertRow(row)
            
            self.rule_table.setItem(row, 0, QTableWidgetItem(str(pattern)))
            self.rule_table.setItem(row, 1, QTableWidgetItem(str(result)))
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, r=row: self._delete_rule(r))
            self.rule_table.setCellWidget(row, 2, delete_btn)
        
        self._update_description()
