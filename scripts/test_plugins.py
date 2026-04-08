#!/usr/bin/env python3
"""
Quick Plugin Test
=================

Quickly test that all plugins load and work correctly.

Run with: python test_plugins.py
"""

import sys
sys.path.insert(0, '.')

from plugins import PLUGIN_REGISTRY, list_plugins


def test_plugin(plugin_name, plugin):
    """Test a single plugin"""
    print(f"\nTesting: {plugin_name}")
    print("-" * 40)
    
    try:
        # Get metadata
        metadata = plugin.get_metadata()
        print(f"✓ Name: {metadata.name}")
        print(f"✓ States: {metadata.num_states}")
        print(f"✓ Neighborhood: {metadata.neighborhood_type.value}")
        
        # Create automaton
        automaton = plugin.create_automaton(50, 50)
        print(f"✓ Created: {automaton.grid.shape}")
        
        # Run a few steps
        for _ in range(10):
            automaton.step()
        print(f"✓ Ran 10 steps")
        
        # Get statistics
        stats = automaton.compute_statistics()
        print(f"✓ Statistics: {stats['active_cells']} active cells, {stats['density']:.2f}% density")
        
        # Check patterns
        patterns = plugin.get_default_patterns()
        print(f"✓ Patterns: {len(patterns)} available ({', '.join(list(patterns.keys())[:3])}...)")
        
        # Check colormap
        colormap = plugin.get_colormap()
        print(f"✓ Colormap: {len(colormap)} colors")
        
        print(f"✓ {plugin_name} PASSED")
        return True
        
    except Exception as e:
        print(f"✗ {plugin_name} FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Test all plugins"""
    print("=" * 60)
    print("CALab Plugin Test Suite")
    print("=" * 60)
    
    plugins = list_plugins()
    print(f"\nFound {len(plugins)} plugins")
    
    results = {}
    for plugin_name in plugins:
        plugin = PLUGIN_REGISTRY[plugin_name]
        results[plugin_name] = test_plugin(plugin_name, plugin)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nResults: {passed}/{total} plugins passed")
    
    if passed == total:
        print("\n🎉 All plugins working correctly!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} plugin(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
