from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
from PyPDF2 import PdfFileReader
import io
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure your Google Generative AI API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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
            # Read the file into memory
            pdf_bytes = file.read()

            # Upload in-memory file content to Google Generative AI
            sample_file = genai.upload_file(file_content=pdf_bytes, display_name=file.filename)
        except Exception as e:
            return jsonify({"error": f"Error uploading file: {e}"}), 500

        # Choose a Gemini model
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        # Generate content based on the uploaded PDF
        try:
            response = model.generate_content([sample_file, "Summarize this document in plain text without any special formatting like bold or italic."])
            summary = response.text
            cleaned_summary = clean_summary(summary)
            return jsonify({"summary": cleaned_summary})
        except Exception as e:
            return jsonify({"error": f"Error generating summary: {e}"}), 500

    return jsonify({"error": "Invalid file format. Only PDFs are allowed."}), 400

if __name__ == '__main__':
    app.run(debug=True, port=3000)
