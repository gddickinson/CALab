#!/usr/bin/env python3
"""
CALab Plugin Catalog
====================

Browse and explore all available cellular automata plugins.

Usage:
    python list_plugins.py              # Show all plugins
    python list_plugins.py --category   # Browse by category
    python list_plugins.py --info       # Detailed information
"""

import sys
import argparse
sys.path.insert(0, '.')

from plugins import (
    PLUGIN_REGISTRY,
    list_plugins,
    get_plugin,
    list_categories,
    get_plugins_by_category,
    get_plugin_info,
    print_plugin_catalog
)


def show_all_plugins():
    """Show all plugins with basic info"""
    print_plugin_catalog()


def show_by_category():
    """Show plugins organized by category"""
    print("\n" + "="*60)
    print("Plugins by Category")
    print("="*60 + "\n")
    
    for category in list_categories():
        print(f"{category}:")
        plugins = get_plugins_by_category(category)
        
        for plugin_name in plugins:
            plugin = PLUGIN_REGISTRY[plugin_name]
            metadata = plugin.get_metadata()
            patterns = plugin.get_default_patterns()
            
            print(f"  • {plugin_name}")
            print(f"    Name: {metadata.name}")
            print(f"    States: {metadata.num_states}")
            print(f"    Neighborhood: {metadata.neighborhood_type.value}")
            print(f"    Patterns: {', '.join(list(patterns.keys())[:3])}...")
            print()
        
        print()


def show_detailed_info():
    """Show detailed information for all plugins"""
    print("\n" + "="*60)
    print("Detailed Plugin Information")
    print("="*60 + "\n")
    
    for i, plugin_name in enumerate(list_plugins(), 1):
        plugin = PLUGIN_REGISTRY[plugin_name]
        metadata = plugin.get_metadata()
        patterns = plugin.get_default_patterns()
        
        print(f"{i}. {metadata.name}")
        print("-" * 60)
        print(f"ID: {plugin_name}")
        print(f"Description: {metadata.description}")
        print(f"Author: {metadata.author}")
        print(f"Version: {metadata.version}")
        print(f"\nProperties:")
        print(f"  • States: {metadata.num_states}")
        print(f"  • Neighborhood: {metadata.neighborhood_type.value}")
        print(f"  • Totalistic: {'Yes' if metadata.is_totalistic else 'No'}")
        print(f"\nAvailable Patterns ({len(patterns)}):")
        
        for pattern_name, pattern_info in patterns.items():
            desc = pattern_info.get('description', 'No description')
            size = pattern_info.get('recommended_size', (150, 150))
            print(f"  • {pattern_name}")
            print(f"    {desc}")
            print(f"    Recommended size: {size[0]}x{size[1]}")
        
        print("\n")


def show_quick_start():
    """Show quick start examples"""
    print("\n" + "="*60)
    print("Quick Start Examples")
    print("="*60 + "\n")
    
    examples = [
        ('game_of_life', 'glider'),
        ('rule_30', 'single_cell'),
        ('cyclic_ca', 'random'),
        ('wireworld', 'simple_circuit'),
        ('von_neumann', 'simple_reproducer'),
    ]
    
    for plugin_name, pattern in examples:
        plugin = PLUGIN_REGISTRY[plugin_name]
        metadata = plugin.get_metadata()
        
        print(f"{metadata.name}:")
        print(f"  from plugins import get_plugin")
        print(f"  plugin = get_plugin('{plugin_name}')")
        print(f"  auto = plugin.create_automaton(150, 150, pattern='{pattern}')")
        print(f"  for _ in range(50):")
        print(f"      auto.step()")
        print()


def interactive_browser():
    """Interactive plugin browser"""
    print("\n" + "="*60)
    print("Interactive Plugin Browser")
    print("="*60 + "\n")
    
    plugins = list_plugins()
    
    while True:
        print("\nAvailable plugins:")
        for i, name in enumerate(plugins, 1):
            info = get_plugin_info(name)
            print(f"  {i:2}. {name:20} - {info}")
        
        print(f"\n  0. Exit")
        
        try:
            choice = input("\nSelect plugin (0-12): ").strip()
            
            if choice == '0':
                break
            
            idx = int(choice) - 1
            if 0 <= idx < len(plugins):
                plugin_name = plugins[idx]
                plugin = PLUGIN_REGISTRY[plugin_name]
                metadata = plugin.get_metadata()
                patterns = plugin.get_default_patterns()
                
                print("\n" + "-"*60)
                print(f"{metadata.name}")
                print("-"*60)
                print(f"Description: {metadata.description}")
                print(f"States: {metadata.num_states}")
                print(f"Patterns: {len(patterns)}")
                print("\nAvailable patterns:")
                for pname, pinfo in patterns.items():
                    print(f"  • {pname}: {pinfo.get('description', 'No description')}")
                print("-"*60)
                
                input("\nPress Enter to continue...")
            else:
                print("Invalid selection!")
                
        except (ValueError, KeyboardInterrupt):
            break
    
    print("\nGoodbye!")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='CALab Plugin Catalog - Browse cellular automata plugins'
    )
    parser.add_argument(
        '--category', '-c',
        action='store_true',
        help='Show plugins by category'
    )
    parser.add_argument(
        '--info', '-i',
        action='store_true',
        help='Show detailed plugin information'
    )
    parser.add_argument(
        '--examples', '-e',
        action='store_true',
        help='Show quick start examples'
    )
    parser.add_argument(
        '--interactive', '-I',
        action='store_true',
        help='Interactive browser'
    )
    
    args = parser.parse_args()
    
    if args.category:
        show_by_category()
    elif args.info:
        show_detailed_info()
    elif args.examples:
        show_quick_start()
    elif args.interactive:
        interactive_browser()
    else:
        show_all_plugins()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Exiting...")
        sys.exit(0)
