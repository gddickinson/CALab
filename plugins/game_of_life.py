"""
CALab - Conway's Game of Life Plugin

The most famous cellular automaton, demonstrating how complex behavior
can emerge from simple rules.

States:
0 - Dead
1 - Alive

Rules:
- Any live cell with 2-3 live neighbors survives
- Any dead cell with exactly 3 live neighbors becomes alive
- All other cells die or stay dead
"""

import numpy as np
from core.automaton_base import (CellularAutomaton, PluginInterface, 
                                AutomatonMetadata, NeighborhoodType)


class GameOfLife(CellularAutomaton):
    """
    Conway's Game of Life
    
    The classic cellular automaton that demonstrates emergence,
    self-organization, and pattern formation.
    """
    
    def __init__(self, width: int, height: int):
        metadata = AutomatonMetadata(
            name="Conway's Game of Life",
            description="The classic cellular automaton (B3/S23)",
            author="John Conway (Implementation: CALab)",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.MOORE,
            is_totalistic=True,
            supports_mutation=False
        )
        super().__init__(width, height, metadata)
        
    def step(self):
        """Apply Game of Life rules"""
        new_grid = self.grid.copy()
        h, w = self.grid.shape
        
        for y in range(h):
            for x in range(w):
                # Count live neighbors (Moore neighborhood)
                neighbors = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0:
                            continue
                        ny, nx = (y + dy) % h, (x + dx) % w
                        neighbors += self.grid[ny, nx]
                
                current = self.grid[y, x]
                
                # Game of Life rules (B3/S23)
                if current == 1:  # Alive
                    if neighbors < 2 or neighbors > 3:
                        new_grid[y, x] = 0  # Dies
                    # else stays alive (2 or 3 neighbors)
                else:  # Dead
                    if neighbors == 3:
                        new_grid[y, x] = 1  # Birth
                        
        self.grid = new_grid
        self.generation += 1
    
    def initialize_pattern(self, pattern_name: str, **kwargs):
        """Initialize with a specific pattern"""
        patterns = {
            'glider_gun': self._create_glider_gun,
            'glider': self._create_glider,
            'pulsar': self._create_pulsar,
            'pentadecathlon': self._create_pentadecathlon,
            'lightweight_spaceship': self._create_lwss,
            'r_pentomino': self._create_r_pentomino,
            'diehard': self._create_diehard,
            'acorn': self._create_acorn,
            'random': self._create_random
        }
        
        pattern_func = patterns.get(pattern_name, self._create_glider_gun)
        pattern_func(**{k: v for k, v in kwargs.items() if k != 'pattern'})
    
    def _create_glider_gun(self, x: int = None, y: int = None):
        """Create Gosper's Glider Gun - the first discovered gun"""
        cx = x if x is not None else 10
        cy = y if y is not None else 10
        
        # Gosper's Glider Gun pattern
        gun = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        
        for dy in range(len(gun)):
            for dx in range(len(gun[0])):
                if cy + dy < self.height and cx + dx < self.width:
                    self.grid[cy + dy, cx + dx] = gun[dy][dx]
    
    def _create_glider(self, x: int = None, y: int = None):
        """Create a single glider"""
        cx = x if x is not None else self.width // 4
        cy = y if y is not None else self.height // 4
        
        glider = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ]
        
        for dy in range(3):
            for dx in range(3):
                if cy + dy < self.height and cx + dx < self.width:
                    self.grid[cy + dy, cx + dx] = glider[dy][dx]
    
    def _create_pulsar(self, x: int = None, y: int = None):
        """Create a pulsar - period 3 oscillator"""
        cx = x if x is not None else self.width // 2 - 6
        cy = y if y is not None else self.height // 2 - 6
        
        pulsar = [
            [0,0,1,1,1,0,0,0,1,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [0,0,1,1,1,0,0,0,1,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,0,0,0,1,1,1,0,0],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,0,0,0,1,1,1,0,0],
        ]
        
        for dy in range(len(pulsar)):
            for dx in range(len(pulsar[0])):
                if cy + dy < self.height and cx + dx < self.width:
                    self.grid[cy + dy, cx + dx] = pulsar[dy][dx]
    
    def _create_pentadecathlon(self, x: int = None, y: int = None):
        """Create pentadecathlon - period 15 oscillator"""
        cx = x if x is not None else self.width // 2 - 5
        cy = y if y is not None else self.height // 2 - 1
        
        pentadecathlon = [
            [0,0,1,0,0,0,0,1,0,0],
            [1,1,0,1,1,1,1,0,1,1],
            [0,0,1,0,0,0,0,1,0,0],
        ]
        
        for dy in range(len(pentadecathlon)):
            for dx in range(len(pentadecathlon[0])):
                if cy + dy < self.height and cx + dx < self.width:
                    self.grid[cy + dy, cx + dx] = pentadecathlon[dy][dx]
    
    def _create_lwss(self, x: int = None, y: int = None):
        """Create lightweight spaceship"""
        cx = x if x is not None else self.width // 4
        cy = y if y is not None else self.height // 4
        
        lwss = [
            [0,1,0,0,1],
            [1,0,0,0,0],
            [1,0,0,0,1],
            [1,1,1,1,0]
        ]
        
        for dy in range(len(lwss)):
            for dx in range(len(lwss[0])):
                if cy + dy < self.height and cx + dx < self.width:
                    self.grid[cy + dy, cx + dx] = lwss[dy][dx]
    
    def _create_r_pentomino(self, x: int = None, y: int = None):
        """Create R-pentomino - chaotic pattern"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2
        
        r_pentomino = [
            [0,1,1],
            [1,1,0],
            [0,1,0]
        ]
        
        for dy in range(len(r_pentomino)):
            for dx in range(len(r_pentomino[0])):
                if cy + dy < self.height and cx + dx < self.width:
                    self.grid[cy + dy, cx + dx] = r_pentomino[dy][dx]
    
    def _create_diehard(self, x: int = None, y: int = None):
        """Create Diehard - dies after 130 generations"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2
        
        diehard = [
            [0,0,0,0,0,0,1,0],
            [1,1,0,0,0,0,0,0],
            [0,1,0,0,0,1,1,1]
        ]
        
        for dy in range(len(diehard)):
            for dx in range(len(diehard[0])):
                if cy + dy < self.height and cx + dx < self.width:
                    self.grid[cy + dy, cx + dx] = diehard[dy][dx]
    
    def _create_acorn(self, x: int = None, y: int = None):
        """Create Acorn - creates lots of activity"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2
        
        acorn = [
            [0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0],
            [1,1,0,0,1,1,1]
        ]
        
        for dy in range(len(acorn)):
            for dx in range(len(acorn[0])):
                if cy + dy < self.height and cx + dx < self.width:
                    self.grid[cy + dy, cx + dx] = acorn[dy][dx]
    
    def _create_random(self, density: float = 0.3, x: int = None, y: int = None, 
                      size_x: int = None, size_y: int = None):
        """Create random pattern"""
        if size_x is None:
            size_x = self.width // 2
        if size_y is None:
            size_y = self.height // 2
        if x is None:
            x = self.width // 4
        if y is None:
            y = self.height // 4
        
        for dy in range(size_y):
            for dx in range(size_x):
                if y + dy < self.height and x + dx < self.width:
                    if np.random.random() < density:
                        self.grid[y + dy, x + dx] = 1


class GameOfLifePlugin(PluginInterface):
    """Plugin interface for Conway's Game of Life"""
    
    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="Conway's Game of Life",
            description="The classic cellular automaton (B3/S23)",
            author="John Conway",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.MOORE,
            is_totalistic=True,
            supports_mutation=False
        )
    
    @staticmethod
    def create_automaton(width: int, height: int, **kwargs):
        automaton = GameOfLife(width, height)
        pattern = kwargs.get('pattern', 'glider_gun')
        automaton.initialize_pattern(pattern, **kwargs)
        return automaton
    
    @staticmethod
    def get_default_patterns():
        return {
            'glider_gun': {
                'description': "Gosper's Glider Gun - creates gliders",
                'recommended_size': (150, 150),
                'period': 30
            },
            'glider': {
                'description': 'Simple glider spaceship',
                'recommended_size': (100, 100),
                'period': 4
            },
            'pulsar': {
                'description': 'Period-3 oscillator',
                'recommended_size': (100, 100),
                'period': 3
            },
            'pentadecathlon': {
                'description': 'Period-15 oscillator',
                'recommended_size': (100, 100),
                'period': 15
            },
            'lightweight_spaceship': {
                'description': 'LWSS - faster than glider',
                'recommended_size': (100, 100),
                'period': 4
            },
            'r_pentomino': {
                'description': 'Chaotic methuselah pattern',
                'recommended_size': (150, 150),
                'stabilizes_at': 1103
            },
            'diehard': {
                'description': 'Dies after 130 generations',
                'recommended_size': (100, 100),
                'lifespan': 130
            },
            'acorn': {
                'description': 'Small pattern with long evolution',
                'recommended_size': (150, 150),
                'stabilizes_at': 5206
            },
            'random': {
                'description': 'Random soup',
                'recommended_size': (100, 100),
                'parameters': {'density': 0.3}
            }
        }
    
    @staticmethod
    def get_colormap():
        return [
            '#000000',  # 0: Dead - black
            '#00FF00',  # 1: Alive - green
        ]
