import whisper

model = whisper.load_model("tiny")

def transcribe_video(file_path):
    return model.transcribe(file_path)
