#!/usr/bin/env python3
"""
CALab - Complete Plugin Demo
=============================

This script demonstrates ALL available CALab plugins interactively.

Available Automata:
1. Langton's Loop - Self-replicating structures
2. Wire World - Circuit simulation
3. Game of Life - The classic (Conway's)
4. Brian's Brain - Beautiful wave patterns
5. Seeds - Explosive fractal growth

Run with: python demo_all.py
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation

# Add CALab to path
sys.path.insert(0, os.path.dirname(__file__))

from plugins import PLUGIN_REGISTRY, list_plugins
from utils.diagnostics import DiagnosticCollector, AutomatonAnalyzer


class PluginShowcase:
    """Interactive showcase of all CALab plugins"""
    
    def __init__(self):
        self.diagnostics = DiagnosticCollector()
        
    def show_menu(self):
        """Display interactive menu"""
        print("\n" + "=" * 60)
        print("CALab - Cellular Automata Showcase")
        print("=" * 60)
        print("\nAvailable Automata:")
        
        plugins = list_plugins()
        for i, plugin_name in enumerate(plugins, 1):
            plugin = PLUGIN_REGISTRY[plugin_name]
            metadata = plugin.get_metadata()
            print(f"  {i}. {metadata.name}")
            print(f"     {metadata.description}")
        
        print(f"\n  {len(plugins) + 1}. Run All Automata")
        print(f"  {len(plugins) + 2}. Compare Two Automata")
        print("  0. Exit")
        
        return plugins
    
    def demonstrate_automaton(self, plugin, pattern_name=None, num_steps=50):
        """Demonstrate a single automaton"""
        metadata = plugin.get_metadata()
        
        print("\n" + "=" * 60)
        print(f"Demonstrating: {metadata.name}")
        print("=" * 60)
        
        # Get patterns
        patterns = plugin.get_default_patterns()
        
        if pattern_name is None:
            print("\nAvailable patterns:")
            for i, (name, info) in enumerate(patterns.items(), 1):
                print(f"  {i}. {name}: {info.get('description', '')}")
            
            choice = input("\nSelect pattern (1-{}) or Enter for default: ".format(len(patterns)))
            if choice.strip():
                try:
                    idx = int(choice) - 1
                    pattern_name = list(patterns.keys())[idx]
                except:
                    pattern_name = list(patterns.keys())[0]
            else:
                pattern_name = list(patterns.keys())[0]
        
        # Create automaton
        print(f"\nCreating {metadata.name} with pattern '{pattern_name}'...")
        automaton = plugin.create_automaton(150, 150, pattern=pattern_name)
        
        print(f"  Grid size: {automaton.grid.shape}")
        print(f"  States: {metadata.num_states}")
        print(f"  Neighborhood: {metadata.neighborhood_type.value}")
        
        # Get initial statistics
        initial_stats = automaton.compute_statistics()
        print(f"  Initial active cells: {initial_stats['active_cells']}")
        
        # Visualize
        self.visualize_evolution(automaton, plugin, num_steps)
        
        # Analyze
        print("\nBehavior Analysis:")
        analysis = AutomatonAnalyzer.analyze_evolution(automaton, num_steps=50)
        print(f"  Classification: {analysis['classification'].upper()}")
        print(f"  Density change: {analysis['density_change']:+.2f}%")
        print(f"  Final density: {analysis['final_density']:.2f}%")
        
        return automaton
    
    def visualize_evolution(self, automaton, plugin, num_steps=50):
        """Visualize automaton evolution"""
        print(f"\nVisualizing {num_steps} generations...")
        print("(Close window to continue)")
        
        # Setup figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle(f'{automaton.metadata.name} Evolution', 
                    fontsize=14, fontweight='bold')
        
        # Get colormap
        colors = plugin.get_colormap()
        cmap = ListedColormap(colors)
        
        # Main display
        im = ax1.imshow(automaton.grid, cmap=cmap, interpolation='nearest',
                       vmin=0, vmax=automaton.metadata.num_states-1)
        ax1.set_title(f'Generation {automaton.generation}')
        ax1.axis('off')
        
        # Statistics
        generations = []
        densities = []
        entropies = []
        
        ax2.set_xlabel('Generation')
        ax2.set_ylabel('Density (%)', color='tab:blue')
        ax2_twin = ax2.twinx()
        ax2_twin.set_ylabel('Entropy', color='tab:red')
        
        line1, = ax2.plot([], [], 'b-', label='Density', linewidth=2)
        line2, = ax2_twin.plot([], [], 'r-', label='Entropy', linewidth=2)
        
        ax2.legend(loc='upper left')
        ax2_twin.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
        def update(frame):
            if frame > 0:
                automaton.step()
            
            im.set_array(automaton.grid)
            ax1.set_title(f'Generation {automaton.generation}')
            
            stats = automaton.compute_statistics()
            generations.append(automaton.generation)
            densities.append(stats['density'])
            entropies.append(stats['entropy'])
            
            line1.set_data(generations, densities)
            line2.set_data(generations, entropies)
            
            if generations:
                ax2.set_xlim(0, max(generations) + 1)
                ax2.set_ylim(0, max(densities) * 1.1 if max(densities) > 0 else 1)
                ax2_twin.set_ylim(0, max(entropies) * 1.1 if max(entropies) > 0 else 1)
            
            return [im, line1, line2]
        
        anim = FuncAnimation(fig, update, frames=num_steps,
                           interval=100, blit=False, repeat=False)
        
        plt.tight_layout()
        plt.show()
    
    def run_all_automata(self):
        """Run quick demo of all automata"""
        print("\n" + "=" * 60)
        print("Running All Automata Quick Demo")
        print("=" * 60)
        
        for plugin_name in list_plugins():
            plugin = PLUGIN_REGISTRY[plugin_name]
            metadata = plugin.get_metadata()
            
            print(f"\n{metadata.name}:")
            automaton = plugin.create_automaton(100, 100)
            
            for _ in range(20):
                automaton.step()
            
            stats = automaton.compute_statistics()
            print(f"  After 20 steps: {stats['active_cells']} active cells")
            print(f"  Density: {stats['density']:.2f}%")
            print(f"  Entropy: {stats['entropy']:.3f}")
    
    def compare_automata(self):
        """Compare two automata side by side"""
        plugins = list_plugins()
        
        print("\n" + "=" * 60)
        print("Compare Two Automata")
        print("=" * 60)
        
        print("\nSelect first automaton:")
        for i, name in enumerate(plugins, 1):
            print(f"  {i}. {PLUGIN_REGISTRY[name].get_metadata().name}")
        
        choice1 = int(input("Choice: ")) - 1
        plugin1 = PLUGIN_REGISTRY[plugins[choice1]]
        
        print("\nSelect second automaton:")
        for i, name in enumerate(plugins, 1):
            print(f"  {i}. {PLUGIN_REGISTRY[name].get_metadata().name}")
        
        choice2 = int(input("Choice: ")) - 1
        plugin2 = PLUGIN_REGISTRY[plugins[choice2]]
        
        # Create automata
        auto1 = plugin1.create_automaton(100, 100)
        auto2 = plugin2.create_automaton(100, 100)
        
        # Visualize side by side
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))
        fig.suptitle('Automata Comparison', fontsize=16, fontweight='bold')
        
        cmap1 = ListedColormap(plugin1.get_colormap())
        cmap2 = ListedColormap(plugin2.get_colormap())
        
        im1 = ax1.imshow(auto1.grid, cmap=cmap1, interpolation='nearest')
        im2 = ax2.imshow(auto2.grid, cmap=cmap2, interpolation='nearest')
        
        ax1.set_title(auto1.metadata.name)
        ax2.set_title(auto2.metadata.name)
        ax1.axis('off')
        ax2.axis('off')
        
        # Statistics plots
        gens1, dens1 = [], []
        gens2, dens2 = [], []
        
        line1, = ax3.plot([], [], 'b-', label=auto1.metadata.name, linewidth=2)
        line2, = ax3.plot([], [], 'r-', label=auto2.metadata.name, linewidth=2)
        ax3.set_xlabel('Generation')
        ax3.set_ylabel('Density (%)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        line3, = ax4.plot([], [], 'b-', label=auto1.metadata.name, linewidth=2)
        line4, = ax4.plot([], [], 'r-', label=auto2.metadata.name, linewidth=2)
        ax4.set_xlabel('Generation')
        ax4.set_ylabel('Entropy')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        def update(frame):
            if frame > 0:
                auto1.step()
                auto2.step()
            
            im1.set_array(auto1.grid)
            im2.set_array(auto2.grid)
            
            stats1 = auto1.compute_statistics()
            stats2 = auto2.compute_statistics()
            
            gens1.append(auto1.generation)
            dens1.append(stats1['density'])
            gens2.append(auto2.generation)
            dens2.append(stats2['density'])
            
            line1.set_data(gens1, dens1)
            line2.set_data(gens2, dens2)
            
            line3.set_data(gens1, [s['entropy'] for s in [auto1.compute_statistics()]])
            line4.set_data(gens2, [s['entropy'] for s in [auto2.compute_statistics()]])
            
            if gens1:
                max_gen = max(max(gens1), max(gens2))
                ax3.set_xlim(0, max_gen + 1)
                ax4.set_xlim(0, max_gen + 1)
                
                max_dens = max(max(dens1 + dens2), 1)
                ax3.set_ylim(0, max_dens * 1.1)
            
            return [im1, im2, line1, line2, line3, line4]
        
        anim = FuncAnimation(fig, update, frames=50, interval=100, 
                           blit=False, repeat=False)
        
        plt.tight_layout()
        plt.show()
    
    def run(self):
        """Main interactive loop"""
        while True:
            plugins = self.show_menu()
            
            try:
                choice = input("\nEnter choice: ").strip()
                
                if not choice or choice == '0':
                    print("\nExiting. Thanks for using CALab!")
                    break
                
                choice = int(choice)
                
                if 1 <= choice <= len(plugins):
                    plugin_name = plugins[choice - 1]
                    plugin = PLUGIN_REGISTRY[plugin_name]
                    self.demonstrate_automaton(plugin)
                    
                elif choice == len(plugins) + 1:
                    self.run_all_automata()
                    
                elif choice == len(plugins) + 2:
                    self.compare_automata()
                    
                else:
                    print("Invalid choice!")
                    
            except KeyboardInterrupt:
                print("\n\nInterrupted. Exiting...")
                break
            except Exception as e:
                print(f"\nError: {e}")
                import traceback
                traceback.print_exc()


def main():
    """Main entry point"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 12 + "CALab Complete Plugin Showcase" + " " * 16 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    showcase = PluginShowcase()
    showcase.run()


if __name__ == "__main__":
    main()
