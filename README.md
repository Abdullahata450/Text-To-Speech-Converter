# Flask Text Translation and Text-to-Speech Application

This Flask application allows users to input text or upload a `.txt` file, detects the language of the input, translates it to a selected language, converts the translated text to speech, and provides options to play or download the resulting audio file.

## Features

- Text input or file upload for translation.
- Language detection for the input text.
- Translation of text to a selected language using Google Translate.
- Text-to-Speech conversion using Google Text-to-Speech (gTTS).
- Options to play or download the generated audio file.
- Flash messages to inform users of the application status and any errors.

## Prerequisites

- Python 3.x
- Flask
- gTTS
- googletrans
- langdetect
- werkzeug
- uuid

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
