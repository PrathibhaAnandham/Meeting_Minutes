from pydub import AudioSegment
from pydub.utils import mediainfo
import os

def split_and_transcribe(audio_path, model):
    audio = AudioSegment.from_file(audio_path)

    # Split into 10-minute chunks (600000 ms)
    chunk_length = 10 * 60 * 1000  # 10 minutes in ms
    chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]

    full_transcription = ""
    os.makedirs('temp_chunks', exist_ok=True)

    for idx, chunk in enumerate(chunks):
        chunk_filename = f"temp_chunks/chunk_{idx}.wav"
        chunk.export(chunk_filename, format="wav")

        result = model.transcribe(chunk_filename, fp16=False)
        full_transcription += result['text'] + "\n"

    # Clean up
    for file in os.listdir('temp_chunks'):
        os.remove(os.path.join('temp_chunks', file))
    os.rmdir('temp_chunks')

    return full_transcription.strip()

def transcribe_audio(audio_file_path, model):
    # Get audio duration
    audio_info = mediainfo(audio_file_path)
    duration = float(audio_info['duration'])  # duration in seconds

    print(f"Audio duration: {duration} seconds")

    # If the audio is shorter than 5 minutes, do not split
    if duration <= 300:  # 5 minutes
        result = model.transcribe(audio_file_path, fp16=False)
        return result['text'].strip()
    else:
        return split_and_transcribe(audio_file_path, model)
