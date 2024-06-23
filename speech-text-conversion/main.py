from flask import Flask, render_template, request, send_file, flash
from gtts import gTTS
import os
from werkzeug.utils import secure_filename
from googletrans import Translator, LANGUAGES
import uuid  # To generate unique file names
from langdetect import detect, LangDetectException, DetectorFactory

DetectorFactory.seed = 0  # To ensure reproducibility in language detection

# Define the Flask application
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Set the UPLOAD_FOLDER to a directory relative to the script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def generate_unique_filename():
    return str(uuid.uuid4()) + ".mp3"

@app.route("/", methods=["GET", "POST"])
def index():
    detected_language_name = None  # Variable to store full language name

    if request.method == "POST":
        text = request.form.get("text")
        language = request.form.get("language")
        file = request.files.get("file")

        if file and file.filename.endswith('.txt'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            with open(file_path, 'r') as f:
                text = f.read()

            # Detect language of the uploaded file
            try:
                detected_language = detect(text)
                detected_language_name = LANGUAGES.get(detected_language)  # Get full language name
                flash(f"Detected language: {detected_language_name} ({detected_language})", "info")
            except LangDetectException:
                flash("Could not detect language. Please provide more text or choose a language manually.", "error")
                return render_template("index.html", detected_language=None, detected_language_name=None)

        if text and language and language != "auto":
            # Check if the selected language is valid
            if language not in LANGUAGES:
                flash("Invalid destination language selected.", "error")
                return render_template("index.html", detected_language_name=detected_language_name)

            # Translate text to the selected language
            translator = Translator()
            try:
                translated_text = translator.translate(text, dest=language).text
            except Exception as e:
                flash(f"Translation failed: {e}", "error")
                return render_template("index.html", detected_language_name=detected_language_name)

            # Convert translated text to speech
            tts = gTTS(translated_text, lang=language)
            output_filename = generate_unique_filename()
            output_file = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            tts.save(output_file)

            return render_template("index.html", message="Conversion successful.", audio=output_filename, detected_language_name=detected_language_name)
        else:
            flash("Please provide text or upload a file and select a language.", "error")
    
    return render_template("index.html", detected_language_name=detected_language_name)

@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash("File not found.", "error")
        return render_template("index.html")

@app.route("/play/<filename>")
def play(filename):
    audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(audio_file_path):
        return send_file(audio_file_path, mimetype="audio/mpeg")
    else:
        flash("File not found.", "error")
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
