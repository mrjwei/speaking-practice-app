import whisper
from openai import OpenAI

class AudioTranscriber:
  """
  Transcribes audio files and stores resulting pieces of text in instance variable using local model or calling remote API.
  -----------
  filepaths: list
    Paths of the audio files to open.

  mode: Literal['local', 'remote']
    Mode decides how audio is processed, by local model or remote API.
    Calling remote API costs a fee.
  ------------
  methods:
    transcribe:
      Processes the audio files, generates transcripts and stores the resulting text pieces in instance variable.
  """
  def __init__(self, *filepaths, mode='local', **kwargs):
    if mode == 'local':
      self.mode = 'local'
      self.model = kwargs.get('model', 'tiny.en')
    elif mode == 'remote':
      self.mode = 'remote'
    else:
      raise Exception('Mode can only be "local" or "remote"')

    self.filepaths = filepaths
    self.texts = []

  def transcribe(self):
    if self.mode == 'local':
      whisper_model = whisper.load_model(self.model)
      for filepath in self.filepaths:
        result = whisper_model.transcribe(filepath.as_posix())
        self.texts.append(result['text'])
      print('processed audio locally')
    elif self.mode == 'remote':
      client = OpenAI()
      for filepath in self.filepaths:
        audio_file = open(filepath.as_posix(), 'rb')
        result = client.audio.transcriptions.create(
          model='whisper-1',
          file=audio_file,
          language='en'
        )
        self.texts.append(result.text)
      print('processed audio by calling API')
