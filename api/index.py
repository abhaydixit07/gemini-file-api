from flask import Flask, request, jsonify
import io
import google.generativeai as genai
from flask_cors import CORS
from PyPDF2 import PdfFileReader
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure your Google Generative AI API key from the environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    text = ""
    try:
        reader = PdfFileReader(io.BytesIO(file.read()))
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text.strip()

def clean_summary(summary):
    """Clean the summary text by removing special formatting characters and ensuring proper newlines."""
    # Remove unwanted characters like asterisks or bullet points
    cleaned_summary = summary.replace('*', '').replace('•', '').strip()
    
    # Ensure proper newlines
    return "\n".join(line.strip() for line in cleaned_summary.split('\n') if line.strip())

@app.route('/')
def home():
    return "Welcome to the PDF Summarization API!"

@app.route('/upload', methods=['POST'])
def upload_and_summarize():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.lower().endswith('.pdf'):
        try:
            # Upload the file to Google Generative AI API directly from memory
            sample_file = genai.upload_file(file.stream, display_name=file.filename)
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
    app.run(debug=True, port=5000)
