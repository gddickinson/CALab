"""
CALab - Sonification Tab
Generate music and sound from cellular automaton patterns
"""

import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QSlider, QComboBox, QGroupBox, QCheckBox,
                             QSpinBox, QDoubleSpinBox, QProgressBar, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import threading
import queue

try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("Warning: sounddevice not available. Install with: pip install sounddevice")


class SonificationTab(QWidget):
    """
    Convert cellular automaton patterns into sound and music
    """
    
    def __init__(self, simulator):
        super().__init__()
        self.simulator = simulator
        
        # Audio settings
        self.sample_rate = 44100
        self.is_playing = False
        self.audio_queue = queue.Queue()
        self.audio_thread = None
        
        # Musical scales (MIDI note offsets from root)
        self.scales = {
            'Major': [0, 2, 4, 5, 7, 9, 11],
            'Minor': [0, 2, 3, 5, 7, 8, 10],
            'Pentatonic': [0, 2, 4, 7, 9],
            'Blues': [0, 3, 5, 6, 7, 10],
            'Chromatic': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'Whole Tone': [0, 2, 4, 6, 8, 10],
            'Harmonic Minor': [0, 2, 3, 5, 7, 8, 11],
        }
        
        # Waveforms
        self.waveforms = {
            'Sine': self._sine_wave,
            'Square': self._square_wave,
            'Sawtooth': self._sawtooth_wave,
            'Triangle': self._triangle_wave,
        }
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel("🎵 Sonification - Turn Patterns into Sound")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        if not AUDIO_AVAILABLE:
            warning = QLabel("⚠️ Audio not available. Install sounddevice: pip install sounddevice")
            warning.setStyleSheet("color: orange; font-weight: bold;")
            layout.addWidget(warning)
            return
        
        # Main controls
        controls = self._create_playback_controls()
        layout.addLayout(controls)
        
        # Settings panels
        settings_layout = QHBoxLayout()
        
        # Left: Sonification mode
        mode_group = self._create_mode_settings()
        settings_layout.addWidget(mode_group)
        
        # Right: Musical settings
        music_group = self._create_musical_settings()
        settings_layout.addWidget(music_group)
        
        layout.addLayout(settings_layout)
        
        # Visualization
        viz_group = self._create_visualization()
        layout.addWidget(viz_group)
        
        # Status
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Ready")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
    def _create_playback_controls(self):
        """Create playback control buttons"""
        layout = QHBoxLayout()
        
        # Play/Stop
        self.play_btn = QPushButton("▶️ Play Sound")
        self.play_btn.clicked.connect(self._toggle_playback)
        self.play_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(self.play_btn)
        
        # Volume
        layout.addWidget(QLabel("Volume:"))
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setMaximumWidth(150)
        layout.addWidget(self.volume_slider)
        
        self.volume_label = QLabel("50%")
        self.volume_slider.valueChanged.connect(
            lambda v: self.volume_label.setText(f"{v}%")
        )
        layout.addWidget(self.volume_label)
        
        layout.addStretch()
        
        return layout
        
    def _create_mode_settings(self):
        """Create sonification mode settings"""
        group = QGroupBox("Sonification Mode")
        layout = QVBoxLayout()
        
        # Mode selection
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Mode:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            'Row Scanner',
            'Column Scanner',
            'Density Wave',
            'State Percussion',
            'Cellular Melody',
            'Chaos Rhythm',
            'Ambient Drone',
        ])
        self.mode_combo.currentTextChanged.connect(self._update_mode_description)
        mode_layout.addWidget(self.mode_combo)
        layout.addLayout(mode_layout)
        
        # Mode description
        self.mode_description = QLabel()
        self.mode_description.setWordWrap(True)
        self.mode_description.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.mode_description)
        
        # Speed
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Scan Speed:"))
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 20)
        self.speed_slider.setValue(5)
        speed_layout.addWidget(self.speed_slider)
        self.speed_label = QLabel("5 Hz")
        self.speed_slider.valueChanged.connect(
            lambda v: self.speed_label.setText(f"{v} Hz")
        )
        speed_layout.addWidget(self.speed_label)
        layout.addLayout(speed_layout)
        
        # Update mode description
        self._update_mode_description()
        
        group.setLayout(layout)
        return group
        
    def _create_musical_settings(self):
        """Create musical parameter settings"""
        group = QGroupBox("Musical Settings")
        layout = QVBoxLayout()
        
        # Scale
        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Scale:"))
        self.scale_combo = QComboBox()
        self.scale_combo.addItems(list(self.scales.keys()))
        scale_layout.addWidget(self.scale_combo)
        layout.addLayout(scale_layout)
        
        # Root note
        root_layout = QHBoxLayout()
        root_layout.addWidget(QLabel("Root Note:"))
        self.root_note = QSpinBox()
        self.root_note.setRange(36, 84)  # C2 to C6
        self.root_note.setValue(60)  # Middle C
        self.root_note.setSuffix(" (MIDI)")
        root_layout.addWidget(self.root_note)
        layout.addLayout(root_layout)
        
        # Octave range
        octave_layout = QHBoxLayout()
        octave_layout.addWidget(QLabel("Octave Range:"))
        self.octave_range = QSpinBox()
        self.octave_range.setRange(1, 4)
        self.octave_range.setValue(2)
        octave_layout.addWidget(self.octave_range)
        layout.addLayout(octave_layout)
        
        # Waveform
        wave_layout = QHBoxLayout()
        wave_layout.addWidget(QLabel("Waveform:"))
        self.wave_combo = QComboBox()
        self.wave_combo.addItems(list(self.waveforms.keys()))
        wave_layout.addWidget(self.wave_combo)
        layout.addLayout(wave_layout)
        
        # Note duration
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("Note Duration:"))
        self.note_duration = QDoubleSpinBox()
        self.note_duration.setRange(0.01, 2.0)
        self.note_duration.setValue(0.1)
        self.note_duration.setSingleStep(0.05)
        self.note_duration.setSuffix(" sec")
        duration_layout.addWidget(self.note_duration)
        layout.addLayout(duration_layout)
        
        # Reverb
        self.reverb_check = QCheckBox("Add Reverb")
        layout.addWidget(self.reverb_check)
        
        group.setLayout(layout)
        return group
        
    def _create_visualization(self):
        """Create audio visualization area"""
        group = QGroupBox("Audio Visualization")
        layout = QVBoxLayout()
        
        # Current note
        note_layout = QHBoxLayout()
        note_layout.addWidget(QLabel("Current Note:"))
        self.current_note_label = QLabel("---")
        self.current_note_label.setStyleSheet("font-size: 18px; font-weight: bold; color: blue;")
        note_layout.addWidget(self.current_note_label)
        note_layout.addStretch()
        layout.addLayout(note_layout)
        
        # Activity indicator
        activity_layout = QHBoxLayout()
        activity_layout.addWidget(QLabel("Activity:"))
        self.activity_bar = QProgressBar()
        self.activity_bar.setRange(0, 100)
        activity_layout.addWidget(self.activity_bar)
        layout.addLayout(activity_layout)
        
        # Frequency display
        freq_layout = QHBoxLayout()
        freq_layout.addWidget(QLabel("Frequency:"))
        self.freq_label = QLabel("--- Hz")
        freq_layout.addWidget(self.freq_label)
        freq_layout.addStretch()
        layout.addLayout(freq_layout)
        
        group.setLayout(layout)
        return group
        
    def _update_mode_description(self):
        """Update mode description text"""
        descriptions = {
            'Row Scanner': 'Scan rows top-to-bottom, mapping active cells to notes',
            'Column Scanner': 'Scan columns left-to-right, creating melodic sequences',
            'Density Wave': 'Cell density controls pitch, creates ambient soundscape',
            'State Percussion': 'Different states trigger different percussion sounds',
            'Cellular Melody': 'Active cells create harmonious melodies',
            'Chaos Rhythm': 'State changes drive rhythmic patterns',
            'Ambient Drone': 'Overall pattern creates evolving drone tones',
        }
        
        mode = self.mode_combo.currentText()
        self.mode_description.setText(descriptions.get(mode, ''))
        
    def _toggle_playback(self):
        """Start or stop audio playback"""
        if not AUDIO_AVAILABLE:
            self.status_label.setText("Audio not available")
            return
            
        if not self.simulator.automaton:
            self.status_label.setText("No automaton loaded")
            return
            
        if self.is_playing:
            self._stop_playback()
        else:
            self._start_playback()
            
    def _start_playback(self):
        """Start audio generation"""
        self.is_playing = True
        self.play_btn.setText("⏸️ Stop Sound")
        self.status_label.setText("Playing...")
        
        # Start audio thread
        self.audio_thread = threading.Thread(target=self._audio_generation_loop, daemon=True)
        self.audio_thread.start()
        
    def _stop_playback(self):
        """Stop audio generation"""
        self.is_playing = False
        self.play_btn.setText("▶️ Play Sound")
        self.status_label.setText("Stopped")
        self.current_note_label.setText("---")
        self.freq_label.setText("--- Hz")
        self.activity_bar.setValue(0)
        
    def _audio_generation_loop(self):
        """Main audio generation loop (runs in thread)"""
        try:
            mode = self.mode_combo.currentText()
            
            # Open audio stream
            with sd.OutputStream(
                samplerate=self.sample_rate,
                channels=2,  # Stereo
                callback=self._audio_callback
            ):
                while self.is_playing:
                    # Generate audio based on current grid
                    if mode == 'Row Scanner':
                        self._generate_row_scanner()
                    elif mode == 'Column Scanner':
                        self._generate_column_scanner()
                    elif mode == 'Density Wave':
                        self._generate_density_wave()
                    elif mode == 'State Percussion':
                        self._generate_state_percussion()
                    elif mode == 'Cellular Melody':
                        self._generate_cellular_melody()
                    elif mode == 'Chaos Rhythm':
                        self._generate_chaos_rhythm()
                    elif mode == 'Ambient Drone':
                        self._generate_ambient_drone()
                    
                    # Small delay based on scan speed
                    import time
                    speed = self.speed_slider.value()
                    time.sleep(1.0 / speed)
                    
        except Exception as e:
            print(f"Audio error: {e}")
            self.is_playing = False
            
    def _audio_callback(self, outdata, frames, time, status):
        """Audio callback to fill output buffer"""
        if status:
            print(status)
            
        try:
            # Get audio from queue
            data = self.audio_queue.get_nowait()
            
            # Apply volume
            volume = self.volume_slider.value() / 100.0
            data = data * volume
            
            # Fill output buffer
            if len(data) < frames:
                outdata[:len(data)] = data
                outdata[len(data):] = 0
            else:
                outdata[:] = data[:frames]
                
        except queue.Empty:
            # No data, output silence
            outdata[:] = 0
            
    def _generate_row_scanner(self):
        """Scan rows and generate notes based on active cells"""
        if not self.simulator.automaton:
            return
            
        grid = self.simulator.automaton.grid
        h, w = grid.shape
        
        # Pick a row to scan (rotating)
        import time
        row_idx = int(time.time() * self.speed_slider.value()) % h
        row = grid[row_idx]
        
        # Count active cells
        active_count = np.sum(row > 0)
        
        if active_count > 0:
            # Map active cells to notes
            density = active_count / w
            note = self._density_to_note(density)
            freq = self._midi_to_freq(note)
            
            # Generate tone
            duration = self.note_duration.value()
            audio = self._generate_tone(freq, duration)
            
            # Add to queue
            self.audio_queue.put(audio)
            
            # Update UI
            self._update_ui(note, freq, density * 100)
            
    def _generate_column_scanner(self):
        """Scan columns left to right"""
        if not self.simulator.automaton:
            return
            
        grid = self.simulator.automaton.grid
        h, w = grid.shape
        
        # Pick a column
        import time
        col_idx = int(time.time() * self.speed_slider.value()) % w
        col = grid[:, col_idx]
        
        # Count active cells
        active_count = np.sum(col > 0)
        
        if active_count > 0:
            density = active_count / h
            note = self._density_to_note(density)
            freq = self._midi_to_freq(note)
            
            duration = self.note_duration.value()
            
            # Add stereo panning based on column position
            pan = col_idx / w  # 0 (left) to 1 (right)
            audio = self._generate_tone(freq, duration, pan=pan)
            
            self.audio_queue.put(audio)
            self._update_ui(note, freq, density * 100)
            
    def _generate_density_wave(self):
        """Generate ambient sound based on overall density"""
        if not self.simulator.automaton:
            return
            
        grid = self.simulator.automaton.grid
        density = np.sum(grid > 0) / grid.size
        
        # Map density to frequency
        note = self._density_to_note(density)
        freq = self._midi_to_freq(note)
        
        # Generate sustained tone
        duration = 0.5
        audio = self._generate_tone(freq, duration)
        
        self.audio_queue.put(audio)
        self._update_ui(note, freq, density * 100)
        
    def _generate_state_percussion(self):
        """Different states trigger different percussion-like sounds"""
        if not self.simulator.automaton:
            return
            
        grid = self.simulator.automaton.grid
        num_states = self.simulator.automaton.num_states
        
        # Count cells in each state
        sounds = []
        
        for state in range(1, num_states):  # Skip state 0 (dead)
            count = np.sum(grid == state)
            
            if count > 0:
                # Different frequency for each state
                note = self.root_note.value() + state * 7  # Perfect fifth intervals
                freq = self._midi_to_freq(note)
                
                # Short percussive sounds
                audio = self._generate_tone(freq, 0.05)
                sounds.append(audio)
        
        if sounds:
            # Mix all sounds
            mixed = np.sum(sounds, axis=0) / len(sounds)
            self.audio_queue.put(mixed)
            
            avg_note = self.root_note.value() + 7
            self._update_ui(avg_note, self._midi_to_freq(avg_note), 50)
            
    def _generate_cellular_melody(self):
        """Create melody from active cell positions"""
        if not self.simulator.automaton:
            return
            
        grid = self.simulator.automaton.grid
        h, w = grid.shape
        
        # Find all active cells
        active = np.argwhere(grid > 0)
        
        if len(active) > 0:
            # Pick a random active cell
            idx = np.random.randint(len(active))
            y, x = active[idx]
            
            # Map position to note
            # Y position = octave, X position = note in scale
            scale_name = self.scale_combo.currentText()
            scale = self.scales[scale_name]
            
            x_norm = x / w
            y_norm = y / h
            
            scale_idx = int(x_norm * len(scale))
            octave = int(y_norm * self.octave_range.value())
            
            note = self.root_note.value() + octave * 12 + scale[scale_idx]
            freq = self._midi_to_freq(note)
            
            duration = self.note_duration.value()
            audio = self._generate_tone(freq, duration)
            
            self.audio_queue.put(audio)
            self._update_ui(note, freq, 50)
            
    def _generate_chaos_rhythm(self):
        """Rhythmic patterns from state changes"""
        if not self.simulator.automaton:
            return
            
        # Advance simulation one step
        old_grid = self.simulator.automaton.grid.copy()
        self.simulator.step()
        new_grid = self.simulator.automaton.grid
        
        # Count changes
        changes = np.sum(old_grid != new_grid)
        
        if changes > 10:  # Threshold for triggering sound
            # Map changes to intensity
            intensity = min(changes / 100, 1.0)
            note = self._density_to_note(intensity)
            freq = self._midi_to_freq(note)
            
            # Short rhythmic hits
            audio = self._generate_tone(freq, 0.08)
            
            self.audio_queue.put(audio)
            self._update_ui(note, freq, intensity * 100)
            
    def _generate_ambient_drone(self):
        """Create ambient drone based on pattern complexity"""
        if not self.simulator.automaton:
            return
            
        grid = self.simulator.automaton.grid
        
        # Calculate entropy/complexity
        density = np.sum(grid > 0) / grid.size
        
        # Generate chord (root + fifth + octave)
        root = self.root_note.value()
        notes = [root, root + 7, root + 12]  # Root, fifth, octave
        
        # Mix frequencies
        sounds = []
        for note in notes:
            freq = self._midi_to_freq(note)
            audio = self._generate_tone(freq, 1.0)
            sounds.append(audio)
        
        # Mix with varying amplitudes based on density
        mixed = sounds[0] * 0.5 + sounds[1] * 0.3 + sounds[2] * 0.2
        
        self.audio_queue.put(mixed)
        self._update_ui(root, self._midi_to_freq(root), density * 100)
        
    def _density_to_note(self, density):
        """Map density (0-1) to MIDI note"""
        scale_name = self.scale_combo.currentText()
        scale = self.scales[scale_name]
        root = self.root_note.value()
        octaves = self.octave_range.value()
        
        # Map density to position in scale across octaves
        total_notes = len(scale) * octaves
        note_idx = int(density * total_notes)
        note_idx = min(note_idx, total_notes - 1)
        
        octave = note_idx // len(scale)
        scale_pos = note_idx % len(scale)
        
        midi_note = root + octave * 12 + scale[scale_pos]
        return midi_note
        
    def _midi_to_freq(self, midi_note):
        """Convert MIDI note to frequency in Hz"""
        return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))
        
    def _generate_tone(self, freq, duration, pan=0.5):
        """Generate a tone at given frequency and duration
        
        Args:
            freq: Frequency in Hz
            duration: Duration in seconds
            pan: Stereo panning 0 (left) to 1 (right)
        
        Returns:
            Stereo audio array
        """
        num_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, num_samples)
        
        # Generate waveform
        wave_name = self.wave_combo.currentText()
        wave_func = self.waveforms[wave_name]
        audio = wave_func(t, freq)
        
        # Apply envelope (ADSR simplified to fade in/out)
        envelope = np.ones_like(audio)
        fade_samples = int(0.01 * self.sample_rate)  # 10ms fade
        if num_samples > fade_samples * 2:
            envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        audio = audio * envelope
        
        # Apply reverb if enabled
        if self.reverb_check.isChecked():
            audio = self._apply_reverb(audio)
        
        # Create stereo with panning
        left = audio * (1 - pan)
        right = audio * pan
        stereo = np.column_stack((left, right))
        
        return stereo
        
    def _sine_wave(self, t, freq):
        """Generate sine wave"""
        return np.sin(2 * np.pi * freq * t)
        
    def _square_wave(self, t, freq):
        """Generate square wave"""
        return np.sign(np.sin(2 * np.pi * freq * t))
        
    def _sawtooth_wave(self, t, freq):
        """Generate sawtooth wave"""
        return 2 * (t * freq - np.floor(t * freq + 0.5))
        
    def _triangle_wave(self, t, freq):
        """Generate triangle wave"""
        return 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
        
    def _apply_reverb(self, audio):
        """Simple reverb effect using delay"""
        # Simple comb filter reverb
        delay_samples = int(0.05 * self.sample_rate)  # 50ms delay
        reverb = np.zeros(len(audio) + delay_samples)
        
        reverb[:len(audio)] += audio
        reverb[delay_samples:] += audio * 0.3  # Delayed signal at 30% volume
        
        return reverb[:len(audio)]
        
    def _update_ui(self, note, freq, activity):
        """Update UI with current audio info"""
        # Note name
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        note_name = note_names[note % 12]
        octave = (note // 12) - 1
        
        self.current_note_label.setText(f"{note_name}{octave}")
        self.freq_label.setText(f"{freq:.1f} Hz")
        self.activity_bar.setValue(int(activity))
