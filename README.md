Bajaj Health Datathon - Intelligent Bill Extraction Pipeline

This repository contains the solution for the Bajaj Health Datathon. It implements an AI-powered pipeline to extract line item details, rates, quantities, and amounts from multi-page medical and retail invoices while reconciling totals and preventing double-counting.

🚀 Approach

1. Architecture

We utilize a Generative AI approach rather than traditional OCR (Tesseract) + Regex. Traditional OCR struggles with the high variance in table structures across different pharmacy and hospital bills.

Framework: FastAPI (High performance, easy async support).

AI Engine: Google Gemini 1.5 Flash.

Image Processing: pdf2image & PIL.

2. Why Gemini 1.5 Flash?

Multimodal Reasoning: It can "see" the bill structure (headers, columns, footers) just like a human, handling skewed scans or complex layouts natively.

Long Context Window: We feed all pages of a PDF simultaneously. This allows the model to understand that Page 3 is a "Summary" of Page 1 and 2, allowing it to logically exclude summary rows from the line-item extraction to prevent double counting.

Structured Output: We enforce a JSON Schema in the generation config, ensuring the API always returns the exact format required by the problem statement.

3. Logic Flow

Ingestion: Download the document URL (PDF or Image).

Preprocessing: Convert PDF pages into a list of high-quality images.

Inference:

Send the images + a system prompt to Gemini.

The prompt instructs the model to iterate pagewise, categorize the page (Pharmacy/Bill Detail/Final Bill), and extract row items.

Double Count Logic: The prompt explicitly forbids extracting "Category Totals" as line items if those items were detailed on previous pages.

Validation: Parse the returned JSON into Pydantic models to ensure type safety (floats, integers).

Response: Return the standardized JSON response with token usage metrics.

🛠️ Setup & Installation

Prerequisites

Docker (Recommended)

Or: Python 3.10+ and poppler-utils installed on your machine.

Google Gemini API Key.

Method 1: Docker (Recommended)

Clone the repo.

Create a .env file containing your API key:

GOOGLE_API_KEY=your_actual_api_key_here


Build and Run:

docker build -t bill-extractor .
docker run -p 8000:8000 --env-file .env bill-extractor


Method 2: Local Run

Install Poppler (Linux: sudo apt-get install poppler-utils, Mac: brew install poppler).

Install Python dependencies:

pip install -r requirements.txt


Set API Key:

export GOOGLE_API_KEY="your_key"


Run Server:

python main.py


📡 API Usage

Endpoint: POST /extract-bill-data

Request Body:

{
    "document": "[https://path-to-your-document.pdf](https://path-to-your-document.pdf)"
}


Response:
Returns is_success, token_usage, and the extracted data strictly adhering to the Datathon schema.


## ⚖️ Evaluation & Accuracy
The model is tuned to maximize **Reconciliation Accuracy**. By classifying pages as "Bill Detail" vs "Final Bill", we isolate granular items from summary totals, ensuring that $\sum \text{Line Items} \approx \text{Actual Bill Total}$.
