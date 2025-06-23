import os
import torch
import whisper
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from summarization import summarize_text
from sentiment_analysis import analyze_sentiment
from key_points_extraction import extract_key_points
from action_items_extraction import extract_action_items
from pydub.utils import mediainfo
import nltk
from transcription import transcribe_audio  # Import the transcribe_audio function

# Download NLTK resources (first time only)
nltk.download("vader_lexicon")

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load Whisper model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("tiny", device=device)

# Check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a .wav file'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(filepath)
        print(f"File saved successfully at {filepath}")

        # Check file size
        if os.path.getsize(filepath) == 0:
            return jsonify({'error': 'Uploaded file is empty or corrupted. Please try again.'})

        # Process the audio file using transcription.py
        transcription = transcribe_audio(filepath, model)

        # Generate outputs
        summary = summarize_text(transcription)
        sentiment = analyze_sentiment(transcription)
        key_points = extract_key_points(transcription)
        action_items = extract_action_items(transcription)

        response = {
            'message': 'File processed successfully',
            'transcription': transcription,
            'summary': summary,
            'sentiment': sentiment,
            'key_points': key_points,
            'action_items': action_items
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)