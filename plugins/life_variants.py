"""
CALab - Life-like Variants: Day and Night, HighLife

Additional variants of Conway's Game of Life with different rules.
"""

import numpy as np
from core.automaton_base import (CellularAutomaton, PluginInterface, 
                                AutomatonMetadata, NeighborhoodType)


class DayAndNight(CellularAutomaton):
    """
    Day and Night (B3678/S34678)
    
    Symmetric rule where the roles of live and dead cells are symmetric.
    Creates complex stable patterns.
    
    Birth: 3, 6, 7, 8 neighbors
    Survival: 3, 4, 6, 7, 8 neighbors
    """
    
    def __init__(self, width: int, height: int):
        metadata = AutomatonMetadata(
            name="Day and Night",
            description="Symmetric Life variant (B3678/S34678)",
            author="Nathan Thompson (Implementation: CALab)",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.MOORE,
            is_totalistic=True,
            supports_mutation=False
        )
        super().__init__(width, height, metadata)
        
    def step(self):
        """Apply Day and Night rules"""
        new_grid = self.grid.copy()
        h, w = self.grid.shape
        
        for y in range(h):
            for x in range(w):
                # Count live neighbors
                neighbors = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0:
                            continue
                        ny, nx = (y + dy) % h, (x + dx) % w
                        neighbors += self.grid[ny, nx]
                
                current = self.grid[y, x]
                
                # Day and Night rules (B3678/S34678)
                if current == 0:  # Dead
                    if neighbors in [3, 6, 7, 8]:
                        new_grid[y, x] = 1  # Birth
                else:  # Alive
                    if neighbors not in [3, 4, 6, 7, 8]:
                        new_grid[y, x] = 0  # Death
                        
        self.grid = new_grid
        self.generation += 1
    
    def initialize_pattern(self, pattern_name: str, **kwargs):
        """Initialize with a specific pattern"""
        if pattern_name == 'random':
            self._create_random(**kwargs)
        elif pattern_name == 'symmetry':
            self._create_symmetry(**kwargs)
        elif pattern_name == 'checkerboard':
            self._create_checkerboard(**kwargs)
        else:
            self._create_random(**kwargs)
    
    def _create_random(self, density: float = 0.5, x: int = None, y: int = None):
        """Random pattern"""
        self.grid = (np.random.random((self.height, self.width)) < density).astype(np.int32)
    
    def _create_symmetry(self, x: int = None, y: int = None):
        """Create symmetrical pattern"""
        cx = self.width // 2
        cy = self.height // 2
        
        # Create random quarter
        quarter = np.random.randint(0, 2, size=(cy, cx))
        
        # Mirror to create full symmetric pattern
        top = np.hstack([quarter, np.fliplr(quarter)])
        full = np.vstack([top, np.flipud(top)])
        
        # Place in grid
        sy = (self.height - full.shape[0]) // 2
        sx = (self.width - full.shape[1]) // 2
        self.grid[sy:sy+full.shape[0], sx:sx+full.shape[1]] = full
    
    def _create_checkerboard(self, x: int = None, y: int = None):
        """Checkerboard pattern"""
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y, x] = (x + y) % 2


class DayAndNightPlugin(PluginInterface):
    """Plugin interface for Day and Night"""
    
    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="Day and Night",
            description="Symmetric Life variant (B3678/S34678)",
            author="Nathan Thompson",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.MOORE,
            is_totalistic=True,
            supports_mutation=False
        )
    
    @staticmethod
    def create_automaton(width: int, height: int, **kwargs):
        automaton = DayAndNight(width, height)
        pattern = kwargs.get('pattern', 'random')
        automaton.initialize_pattern(pattern, **{k: v for k, v in kwargs.items() if k != 'pattern'})
        return automaton
    
    @staticmethod
    def get_default_patterns():
        return {
            'random': {
                'description': 'Random soup',
                'recommended_size': (150, 150),
                'parameters': {'density': 0.5}
            },
            'symmetry': {
                'description': 'Symmetric pattern',
                'recommended_size': (150, 150)
            },
            'checkerboard': {
                'description': 'Checkerboard (interesting evolution)',
                'recommended_size': (150, 150)
            }
        }
    
    @staticmethod
    def get_colormap():
        return [
            '#000000',  # 0: Dead - black
            '#FFFFFF',  # 1: Alive - white
        ]


class HighLife(CellularAutomaton):
    """
    HighLife (B36/S23)
    
    Like Conway's Life but with an additional birth rule.
    Contains a small replicator pattern!
    
    Birth: 3, 6 neighbors
    Survival: 2, 3 neighbors
    """
    
    def __init__(self, width: int, height: int):
        metadata = AutomatonMetadata(
            name="HighLife",
            description="Life variant with replicators (B36/S23)",
            author="Nathan Thompson (Implementation: CALab)",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.MOORE,
            is_totalistic=True,
            supports_mutation=False
        )
        super().__init__(width, height, metadata)
        
    def step(self):
        """Apply HighLife rules"""
        new_grid = self.grid.copy()
        h, w = self.grid.shape
        
        for y in range(h):
            for x in range(w):
                # Count live neighbors
                neighbors = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0:
                            continue
                        ny, nx = (y + dy) % h, (x + dx) % w
                        neighbors += self.grid[ny, nx]
                
                current = self.grid[y, x]
                
                # HighLife rules (B36/S23)
                if current == 0:  # Dead
                    if neighbors in [3, 6]:
                        new_grid[y, x] = 1  # Birth
                else:  # Alive
                    if neighbors not in [2, 3]:
                        new_grid[y, x] = 0  # Death
                        
        self.grid = new_grid
        self.generation += 1
    
    def initialize_pattern(self, pattern_name: str, **kwargs):
        """Initialize with a specific pattern"""
        if pattern_name == 'replicator':
            self._create_replicator(**kwargs)
        elif pattern_name == 'random':
            self._create_random(**kwargs)
        elif pattern_name == 'glider':
            self._create_glider(**kwargs)
        else:
            self._create_replicator(**kwargs)
    
    def _create_replicator(self, x: int = None, y: int = None):
        """Create the famous replicator pattern"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2
        
        # Replicator pattern
        replicator = [
            [0, 0, 1, 1, 1],
            [0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 1, 1, 0, 0]
        ]
        
        for dy in range(len(replicator)):
            for dx in range(len(replicator[0])):
                if cy + dy < self.height and cx + dx < self.width:
                    self.grid[cy + dy, cx + dx] = replicator[dy][dx]
    
    def _create_random(self, density: float = 0.3, x: int = None, y: int = None):
        """Random pattern"""
        if x is None or y is None:
            self.grid = (np.random.random((self.height, self.width)) < density).astype(np.int32)
        else:
            size_x = kwargs.get('size_x', self.width // 2)
            size_y = kwargs.get('size_y', self.height // 2)
            for dy in range(size_y):
                for dx in range(size_x):
                    if y + dy < self.height and x + dx < self.width:
                        if np.random.random() < density:
                            self.grid[y + dy, x + dx] = 1
    
    def _create_glider(self, x: int = None, y: int = None):
        """Create a glider"""
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


class HighLifePlugin(PluginInterface):
    """Plugin interface for HighLife"""
    
    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="HighLife",
            description="Life variant with replicators (B36/S23)",
            author="Nathan Thompson",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.MOORE,
            is_totalistic=True,
            supports_mutation=False
        )
    
    @staticmethod
    def create_automaton(width: int, height: int, **kwargs):
        automaton = HighLife(width, height)
        pattern = kwargs.get('pattern', 'replicator')
        automaton.initialize_pattern(pattern, **{k: v for k, v in kwargs.items() if k != 'pattern'})
        return automaton
    
    @staticmethod
    def get_default_patterns():
        return {
            'replicator': {
                'description': 'Famous replicator pattern!',
                'recommended_size': (150, 150)
            },
            'random': {
                'description': 'Random soup',
                'recommended_size': (150, 150),
                'parameters': {'density': 0.3}
            },
            'glider': {
                'description': 'Simple glider',
                'recommended_size': (100, 100)
            }
        }
    
    @staticmethod
    def get_colormap():
        return [
            '#000000',  # 0: Dead - black
            '#00FFFF',  # 1: Alive - cyan
        ]
