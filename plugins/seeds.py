"""
CALab - Seeds Plugin

Seeds (also known as B2/S) is a cellular automaton with explosive growth.
Every cell dies immediately after being born, creating intricate patterns.

States:
0 - Dead
1 - Alive

Rules:
- Dead cell with exactly 2 alive neighbors becomes alive
- All alive cells die in the next generation
"""

import numpy as np
from core.automaton_base import (CellularAutomaton, PluginInterface,
                                AutomatonMetadata, NeighborhoodType)


class Seeds(CellularAutomaton):
    """
    Seeds Cellular Automaton (B2/S)

    An explosive automaton where patterns quickly expand and create
    beautiful fractal-like structures. Every live cell dies immediately,
    making all patterns ephemeral.
    """

    def __init__(self, width: int, height: int):
        metadata = AutomatonMetadata(
            name="Seeds",
            description="Explosive CA with fractal patterns (B2/S)",
            author="Brian Silverman (Implementation: CALab)",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.MOORE,
            is_totalistic=True,
            supports_mutation=False
        )
        super().__init__(width, height, metadata)

    def step(self):
        """Apply Seeds rules (B2/S)"""
        new_grid = np.zeros_like(self.grid)  # All cells die
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

                # Birth only - no survival
                if self.grid[y, x] == 0 and neighbors == 2:
                    new_grid[y, x] = 1

        self.grid = new_grid
        self.generation += 1

    def initialize_pattern(self, pattern_name: str, **kwargs):
        """Initialize with a specific pattern"""
        patterns = {
            'single_cell': self._create_single_cell,
            'line': self._create_line,
            'cross': self._create_cross,
            'random': self._create_random,
            'serviette': self._create_serviette,
            'two_cells': self._create_two_cells
        }

        pattern_func = patterns.get(pattern_name, self._create_single_cell)
        pattern_func(**{k: v for k, v in kwargs.items() if k != 'pattern'})

    def _create_single_cell(self, x: int = None, y: int = None):
        """Create single cell - creates interesting explosion"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2

        if 0 <= cy < self.height and 0 <= cx < self.width:
            self.grid[cy, cx] = 1

    def _create_line(self, x: int = None, y: int = None, length: int = 10):
        """Create horizontal line"""
        cx = x if x is not None else self.width // 2 - length // 2
        cy = y if y is not None else self.height // 2

        for i in range(length):
            if 0 <= cy < self.height and 0 <= cx + i < self.width:
                self.grid[cy, cx + i] = 1

    def _create_cross(self, x: int = None, y: int = None, size: int = 5):
        """Create cross pattern"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2

        # Horizontal
        for i in range(-size, size + 1):
            if 0 <= cy < self.height and 0 <= cx + i < self.width:
                self.grid[cy, cx + i] = 1

        # Vertical
        for i in range(-size, size + 1):
            if 0 <= cy + i < self.height and 0 <= cx < self.width:
                self.grid[cy + i, cx] = 1

    def _create_random(self, density: float = 0.05, x: int = None, y: int = None,
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

    def _create_serviette(self, x: int = None, y: int = None):
        """Create serviette pattern - famous Seeds pattern"""
        cx = x if x is not None else self.width // 2 - 1
        cy = y if y is not None else self.height // 2 - 1

        serviette = [
            [1, 1],
            [1, 1]
        ]

        for dy in range(2):
            for dx in range(2):
                if cy + dy < self.height and cx + dx < self.width:
                    self.grid[cy + dy, cx + dx] = serviette[dy][dx]

    def _create_two_cells(self, x: int = None, y: int = None):
        """Create two adjacent cells"""
        cx = x if x is not None else self.width // 2
        cy = y if y is not None else self.height // 2

        if 0 <= cy < self.height:
            if 0 <= cx < self.width:
                self.grid[cy, cx] = 1
            if 0 <= cx + 1 < self.width:
                self.grid[cy, cx + 1] = 1


class SeedsPlugin(PluginInterface):
    """Plugin interface for Seeds"""

    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="Seeds",
            description="Explosive CA with fractal patterns (B2/S)",
            author="Brian Silverman",
            version="1.0",
            num_states=2,
            neighborhood_type=NeighborhoodType.MOORE,
            is_totalistic=True,
            supports_mutation=False
        )

    @staticmethod
    def create_automaton(width: int, height: int, **kwargs):
        automaton = Seeds(width, height)
        pattern = kwargs.get('pattern', 'serviette')  # Changed from single_cell
        automaton.initialize_pattern(pattern, **{k: v for k, v in kwargs.items() if k != 'pattern'})
        return automaton

    @staticmethod
    def get_default_patterns():
        return {
            'serviette': {
                'description': 'Famous 2x2 pattern (RECOMMENDED)',
                'recommended_size': (150, 150)
            },
            'two_cells': {
                'description': 'Two adjacent cells - explosive!',
                'recommended_size': (150, 150)
            },
            'line': {
                'description': 'Horizontal line explosion',
                'recommended_size': (150, 150),
                'parameters': {'length': 10}
            },
            'cross': {
                'description': 'Cross pattern explosion',
                'recommended_size': (150, 150),
                'parameters': {'size': 5}
            },
            'random': {
                'description': 'Random seed pattern',
                'recommended_size': (150, 150),
                'parameters': {'density': 0.05}
            },
            'single_cell': {
                'description': 'Single cell (dies immediately - demo only)',
                'recommended_size': (150, 150)
            }
        }

    @staticmethod
    def get_colormap():
        return [
            '#000000',  # 0: Dead - black
            '#FFAA00',  # 1: Alive - orange
        ]
