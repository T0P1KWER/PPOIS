import math
from array import array

import pygame


class AudioManager:
    def __init__(self, enabled, volume_effects, volume_music):
        self.enabled = enabled
        self.volume_effects = volume_effects
        self.volume_music = volume_music
        self.sounds = {}
        self.music_sound = None
        self.music_channel = None

        if not enabled:
            return

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1)
            self._create_sounds()
        except pygame.error:
            self.enabled = False

    def _create_tone(self, frequency, duration_ms, volume, wave_type="sine"):
        sample_rate = 44100
        sample_count = int(sample_rate * duration_ms / 1000)
        buffer = array("h")

        for sample_index in range(sample_count):
            time_position = sample_index / sample_rate

            if wave_type == "square":
                raw_value = 1.0 if math.sin(2 * math.pi * frequency * time_position) >= 0 else -1.0
            else:
                raw_value = math.sin(2 * math.pi * frequency * time_position)

            fade = 1.0
            attack_samples = max(1, int(sample_rate * 0.01))
            release_samples = max(1, int(sample_rate * 0.03))

            if sample_index < attack_samples:
                fade = sample_index / attack_samples
            elif sample_index > sample_count - release_samples:
                fade = max(0.0, (sample_count - sample_index) / release_samples)

            value = int(raw_value * 32767 * volume * fade)
            buffer.append(value)

        return pygame.mixer.Sound(buffer=buffer.tobytes())

    def _create_music_loop(self):
        notes = [
            (330, 220),
            (392, 220),
            (523, 220),
            (392, 220),
            (294, 220),
            (349, 220),
            (494, 220),
            (349, 220),
        ]

        sample_rate = 44100
        buffer = array("h")

        for frequency, duration_ms in notes:
            sample_count = int(sample_rate * duration_ms / 1000)
            for sample_index in range(sample_count):
                time_position = sample_index / sample_rate
                wave = math.sin(2 * math.pi * frequency * time_position)
                wave += 0.3 * math.sin(2 * math.pi * (frequency / 2) * time_position)
                value = int(wave * 12000 * self.volume_music)
                buffer.append(max(-32767, min(32767, value)))


        return pygame.mixer.Sound(buffer=buffer.tobytes())

    def _create_sounds(self):
        self.sounds["select"] = self._create_tone(660, 70, self.volume_effects, "square")
        self.sounds["swap"] = self._create_tone(520, 120, self.volume_effects)
        self.sounds["match"] = self._create_tone(820, 180, self.volume_effects)
        self.sounds["drop"] = self._create_tone(420, 90, self.volume_effects)
        self.sounds["win"] = self._create_tone(1040, 400, self.volume_effects)
        self.sounds["lose"] = self._create_tone(240, 400, self.volume_effects, "square")
        self.music_sound = self._create_music_loop()

    def play(self, sound_name):
        if self.enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()

    def play_music(self):
        if self.enabled and self.music_sound is not None:
            self.music_channel = self.music_sound.play(loops=-1)

    def stop_music(self):
        if self.music_channel is not None:
            self.music_channel.stop()
