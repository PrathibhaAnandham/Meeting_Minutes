import whisper
from pydub import AudioSegment
import os

def split_and_transcribe(audio_path):
    # Load model
    model = whisper.load_model("tiny")

    # Load your audio
    audio = AudioSegment.from_file(audio_path)

    # Split into 10 minute chunks
    chunk_length = 10 * 60 * 1000  # 10 minutes in milliseconds
    chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]

    full_transcription = ""

    # Create temp folder to store chunks
    os.makedirs('temp_chunks', exist_ok=True)

    for idx, chunk in enumerate(chunks):
        chunk_filename = f"temp_chunks/chunk_{idx}.wav"
        chunk.export(chunk_filename, format="wav")
        
        # Transcribe
        result = model.transcribe(chunk_filename)
        full_transcription += result['text'] + "\n"

    # Clean up temporary files
    for file in os.listdir('temp_chunks'):
        os.remove(os.path.join('temp_chunks', file))
    os.rmdir('temp_chunks')

    return full_transcription

# Example usage (only when running fast_transcription.py directly)
if __name__ == "__main__":
    transcription = split_and_transcribe("C:\\Users\\prath\\OneDrive\\Desktop\\miniprojCopy\\meeting-minutes\\audio\\EarningsCall.wav")
    print(transcription)
