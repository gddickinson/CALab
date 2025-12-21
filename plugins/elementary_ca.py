"""
CALab - Elementary Cellular Automata Plugin

1D cellular automata visualized in 2D, showing evolution over time.
Includes famous rules like Rule 30, Rule 110, Rule 90, etc.

Each row represents one generation, creating beautiful patterns.
"""

import numpy as np
from core.automaton_base import (CellularAutomaton, PluginInterface, 
                                AutomatonMetadata, NeighborhoodType)


class ElementaryCA(CellularAutomaton):
    """
    Elementary Cellular Automaton
    
    1D automaton with 2 states, visualized as 2D (time going down).
    256 possible rules (0-255).
    
    Famous rules:
    - Rule 30: Chaotic, used in random number generation
    - Rule 110: Turing complete (computationally universal)
    - Rule 90: Sierpinski triangle
    - Rule 184: Traffic flow model
    """
    
    def __init__(self, width: int, height: int, rule: int = 30):
        metadata = AutomatonMetadata(
            name=f"Elementary CA - Rule {rule}",
            description=f"1D cellular automaton (Rule {rule})",
            author="Stephen Wolfram (Implementation: CALab)",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.CUSTOM
        )
        super().__init__(width, height, metadata)
        
        self.rule_number = rule
        self.rule_table = self._generate_rule_table(rule)
        self.current_row = 0
        
    def _generate_rule_table(self, rule: int):
        """Generate lookup table for rule"""
        # Convert rule number to 8-bit binary
        binary = format(rule, '08b')[::-1]  # Reverse for correct indexing
        
        # Create lookup table for all 8 neighborhood patterns
        # Pattern: (left, center, right) -> new_state
        table = {}
        for i in range(8):
            pattern = (i >> 2, (i >> 1) & 1, i & 1)
            table[pattern] = int(binary[i])
        
        return table
    
    def step(self):
        """Apply elementary CA rule to current row"""
        if self.current_row >= self.height - 1:
            return  # Filled entire grid
        
        w = self.width
        current = self.grid[self.current_row]
        next_row = np.zeros(w, dtype=np.int32)
        
        # Apply rule to each cell
        for x in range(w):
            left = current[(x - 1) % w]
            center = current[x]
            right = current[(x + 1) % w]
            
            pattern = (left, center, right)
            next_row[x] = self.rule_table[pattern]
        
        # Set next row
        self.current_row += 1
        self.grid[self.current_row] = next_row
        self.generation += 1
    
    def initialize_pattern(self, pattern_name: str, **kwargs):
        """Initialize first row with a pattern"""
        self.current_row = 0
        
        if pattern_name == 'single_cell':
            self._create_single_cell(**kwargs)
        elif pattern_name == 'random':
            self._create_random(**kwargs)
        elif pattern_name == 'alternating':
            self._create_alternating(**kwargs)
        elif pattern_name == 'three_cells':
            self._create_three_cells(**kwargs)
        else:
            self._create_single_cell(**kwargs)
    
    def _create_single_cell(self, x: int = None, y: int = None):
        """Single cell in center"""
        cx = x if x is not None else self.width // 2
        self.grid[0, cx] = 1
    
    def _create_random(self, density: float = 0.5, x: int = None, y: int = None):
        """Random first row"""
        self.grid[0] = (np.random.random(self.width) < density).astype(np.int32)
    
    def _create_alternating(self, x: int = None, y: int = None):
        """Alternating pattern"""
        for i in range(0, self.width, 2):
            self.grid[0, i] = 1
    
    def _create_three_cells(self, x: int = None, y: int = None):
        """Three cells in center"""
        cx = x if x is not None else self.width // 2
        if cx - 1 >= 0:
            self.grid[0, cx - 1] = 1
        self.grid[0, cx] = 1
        if cx + 1 < self.width:
            self.grid[0, cx + 1] = 1


class ElementaryCAPlugin(PluginInterface):
    """Plugin interface for Elementary CA"""
    
    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="Elementary Cellular Automata",
            description="1D automaton rules (Wolfram)",
            author="Stephen Wolfram",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.CUSTOM,
            is_totalistic=False,
            supports_mutation=False
        )
    
    @staticmethod
    def create_automaton(width: int, height: int, **kwargs):
        rule = kwargs.get('rule', 30)
        automaton = ElementaryCA(width, height, rule)
        pattern = kwargs.get('pattern', 'single_cell')
        automaton.initialize_pattern(pattern, **{k: v for k, v in kwargs.items() if k not in ['pattern', 'rule']})
        return automaton
    
    @staticmethod
    def get_default_patterns():
        return {
            'single_cell': {
                'description': 'Single cell (classic)',
                'recommended_size': (200, 200),
                'rules': {
                    'rule_30': 'Chaotic (used in Mathematica RNG)',
                    'rule_110': 'Turing complete!',
                    'rule_90': 'Sierpinski triangle',
                    'rule_184': 'Traffic flow model'
                }
            },
            'random': {
                'description': 'Random initial row',
                'recommended_size': (200, 200),
                'parameters': {'density': 0.5}
            },
            'alternating': {
                'description': 'Alternating cells',
                'recommended_size': (200, 200)
            },
            'three_cells': {
                'description': 'Three cells in center',
                'recommended_size': (200, 200)
            }
        }
    
    @staticmethod
    def get_colormap():
        return [
            '#000000',  # 0: Dead - black
            '#FFFFFF',  # 1: Alive - white
        ]


# Create specific rule plugins for easy access

class Rule30Plugin(PluginInterface):
    """Rule 30 - Chaotic pattern"""
    
    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="Rule 30 (Chaotic)",
            description="Chaotic elementary CA - random number generation",
            author="Stephen Wolfram",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.CUSTOM
        )
    
    @staticmethod
    def create_automaton(width: int, height: int, **kwargs):
        automaton = ElementaryCA(width, height, rule=30)
        pattern = kwargs.get('pattern', 'single_cell')
        automaton.initialize_pattern(pattern, **{k: v for k, v in kwargs.items() if k != 'pattern'})
        return automaton
    
    @staticmethod
    def get_default_patterns():
        return ElementaryCAPlugin.get_default_patterns()
    
    @staticmethod
    def get_colormap():
        return ElementaryCAPlugin.get_colormap()


class Rule110Plugin(PluginInterface):
    """Rule 110 - Turing complete"""
    
    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="Rule 110 (Turing Complete)",
            description="Computationally universal elementary CA",
            author="Stephen Wolfram",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.CUSTOM
        )
    
    @staticmethod
    def create_automaton(width: int, height: int, **kwargs):
        automaton = ElementaryCA(width, height, rule=110)
        pattern = kwargs.get('pattern', 'random')
        automaton.initialize_pattern(pattern, **{k: v for k, v in kwargs.items() if k != 'pattern'})
        return automaton
    
    @staticmethod
    def get_default_patterns():
        return ElementaryCAPlugin.get_default_patterns()
    
    @staticmethod
    def get_colormap():
        return ElementaryCAPlugin.get_colormap()


class Rule90Plugin(PluginInterface):
    """Rule 90 - Sierpinski triangle"""
    
    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="Rule 90 (Sierpinski)",
            description="Generates Sierpinski triangle fractal",
            author="Stephen Wolfram",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.CUSTOM
        )
    
    @staticmethod
    def create_automaton(width: int, height: int, **kwargs):
        automaton = ElementaryCA(width, height, rule=90)
        pattern = kwargs.get('pattern', 'single_cell')
        automaton.initialize_pattern(pattern, **{k: v for k, v in kwargs.items() if k != 'pattern'})
        return automaton
    
    @staticmethod
    def get_default_patterns():
        return ElementaryCAPlugin.get_default_patterns()
    
    @staticmethod
    def get_colormap():
        return ElementaryCAPlugin.get_colormap()
