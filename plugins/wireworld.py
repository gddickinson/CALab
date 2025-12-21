"""
CALab - Wire World Plugin

Wire World is a cellular automaton particularly suited to simulating
electronic logic circuits. It demonstrates signal propagation beautifully.

States:
0 - Empty (background)
1 - Wire (conductor)
2 - Electron head
3 - Electron tail
"""

import numpy as np
from core.automaton_base import (CellularAutomaton, PluginInterface, 
                                AutomatonMetadata, NeighborhoodType)


class WireWorld(CellularAutomaton):
    """
    Wire World Cellular Automaton
    
    A cellular automaton that simulates electronic circuits with electrons
    flowing through wires.
    
    Rules:
    - Empty -> Empty (always)
    - Electron head -> Electron tail (always)
    - Electron tail -> Wire (always)
    - Wire -> Electron head (if exactly 1 or 2 electron heads in Moore neighborhood)
    """
    
    def __init__(self, width: int, height: int):
        metadata = AutomatonMetadata(
            name="Wire World",
            description="Cellular automaton for simulating circuits",
            author="Brian Silverman (Implementation: CALab)",
            version="1.0",
            num_states=4,
            neighborhood_type=NeighborhoodType.MOORE
        )
        super().__init__(width, height, metadata)
        
    def step(self):
        """Apply Wire World transition rules"""
        new_grid = self.grid.copy()
        h, w = self.grid.shape
        
        for y in range(h):
            for x in range(w):
                current = self.grid[y, x]
                
                if current == 0:  # Empty stays empty
                    continue
                    
                elif current == 2:  # Electron head -> tail
                    new_grid[y, x] = 3
                    
                elif current == 3:  # Electron tail -> wire
                    new_grid[y, x] = 1
                    
                elif current == 1:  # Wire
                    # Count electron heads in Moore neighborhood (8 neighbors)
                    heads = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dy == 0 and dx == 0:
                                continue
                            ny, nx = (y + dy) % h, (x + dx) % w
                            if self.grid[ny, nx] == 2:
                                heads += 1
                    
                    # Wire becomes electron head if exactly 1 or 2 heads nearby
                    if heads in [1, 2]:
                        new_grid[y, x] = 2
                        
        self.grid = new_grid
        self.generation += 1
    
    def initialize_pattern(self, pattern_name: str, **kwargs):
        """Initialize with a specific pattern"""
        if pattern_name == "simple_circuit":
            self._create_simple_circuit(**{k: v for k, v in kwargs.items() if k != 'pattern'})
        elif pattern_name == "or_gate":
            self._create_or_gate(**{k: v for k, v in kwargs.items() if k != 'pattern'})
        elif pattern_name == "diode":
            self._create_diode(**{k: v for k, v in kwargs.items() if k != 'pattern'})
        elif pattern_name == "clock":
            self._create_clock(**{k: v for k, v in kwargs.items() if k != 'pattern'})
        else:
            self._create_simple_circuit(**{k: v for k, v in kwargs.items() if k != 'pattern'})
    
    def _create_simple_circuit(self, x: int = None, y: int = None):
        """Create a simple circular circuit"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2
        
        # Create a circular wire
        radius = 20
        for angle in np.linspace(0, 2*np.pi, 120):
            wx = int(cx + radius * np.cos(angle))
            wy = int(cy + radius * np.sin(angle))
            if 0 <= wx < self.width and 0 <= wy < self.height:
                self.grid[wy, wx] = 1
                
        # Add some branching wires
        for i in range(25):
            if 0 <= cy < self.height and 0 <= cx + i < self.width:
                self.grid[cy, cx + i] = 1
            if 0 <= cy + i < self.height and 0 <= cx < self.width:
                self.grid[cy + i, cx] = 1
            if 0 <= cy < self.height and 0 <= cx - i < self.width:
                self.grid[cy, cx - i] = 1
                
        # Add electrons
        if 0 <= cy - radius < self.height and 0 <= cx < self.width:
            self.grid[cy - radius, cx] = 2
            if 0 <= cy - radius + 1 < self.height:
                self.grid[cy - radius + 1, cx] = 3
        
        if 0 <= cy < self.height and 0 <= cx + 5 < self.width:
            self.grid[cy, cx + 5] = 2
            if 0 <= cx + 6 < self.width:
                self.grid[cy, cx + 6] = 3
    
    def _create_or_gate(self, x: int = None, y: int = None):
        """Create an OR gate circuit"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2
        
        # OR gate pattern (simplified)
        # Input A
        for i in range(10):
            if 0 <= cy - 5 < self.height and 0 <= cx + i < self.width:
                self.grid[cy - 5, cx + i] = 1
        
        # Input B
        for i in range(10):
            if 0 <= cy + 5 < self.height and 0 <= cx + i < self.width:
                self.grid[cy + 5, cx + i] = 1
        
        # Output wire
        for i in range(15):
            if 0 <= cy < self.height and 0 <= cx + 10 + i < self.width:
                self.grid[cy, cx + 10 + i] = 1
        
        # Connecting wires
        for i in range(5):
            if 0 <= cy - 5 + i < self.height and 0 <= cx + 10 < self.width:
                self.grid[cy - 5 + i, cx + 10] = 1
            if 0 <= cy + 5 - i < self.height and 0 <= cx + 10 < self.width:
                self.grid[cy + 5 - i, cx + 10] = 1
        
        # Add input electrons
        if 0 <= cy - 5 < self.height and 0 <= cx < self.width:
            self.grid[cy - 5, cx] = 2
            if 0 <= cx + 1 < self.width:
                self.grid[cy - 5, cx + 1] = 3
    
    def _create_diode(self, x: int = None, y: int = None):
        """Create a diode (one-way conductor)"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2
        
        # Diode pattern
        diode = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        
        for dy in range(len(diode)):
            for dx in range(len(diode[0])):
                ny, nx = cy + dy - 3, cx + dx - 5
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    self.grid[ny, nx] = diode[dy][dx]
        
        # Add electron
        if 0 <= cy < self.height and 0 <= cx - 5 < self.width:
            self.grid[cy, cx - 5] = 2
            if 0 <= cx - 4 < self.width:
                self.grid[cy, cx - 4] = 3
    
    def _create_clock(self, x: int = None, y: int = None):
        """Create a clock generator circuit"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2
        
        # Small loop for clock
        size = 10
        for i in range(size):
            # Top and bottom
            if 0 <= cy - size//2 < self.height:
                if 0 <= cx - size//2 + i < self.width:
                    self.grid[cy - size//2, cx - size//2 + i] = 1
                if 0 <= cy + size//2 < self.height:
                    self.grid[cy + size//2, cx - size//2 + i] = 1
            
            # Left and right
            if 0 <= cx - size//2 < self.width:
                if 0 <= cy - size//2 + i < self.height:
                    self.grid[cy - size//2 + i, cx - size//2] = 1
                if 0 <= cx + size//2 < self.width:
                    self.grid[cy - size//2 + i, cx + size//2] = 1
        
        # Add electrons to create oscillation
        if 0 <= cy - size//2 < self.height and 0 <= cx < self.width:
            self.grid[cy - size//2, cx] = 2
            if 0 <= cx + 1 < self.width:
                self.grid[cy - size//2, cx + 1] = 3


class WireWorldPlugin(PluginInterface):
    """Plugin interface for Wire World"""
    
    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="Wire World",
            description="Circuit simulation cellular automaton",
            author="Brian Silverman",
            version="1.0",
            num_states=4,
            neighborhood_type=NeighborhoodType.MOORE,
            is_totalistic=False,
            supports_mutation=False
        )
    
    @staticmethod
    def create_automaton(width: int, height: int, **kwargs):
        automaton = WireWorld(width, height)
        pattern = kwargs.get('pattern', 'simple_circuit')
        automaton.initialize_pattern(pattern, **kwargs)
        return automaton
    
    @staticmethod
    def get_default_patterns():
        return {
            'simple_circuit': {
                'description': 'Simple circuit with electrons',
                'recommended_size': (150, 150)
            },
            'or_gate': {
                'description': 'OR logic gate',
                'recommended_size': (100, 100)
            },
            'diode': {
                'description': 'One-way conductor',
                'recommended_size': (100, 100)
            },
            'clock': {
                'description': 'Clock signal generator',
                'recommended_size': (100, 100)
            }
        }
    
    @staticmethod
    def get_colormap():
        return [
            '#000000',  # 0: Empty - black
            '#FFFF00',  # 1: Wire - yellow
            '#0000FF',  # 2: Electron head - blue
            '#FF0000',  # 3: Electron tail - red
        ]
