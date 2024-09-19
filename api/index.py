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
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure your Google Generative AI API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=api_key)

def clean_summary(summary):
    """Clean the summary text by removing special formatting characters and ensuring proper newlines."""
    cleaned_summary = summary.replace('*', '').replace('•', '').strip()
    return "\n".join(line.strip() for line in cleaned_summary.split('\n') if line.strip())

@app.route('/upload', methods=['POST'])
def upload_and_summarize():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.lower().endswith('.pdf'):
        try:
            # Read the file in-memory without storing it
            pdf_bytes = file.read()
            pdf_stream = io.BytesIO(pdf_bytes)

            # Prepare the file as a Blob object expected by the API
            sample_file = {
                "mime_type": "application/pdf",  # Set the correct MIME type for PDFs
                "data": pdf_stream.getvalue()    # Pass the raw binary content
            }

        except Exception as e:
            app.logger.error(f"Error reading in-memory file: {e}")
            return jsonify({"error": f"Error reading file: {e}"}), 500

        # Choose a Gemini model
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        # Generate content based on the in-memory PDF data
        try:
            # Pass the prepared Blob as the input
            response = model.generate_content([sample_file, "Summarize this document in plain text without any special formatting like bold or italic."])
            summary = response.text
            cleaned_summary = clean_summary(summary)
            return jsonify({"summary": cleaned_summary})
        except Exception as e:
            app.logger.error(f"Error generating summary: {e}")
            return jsonify({"error": f"Error generating summary: {e}"}), 500

    return jsonify({"error": "Invalid file format. Only PDFs are allowed."}), 400
