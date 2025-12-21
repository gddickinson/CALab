"""
CALab - Simulation Engine
Manages simulation execution, threading, and state management
"""

import numpy as np
from typing import Optional, Callable, List
from threading import Thread, Event, Lock
import time
from datetime import datetime


class SimulationEngine:
    """
    Core simulation engine
    
    Handles running simulations with proper threading and state management.
    """
    
    def __init__(self, automaton=None):
        """
        Initialize simulation engine
        
        Args:
            automaton: Cellular automaton instance
        """
        self.automaton = automaton
        self.running = False
        self.paused = False
        self.stop_event = Event()
        self.pause_event = Event()
        self.pause_event.set()  # Start unpaused
        self.lock = Lock()
        self.thread: Optional[Thread] = None
        
        # Simulation parameters
        self.speed_ms = 50  # Milliseconds between steps
        self.max_generations = None  # None = run indefinitely
        
        # Callbacks
        self.on_step_callback: Optional[Callable] = None
        self.on_complete_callback: Optional[Callable] = None
        self.on_error_callback: Optional[Callable] = None
        
        # Statistics
        self.start_time: Optional[datetime] = None
        self.total_steps = 0
        self.fps = 0.0
        
    def set_automaton(self, automaton) -> None:
        """Set the automaton to simulate"""
        with self.lock:
            self.automaton = automaton
    
    def start(self) -> None:
        """Start the simulation"""
        if self.automaton is None:
            raise ValueError("No automaton set")
        
        if self.running:
            return
        
        self.running = True
        self.stop_event.clear()
        self.pause_event.set()
        self.paused = False
        self.start_time = datetime.now()
        self.total_steps = 0
        
        self.thread = Thread(target=self._run_loop, daemon=True)
        self.thread.start()
    
    def stop(self) -> None:
        """Stop the simulation"""
        self.running = False
        self.stop_event.set()
        self.pause_event.set()  # Unpause if paused
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
    
    def pause(self) -> None:
        """Pause the simulation"""
        self.paused = True
        self.pause_event.clear()
    
    def resume(self) -> None:
        """Resume the simulation"""
        self.paused = False
        self.pause_event.set()
    
    def step_once(self) -> None:
        """Execute a single simulation step"""
        if self.automaton is None:
            return
        
        try:
            with self.lock:
                self.automaton.step()
                self.total_steps += 1
                
            if self.on_step_callback:
                self.on_step_callback(self.automaton)
                
        except Exception as e:
            if self.on_error_callback:
                self.on_error_callback(e)
            else:
                raise
    
    def _run_loop(self) -> None:
        """Internal simulation loop (runs in thread)"""
        last_step_time = time.time()
        step_times: List[float] = []
        
        try:
            while self.running and not self.stop_event.is_set():
                # Wait if paused
                self.pause_event.wait()
                
                # Check if we should stop
                if self.stop_event.is_set():
                    break
                
                # Check max generations
                if self.max_generations and self.total_steps >= self.max_generations:
                    break
                
                # Execute step
                step_start = time.time()
                self.step_once()
                step_end = time.time()
                
                # Calculate FPS
                step_times.append(step_end - step_start)
                if len(step_times) > 10:
                    step_times.pop(0)
                avg_step_time = sum(step_times) / len(step_times)
                self.fps = 1.0 / avg_step_time if avg_step_time > 0 else 0.0
                
                # Sleep for speed control
                sleep_time = max(0, (self.speed_ms / 1000.0) - (step_end - step_start))
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
        except Exception as e:
            if self.on_error_callback:
                self.on_error_callback(e)
            raise
        finally:
            self.running = False
            if self.on_complete_callback:
                self.on_complete_callback()
    
    def set_speed(self, speed_ms: int) -> None:
        """Set simulation speed in milliseconds per step"""
        self.speed_ms = max(1, speed_ms)
    
    def get_status(self) -> dict:
        """Get current simulation status"""
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        return {
            'running': self.running,
            'paused': self.paused,
            'generation': self.automaton.generation if self.automaton else 0,
            'total_steps': self.total_steps,
            'elapsed_seconds': elapsed,
            'fps': self.fps,
            'speed_ms': self.speed_ms
        }


class BatchSimulation:
    """
    Run multiple simulations in batch mode
    
    Useful for parameter sweeps, testing, and analysis
    """
    
    def __init__(self):
        self.results = []
        
    def run_batch(self, automaton_factory: Callable, 
                  parameter_sets: List[dict],
                  num_steps: int,
                  callback: Optional[Callable] = None) -> List[dict]:
        """
        Run batch simulations
        
        Args:
            automaton_factory: Function that creates automaton with given parameters
            parameter_sets: List of parameter dictionaries
            num_steps: Number of steps to run each simulation
            callback: Optional callback for progress updates
            
        Returns:
            List of result dictionaries
        """
        self.results = []
        
        for i, params in enumerate(parameter_sets):
            # Create automaton
            automaton = automaton_factory(**params)
            
            # Run simulation
            for step in range(num_steps):
                automaton.step()
            
            # Collect results
            result = {
                'parameters': params,
                'final_generation': automaton.generation,
                'final_statistics': automaton.compute_statistics(),
                'final_grid': automaton.export_grid()
            }
            self.results.append(result)
            
            # Progress callback
            if callback:
                callback(i + 1, len(parameter_sets), result)
        
        return self.results
    
    def export_results(self, filename: str) -> None:
        """Export results to file"""
        import json
        
        # Convert numpy arrays to lists for JSON serialization
        export_data = []
        for result in self.results:
            export_result = result.copy()
            export_result['final_grid'] = result['final_grid'].tolist()
            export_data.append(export_result)
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
