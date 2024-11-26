# Gemini File API

The **Gemini File API** is a powerful service designed to process and generate summaries from PDF documents and extract text from images. Built with Flask, it integrates seamlessly with Google's Generative AI API (Gemini 1.5) to summarize content from documents or generate text from image-based content like scanned text or handwritten notes.

This API supports secure file uploads and ensures that only authorized requests are processed using a secret token. It is capable of handling both **PDF files** for content summarization and **image files** (PNG, JPG, JPEG) for text extraction.

---

## Features

- **PDF Summarization**: Upload PDF files, and the API will return a cleaned summary of the document.
- **Image Text Extraction**: Upload images in formats like PNG, JPG, or JPEG, and the API will extract text from the image.
- **Secure Access**: Authentication using a secret token to ensure authorized access.
- **Error Handling**: Clear error messages for invalid file types or issues during processing.

---

## Tech Stack

- **Python**: Backend language powering the API.
- **Flask**: Web framework for building the API.
- **Google Gemini 1.5**: AI model used for content generation and summarization.
- **Flask-CORS**: Cross-Origin Resource Sharing support for secure API interaction.
- **dotenv**: For environment variable management.
- **Logging**: Integrated logging for debugging and tracking API usage.

---

## API Endpoints

### 1. **Upload and Summarize PDF**
**Endpoint**: `/upload`  
Upload a PDF file and get a summarized version of its content.

- **Method**: `POST`
- **URL**: `/upload`
  
#### Request Body
```json
{
  "file": "PDF_FILE",
  "Authorization": "Bearer <SECRET_TOKEN>"
}
```

#### Response Example
```json
{
  "summary": "This is a summarized version of the PDF document..."
}
```

---

### 2. **Upload and Process Image**
**Endpoint**: `/upload-image`  
Upload an image file and get the extracted text content from the image.

- **Method**: `POST`
- **URL**: `/upload-image`

#### Request Body
```json
{
  "file": "IMAGE_FILE",
  "Authorization": "Bearer <SECRET_TOKEN>"
}
```

#### Response Example
```json
{
  "text": "Extracted text from the image..."
}
```

---

## Installation and Local Deployment

### Prerequisites

- Python installed on your machine.
- Google Cloud API credentials for **Generative AI** (Gemini 1.5).

### Steps to Run Locally

1. **Clone the repository**:
   ```bash
   cd gemini-file-api
   ```

2. **Create a `.env` file** in the root directory and add your environment variables:
   ```env
   GOOGLE_API_KEY=<Your_Google_Generative_AI_API_Key>
   SECRET_TOKEN=<Your_Secret_Token>
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**:
   ```bash
   python api/index.py
   ```

5. The server will be running locally on `http://127.0.0.1:5000`. You can use tools like **Postman** or **cURL** to test the endpoints.

---

## Example Scenarios

1. **Document Summarizer**: Use the `/upload` endpoint to upload PDF files and generate summarized content.
2. **Image Text Extraction**: Use the `/upload-image` endpoint to process images and extract text, perfect for scanning documents or OCR tasks.

---

## Contribution Guidelines

We welcome contributions! Here’s how you can get involved:
1. Fork the repository.
2. Create a new branch (`feature-name` or `bugfix-name`).
3. Commit your changes.
4. Submit a pull request with a detailed description.

---

## License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute it in accordance with the license terms.


The **AyurGuru Frontend** repository is the user interface of the AyurGuru platform. It provides a seamless, interactive experience for users to engage with Ayurvedic content, submit documents, and receive AI-powered insights. This frontend application works in harmony with the **AyurGuru Flask API** for document summarization and image text extraction, enabling users to easily interact with the platform's features.

You can find the **AyurGuru** repository here:  
[**AyurGuru Frontend**](https://github.com/abhaydixit07/ayurguru-frontend)
