import sounddevice as sd
import numpy as np
import threading
import time

class AudioRecorder:
  def __init__(self):
    self.recordings = []
    self.is_recording = False
    self.is_paused = False
    self.samplerate = 44100
    self.audio_thread = None

  def _callback(self, indata, frames, time, status):
    if status:
      print(status, file=sys.stderr)
    if self.is_recording and not self.is_paused:
      self.recordings.append(indata.copy())

  def start_recording(self):
    self.recordings = []
    self.is_recording = True
    self.is_paused = False
    self.audio_thread = threading.Thread(target=self._record)
    self.audio_thread.start()

  def _record(self):
    with sd.InputStream(samplerate=self.samplerate, channels=1, callback=self._callback):
      while self.is_recording:
        time.sleep(1)

  def toggle_recording(self):
    self.is_paused = not self.toggle_recording

  def stop_recording(self):
    self.is_recording = False
    if self.audio_thread:
      self.audio_thread.join()
    return np.concatenate(self.recordings, axis=0) if self.recordings else None
