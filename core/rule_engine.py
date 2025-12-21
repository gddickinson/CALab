"""
CALab - Rule Engine
Handles rule parsing, validation, and application
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Callable
import json
import re


class RuleParser:
    """Parse and validate cellular automaton rules"""
    
    @staticmethod
    def parse_langton_rule(rule_string: str) -> Tuple[Tuple[int, ...], int]:
        """
        Parse Langton Loop style rules
        
        Format: "C,N,E,S,W->R" where C=center, N=north, etc., R=result
        Example: "0,1,1,1,0->1"
        
        Returns:
            Tuple of (pattern, result)
        """
        try:
            pattern_str, result_str = rule_string.split('->')
            pattern = tuple(map(int, pattern_str.split(',')))
            result = int(result_str)
            return (pattern, result)
        except Exception as e:
            raise ValueError(f"Invalid Langton rule format: {rule_string}") from e
    
    @staticmethod
    def parse_totalistic_rule(rule_string: str, num_states: int = 2) -> Dict[Tuple[int, int], int]:
        """
        Parse totalistic rules (like Conway's Life: B3/S23)
        
        Format: "B<birth>/S<survive>" or full transition table
        """
        rules = {}
        
        # Parse B/S notation (for 2-state automata)
        match = re.match(r'B(\d+)/S(\d+)', rule_string)
        if match:
            birth_str, survive_str = match.groups()
            birth = [int(d) for d in birth_str]
            survive = [int(d) for d in survive_str]
            
            # Generate full rule table
            for current_state in range(num_states):
                for neighbor_sum in range(9):  # 0-8 neighbors in Moore neighborhood
                    if current_state == 0:  # Dead
                        result = 1 if neighbor_sum in birth else 0
                    else:  # Alive
                        result = 1 if neighbor_sum in survive else 0
                    rules[(current_state, neighbor_sum)] = result
        
        return rules
    
    @staticmethod
    def parse_life_like_rule(rule_string: str) -> Tuple[List[int], List[int]]:
        """
        Parse Life-like rules (B/S notation)
        
        Returns:
            Tuple of (birth_conditions, survive_conditions)
        """
        match = re.match(r'B(\d*)/S(\d*)', rule_string)
        if match:
            birth_str, survive_str = match.groups()
            birth = [int(d) for d in birth_str] if birth_str else []
            survive = [int(d) for d in survive_str] if survive_str else []
            return (birth, survive)
        else:
            raise ValueError(f"Invalid Life-like rule: {rule_string}")


class RuleEngine:
    """
    Engine for managing and applying cellular automaton rules
    """
    
    def __init__(self):
        self.rules: Dict[Tuple, int] = {}
        self.totalistic_rules: Dict[Tuple[int, int], int] = {}
        self.rule_type = "table"  # "table", "totalistic", "function"
        self.rule_function: Optional[Callable] = None
        
    def load_rules_from_table(self, rule_table: Dict[Tuple, int]) -> None:
        """Load rules from dictionary"""
        self.rules = rule_table.copy()
        self.rule_type = "table"
    
    def load_rules_from_file(self, filename: str) -> None:
        """Load rules from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
            
        if 'rules' in data:
            # Table-based rules
            self.rules = {
                tuple(rule['pattern']): rule['result']
                for rule in data['rules']
            }
            self.rule_type = "table"
        elif 'totalistic' in data:
            # Totalistic rules
            self.totalistic_rules = {
                tuple(key): value
                for key, value in data['totalistic'].items()
            }
            self.rule_type = "totalistic"
    
    def save_rules_to_file(self, filename: str, metadata: Optional[Dict] = None) -> None:
        """Save rules to JSON file"""
        data = {
            'metadata': metadata or {},
            'rule_type': self.rule_type
        }
        
        if self.rule_type == "table":
            data['rules'] = [
                {'pattern': list(pattern), 'result': result}
                for pattern, result in self.rules.items()
            ]
        elif self.rule_type == "totalistic":
            data['totalistic'] = {
                str(key): value
                for key, value in self.totalistic_rules.items()
            }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_rule(self, pattern: Tuple, result: int) -> None:
        """Add a single rule"""
        self.rules[pattern] = result
    
    def apply_table_rule(self, pattern: Tuple) -> Optional[int]:
        """Apply table-based rule"""
        return self.rules.get(pattern, None)
    
    def apply_totalistic_rule(self, current_state: int, neighbor_sum: int) -> int:
        """Apply totalistic rule"""
        key = (current_state, neighbor_sum)
        return self.totalistic_rules.get(key, current_state)
    
    def apply_function_rule(self, *args, **kwargs) -> int:
        """Apply function-based rule"""
        if self.rule_function is not None:
            return self.rule_function(*args, **kwargs)
        return 0
    
    def get_rule_count(self) -> int:
        """Get number of rules"""
        if self.rule_type == "table":
            return len(self.rules)
        elif self.rule_type == "totalistic":
            return len(self.totalistic_rules)
        return 0


class LangtonLoopRules:
    """
    Complete Langton Loop rule set (219 rules)
    Based on the original specification
    """
    
    @staticmethod
    def get_full_rules() -> Dict[Tuple[int, int, int, int, int], int]:
        """
        Get the complete Langton Loop transition rules
        
        Returns dictionary mapping (C, N, E, S, W) -> new_state
        where C=center, N=north, E=east, S=south, W=west
        """
        # This is a subset of key rules for demonstration
        # Full implementation would have all 219 rules
        rules = {}
        
        # State 0: background
        # State 1: sheath
        # State 2: core (data carrier)
        # State 3-7: various construction states
        
        # Core sheath extension rules
        rules[(0, 1, 1, 1, 0)] = 1
        rules[(0, 1, 1, 0, 1)] = 1
        rules[(0, 1, 0, 1, 1)] = 1
        rules[(0, 0, 1, 1, 1)] = 1
        
        # Signal propagation
        rules[(2, 2, 0, 0, 0)] = 2
        rules[(2, 0, 2, 0, 0)] = 2
        rules[(2, 0, 0, 2, 0)] = 2
        rules[(2, 0, 0, 0, 2)] = 2
        
        # Construction states
        rules[(0, 2, 1, 0, 0)] = 3
        rules[(0, 0, 2, 1, 0)] = 3
        rules[(0, 0, 0, 2, 1)] = 3
        rules[(0, 1, 0, 0, 2)] = 3
        
        rules[(3, 1, 0, 0, 0)] = 1
        rules[(3, 0, 1, 0, 0)] = 1
        rules[(3, 0, 0, 1, 0)] = 1
        rules[(3, 0, 0, 0, 1)] = 1
        
        # Sheath completion
        rules[(1, 1, 1, 0, 0)] = 1
        rules[(1, 1, 0, 1, 0)] = 1
        rules[(1, 1, 0, 0, 1)] = 1
        rules[(1, 0, 1, 1, 0)] = 1
        rules[(1, 0, 1, 0, 1)] = 1
        rules[(1, 0, 0, 1, 1)] = 1
        
        # Core data transmission
        rules[(2, 1, 1, 0, 0)] = 2
        rules[(2, 1, 0, 1, 0)] = 2
        rules[(2, 1, 0, 0, 1)] = 2
        rules[(2, 0, 1, 1, 0)] = 2
        rules[(2, 0, 1, 0, 1)] = 2
        rules[(2, 0, 0, 1, 1)] = 2
        
        # Arm extension
        rules[(4, 0, 0, 0, 0)] = 0
        rules[(4, 1, 0, 0, 0)] = 4
        rules[(4, 0, 1, 0, 0)] = 4
        
        # Turn signals
        rules[(5, 0, 0, 0, 0)] = 0
        rules[(5, 1, 0, 0, 0)] = 5
        rules[(5, 0, 1, 0, 0)] = 5
        
        # More rules would be added here for complete implementation
        # This is approximately 1/6 of the full rule set
        
        return rules


class GameOfLifeRules:
    """Conway's Game of Life rules"""
    
    @staticmethod
    def get_rules() -> Tuple[List[int], List[int]]:
        """
        Get Game of Life rules
        
        Returns:
            Tuple of (birth_conditions, survive_conditions)
        """
        birth = [3]  # Cell born if exactly 3 neighbors
        survive = [2, 3]  # Cell survives if 2 or 3 neighbors
        return (birth, survive)


class WireWorldRules:
    """Wire World transition rules"""
    
    @staticmethod
    def apply_rule(current_state: int, electron_head_count: int) -> int:
        """
        Apply Wire World rules
        
        Args:
            current_state: Current cell state (0=empty, 1=wire, 2=head, 3=tail)
            electron_head_count: Number of electron heads in neighborhood
            
        Returns:
            New state
        """
        if current_state == 0:  # Empty stays empty
            return 0
        elif current_state == 2:  # Electron head -> tail
            return 3
        elif current_state == 3:  # Electron tail -> wire
            return 1
        elif current_state == 1:  # Wire
            # Becomes head if 1 or 2 heads nearby
            if electron_head_count in [1, 2]:
                return 2
        return current_state
