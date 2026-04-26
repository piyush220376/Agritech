import vosk
import pyaudio
import json
from PyQt5.QtCore import QThread, pyqtSignal


MODEL_PATHS = {
    "English": r"D:\ai farmer chat bot\models\vosk-model-small-en-us-0.15",
    "Hindi": r"D:\ai farmer chat bot\models\vosk-model-small-hi-0.22"
}


_loaded_models = {}


def get_model(language):
    """Load (and cache) the Vosk model for the requested language.
    Falls back to English if the requested model path is missing."""
    if language not in MODEL_PATHS:
        language = "English"

    if language not in _loaded_models:
        path = MODEL_PATHS[language]
        import os
        if not os.path.isdir(path):
            # Requested model not downloaded – fall back to English
            path = MODEL_PATHS["English"]
        _loaded_models[language] = vosk.Model(path)

    return _loaded_models[language]


class VoiceThread(QThread):
    voice_recognized = pyqtSignal(str)
    voice_error = pyqtSignal(str)

    def __init__(self, language):
        super().__init__()
        self.language = language

    def run(self):
        p = None
        stream = None
        try:
            model = get_model(self.language)
            rec = vosk.KaldiRecognizer(model, 16000)

            p = pyaudio.PyAudio()

            # Check that at least one input device exists
            if p.get_default_input_device_info() is None:
                raise RuntimeError("No microphone found. Please connect a microphone.")

            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000
            )
            stream.start_stream()

            while True:
                data = stream.read(4000, exception_on_overflow=False)
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").strip()
                    if text:
                        self.voice_recognized.emit(text)
                        break

        except Exception as e:
            self.voice_error.emit(f"Voice error: {e}")

        finally:
            # Always release audio resources
            if stream is not None:
                try:
                    stream.stop_stream()
                    stream.close()
                except Exception:
                    pass
            if p is not None:
                try:
                    p.terminate()
                except Exception:
                    pass
