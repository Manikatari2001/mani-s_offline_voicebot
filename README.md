# 🗣️📄 PDF VoiceBot with GPT4All & Vosk

This is a Flask web application that allows users to:

- 📤 Upload a **PDF**
- 🎙️ Ask questions either via **text or voice**
- 🤖 Get answers based only on the **PDF content**

It uses **GPT4All** for local LLM inference and **Vosk** for offline speech recognition.

---

## 🚀 Features

- Upload and process any text-based PDF.
- Ask questions via text or microphone.
- Local inference with no cloud dependencies.
- Offline voice recognition (no Google Speech API).
- Works entirely on your machine (privacy-focused).

---

## 📂 Project Structure

├── app.py # Main Flask app
├── templates/
│ └── index.html # Frontend HTML
├── uploads/ # Uploaded PDFs and audio files
├── vosk_model/ # Vosk speech recognition model
├── orca-mini-3b-gguf2-q4_0.gguf # GPT4All model file (example)
├── requirements.txt # Python dependencies
└── README.md # This file

yaml
Copy code

---

## ⚙️ Setup Instructions

### 1. 🐍 Python Environment

Make sure you're using **Python 3.8+**

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
2. 📦 Install Requirements
bash
Copy code
pip install -r requirements.txt
Make sure ffmpeg is installed and added to PATH (for audio conversion).

3. ⬇️ Download Models
GPT4All Model
Download orca-mini-3b-gguf2-q4_0.gguf or another compatible .gguf model from https://gpt4all.io/models

Place it in the project root folder.

Vosk Model
Download the Vosk model (e.g., vosk-model-small-en-in-0.4) from https://alphacephei.com/vosk/models

Extract and place it under vosk_model/

Example structure:

Copy code
vosk_model/
└── vosk-model-small-en-in-0.4/
    ├── am
    ├── conf
    └── ...
4. 🏃‍♂️ Run the App
bash
Copy code
python app.py
Visit: http://127.0.0.1:5000

🌐 Frontend Preview
Simple web interface with:

PDF Upload

Text input box for questions

Microphone button for voice questions

You can expand it with custom CSS, JS or React later.

🎤 Voice Input Requirements
ffmpeg must be installed for converting .webm to .wav

Vosk handles speech recognition offline.

Install ffmpeg:

Windows: https://ffmpeg.org/download.html

macOS: brew install ffmpeg

Linux: sudo apt install ffmpeg

🧠 LLM Details
Uses gpt4all Python library.

Make sure model is in .gguf format and supported by your system (e.g., CPU only).

✅ TODO / Improvements
Add PDF chunking with semantic search

Add better UI with React or Vue

Add support for non-English PDFs/audio

Dockerize the app for easy deployment

📜 License
MIT License

🙌 Acknowledgements
GPT4All

Vosk API

Flask

yaml
Copy code

