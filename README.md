# AI Review Analysis & RAG Chatbot

A beginner-friendly Python project that:

* Cleans customer reviews
* Detects owner responses
* Chunks reviews into AI-searchable pieces
* Stores embeddings in Pinecone
* Lets you ask questions about reviews using AI (RAG)

This project is designed for beginners learning:

* Python packages
* AI embeddings
* Retrieval-Augmented Generation (RAG)
* Pinecone vector databases
* OpenAI APIs

---

# What This Project Does

Imagine you have hundreds or thousands of customer reviews from:

* Google Reviews
* Yelp
* TripAdvisor
* etc.

This project helps you:

1. Clean the review data
2. Separate customer reviews from owner replies
3. Split reviews into smaller searchable chunks
4. Store them in Pinecone
5. Ask AI questions like:

   * "What do customers complain about most?"
   * "How do people feel about service speed?"
   * "What recurring food quality issues appear?"

The AI answers only using your review data.

---

# Project Structure

Your project should look like this:

```text
project_root/
│
├── app/
│   ├── __init__.py
│   ├── rag.py
│   ├── sentiment.py
│   ├── themes.py
│   └── util.py
│
├── scripts/
│   ├── __init__.py
│   ├── clean_reviews.py
│   ├── chunk_reviews.py
│   ├── index_pinecone.py
│   ├── query_bot.py
│   └── eval.py
│
├── data/
│   ├── raw_reviews.json
│   ├── cleaned_reviews.json
│   └── chunks.jsonl
│
├── .env
├── requirements.txt
└── README.md
```

---

# Step 1 — Install Python

Install Python 3.10 or newer.

Check if Python is installed:

```bash
python --version
```

or:

```bash
python3 --version
```

---

# Step 2 — Create a Virtual Environment

A virtual environment keeps project packages isolated.

## Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

After activation, your terminal should show:

```text
(venv)
```

---

# Step 3 — Install Dependencies

Create a `requirements.txt` file:

```text
python-dotenv
openai
pinecone
tiktoken
tqdm
nltk
```

Then install everything:

```bash
pip install -r requirements.txt
```

---

# Step 4 — Create a `.env` File

Create a file named:

```text
.env
```

Example:

```env
OPENAI_API_KEY=your_openai_key_here
PINECONE_API_KEY=your_pinecone_key_here

PINECONE_INDEX=reviews-index
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1

OPENAI_EMBED_MODEL=text-embedding-3-small

BUSINESS_NAME=My Restaurant
BUSINESS_LOCATION=New York
REVIEW_SOURCE=google
```

---

# Step 5 — Add Your Review Data

Put your raw reviews into:

```text
data/raw_reviews.json
```

Example format:

```json
[
  {
    "author": "John",
    "rating": 5,
    "text": "Amazing food and great service!",
    "date": "2025-01-01"
  }
]
```

---

# IMPORTANT — Why We Use `python -m`

This project uses imports like:

```python
from app.util import normalize_review
```

Because of this, you MUST run scripts using:

```bash
python -m
```

This tells Python:

> "Treat this project like a package."

Without `-m`, imports may fail.

---

# Step 6 — Clean the Reviews

Run:

```bash
python -m scripts.clean_reviews \
  --in data/raw_reviews.json \
  --out data/cleaned_reviews.json
```

What this script does:

* Normalizes review format
* Detects owner responses
* Cleans bad data
* Creates structured review records

Output:

```text
data/cleaned_reviews.json
```

---

# Step 7 — Chunk the Reviews

Run:

```bash
python -m scripts.chunk_reviews \
  --in data/cleaned_reviews.json \
  --out data/chunks.jsonl
```

What this does:

* Splits long reviews into smaller AI-searchable chunks
* Adds sentiment analysis
* Detects themes
* Creates metadata

Optional:
Include owner responses too:

```bash
python -m scripts.chunk_reviews \
  --in data/cleaned_reviews.json \
  --out data/chunks.jsonl \
  --include_owner
```

Output:

```text
data/chunks.jsonl
```

---

# Step 8 — Upload Embeddings to Pinecone

Run:

```bash
python -m scripts.index_pinecone \
  --chunks data/chunks.jsonl \
  --reset
```

What this does:

1. Converts text into embeddings using OpenAI
2. Creates a Pinecone vector index
3. Uploads vectors for semantic search

The `--reset` flag clears old vectors first.

---

# Step 9 — Ask Questions About Reviews

Run:

```bash
python -m scripts.query_bot \
  --q "What are the main customer complaints?"
```

Example questions:

```bash
python -m scripts.query_bot \
  --q "What do customers think about pricing?"
```

```bash
python -m scripts.query_bot \
  --q "Are there recurring complaints about cleanliness?"
```

---

# Debug Mode

To see retrieved chunks and grounding information:

```bash
python -m scripts.query_bot \
  --q "What are customers saying about service?" \
  --debug
```

---

# Step 10 — Run Evaluation Tests

Run:

```bash
python -m scripts.eval
```

This checks:

* Output structure
* AI grounding
* SMS formatting
* Required fields

Output:

```text
data/eval_results.jsonl
```

---

# Common Beginner Errors

## Error: `ModuleNotFoundError: No module named 'app'`

Cause:
You ran the script incorrectly.

Wrong:

```bash
python scripts/clean_reviews.py
```

Correct:

```bash
python -m scripts.clean_reviews
```

---

## Error: Missing API Keys

Cause:
Your `.env` file is missing or incorrect.

Fix:
Make sure:

```env
OPENAI_API_KEY=...
PINECONE_API_KEY=...
```

exist in `.env`.

---

## Error: `No module named dotenv`

Fix:

```bash
pip install python-dotenv
```

---

## Error: `chunks.jsonl is empty`

Cause:
The cleaning step failed or input reviews are empty.

Fix:
Run the cleaning script again and check output.

---

# What Is Pinecone?

Pinecone is a vector database.

Instead of searching keywords, it searches meaning.

Example:

* User asks:

  > "Do customers complain about slow service?"
* Pinecone finds semantically similar review chunks even if they do not use the exact words "slow service."

---

# What Is RAG?

RAG = Retrieval-Augmented Generation.

It works like this:

```text
User Question
      ↓
Find Relevant Review Chunks
      ↓
Send Chunks to AI
      ↓
Generate Grounded Answer
```

This prevents hallucinations because the AI answers using your real review data.

---

# Recommended Beginner Workflow

Run these in order:

## 1. Clean reviews

```bash
python -m scripts.clean_reviews \
  --in data/raw_reviews.json \
  --out data/cleaned_reviews.json
```

## 2. Chunk reviews

```bash
python -m scripts.chunk_reviews \
  --in data/cleaned_reviews.json \
  --out data/chunks.jsonl
```

## 3. Index into Pinecone

```bash
python -m scripts.index_pinecone \
  --chunks data/chunks.jsonl \
  --reset
```

## 4. Query the chatbot

```bash
python -m scripts.query_bot \
  --q "What issues appear most often?"
```

---

# Recommended Improvements

As you learn more, you can add:

* FastAPI backend
* Streamlit frontend
* LangChain
* Better theme classification
* Better evaluation metrics
* Multi-business support
* Dashboard UI
* Automated review scraping

---

# Final Notes

This project teaches real-world AI engineering concepts:

* embeddings
* vector databases
* semantic search
* RAG pipelines
* AI grounding
* data preprocessing

If you are a beginner:

* Start slowly
* Run one script at a time
* Print intermediate outputs
* Read the JSON files to understand the data flow

That is how real AI systems are built.
