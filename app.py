import os
import subprocess
from flask import Flask, render_template, request, jsonify
import pdfplumber
from gpt4all import GPT4All
from vosk import Model, KaldiRecognizer
import wave
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

pdf_chunks = []
chunk_size = 1500

model_path = os.path.join(os.path.dirname(__file__), "orca-mini-3b-gguf2-q4_0.gguf")
llm = GPT4All(model_path, allow_download=False, device="cpu")

vosk_model = Model(r"C:/Users/yalag/PycharmProjects/Mani's_VoiceBot/vosk_model/vosk-model-small-en-in-0.4")


def load_pdf(file_path):
    global pdf_chunks
    full_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += f"\n{text}\n"

    pdf_chunks = [full_text[i:i + chunk_size] for i in range(0, len(full_text), chunk_size)]
    return "success" if pdf_chunks else "no_text"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_pdf():
    file = request.files.get('pdf')
    if not file:
        return jsonify({'status': 'No file received'})

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    result = load_pdf(file_path)
    if result == "success":
        return jsonify({'status': '✅ PDF uploaded and processed successfully'})
    return jsonify({'status': '⚠️ PDF contains no readable text'})


@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')

    if not question or not pdf_chunks:
        return jsonify({'answer': 'Please upload a PDF and ask a valid question.'})

    combined_context = "\n".join(pdf_chunks)
    prompt = f"You are an expert assistant. Answer the question using the PDF content below only.\n\nPDF Content:\n{combined_context}\n\nQuestion: {question}\nAnswer:"

    with llm.chat_session():
        response = llm.generate(prompt, max_tokens=200)

    return jsonify({'answer': response.strip()})


@app.route('/ask_by_voice', methods=['POST'])
def ask_by_voice():
    if 'audio' not in request.files:
        return jsonify({'answer': 'No audio file received.'})

    audio_webm = os.path.join(app.config['UPLOAD_FOLDER'], "input.webm")
    audio_wav = os.path.join(app.config['UPLOAD_FOLDER'], "input.wav")
    request.files['audio'].save(audio_webm)

    subprocess.call(['ffmpeg', '-y', '-i', audio_webm, audio_wav], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        wf = wave.open(audio_wav, "rb")
    except wave.Error:
        return jsonify({'answer': 'Uploaded audio is invalid or corrupted.'})

    rec = KaldiRecognizer(vosk_model, wf.getframerate())
    text = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text += result.get("text", "")

    text += json.loads(rec.FinalResult()).get("text", "")
    wf.close()

    if not text.strip():
        return jsonify({'answer': 'Could not recognize speech.'})

    combined_context = "\n".join(pdf_chunks)
    prompt = f"You are an expert assistant. Answer the question using the PDF content below only.\n\nPDF Content:\n{combined_context}\n\nQuestion: {text}\nAnswer:"

    with llm.chat_session():
        response = llm.generate(prompt, max_tokens=200)

    return jsonify({'answer': response.strip()})


if __name__ == '__main__':
    app.run(debug=True)
