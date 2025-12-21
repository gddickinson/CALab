#!/usr/bin/env python3
"""
CALab - Core Demonstration
==========================

This script demonstrates the CALab framework without requiring the GUI.
Perfect for:
- Testing the core modules
- Understanding the architecture
- Running batch simulations
- Generating diagnostics

Run with: python demo.py
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation

# Add CALab to path
sys.path.insert(0, os.path.dirname(__file__))

from core.automaton_base import NeighborhoodType
from plugins.langton_loop import LangtonLoopPlugin
from core.simulator import SimulationEngine
from utils.diagnostics import DiagnosticCollector, AutomatonAnalyzer


class CALabDemo:
    """Simple demonstration of CALab framework"""
    
    def __init__(self):
        self.diagnostics = DiagnosticCollector()
        
    def test_langton_loop(self):
        """Test the Langton Loop implementation"""
        print("=" * 60)
        print("Testing Langton's Loop")
        print("=" * 60)
        
        # Create automaton
        print("\n1. Creating Langton Loop automaton...")
        automaton = LangtonLoopPlugin.create_automaton(100, 100)
        print(f"   ✓ Created {automaton.metadata.name}")
        print(f"   Grid size: {automaton.grid.shape}")
        print(f"   Number of states: {automaton.metadata.num_states}")
        print(f"   Number of rules: {len(automaton.rules)}")
        
        # Test stepping
        print("\n2. Testing simulation steps...")
        initial_stats = automaton.compute_statistics()
        print(f"   Initial active cells: {initial_stats['active_cells']}")
        
        for i in range(10):
            automaton.step()
        
        stats_after_10 = automaton.compute_statistics()
        print(f"   After 10 steps: {stats_after_10['active_cells']} active cells")
        print(f"   Density: {stats_after_10['density']:.2f}%")
        
        # Capture diagnostic snapshot
        self.diagnostics.capture_automaton_state(automaton, "after_10_steps")
        
        print("\n3. ✓ Langton Loop test complete")
        return automaton
    
    def visualize_automaton(self, automaton, num_steps=50):
        """Create visualization of automaton evolution"""
        print("\n" + "=" * 60)
        print("Visualizing Automaton Evolution")
        print("=" * 60)
        
        print(f"\nRunning {num_steps} steps and creating visualization...")
        
        # Setup figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle(f'{automaton.metadata.name} Evolution', fontsize=14, fontweight='bold')
        
        # Get colormap
        colors = LangtonLoopPlugin.get_colormap()
        cmap = ListedColormap(colors)
        
        # Main display
        im = ax1.imshow(automaton.grid, cmap=cmap, interpolation='nearest',
                       vmin=0, vmax=automaton.metadata.num_states-1)
        ax1.set_title(f'Generation {automaton.generation}')
        ax1.axis('off')
        
        # Statistics plot
        generations = []
        densities = []
        entropies = []
        
        ax2.set_xlabel('Generation')
        ax2.set_ylabel('Density (%)', color='tab:blue')
        ax2_twin = ax2.twinx()
        ax2_twin.set_ylabel('Entropy', color='tab:red')
        
        line1, = ax2.plot([], [], 'b-', label='Density')
        line2, = ax2_twin.plot([], [], 'r-', label='Entropy')
        
        ax2.legend(loc='upper left')
        ax2_twin.legend(loc='upper right')
        
        # Animation update function
        def update(frame):
            if frame > 0:
                automaton.step()
            
            # Update grid display
            im.set_array(automaton.grid)
            ax1.set_title(f'Generation {automaton.generation}')
            
            # Update statistics
            stats = automaton.compute_statistics()
            generations.append(automaton.generation)
            densities.append(stats['density'])
            entropies.append(stats['entropy'])
            
            line1.set_data(generations, densities)
            line2.set_data(generations, entropies)
            
            if generations:
                ax2.set_xlim(0, max(generations) + 1)
                ax2.set_ylim(0, max(densities) * 1.1 if densities else 1)
                ax2_twin.set_ylim(0, max(entropies) * 1.1 if entropies else 1)
            
            return [im, line1, line2]
        
        # Create animation
        anim = FuncAnimation(fig, update, frames=num_steps,
                           interval=100, blit=False, repeat=False)
        
        print("✓ Visualization ready. Close window to continue...")
        plt.tight_layout()
        plt.show()
        
        print(f"\nFinal statistics:")
        print(f"  Generation: {automaton.generation}")
        print(f"  Density: {densities[-1]:.2f}%")
        print(f"  Entropy: {entropies[-1]:.3f}")
    
    def analyze_automaton(self, automaton):
        """Perform detailed analysis"""
        print("\n" + "=" * 60)
        print("Analyzing Automaton Behavior")
        print("=" * 60)
        
        print("\nRunning analysis (this may take a moment)...")
        analysis = AutomatonAnalyzer.analyze_evolution(automaton, num_steps=100)
        
        print("\nAnalysis Results:")
        print(f"  Behavior Classification: {analysis['classification'].upper()}")
        print(f"  Density Change: {analysis['density_change']:+.2f}%")
        print(f"  Average Density: {analysis['avg_density']:.2f}%")
        print(f"  Density Std Dev: {analysis['density_std']:.2f}")
        print(f"  Entropy Change: {analysis['entropy_change']:+.3f}")
        
        return analysis
    
    def export_diagnostics(self):
        """Export diagnostic report"""
        print("\n" + "=" * 60)
        print("Exporting Diagnostics")
        print("=" * 60)
        
        filename = "data/diagnostics/demo_diagnostics.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        self.diagnostics.export_report(filename)
        print(f"\n✓ Diagnostics exported to: {filename}")
        print("\nReport Summary:")
        print(self.diagnostics.get_summary())
    
    def run_full_demo(self):
        """Run complete demonstration"""
        print("\n")
        print("╔" + "=" * 58 + "╗")
        print("║" + " " * 15 + "CALab Framework Demo" + " " * 23 + "║")
        print("╚" + "=" * 58 + "╝")
        print()
        
        try:
            # Test Langton Loop
            automaton = self.test_langton_loop()
            
            # Visualize
            print("\nPress Enter to visualize automaton evolution...")
            input()
            self.visualize_automaton(automaton, num_steps=50)
            
            # Analyze
            print("\nPress Enter to run behavior analysis...")
            input()
            self.analyze_automaton(automaton)
            
            # Export diagnostics
            self.export_diagnostics()
            
            print("\n" + "=" * 60)
            print("Demo Complete!")
            print("=" * 60)
            print("\nNext steps:")
            print("  1. Review diagnostics in data/diagnostics/")
            print("  2. Run 'python main.py' to use the full GUI")
            print("  3. Check tests/ directory for unit tests")
            print("  4. Read README.md for detailed documentation")
            
        except Exception as e:
            print(f"\n✗ Error occurred: {e}")
            import traceback
            traceback.print_exc()
            self.diagnostics.log_error(e, context="demo_execution")
            self.export_diagnostics()
            print("\nDiagnostics exported for debugging.")


def main():
    """Main entry point"""
    demo = CALabDemo()
    demo.run_full_demo()


if __name__ == "__main__":
    main()
