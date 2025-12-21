"""
CALab - Cellular Automata Laboratory
Core Base Classes

This module provides the foundational classes for all cellular automata simulations.
"""

import numpy as np
from typing import Dict, Tuple, List, Optional, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class NeighborhoodType(Enum):
    """Types of cellular automaton neighborhoods"""
    VON_NEUMANN = "von_neumann"  # 4-connected
    MOORE = "moore"  # 8-connected
    HEXAGONAL = "hexagonal"
    CUSTOM = "custom"


@dataclass
class AutomatonMetadata:
    """Metadata for a cellular automaton"""
    name: str
    description: str
    author: str
    version: str
    num_states: int
    neighborhood_type: NeighborhoodType
    is_totalistic: bool = False
    supports_mutation: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'author': self.author,
            'version': self.version,
            'num_states': self.num_states,
            'neighborhood_type': self.neighborhood_type.value,
            'is_totalistic': self.is_totalistic,
            'supports_mutation': self.supports_mutation
        }


class CellularAutomaton(ABC):
    """
    Abstract base class for all cellular automata
    
    This class defines the interface that all automaton implementations must follow.
    It provides common functionality for grid management, stepping, and state tracking.
    """
    
    def __init__(self, width: int, height: int, metadata: AutomatonMetadata):
        """
        Initialize the cellular automaton
        
        Args:
            width: Grid width
            height: Grid height
            metadata: Automaton metadata
        """
        self.width = width
        self.height = height
        self.metadata = metadata
        self.grid = np.zeros((height, width), dtype=np.int32)
        self.generation = 0
        self.history: List[np.ndarray] = []
        self.statistics: Dict[int, Dict[str, Any]] = {}
        
    @abstractmethod
    def step(self) -> None:
        """
        Advance the automaton by one generation
        
        This must be implemented by each specific automaton type.
        """
        pass
    
    @abstractmethod
    def initialize_pattern(self, pattern_name: str, **kwargs) -> None:
        """
        Initialize the grid with a named pattern
        
        Args:
            pattern_name: Name of the pattern to initialize
            **kwargs: Additional pattern-specific parameters
        """
        pass
    
    def reset(self) -> None:
        """Reset the automaton to initial state"""
        self.grid = np.zeros((self.height, self.width), dtype=np.int32)
        self.generation = 0
        self.history.clear()
        self.statistics.clear()
    
    def get_neighborhood(self, x: int, y: int, 
                        neighborhood_type: Optional[NeighborhoodType] = None) -> np.ndarray:
        """
        Get neighborhood of a cell
        
        Args:
            x: X coordinate
            y: Y coordinate
            neighborhood_type: Type of neighborhood (uses automaton's default if None)
            
        Returns:
            Neighborhood array
        """
        if neighborhood_type is None:
            neighborhood_type = self.metadata.neighborhood_type
            
        h, w = self.grid.shape
        
        if neighborhood_type == NeighborhoodType.VON_NEUMANN:
            # Return dict for von Neumann (4-connected)
            return {
                'center': self.grid[y, x],
                'north': self.grid[(y-1) % h, x],
                'south': self.grid[(y+1) % h, x],
                'east': self.grid[y, (x+1) % w],
                'west': self.grid[y, (x-1) % w]
            }
            
        elif neighborhood_type == NeighborhoodType.MOORE:
            # Return 3x3 array for Moore (8-connected)
            neighborhood = np.zeros((3, 3), dtype=np.int32)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    ny, nx = (y + dy) % h, (x + dx) % w
                    neighborhood[dy+1, dx+1] = self.grid[ny, nx]
            return neighborhood
            
        else:
            raise NotImplementedError(f"Neighborhood type {neighborhood_type} not implemented")
    
    def compute_statistics(self) -> Dict[str, Any]:
        """
        Compute current statistics for the automaton
        
        Returns:
            Dictionary of statistics
        """
        unique, counts = np.unique(self.grid, return_counts=True)
        state_counts = dict(zip(unique.tolist(), counts.tolist()))
        
        total_cells = self.grid.size
        active_cells = np.count_nonzero(self.grid)
        density = (active_cells / total_cells) * 100
        
        # Shannon entropy
        probabilities = counts / counts.sum()
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        
        stats = {
            'generation': self.generation,
            'total_cells': total_cells,
            'active_cells': int(active_cells),
            'density': float(density),
            'entropy': float(entropy),
            'state_counts': state_counts,
            'unique_states': len(unique)
        }
        
        self.statistics[self.generation] = stats
        return stats
    
    def save_snapshot(self) -> np.ndarray:
        """Save current grid state to history"""
        snapshot = self.grid.copy()
        self.history.append(snapshot)
        return snapshot
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get complete state information"""
        return {
            'generation': self.generation,
            'grid_shape': self.grid.shape,
            'metadata': self.metadata.to_dict(),
            'statistics': self.compute_statistics()
        }
    
    def set_cell(self, x: int, y: int, state: int) -> None:
        """Set individual cell state"""
        if 0 <= x < self.width and 0 <= y < self.height:
            if 0 <= state < self.metadata.num_states:
                self.grid[y, x] = state
    
    def get_cell(self, x: int, y: int) -> int:
        """Get individual cell state"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return int(self.grid[y, x])
        return 0
    
    def import_grid(self, grid: np.ndarray) -> None:
        """Import a grid from external source"""
        if grid.shape == self.grid.shape:
            self.grid = grid.copy()
        else:
            raise ValueError(f"Grid shape mismatch: expected {self.grid.shape}, got {grid.shape}")
    
    def export_grid(self) -> np.ndarray:
        """Export current grid"""
        return self.grid.copy()


class RuleBasedAutomaton(CellularAutomaton):
    """
    Base class for rule-based cellular automata
    
    This class adds support for rule tables and rule-based transitions.
    """
    
    def __init__(self, width: int, height: int, metadata: AutomatonMetadata):
        super().__init__(width, height, metadata)
        self.rules: Dict[Tuple, int] = {}
        
    def add_rule(self, pattern: Tuple, result: int) -> None:
        """Add a transition rule"""
        self.rules[pattern] = result
    
    def remove_rule(self, pattern: Tuple) -> None:
        """Remove a transition rule"""
        if pattern in self.rules:
            del self.rules[pattern]
    
    def clear_rules(self) -> None:
        """Clear all rules"""
        self.rules.clear()
    
    def get_rules(self) -> Dict[Tuple, int]:
        """Get all rules"""
        return self.rules.copy()
    
    def apply_rule(self, pattern: Tuple) -> Optional[int]:
        """Apply rule for given pattern"""
        return self.rules.get(pattern, None)
    
    def export_rules(self) -> List[Dict[str, Any]]:
        """Export rules to serializable format"""
        return [
            {'pattern': list(pattern), 'result': result}
            for pattern, result in self.rules.items()
        ]
    
    def import_rules(self, rules: List[Dict[str, Any]]) -> None:
        """Import rules from serializable format"""
        self.clear_rules()
        for rule in rules:
            pattern = tuple(rule['pattern'])
            result = rule['result']
            self.add_rule(pattern, result)


class PluginInterface(ABC):
    """
    Interface for automaton plugins
    
    All plugins must implement this interface to be loaded by the system.
    """
    
    @staticmethod
    @abstractmethod
    def get_metadata() -> AutomatonMetadata:
        """Return plugin metadata"""
        pass
    
    @staticmethod
    @abstractmethod
    def create_automaton(width: int, height: int, **kwargs) -> CellularAutomaton:
        """Create an instance of the automaton"""
        pass
    
    @staticmethod
    @abstractmethod
    def get_default_patterns() -> Dict[str, Any]:
        """Return dictionary of default patterns"""
        pass
    
    @staticmethod
    def get_colormap() -> List[str]:
        """Return color scheme for states (default: grayscale)"""
        num_states = PluginInterface.get_metadata().num_states
        from matplotlib import cm
        import matplotlib.pyplot as plt
        cmap = plt.cm.viridis
        colors = [cmap(i / max(1, num_states - 1)) for i in range(num_states)]
        return ['#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255)) 
                for r, g, b, _ in colors]
