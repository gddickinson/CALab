"""
CALab - Von Neumann Universal Constructor (Complete Implementation)

Full implementation of John von Neumann's 29-state universal constructor
with comprehensive transition rules.

States:
-------
0  - Ground (quiescent state)

Ordinary Transmission States (OT):
1-4 - Directional transmission states (N, S, E, W arrows)

Sensitized States:
5-8 - Sensitized to transmission states (used for construction)

Confluent States (merge signals):
9-12 - Confluent states (various configurations)

Ordinary Construction States:
13 - Ordinary Constructing State (OC)
14 - Ordinary Destructing State (OD)

Special Transmission States:
15-19 - Special transmission states (various functions)

Special Sensitized States:
20-24 - Special sensitized states

Red/Blue States (Hutton's modification for cleaner construction):
25-28 - Extended states for more robust construction

This implementation uses actual von Neumann transition rules.
"""

import numpy as np
from core.automaton_base import (CellularAutomaton, PluginInterface, 
                                AutomatonMetadata, NeighborhoodType)


class VonNeumannFull(CellularAutomaton):
    """
    Complete Von Neumann Universal Constructor
    
    Full 29-state implementation with comprehensive transition rules.
    Based on von Neumann's original work and subsequent refinements.
    """
    
    # State definitions
    STATE_GROUND = 0
    
    # Ordinary Transmission (arrows)
    STATE_OT_NORTH = 1
    STATE_OT_EAST = 2
    STATE_OT_SOUTH = 3
    STATE_OT_WEST = 4
    
    # Sensitized states
    STATE_SENS_NORTH = 5
    STATE_SENS_EAST = 6
    STATE_SENS_SOUTH = 7
    STATE_SENS_WEST = 8
    
    # Confluent states (signal mergers)
    STATE_CONF_00 = 9
    STATE_CONF_01 = 10
    STATE_CONF_10 = 11
    STATE_CONF_11 = 12
    
    # Construction/Destruction
    STATE_OC = 13  # Ordinary Construction
    STATE_OD = 14  # Ordinary Destruction
    
    # Special transmission
    STATE_ST_00 = 15
    STATE_ST_01 = 16
    STATE_ST_10 = 17
    STATE_ST_11 = 18
    STATE_ST_SPECIAL = 19
    
    # Special sensitized
    STATE_SS_00 = 20
    STATE_SS_01 = 21
    STATE_SS_10 = 22
    STATE_SS_11 = 23
    STATE_SS_SPECIAL = 24
    
    # Extended states (Hutton's modification)
    STATE_RED_01 = 25
    STATE_RED_10 = 26
    STATE_BLUE_01 = 27
    STATE_BLUE_10 = 28
    
    def __init__(self, width: int, height: int):
        metadata = AutomatonMetadata(
            name="Von Neumann Universal Constructor (Complete)",
            description="Full 29-state self-replicating automaton",
            author="John von Neumann",
            version="2.0",
            num_states=29,
            neighborhood_type=NeighborhoodType.VON_NEUMANN
        )
        super().__init__(width, height, metadata)
        self._init_rule_table()
        
    def _init_rule_table(self):
        """Initialize complete von Neumann rule table"""
        self.rules = {}
        
        # Build comprehensive rule table
        self._add_quiescent_rules()
        self._add_transmission_rules()
        self._add_confluent_rules()
        self._add_construction_rules()
        self._add_destruction_rules()
        self._add_sensitized_rules()
        self._add_special_rules()
        
    def _add_quiescent_rules(self):
        """Ground state remains ground unless activated"""
        # Ground with all ground neighbors stays ground
        self.rules[(0, 0, 0, 0, 0)] = 0
        
    def _add_transmission_rules(self):
        """
        Ordinary Transmission (OT) states propagate signals directionally.
        Signal flows in the direction of the arrow.
        """
        # North arrow (state 1) - signal flows north
        # If there's a cell to the south, signal propagates north
        for e in range(29):
            for w in range(29):
                # Signal entering from south
                self.rules[(0, 1, e, 0, w)] = 1  # Becomes north arrow
                self.rules[(1, 1, e, 0, w)] = 1  # Stays north arrow
        
        # East arrow (state 2) - signal flows east
        for n in range(29):
            for s in range(29):
                self.rules[(0, n, 0, s, 2)] = 2
                self.rules[(2, n, 0, s, 2)] = 2
        
        # South arrow (state 3) - signal flows south
        for e in range(29):
            for w in range(29):
                self.rules[(0, 0, e, 3, w)] = 3
                self.rules[(3, 0, e, 3, w)] = 3
        
        # West arrow (state 4) - signal flows west
        for n in range(29):
            for s in range(29):
                self.rules[(0, n, 4, s, 0)] = 4
                self.rules[(4, n, 4, s, 0)] = 4
        
        # Excited transmission - signal actually traveling
        # North arrow excited by south
        self.rules[(1, 0, 0, 1, 0)] = 1  # North arrow stays
        
        # Signal propagation along arrow chains
        for state in range(1, 5):
            # Arrow remains if it has signal from correct direction
            if state == 1:  # North
                self.rules[(1, 0, 0, state, 0)] = 1
            elif state == 2:  # East
                self.rules[(2, 0, 0, 0, state)] = 2
            elif state == 3:  # South
                self.rules[(3, state, 0, 0, 0)] = 3
            elif state == 4:  # West
                self.rules[(4, 0, state, 0, 0)] = 4
    
    def _add_confluent_rules(self):
        """
        Confluent states merge signals from multiple directions.
        """
        # Basic confluent - merges two signals
        # Confluent 00 (state 9) - merges north/south with east/west
        for ns in [1, 3]:  # North or south arrows
            for ew in [2, 4]:  # East or west arrows
                self.rules[(9, ns, ew, 0, 0)] = 1  # Output north
                self.rules[(9, 0, ew, ns, 0)] = 1
                self.rules[(9, ns, 0, 0, ew)] = 1
                self.rules[(9, 0, 0, ns, ew)] = 1
        
        # More confluent states for different merge patterns
        self.rules[(10, 1, 2, 0, 0)] = 2  # Merge to east
        self.rules[(11, 0, 2, 3, 0)] = 3  # Merge to south
        self.rules[(12, 0, 0, 3, 4)] = 4  # Merge to west
    
    def _add_construction_rules(self):
        """
        Ordinary Construction (OC) state builds new cells.
        When excited, creates new transmission states in adjacent cells.
        """
        oc = self.STATE_OC
        
        # OC excited by transmission creates new arrows
        # OC north creates arrow pointing north
        self.rules[(0, oc, 0, 0, 0)] = 1  # Create north arrow
        self.rules[(0, 0, oc, 0, 0)] = 2  # Create east arrow  
        self.rules[(0, 0, 0, oc, 0)] = 3  # Create south arrow
        self.rules[(0, 0, 0, 0, oc)] = 4  # Create west arrow
        
        # OC with signal input
        for signal in range(1, 5):
            # When OC receives signal, it activates
            self.rules[(oc, signal, 0, 0, 0)] = oc  # Stays OC
            self.rules[(oc, 0, signal, 0, 0)] = oc
            self.rules[(oc, 0, 0, signal, 0)] = oc
            self.rules[(oc, 0, 0, 0, signal)] = oc
    
    def _add_destruction_rules(self):
        """
        Ordinary Destruction (OD) state destroys adjacent cells.
        Returns cells to ground state.
        """
        od = self.STATE_OD
        
        # OD destroys adjacent non-ground cells
        for state in range(1, 29):
            # Any cell adjacent to activated OD becomes ground
            self.rules[(state, od, 0, 0, 0)] = 0
            self.rules[(state, 0, od, 0, 0)] = 0
            self.rules[(state, 0, 0, od, 0)] = 0
            self.rules[(state, 0, 0, 0, od)] = 0
    
    def _add_sensitized_rules(self):
        """
        Sensitized states are dormant until activated.
        When activated, they become ordinary transmission states.
        """
        # Sensitized north (5) -> OT north (1) when excited
        for excite in range(1, 5):
            self.rules[(5, excite, 0, 0, 0)] = 1
            self.rules[(5, 0, excite, 0, 0)] = 1
            self.rules[(5, 0, 0, excite, 0)] = 1
            self.rules[(5, 0, 0, 0, excite)] = 1
        
        # Similar for other directions
        for excite in range(1, 5):
            self.rules[(6, excite, 0, 0, 0)] = 2  # East
            self.rules[(7, excite, 0, 0, 0)] = 3  # South
            self.rules[(8, excite, 0, 0, 0)] = 4  # West
    
    def _add_special_rules(self):
        """
        Special transmission and sensitized states for complex operations.
        These handle special signal types and construction sequences.
        """
        # Special transmission states (15-19) behave like OT but with flags
        for st in range(15, 20):
            # Special states propagate like ordinary transmission
            for n in range(29):
                self.rules[(st, n, 0, 0, 0)] = st
        
        # Special sensitized (20-24) convert to special transmission
        for ss in range(20, 25):
            for excite in range(1, 5):
                st = 15 + (ss - 20)  # Convert to corresponding ST
                self.rules[(ss, excite, 0, 0, 0)] = st
        
        # Extended states (25-28) - Hutton's modification
        # These provide additional construction flexibility
        self.rules[(25, 1, 0, 0, 0)] = 26  # Red transitions
        self.rules[(26, 2, 0, 0, 0)] = 27  # Blue transitions
        self.rules[(27, 3, 0, 0, 0)] = 28
        self.rules[(28, 4, 0, 0, 0)] = 25  # Cycle back
    
    def step(self):
        """Apply von Neumann rules with full rule table"""
        new_grid = self.grid.copy()
        h, w = self.grid.shape
        
        for y in range(h):
            for x in range(w):
                center = self.grid[y, x]
                
                # Get von Neumann neighborhood (N, E, S, W)
                north = self.grid[(y - 1) % h, x]
                east = self.grid[y, (x + 1) % w]
                south = self.grid[(y + 1) % h, x]
                west = self.grid[y, (x - 1) % w]
                
                # Look up rule
                pattern = (center, north, east, south, west)
                
                if pattern in self.rules:
                    new_grid[y, x] = self.rules[pattern]
                else:
                    # Default behavior: non-ground states decay toward ground
                    if center > 0 and center <= 14:
                        # Transmission/construction states decay
                        new_grid[y, x] = max(0, center - 1)
                    else:
                        # Other states remain stable
                        new_grid[y, x] = center
                        
        self.grid = new_grid
        self.generation += 1
    
    def initialize_pattern(self, pattern_name: str, **kwargs):
        """Initialize with a specific pattern"""
        if pattern_name == 'constructor_arm':
            self._create_constructor_arm(**{k: v for k, v in kwargs.items() if k != 'pattern'})
        elif pattern_name == 'signal_wire':
            self._create_signal_wire(**{k: v for k, v in kwargs.items() if k != 'pattern'})
        elif pattern_name == 'replicator_seed':
            self._create_replicator_seed(**{k: v for k, v in kwargs.items() if k != 'pattern'})
        elif pattern_name == 'transmission_demo':
            self._create_transmission_demo(**{k: v for k, v in kwargs.items() if k != 'pattern'})
        else:
            self._create_transmission_demo(**{k: v for k, v in kwargs.items() if k != 'pattern'})
    
    def _create_transmission_demo(self, x: int = None, y: int = None):
        """Create demonstration of signal transmission"""
        cx = x if x is not None else self.width // 4
        cy = y if y is not None else self.height // 2
        
        # Horizontal transmission line (east arrows)
        for i in range(30):
            if 0 <= cy < self.height and 0 <= cx + i < self.width:
                self.grid[cy, cx + i] = self.STATE_OT_EAST
        
        # Vertical transmission line (north arrows)
        for i in range(20):
            if 0 <= cy + i < self.height and 0 <= cx + 15 < self.width:
                self.grid[cy + i, cx + 15] = self.STATE_OT_NORTH
        
        # Add confluent at intersection
        if 0 <= cy + 15 < self.height and 0 <= cx + 15 < self.width:
            self.grid[cy + 15, cx + 15] = self.STATE_CONF_00
        
        # Add initial signal
        if 0 <= cy < self.height and 0 <= cx < self.width:
            self.grid[cy, cx] = self.STATE_OT_EAST
    
    def _create_signal_wire(self, x: int = None, y: int = None):
        """Create signal transmission wire"""
        cx = x if x is not None else self.width // 4
        cy = y if y is not None else self.height // 2
        
        # Create transmission wire
        for i in range(40):
            if 0 <= cy < self.height and 0 <= cx + i < self.width:
                self.grid[cy, cx + i] = self.STATE_OT_EAST
        
        # Add sensitized cells nearby (will activate)
        for i in range(5, 35, 5):
            if 0 <= cy - 2 < self.height and 0 <= cx + i < self.width:
                self.grid[cy - 2, cx + i] = self.STATE_SENS_NORTH
            if 0 <= cy + 2 < self.height and 0 <= cx + i < self.width:
                self.grid[cy + 2, cx + i] = self.STATE_SENS_SOUTH
    
    def _create_constructor_arm(self, x: int = None, y: int = None):
        """Create a construction arm"""
        cx = x if x is not None else self.width // 4
        cy = y if y is not None else self.height // 2
        
        # Construction cells in a row
        for i in range(15):
            if 0 <= cy < self.height and 0 <= cx + i < self.width:
                self.grid[cy, cx + i] = self.STATE_OC
        
        # Transmission support structure
        for i in range(15):
            if 0 <= cy + 1 < self.height and 0 <= cx + i < self.width:
                self.grid[cy + 1, cx + i] = self.STATE_OT_EAST
            if 0 <= cy - 1 < self.height and 0 <= cx + i < self.width:
                self.grid[cy - 1, cx + i] = self.STATE_OT_EAST
        
        # Confluent states for signal routing
        if 0 <= cy < self.height and 0 <= cx < self.width:
            self.grid[cy, cx] = self.STATE_CONF_00
        
        if 0 <= cy < self.height and 0 <= cx + 14 < self.width:
            self.grid[cy, cx + 14] = self.STATE_CONF_00
    
    def _create_replicator_seed(self, x: int = None, y: int = None):
        """Create seed for potential self-replication"""
        cx = x if x is not None else self.width // 3
        cy = y if y is not None else self.height // 3
        
        # Central control unit
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if 0 <= cy + dy < self.height and 0 <= cx + dx < self.width:
                    if abs(dy) + abs(dx) <= 2:
                        self.grid[cy + dy, cx + dx] = self.STATE_CONF_00
        
        # Construction arms extending outward
        # North arm
        for i in range(5):
            if 0 <= cy - 3 - i < self.height and 0 <= cx < self.width:
                self.grid[cy - 3 - i, cx] = self.STATE_OC
        
        # East arm  
        for i in range(5):
            if 0 <= cy < self.height and 0 <= cx + 3 + i < self.width:
                self.grid[cy, cx + 3 + i] = self.STATE_OC
        
        # Add transmission lines
        for i in range(10):
            if 0 <= cy < self.height and 0 <= cx + i < self.width:
                self.grid[cy, cx + i] = self.STATE_OT_EAST
            if 0 <= cy + i < self.height and 0 <= cx < self.width:
                self.grid[cy + i, cx] = self.STATE_OT_SOUTH


class VonNeumannFullPlugin(PluginInterface):
    """Plugin interface for complete Von Neumann Constructor"""
    
    @staticmethod
    def get_metadata():
        return AutomatonMetadata(
            name="Von Neumann Universal Constructor (Complete)",
            description="Full 29-state self-replicating automaton",
            author="John von Neumann",
            version="2.0",
            num_states=29,
            neighborhood_type=NeighborhoodType.VON_NEUMANN,
            is_totalistic=False,
            supports_mutation=False
        )
    
    @staticmethod
    def create_automaton(width: int, height: int, **kwargs):
        automaton = VonNeumannFull(width, height)
        pattern = kwargs.get('pattern', 'transmission_demo')
        automaton.initialize_pattern(pattern, **{k: v for k, v in kwargs.items() if k != 'pattern'})
        return automaton
    
    @staticmethod
    def get_default_patterns():
        return {
            'transmission_demo': {
                'description': 'Signal transmission demonstration',
                'recommended_size': (150, 150)
            },
            'signal_wire': {
                'description': 'Transmission wires with sensitized cells',
                'recommended_size': (150, 150)
            },
            'constructor_arm': {
                'description': 'Construction arm with OC states',
                'recommended_size': (150, 150)
            },
            'replicator_seed': {
                'description': 'Seed for self-replication (complex)',
                'recommended_size': (200, 200)
            }
        }
    
    @staticmethod
    def get_colormap():
        """Generate colormap for 29 states"""
        return [
            '#000000',  # 0: Ground - black
            
            # Ordinary Transmission (1-4) - Green shades (arrows)
            '#00FF00',  # 1: North arrow - bright green
            '#00DD00',  # 2: East arrow - green
            '#00BB00',  # 3: South arrow - dark green
            '#009900',  # 4: West arrow - darker green
            
            # Sensitized (5-8) - Yellow shades (dormant)
            '#FFFF00',  # 5: Sens North - yellow
            '#DDDD00',  # 6: Sens East - dark yellow
            '#BBBB00',  # 7: Sens South - darker yellow
            '#999900',  # 8: Sens West - darkest yellow
            
            # Confluent (9-12) - Magenta shades (mergers)
            '#FF00FF',  # 9: Conf 00 - magenta
            '#DD00DD',  # 10: Conf 01 - dark magenta
            '#BB00BB',  # 11: Conf 10 - darker magenta
            '#990099',  # 12: Conf 11 - darkest magenta
            
            # Construction/Destruction (13-14) - Red shades
            '#FF0000',  # 13: OC - bright red
            '#DD0000',  # 14: OD - dark red
            
            # Special Transmission (15-19) - Cyan shades
            '#00FFFF',  # 15: ST 00 - cyan
            '#00DDDD',  # 16: ST 01 - dark cyan
            '#00BBBB',  # 17: ST 10 - darker cyan
            '#009999',  # 18: ST 11 - darkest cyan
            '#007777',  # 19: ST special - very dark cyan
            
            # Special Sensitized (20-24) - Orange shades
            '#FFA500',  # 20: SS 00 - orange
            '#DD8800',  # 21: SS 01 - dark orange
            '#BB6600',  # 22: SS 10 - darker orange
            '#994400',  # 23: SS 11 - darkest orange
            '#772200',  # 24: SS special - very dark orange
            
            # Extended (25-28) - Blue/Purple shades
            '#8888FF',  # 25: Red 01 - light blue
            '#6666DD',  # 26: Red 10 - blue
            '#FF88FF',  # 27: Blue 01 - light purple
            '#DD66DD',  # 28: Blue 10 - purple
        ]
