"""
CALab - Von Neumann Universal Constructor Plugin

The original self-replicating cellular automaton designed by John von Neumann
in the 1940s. This is a 29-state automaton with von Neumann neighborhood.

States:
0 - Ground (background)
1-4 - Transmission states (signal carriers)
5-8 - Confluent states (signal mergers)
9-15 - Special transmission states
16-23 - Sensitized states
24-28 - Special function states
"""

import numpy as np
from core.automaton_base import (CellularAutomaton, PluginInterface, 
                                AutomatonMetadata, NeighborhoodType)


class VonNeumannConstructor(CellularAutomaton):
    """
    Von Neumann's Universal Constructor
    
    The first self-replicating cellular automaton, designed to prove
    that self-replication is possible in artificial systems.
    
    This is a simplified implementation focusing on basic transmission
    and construction capabilities.
    """
    
    def __init__(self, width: int, height: int):
        metadata = AutomatonMetadata(
            name="Von Neumann Universal Constructor",
            description="The original self-replicating automaton (29 states)",
            author="John von Neumann (Implementation: CALab)",
            version="1.0",
            num_states=29,
            neighborhood_type=NeighborhoodType.VON_NEUMANN
        )
        super().__init__(width, height, metadata)
        self._init_rules()
        
    def _init_rules(self):
        """Initialize simplified von Neumann rules"""
        # This is a simplified subset of rules for demonstration
        # Full implementation would have ~10,000 rules
        
        # Basic rule structure: (center, north, east, south, west) -> new_state
        self.rules = {}
        
        # Ground state (0) rules - stay ground unless activated
        self.rules[(0, 0, 0, 0, 0)] = 0
        
        # Transmission states propagate signals
        # State 1 = ordinary transmission cell (OT)
        # Signals flow through transmission states
        for n in [0, 1, 2, 3, 4]:
            for e in [0, 1, 2, 3, 4]:
                for s in [0, 1, 2, 3, 4]:
                    for w in [0, 1, 2, 3, 4]:
                        # Simple transmission: if any neighbor is active, become active
                        if n > 0 or e > 0 or s > 0 or w > 0:
                            self.rules[(1, n, e, s, w)] = min(n + e + s + w, 4)
        
        # Construction states - build new cells
        # State 5 = ordinary construction cell (OC)
        self.rules[(0, 5, 0, 0, 0)] = 1  # OC north creates transmission
        self.rules[(0, 0, 5, 0, 0)] = 1  # OC east creates transmission
        self.rules[(0, 0, 0, 5, 0)] = 1  # OC south creates transmission
        self.rules[(0, 0, 0, 0, 5)] = 1  # OC west creates transmission
        
        # Confluent states merge signals
        # State 6 = confluent cell
        for n in range(5):
            for e in range(5):
                if n > 0 and e > 0:
                    self.rules[(6, n, e, 0, 0)] = 4  # Merge signals
        
    def step(self):
        """Apply von Neumann rules"""
        new_grid = self.grid.copy()
        h, w = self.grid.shape
        
        for y in range(h):
            for x in range(w):
                center = self.grid[y, x]
                
                # Get von Neumann neighborhood
                north = self.grid[(y - 1) % h, x]
                east = self.grid[y, (x + 1) % w]
                south = self.grid[(y + 1) % h, x]
                west = self.grid[y, (x - 1) % w]
                
                # Apply rule if it exists
                pattern = (center, north, east, south, west)
                if pattern in self.rules:
                    new_grid[y, x] = self.rules[pattern]
                else:
                    # Default: decay to ground or stay the same
                    if center > 5:
                        new_grid[y, x] = max(0, center - 1)
                        
        self.grid = new_grid
        self.generation += 1
    
    def initialize_pattern(self, pattern_name: str, **kwargs):
        """Initialize with a specific pattern"""
        if pattern_name == 'simple_reproducer':
            self._create_simple_reproducer(**kwargs)
        elif pattern_name == 'signal_line':
            self._create_signal_line(**kwargs)
        elif pattern_name == 'constructor_arm':
            self._create_constructor_arm(**kwargs)
        else:
            self._create_simple_reproducer(**kwargs)
    
    def _create_simple_reproducer(self, x: int = None, y: int = None):
        """Create a simple self-replicating pattern"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2
        
        # Create a small pattern that demonstrates construction
        pattern = [
            [0, 5, 0],
            [1, 6, 1],
            [0, 5, 0]
        ]
        
        for dy in range(len(pattern)):
            for dx in range(len(pattern[0])):
                ny, nx = cy + dy - 1, cx + dx - 1
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    self.grid[ny, nx] = pattern[dy][dx]
    
    def _create_signal_line(self, x: int = None, y: int = None):
        """Create a signal transmission line"""
        cx = x if x is not None else self.width // 4
        cy = y if y is not None else self.height // 2
        
        # Horizontal transmission line
        for i in range(30):
            if 0 <= cy < self.height and 0 <= cx + i < self.width:
                self.grid[cy, cx + i] = 1  # Transmission state
        
        # Add signal at start
        if 0 <= cy < self.height and 0 <= cx < self.width:
            self.grid[cy, cx] = 4  # Active signal
        
        # Vertical line
        for i in range(20):
            if 0 <= cy + i < self.height and 0 <= cx + 15 < self.width:
                self.grid[cy + i, cx + 15] = 1
    
    def _create_constructor_arm(self, x: int = None, y: int = None):
        """Create a construction arm"""
        cx = x if x is not None else self.width // 4
        cy = y if y is not None else self.height // 2
        
        # Construction cells
        for i in range(10):
            if 0 <= cy < self.height and 0 <= cx + i < self.width:
                self.grid[cy, cx + i] = 5  # Construction state
        
        # Add some transmission support
        for i in range(10):
            if 0 <= cy + 1 < self.height and 0 <= cx + i < self.width:
                self.grid[cy + 1, cx + i] = 1
            if 0 <= cy - 1 < self.height and 0 <= cx + i < self.width:
                self.grid[cy - 1, cx + i] = 1


class VonNeumannConstructorPlugin(PluginInterface):
    """Plugin interface for Von Neumann Constructor"""
    
    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="Von Neumann Universal Constructor",
            description="The original self-replicating automaton (29 states)",
            author="John von Neumann",
            version="1.0",
            num_states=29,
            neighborhood_type=NeighborhoodType.VON_NEUMANN,
            is_totalistic=False,
            supports_mutation=False
        )
    
    @staticmethod
    def create_automaton(width: int, height: int, **kwargs):
        automaton = VonNeumannConstructor(width, height)
        pattern = kwargs.get('pattern', 'simple_reproducer')
        automaton.initialize_pattern(pattern, **{k: v for k, v in kwargs.items() if k != 'pattern'})
        return automaton
    
    @staticmethod
    def get_default_patterns():
        return {
            'simple_reproducer': {
                'description': 'Simple self-replicating pattern',
                'recommended_size': (150, 150)
            },
            'signal_line': {
                'description': 'Signal transmission demonstration',
                'recommended_size': (150, 150)
            },
            'constructor_arm': {
                'description': 'Construction arm pattern',
                'recommended_size': (150, 150)
            }
        }
    
    @staticmethod
    def get_colormap():
        """Generate colormap for 29 states"""
        colors = [
            '#000000',  # 0: Ground - black
            '#00FF00',  # 1: Transmission - green
            '#00DD00',  # 2: Transmission - darker green
            '#00BB00',  # 3: Transmission - darker green
            '#00FF00',  # 4: Active signal - bright green
            '#FF0000',  # 5: Construction - red
            '#FF00FF',  # 6: Confluent - magenta
            '#FFFF00',  # 7: Special - yellow
            '#00FFFF',  # 8: Special - cyan
        ]
        
        # Add more colors for remaining states
        additional_colors = [
            '#FF8800', '#8800FF', '#FF0088', '#00FF88',
            '#888800', '#FF8888', '#88FF88', '#8888FF',
            '#FFFF88', '#FF88FF', '#88FFFF', '#FF8800',
            '#8800FF', '#FF0088', '#00FF88', '#888800',
            '#FF8888', '#88FF88', '#8888FF', '#FFFF88'
        ]
        
        return colors + additional_colors
