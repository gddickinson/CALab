"""
CALab - Diagnostics System
Comprehensive diagnostics collection and analysis
"""

import numpy as np
from typing import Dict, List, Any, Optional
import json
import traceback
from datetime import datetime
import sys
import platform


class DiagnosticCollector:
    """
    Collects comprehensive diagnostic information for debugging
    and analysis
    """
    
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.performance_metrics: List[Dict[str, Any]] = []
        self.automaton_snapshots: List[Dict[str, Any]] = []
        
    def log_event(self, event_type: str, message: str, **kwargs) -> None:
        """Log an event"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'message': message,
            **kwargs
        }
        self.logs.append(entry)
    
    def log_error(self, error: Exception, context: Optional[str] = None) -> None:
        """Log an error with full traceback"""
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context
        }
        self.errors.append(error_info)
    
    def log_performance(self, operation: str, duration_ms: float, **kwargs) -> None:
        """Log performance metrics"""
        metric = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'duration_ms': duration_ms,
            **kwargs
        }
        self.performance_metrics.append(metric)
    
    def capture_automaton_state(self, automaton, label: str = "snapshot") -> None:
        """Capture complete automaton state"""
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'label': label,
            'generation': automaton.generation,
            'grid_shape': automaton.grid.shape,
            'statistics': automaton.compute_statistics(),
            'metadata': automaton.metadata.to_dict(),
            'grid_sample': self._get_grid_sample(automaton.grid)
        }
        self.automaton_snapshots.append(snapshot)
    
    def _get_grid_sample(self, grid: np.ndarray, sample_size: int = 20) -> List[List[int]]:
        """Get a sample of the grid (center region)"""
        h, w = grid.shape
        cy, cx = h // 2, w // 2
        half_size = sample_size // 2
        
        y_start = max(0, cy - half_size)
        y_end = min(h, cy + half_size)
        x_start = max(0, cx - half_size)
        x_end = min(w, cx + half_size)
        
        sample = grid[y_start:y_end, x_start:x_end]
        return sample.tolist()
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            'platform': platform.platform(),
            'python_version': sys.version,
            'numpy_version': np.__version__,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate complete diagnostic report"""
        return {
            'system_info': self.get_system_info(),
            'summary': {
                'total_logs': len(self.logs),
                'total_errors': len(self.errors),
                'total_performance_metrics': len(self.performance_metrics),
                'total_snapshots': len(self.automaton_snapshots)
            },
            'logs': self.logs,
            'errors': self.errors,
            'performance_metrics': self.performance_metrics,
            'automaton_snapshots': self.automaton_snapshots
        }
    
    def export_report(self, filename: str) -> None:
        """Export diagnostic report to JSON file"""
        report = self.generate_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
    
    def get_summary(self) -> str:
        """Get human-readable summary"""
        report = self.generate_report()
        
        lines = [
            "=" * 60,
            "CALab Diagnostic Report",
            "=" * 60,
            f"Generated: {report['system_info']['timestamp']}",
            f"Platform: {report['system_info']['platform']}",
            f"Python: {report['system_info']['python_version']}",
            "",
            "Summary:",
            f"  Total Events: {report['summary']['total_logs']}",
            f"  Total Errors: {report['summary']['total_errors']}",
            f"  Performance Metrics: {report['summary']['total_performance_metrics']}",
            f"  Automaton Snapshots: {report['summary']['total_snapshots']}",
            ""
        ]
        
        if self.errors:
            lines.append("Recent Errors:")
            for error in self.errors[-5:]:  # Last 5 errors
                lines.append(f"  [{error['timestamp']}] {error['error_type']}: {error['error_message']}")
            lines.append("")
        
        return "\n".join(lines)


class AutomatonAnalyzer:
    """
    Analyzes automaton behavior and provides insights
    """
    
    @staticmethod
    def analyze_evolution(automaton, num_steps: int = 100) -> Dict[str, Any]:
        """
        Analyze how an automaton evolves over time
        
        Returns metrics about growth, stability, periodicity, etc.
        """
        initial_grid = automaton.export_grid()
        statistics_over_time = []
        
        # Run simulation
        for _ in range(num_steps):
            automaton.step()
            stats = automaton.compute_statistics()
            statistics_over_time.append(stats)
        
        # Analyze trends
        densities = [s['density'] for s in statistics_over_time]
        entropies = [s['entropy'] for s in statistics_over_time]
        
        analysis = {
            'initial_density': densities[0] if densities else 0,
            'final_density': densities[-1] if densities else 0,
            'density_change': densities[-1] - densities[0] if densities else 0,
            'max_density': max(densities) if densities else 0,
            'min_density': min(densities) if densities else 0,
            'avg_density': np.mean(densities) if densities else 0,
            'density_std': np.std(densities) if densities else 0,
            'initial_entropy': entropies[0] if entropies else 0,
            'final_entropy': entropies[-1] if entropies else 0,
            'entropy_change': entropies[-1] - entropies[0] if entropies else 0,
            'statistics_over_time': statistics_over_time,
            'classification': AutomatonAnalyzer._classify_behavior(densities, entropies)
        }
        
        # Restore initial state
        automaton.import_grid(initial_grid)
        automaton.generation = 0
        
        return analysis
    
    @staticmethod
    def _classify_behavior(densities: List[float], entropies: List[float]) -> str:
        """Classify automaton behavior based on metrics"""
        if not densities or not entropies:
            return "unknown"
        
        density_change = densities[-1] - densities[0]
        density_std = np.std(densities)
        
        if abs(density_change) < 1.0 and density_std < 0.5:
            return "static"
        elif density_change > 5.0:
            return "growing"
        elif density_change < -5.0:
            return "dying"
        elif density_std > 2.0:
            return "chaotic"
        elif density_std > 0.5:
            return "oscillating"
        else:
            return "stable"
    
    @staticmethod
    def detect_periodicity(automaton, max_period: int = 50) -> Optional[int]:
        """
        Detect if automaton has periodic behavior
        
        Returns period if found, None otherwise
        """
        history = []
        
        for _ in range(max_period * 2):
            grid_hash = hash(automaton.grid.tobytes())
            if grid_hash in history:
                period = len(history) - history.index(grid_hash)
                return period
            history.append(grid_hash)
            automaton.step()
        
        return None
    
    @staticmethod
    def compare_automata(automaton1, automaton2, num_steps: int = 50) -> Dict[str, Any]:
        """Compare evolution of two automata"""
        stats1 = []
        stats2 = []
        
        for _ in range(num_steps):
            automaton1.step()
            automaton2.step()
            stats1.append(automaton1.compute_statistics())
            stats2.append(automaton2.compute_statistics())
        
        # Compare densities
        densities1 = [s['density'] for s in stats1]
        densities2 = [s['density'] for s in stats2]
        
        correlation = np.corrcoef(densities1, densities2)[0, 1] if len(densities1) > 1 else 0
        
        return {
            'density_correlation': float(correlation),
            'final_density_diff': abs(densities1[-1] - densities2[-1]),
            'automaton1_stats': stats1,
            'automaton2_stats': stats2
        }
