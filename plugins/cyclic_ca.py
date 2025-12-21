"""
CALab - Cyclic Cellular Automaton Plugin

Beautiful automaton where states cycle: 0→1→2→3→...→N→0
Creates amazing spiral patterns and waves.

Rules:
- A cell takes the next state if one or more neighbors is in the next state
- Creates self-organizing spirals and domains
"""

import numpy as np
from core.automaton_base import (CellularAutomaton, PluginInterface, 
                                AutomatonMetadata, NeighborhoodType)


class CyclicCA(CellularAutomaton):
    """
    Cyclic Cellular Automaton
    
    States cycle through: 0 → 1 → 2 → ... → N → 0
    
    A cell advances to the next state if at least T neighbors
    are in the next state (threshold).
    
    Creates beautiful self-organizing spiral patterns.
    """
    
    def __init__(self, width: int, height: int, num_states: int = 14, threshold: int = 3):
        metadata = AutomatonMetadata(
            name=f"Cyclic CA ({num_states} states)",
            description=f"Self-organizing spirals (threshold={threshold})",
            author="David Griffeath (Implementation: CALab)",
            version="1.0",
            num_states=num_states,
            neighborhood_type=NeighborhoodType.MOORE
        )
        super().__init__(width, height, metadata)
        
        self.num_states_ca = num_states
        self.threshold = threshold
        
    def step(self):
        """Apply cyclic CA rules"""
        new_grid = self.grid.copy()
        h, w = self.grid.shape
        
        for y in range(h):
            for x in range(w):
                current = self.grid[y, x]
                next_state = (current + 1) % self.num_states_ca
                
                # Count neighbors in next state (Moore neighborhood)
                count = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0:
                            continue
                        ny, nx = (y + dy) % h, (x + dx) % w
                        if self.grid[ny, nx] == next_state:
                            count += 1
                
                # Advance if threshold met
                if count >= self.threshold:
                    new_grid[y, x] = next_state
                    
        self.grid = new_grid
        self.generation += 1
    
    def initialize_pattern(self, pattern_name: str, **kwargs):
        """Initialize with a specific pattern"""
        if pattern_name == 'random':
            self._create_random(**kwargs)
        elif pattern_name == 'spiral_seeds':
            self._create_spiral_seeds(**kwargs)
        elif pattern_name == 'domains':
            self._create_domains(**kwargs)
        elif pattern_name == 'gradient':
            self._create_gradient(**kwargs)
        else:
            self._create_random(**kwargs)
    
    def _create_random(self, density: float = 1.0, x: int = None, y: int = None):
        """Random initial state"""
        self.grid = np.random.randint(0, self.num_states_ca, 
                                     size=(self.height, self.width))
    
    def _create_spiral_seeds(self, x: int = None, y: int = None):
        """Create seeds that will form spirals"""
        # Random background
        self.grid = np.random.randint(0, self.num_states_ca, 
                                     size=(self.height, self.width))
        
        # Add some organized regions to seed spirals
        num_seeds = 5
        for _ in range(num_seeds):
            sx = np.random.randint(10, self.width - 10)
            sy = np.random.randint(10, self.height - 10)
            state = np.random.randint(0, self.num_states_ca)
            
            # Create small coherent region
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    if 0 <= sy + dy < self.height and 0 <= sx + dx < self.width:
                        self.grid[sy + dy, sx + dx] = state
    
    def _create_domains(self, x: int = None, y: int = None):
        """Create distinct domains"""
        # Divide grid into regions with different states
        region_size = self.width // 4
        
        for i in range(4):
            for j in range(4):
                y_start = i * region_size
                y_end = min((i + 1) * region_size, self.height)
                x_start = j * region_size
                x_end = min((j + 1) * region_size, self.width)
                
                state = ((i + j) * self.num_states_ca // 4) % self.num_states_ca
                self.grid[y_start:y_end, x_start:x_end] = state
    
    def _create_gradient(self, x: int = None, y: int = None):
        """Create gradient of states"""
        for y in range(self.height):
            state = int((y / self.height) * self.num_states_ca) % self.num_states_ca
            self.grid[y, :] = state


class CyclicCAPlugin(PluginInterface):
    """Plugin interface for Cyclic CA"""
    
    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="Cyclic Cellular Automaton",
            description="Self-organizing spiral patterns",
            author="David Griffeath",
            version="1.0",
            num_states=14,
            neighborhood_type=NeighborhoodType.MOORE,
            is_totalistic=False,
            supports_mutation=False
        )
    
    @staticmethod
    def create_automaton(width: int, height: int, **kwargs):
        num_states = kwargs.get('num_states', 14)
        threshold = kwargs.get('threshold', 3)
        automaton = CyclicCA(width, height, num_states, threshold)
        pattern = kwargs.get('pattern', 'random')
        automaton.initialize_pattern(pattern, **{k: v for k, v in kwargs.items() 
                                                 if k not in ['pattern', 'num_states', 'threshold']})
        return automaton
    
    @staticmethod
    def get_default_patterns():
        return {
            'random': {
                'description': 'Random initialization (forms spirals)',
                'recommended_size': (150, 150),
                'parameters': {'num_states': 14, 'threshold': 3}
            },
            'spiral_seeds': {
                'description': 'Seeds for spiral formation',
                'recommended_size': (150, 150),
                'parameters': {'num_states': 14, 'threshold': 3}
            },
            'domains': {
                'description': 'Distinct color domains',
                'recommended_size': (150, 150),
                'parameters': {'num_states': 16, 'threshold': 2}
            },
            'gradient': {
                'description': 'Gradient pattern',
                'recommended_size': (150, 150),
                'parameters': {'num_states': 12, 'threshold': 4}
            }
        }
    
    @staticmethod
    def get_colormap():
        """Generate rainbow colormap for cyclic states"""
        # Create smooth color transitions
        import colorsys
        colors = []
        
        # Generate 20 colors in HSV space (full rainbow)
        for i in range(20):
            hue = i / 20.0
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb[0] * 255),
                int(rgb[1] * 255),
                int(rgb[2] * 255)
            )
            colors.append(hex_color)
        
        return colors
