import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import threading
import time
from pathlib import Path

import win32com.client
import pygame

AUDIO_ENABLED = True

BASE_DIR = Path(__file__).parent
SOUND_DIR = BASE_DIR / "sound"

# Lautstärke: 1.0 = 100%, 0.5 = halb so laut
SFX_VOLUME = 0.3
MUSIC_VOLUME = 0.10

_speaker = None
_pygame_init = False


def _init_pygame():
    global _pygame_init
    if not _pygame_init:
        pygame.mixer.init()
        _pygame_init = True


def _init_speaker():
    global _speaker
    if _speaker is None:
        _speaker = win32com.client.Dispatch("SAPI.SpVoice")
        _speaker.Volume = 100  # max
        _speaker.Rate = 0


def speak_async(text: str, delay_seconds: int = 0):
    """Windows TTS (SAPI) asynchron, optional verzögert."""
    if not AUDIO_ENABLED:
        return

    def run():
        if delay_seconds > 0:
            time.sleep(delay_seconds)
        _init_speaker()
        _speaker.Speak(text)

    threading.Thread(target=run, daemon=True).start()


def play_wav(name: str):
    """WAV asynchron via pygame (damit Lautstärke steuerbar ist)."""
    if not AUDIO_ENABLED:
        return

    path = SOUND_DIR / name
    if not path.exists():
        return

    _init_pygame()

    try:
        s = pygame.mixer.Sound(str(path))
        s.set_volume(SFX_VOLUME)
        s.play()
    except Exception:
        pass


def _apply_music_volume():
    """Setzt die Musiklautstärke (hilft auch, wenn pygame sie erst nach Start annimmt)."""
    try:
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
    except Exception:
        pass


def play_mp3_loop(name: str):
    """MP3 als Loop, Lautstärke wird zuverlässig gesetzt (mehrfach)."""
    if not AUDIO_ENABLED:
        return

    path = SOUND_DIR / name
    if not path.exists():
        return

    _init_pygame()

    try:
        # Falls schon etwas läuft, sauber stoppen
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

        pygame.mixer.music.load(str(path))

        # Lautstärke vor dem Start setzen
        _apply_music_volume()

        pygame.mixer.music.play(-1)  # Loop

        # Lautstärke direkt nach Start nochmal setzen
        _apply_music_volume()

        # Und nach kurzer Zeit nochmal (Workaround für Setups, wo es sonst "ignoriert" wirkt)
        threading.Timer(0.2, _apply_music_volume).start()
        threading.Timer(1.0, _apply_music_volume).start()

    except Exception:
        pass


def stop_mp3():
    if _pygame_init:
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
