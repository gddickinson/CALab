"""
CALab - Brian's Brain Plugin

Brian's Brain is a beautiful cellular automaton that creates
propagating wave patterns. It's named after Brian Silverman.

States:
0 - Dead (off)
1 - Alive (on)
2 - Dying (refractory)

Rules:
- Dead cell with exactly 2 alive neighbors becomes alive
- Alive cell always becomes dying
- Dying cell always becomes dead
"""

import numpy as np
from core.automaton_base import (CellularAutomaton, PluginInterface, 
                                AutomatonMetadata, NeighborhoodType)


class BriansBrain(CellularAutomaton):
    """
    Brian's Brain Cellular Automaton
    
    Creates beautiful propagating wave patterns with three states.
    Known for its aesthetic appeal and complex emergent behavior.
    """
    
    def __init__(self, width: int, height: int):
        metadata = AutomatonMetadata(
            name="Brian's Brain",
            description="Three-state CA with propagating waves",
            author="Brian Silverman (Implementation: CALab)",
            version="1.0",
            num_states=3,
            neighborhood_type=NeighborhoodType.MOORE,
            is_totalistic=True,
            supports_mutation=False
        )
        super().__init__(width, height, metadata)
        
    def step(self):
        """Apply Brian's Brain rules"""
        new_grid = self.grid.copy()
        h, w = self.grid.shape
        
        for y in range(h):
            for x in range(w):
                current = self.grid[y, x]
                
                # Count alive neighbors (Moore neighborhood)
                alive_neighbors = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0:
                            continue
                        ny, nx = (y + dy) % h, (x + dx) % w
                        if self.grid[ny, nx] == 1:
                            alive_neighbors += 1
                
                # Brian's Brain rules
                if current == 0:  # Dead
                    if alive_neighbors == 2:
                        new_grid[y, x] = 1  # Birth
                elif current == 1:  # Alive
                    new_grid[y, x] = 2  # Always becomes dying
                elif current == 2:  # Dying
                    new_grid[y, x] = 0  # Always dies
                    
        self.grid = new_grid
        self.generation += 1
    
    def initialize_pattern(self, pattern_name: str, **kwargs):
        """Initialize with a specific pattern"""
        patterns = {
            'random': self._create_random,
            'circle': self._create_circle,
            'lines': self._create_lines,
            'cross': self._create_cross,
            'glider': self._create_glider,
            'gun': self._create_gun,
            'spiral': self._create_spiral
        }
        
        pattern_func = patterns.get(pattern_name, self._create_random)
        pattern_func(**{k: v for k, v in kwargs.items() if k != 'pattern'})
    
    def _create_random(self, density: float = 0.1, x: int = None, y: int = None,
                       size_x: int = None, size_y: int = None):
        """Create random pattern"""
        if size_x is None:
            size_x = self.width
        if size_y is None:
            size_y = self.height
        if x is None:
            x = 0
        if y is None:
            y = 0
        
        for dy in range(size_y):
            for dx in range(size_x):
                if y + dy < self.height and x + dx < self.width:
                    if np.random.random() < density:
                        self.grid[y + dy, x + dx] = 1
    
    def _create_circle(self, x: int = None, y: int = None, radius: int = 20):
        """Create circular pattern"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2
        
        for angle in np.linspace(0, 2*np.pi, 60):
            px = int(cx + radius * np.cos(angle))
            py = int(cy + radius * np.sin(angle))
            if 0 <= py < self.height and 0 <= px < self.width:
                self.grid[py, px] = 1
    
    def _create_lines(self, x: int = None, y: int = None, spacing: int = 10):
        """Create parallel lines"""
        x = x if x is not None else 0
        y = y if y is not None else 0
        
        for i in range(0, self.width, spacing):
            for j in range(self.height):
                if 0 <= j < self.height and 0 <= x + i < self.width:
                    self.grid[j, x + i] = 1
    
    def _create_cross(self, x: int = None, y: int = None, size: int = 30):
        """Create cross pattern"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2
        
        # Horizontal line
        for i in range(-size, size + 1):
            if 0 <= cy < self.height and 0 <= cx + i < self.width:
                self.grid[cy, cx + i] = 1
        
        # Vertical line
        for i in range(-size, size + 1):
            if 0 <= cy + i < self.height and 0 <= cx < self.width:
                self.grid[cy + i, cx] = 1
    
    def _create_glider(self, x: int = None, y: int = None):
        """Create a Brian's Brain glider"""
        cx = x if x is not None else self.width // 4
        cy = y if y is not None else self.height // 4
        
        # Brian's Brain glider pattern
        glider = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ]
        
        for dy in range(len(glider)):
            for dx in range(len(glider[0])):
                if cy + dy < self.height and cx + dx < self.width:
                    self.grid[cy + dy, cx + dx] = glider[dy][dx]
    
    def _create_gun(self, x: int = None, y: int = None):
        """Create a pattern that generates waves"""
        cx = x if x is not None else self.width // 4
        cy = y if y is not None else self.height // 4
        
        # Create a source pattern
        for i in range(5):
            for j in range(5):
                if (i + j) % 2 == 0:
                    if cy + i < self.height and cx + j < self.width:
                        self.grid[cy + i, cx + j] = 1
    
    def _create_spiral(self, x: int = None, y: int = None, turns: int = 3):
        """Create spiral pattern"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2
        
        max_radius = min(self.width, self.height) // 4
        points = 200
        
        for i in range(points):
            angle = (i / points) * turns * 2 * np.pi
            radius = (i / points) * max_radius
            px = int(cx + radius * np.cos(angle))
            py = int(cy + radius * np.sin(angle))
            if 0 <= py < self.height and 0 <= px < self.width:
                self.grid[py, px] = 1


class BriansBrainPlugin(PluginInterface):
    """Plugin interface for Brian's Brain"""
    
    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="Brian's Brain",
            description="Three-state CA with beautiful wave patterns",
            author="Brian Silverman",
            version="1.0",
            num_states=3,
            neighborhood_type=NeighborhoodType.MOORE,
            is_totalistic=True,
            supports_mutation=False
        )
    
    @staticmethod
    def create_automaton(width: int, height: int, **kwargs):
        automaton = BriansBrain(width, height)
        pattern = kwargs.get('pattern', 'random')
        automaton.initialize_pattern(pattern, **kwargs)
        return automaton
    
    @staticmethod
    def get_default_patterns():
        return {
            'random': {
                'description': 'Random soup - creates beautiful waves',
                'recommended_size': (150, 150),
                'parameters': {'density': 0.1}
            },
            'circle': {
                'description': 'Expanding circle wave',
                'recommended_size': (150, 150),
                'parameters': {'radius': 20}
            },
            'lines': {
                'description': 'Parallel wave sources',
                'recommended_size': (150, 150),
                'parameters': {'spacing': 10}
            },
            'cross': {
                'description': 'Cross pattern',
                'recommended_size': (150, 150),
                'parameters': {'size': 30}
            },
            'glider': {
                'description': 'Moving pattern',
                'recommended_size': (100, 100)
            },
            'gun': {
                'description': 'Wave generator',
                'recommended_size': (150, 150)
            },
            'spiral': {
                'description': 'Spiral wave source',
                'recommended_size': (150, 150),
                'parameters': {'turns': 3}
            }
        }
    
    @staticmethod
    def get_colormap():
        return [
            '#000000',  # 0: Dead - black
            '#00FF00',  # 1: Alive - green
            '#0000FF',  # 2: Dying - blue
        ]
