from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
import io

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure your Google Generative AI API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=api_key)

# Define the secret token (in a real application, store this securely)
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

def clean_summary(summary):
    """Clean the summary text by removing special formatting characters and ensuring proper newlines."""
    cleaned_summary = summary.replace('*', '').replace('•', '').strip()
    return "\n".join(line.strip() for line in cleaned_summary.split('\n') if line.strip())

def clean_text(text):
    """Clean the text by removing special formatting characters and ensuring proper newlines."""
    cleaned_text = text.replace('*', '').strip()
    return "\n".join(line.strip() for line in cleaned_text.split('\n') if line.strip())

@app.route('/')
def home():
    return "Hello World"

@app.route('/upload', methods=['POST'])
def upload_and_summarize():
    token = request.headers.get('Authorization')
    if token != f"Bearer {SECRET_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 403

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.lower().endswith('.pdf'):
        try:
            pdf_bytes = file.read()
            pdf_stream = io.BytesIO(pdf_bytes)

            sample_file = {
                "mime_type": "application/pdf",
                "data": pdf_stream.getvalue()
            }

        except Exception as e:
            app.logger.error(f"Error reading in-memory file: {e}")
            return jsonify({"error": f"Error reading file: {e}"}), 500

        model = genai.GenerativeModel(model_name="gemini-2.5-pro")

        try:
            response = model.generate_content([sample_file, "Summarize this document in plain text without any special formatting like bold or italic."])
            summary = response.text
            cleaned_summary = clean_summary(summary)
            return jsonify({"summary": cleaned_summary})
        except Exception as e:
            app.logger.error(f"Error generating summary: {e}")
            return jsonify({"error": f"Error generating summary: {e}"}), 500

    return jsonify({"error": "Invalid file format. Only PDFs are allowed."}), 400

@app.route('/upload-image', methods=['POST'])
def upload_and_process_image():
    token = request.headers.get('Authorization')
    if token != f"Bearer {SECRET_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 403

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    mime_type = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg"
    }.get(os.path.splitext(file.filename)[1].lower(), "image/png")

    if file and os.path.splitext(file.filename)[1].lower() in ('.png', '.jpg', '.jpeg'):
        try:
            image_bytes = file.read()
            image_stream = io.BytesIO(image_bytes)

            sample_file = {
                "mime_type": mime_type,
                "data": image_stream.getvalue()
            }

        except Exception as e:
            app.logger.error(f"Error reading in-memory file: {e}")
            return jsonify({"error": f"Error reading file: {e}"}), 500

        model = genai.GenerativeModel(model_name="gemini-2.5-pro")

        try:
            response = model.generate_content([sample_file, "Give the text written in it."])
            text = response.text
            cleaned_text = clean_text(text)
            return jsonify({"text": cleaned_text})
        except Exception as e:
            app.logger.error(f"Error generating text from image: {e}")
            return jsonify({"error": f"Error generating text: {e}"}), 500

    return jsonify({"error": "Invalid file format. Only PNG, JPG, and JPEG images are allowed."}), 400


