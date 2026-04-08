#!/usr/bin/env python3
"""
CALab Comprehensive Diagnostic Test
====================================

Tests all plugins to verify they are working as expected.
Detects common issues like:
- Automata that don't evolve
- Stuck/frozen grids
- No state changes
- Unexpected behavior

Generates detailed report for debugging.

Usage: python diagnose_plugins.py
"""

import sys
import os
from datetime import datetime
sys.path.insert(0, '.')

import numpy as np
from plugins import PLUGIN_REGISTRY, list_plugins


class AutomatonDiagnostic:
    """Diagnostic tests for a single automaton"""
    
    def __init__(self, plugin_name, plugin):
        self.plugin_name = plugin_name
        self.plugin = plugin
        self.results = {
            'plugin_name': plugin_name,
            'tests_passed': [],
            'tests_failed': [],
            'warnings': [],
            'metrics': {},
            'recommendation': ''
        }
    
    def run_all_tests(self):
        """Run complete diagnostic suite"""
        print(f"\n{'='*70}")
        print(f"Diagnosing: {self.plugin_name}")
        print('='*70)
        
        metadata = self.plugin.get_metadata()
        print(f"Name: {metadata.name}")
        print(f"States: {metadata.num_states}")
        print(f"Neighborhood: {metadata.neighborhood_type.value}")
        
        # Test 1: Basic creation
        self._test_creation()
        
        # Test 2: Evolution (does it change?)
        self._test_evolution()
        
        # Test 3: Pattern diversity
        self._test_patterns()
        
        # Test 4: State usage
        self._test_state_usage()
        
        # Test 5: Long-term behavior
        self._test_long_term_behavior()
        
        # Generate recommendation
        self._generate_recommendation()
        
        return self.results
    
    def _test_creation(self):
        """Test basic creation"""
        print("\n[TEST 1: Creation]", end=' ')
        try:
            auto = self.plugin.create_automaton(50, 50)
            if auto.grid.shape == (50, 50):
                print("✓ PASS")
                self.results['tests_passed'].append('creation')
            else:
                print(f"✗ FAIL - Wrong shape: {auto.grid.shape}")
                self.results['tests_failed'].append('creation')
        except Exception as e:
            print(f"✗ FAIL - {e}")
            self.results['tests_failed'].append('creation')
    
    def _test_evolution(self):
        """Test if automaton actually evolves"""
        print("[TEST 2: Evolution]", end=' ')
        
        try:
            auto = self.plugin.create_automaton(100, 100)
            
            # Get initial state
            initial_grid = auto.grid.copy()
            initial_stats = auto.compute_statistics()
            
            # Run 20 steps
            changes_detected = []
            for i in range(20):
                auto.step()
                if not np.array_equal(auto.grid, initial_grid):
                    changes_detected.append(i + 1)
            
            final_grid = auto.grid.copy()
            final_stats = auto.compute_statistics()
            
            # Check if anything changed
            if len(changes_detected) > 0:
                print(f"✓ PASS - Changed on step {changes_detected[0]}")
                self.results['tests_passed'].append('evolution')
                self.results['metrics']['first_change'] = changes_detected[0]
                self.results['metrics']['total_changes'] = len(changes_detected)
            else:
                print("✗ FAIL - No changes detected!")
                self.results['tests_failed'].append('evolution')
                self.results['warnings'].append("Grid never changes - possible bug")
            
            # Check if it's just completely static
            if np.array_equal(initial_grid, final_grid):
                self.results['warnings'].append("Grid completely static over 20 steps")
            
            # Track metrics
            self.results['metrics']['initial_density'] = initial_stats['density']
            self.results['metrics']['final_density'] = final_stats['density']
            self.results['metrics']['density_change'] = final_stats['density'] - initial_stats['density']
            
        except Exception as e:
            print(f"✗ FAIL - {e}")
            self.results['tests_failed'].append('evolution')
    
    def _test_patterns(self):
        """Test different patterns"""
        print("[TEST 3: Pattern Diversity]", end=' ')
        
        try:
            patterns = self.plugin.get_default_patterns()
            
            if len(patterns) == 0:
                print("✗ FAIL - No patterns available")
                self.results['tests_failed'].append('patterns')
                return
            
            # Test each pattern
            pattern_results = {}
            for pattern_name in list(patterns.keys())[:3]:  # Test first 3
                try:
                    auto = self.plugin.create_automaton(50, 50, pattern=pattern_name)
                    stats = auto.compute_statistics()
                    pattern_results[pattern_name] = {
                        'active_cells': stats['active_cells'],
                        'density': stats['density'],
                        'success': True
                    }
                except Exception as e:
                    pattern_results[pattern_name] = {
                        'success': False,
                        'error': str(e)
                    }
            
            success_count = sum(1 for p in pattern_results.values() if p.get('success', False))
            
            if success_count == len(pattern_results):
                print(f"✓ PASS - All {success_count} patterns work")
                self.results['tests_passed'].append('patterns')
            else:
                print(f"⚠ PARTIAL - {success_count}/{len(pattern_results)} patterns work")
                self.results['warnings'].append(f"Some patterns failed: {pattern_results}")
            
            self.results['metrics']['patterns_tested'] = pattern_results
            
        except Exception as e:
            print(f"✗ FAIL - {e}")
            self.results['tests_failed'].append('patterns')
    
    def _test_state_usage(self):
        """Test if all states are actually used"""
        print("[TEST 4: State Usage]", end=' ')
        
        try:
            auto = self.plugin.create_automaton(100, 100)
            metadata = self.plugin.get_metadata()
            
            # Run for a while
            for _ in range(30):
                auto.step()
            
            # Check which states are used
            unique_states = np.unique(auto.grid)
            states_used = len(unique_states)
            total_states = metadata.num_states
            
            usage_percent = (states_used / total_states) * 100
            
            if states_used >= 2:  # At least 2 states used
                print(f"✓ PASS - Using {states_used}/{total_states} states ({usage_percent:.1f}%)")
                self.results['tests_passed'].append('state_usage')
            else:
                print(f"⚠ WARNING - Only {states_used}/{total_states} states used")
                self.results['warnings'].append(f"Low state diversity: {states_used}/{total_states}")
            
            self.results['metrics']['states_used'] = states_used
            self.results['metrics']['total_states'] = total_states
            self.results['metrics']['state_usage_percent'] = usage_percent
            
        except Exception as e:
            print(f"✗ FAIL - {e}")
            self.results['tests_failed'].append('state_usage')
    
    def _test_long_term_behavior(self):
        """Test long-term behavior (100 steps)"""
        print("[TEST 5: Long-term Behavior]", end=' ')
        
        try:
            auto = self.plugin.create_automaton(100, 100)
            
            # Track metrics over time
            densities = []
            entropies = []
            changes = []
            
            prev_grid = auto.grid.copy()
            
            for step in range(100):
                auto.step()
                stats = auto.compute_statistics()
                
                densities.append(stats['density'])
                entropies.append(stats['entropy'])
                
                # Count cells that changed
                changed = np.sum(auto.grid != prev_grid)
                changes.append(changed)
                prev_grid = auto.grid.copy()
            
            # Analyze behavior
            avg_density = np.mean(densities)
            std_density = np.std(densities)
            avg_entropy = np.mean(entropies)
            avg_changes = np.mean(changes)
            
            # Check if it's doing something
            if avg_changes > 10:
                print(f"✓ PASS - Active ({avg_changes:.0f} avg changes/step)")
                self.results['tests_passed'].append('long_term')
            elif avg_changes > 0:
                print(f"⚠ SLOW - Low activity ({avg_changes:.1f} avg changes/step)")
                self.results['warnings'].append(f"Low activity: {avg_changes:.1f} changes/step")
                self.results['tests_passed'].append('long_term')
            else:
                print("✗ FAIL - No activity detected")
                self.results['tests_failed'].append('long_term')
                self.results['warnings'].append("Automaton appears frozen")
            
            # Classify behavior
            if std_density < 0.1 and avg_changes < 1:
                behavior = "STATIC"
            elif std_density > 10:
                behavior = "HIGHLY_VARIABLE"
            elif avg_changes > 1000:
                behavior = "VERY_ACTIVE"
            elif avg_changes > 100:
                behavior = "ACTIVE"
            elif avg_changes > 10:
                behavior = "MODERATE"
            else:
                behavior = "SLOW"
            
            self.results['metrics']['behavior_class'] = behavior
            self.results['metrics']['avg_density'] = avg_density
            self.results['metrics']['std_density'] = std_density
            self.results['metrics']['avg_entropy'] = avg_entropy
            self.results['metrics']['avg_changes_per_step'] = avg_changes
            self.results['metrics']['max_changes'] = max(changes)
            self.results['metrics']['min_changes'] = min(changes)
            
            # Check for convergence
            recent_changes = changes[-10:]
            if all(c == 0 for c in recent_changes):
                self.results['warnings'].append("Converged to static state")
            elif all(c < 1 for c in recent_changes):
                self.results['warnings'].append("Near convergence (very slow)")
            
        except Exception as e:
            print(f"✗ FAIL - {e}")
            self.results['tests_failed'].append('long_term')
    
    def _generate_recommendation(self):
        """Generate overall recommendation"""
        passed = len(self.results['tests_passed'])
        failed = len(self.results['tests_failed'])
        warnings = len(self.results['warnings'])
        
        if failed == 0 and warnings == 0:
            self.results['recommendation'] = "✓ EXCELLENT - Working perfectly"
            self.results['status'] = 'EXCELLENT'
        elif failed == 0 and warnings <= 2:
            self.results['recommendation'] = "✓ GOOD - Minor issues, generally working"
            self.results['status'] = 'GOOD'
        elif failed <= 1:
            self.results['recommendation'] = "⚠ NEEDS ATTENTION - Some issues detected"
            self.results['status'] = 'NEEDS_ATTENTION'
        else:
            self.results['recommendation'] = "✗ BROKEN - Major issues, needs fixes"
            self.results['status'] = 'BROKEN'
        
        print(f"\n{'='*70}")
        print(f"Status: {self.results['recommendation']}")
        print(f"Passed: {passed}/5 tests")
        if warnings > 0:
            print(f"Warnings: {warnings}")
        if failed > 0:
            print(f"Failed: {failed}")


def run_full_diagnostic():
    """Run diagnostic on all plugins"""
    
    print("\n" + "="*70)
    print("CALab Comprehensive Diagnostic Suite")
    print("="*70)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing {len(list_plugins())} plugins...")
    
    all_results = {}
    
    for plugin_name in list_plugins():
        plugin = PLUGIN_REGISTRY[plugin_name]
        
        diagnostic = AutomatonDiagnostic(plugin_name, plugin)
        results = diagnostic.run_all_tests()
        all_results[plugin_name] = results
    
    # Generate summary
    print("\n\n" + "="*70)
    print("DIAGNOSTIC SUMMARY")
    print("="*70)
    
    excellent = []
    good = []
    needs_attention = []
    broken = []
    
    for name, results in all_results.items():
        status = results['status']
        if status == 'EXCELLENT':
            excellent.append(name)
        elif status == 'GOOD':
            good.append(name)
        elif status == 'NEEDS_ATTENTION':
            needs_attention.append(name)
        else:
            broken.append(name)
    
    print(f"\n✓ EXCELLENT ({len(excellent)}):")
    for name in excellent:
        print(f"  • {name}")
    
    if good:
        print(f"\n✓ GOOD ({len(good)}):")
        for name in good:
            print(f"  • {name}")
    
    if needs_attention:
        print(f"\n⚠ NEEDS ATTENTION ({len(needs_attention)}):")
        for name in needs_attention:
            results = all_results[name]
            print(f"  • {name}")
            for warning in results['warnings'][:2]:
                print(f"    - {warning}")
    
    if broken:
        print(f"\n✗ BROKEN ({len(broken)}):")
        for name in broken:
            results = all_results[name]
            print(f"  • {name}")
            for failure in results['tests_failed']:
                print(f"    - Failed: {failure}")
    
    # Detailed metrics
    print("\n" + "="*70)
    print("DETAILED METRICS")
    print("="*70)
    
    for plugin_name, results in all_results.items():
        metrics = results.get('metrics', {})
        if metrics:
            print(f"\n{plugin_name}:")
            
            if 'behavior_class' in metrics:
                print(f"  Behavior: {metrics['behavior_class']}")
            
            if 'avg_changes_per_step' in metrics:
                print(f"  Activity: {metrics['avg_changes_per_step']:.1f} changes/step")
            
            if 'density_change' in metrics:
                print(f"  Density: {metrics['initial_density']:.2f}% → {metrics['final_density']:.2f}%")
            
            if 'state_usage_percent' in metrics:
                print(f"  States: {metrics['states_used']}/{metrics['total_states']} ({metrics['state_usage_percent']:.1f}%)")
    
    # Save to file
    output_file = 'diagnostic_report.txt'
    with open(output_file, 'w') as f:
        f.write("="*70 + "\n")
        f.write("CALab Diagnostic Report\n")
        f.write("="*70 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for plugin_name, results in all_results.items():
            f.write(f"\n{'='*70}\n")
            f.write(f"{plugin_name}\n")
            f.write('='*70 + "\n")
            f.write(f"Status: {results['recommendation']}\n")
            f.write(f"Tests Passed: {results['tests_passed']}\n")
            f.write(f"Tests Failed: {results['tests_failed']}\n")
            f.write(f"Warnings: {results['warnings']}\n")
            f.write(f"Metrics: {results['metrics']}\n")
    
    print(f"\n{'='*70}")
    print(f"Full report saved to: {output_file}")
    print("="*70 + "\n")
    
    return all_results


if __name__ == "__main__":
    try:
        results = run_full_diagnostic()
    except KeyboardInterrupt:
        print("\n\nDiagnostic interrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
