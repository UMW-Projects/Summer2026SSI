# Review Intelligence RAG Pipeline

A retrieval-augmented review analysis system for extracting operational insights from customer feedback using semantic search, embeddings, sentiment analysis, and grounded LLM responses.

This project processes raw review data, detects owner responses, chunks and enriches review text, indexes embeddings in Pinecone, and exposes a query interface for grounded business intelligence.

---

# Features

* Review normalization and cleaning
* Owner-response detection
* Token-aware chunking
* Theme extraction
* Sentiment scoring
* OpenAI embeddings
* Pinecone vector indexing
* Retrieval-Augmented Generation (RAG)
* Grounded response generation
* Evaluation pipeline with schema validation

---

# Architecture Overview

```text id="x2m4zi"
Raw Reviews JSON
       │
       ▼
clean_reviews.py
       │
       ▼
Normalized Reviews
       │
       ▼
chunk_reviews.py
       │
       ▼
Enriched JSONL Chunks
(sentiment + themes + metadata)
       │
       ▼
index_pinecone.py
       │
       ▼
Pinecone Vector Index
       │
       ▼
query_bot.py
       │
       ▼
Grounded LLM Responses
```

---

# Project Structure

```text id="16svyc"
project_root/
│
├── app/
│   ├── rag.py
│   ├── sentiment.py
│   ├── themes.py
│   ├── util.py
│   └── ...
│
├── scripts/
│   ├── clean_reviews.py
│   ├── chunk_reviews.py
│   ├── index_pinecone.py
│   ├── query_bot.py
│   └── eval.py
│
├── data/
│   ├── raw_reviews.json
│   ├── cleaned_reviews.json
│   ├── chunks.jsonl
│   └── eval_results.jsonl
│
├── .env
├── requirements.txt
└── README.md
```

---

# Pipeline Stages

## 1. Review Cleaning

Script:

```bash id="x4upz0"
python -m scripts.clean_reviews
```

Purpose:

* Normalizes inconsistent review records
* Separates owner responses from customer reviews
* Adds canonical metadata
* Filters malformed records

Input:

* Raw scraped review JSON

Output:

* Structured review records

Key behaviors:

* heuristic owner-response detection
* stable review IDs
* parent-child linkage for owner replies

---

## 2. Chunking + Enrichment

Script:

```bash id="d65l9m"
python -m scripts.chunk_reviews
```

Purpose:

* Splits reviews into embedding-friendly chunks
* Adds sentiment analysis
* Detects operational themes
* Produces retrieval-ready JSONL

Enrichment includes:

* sentiment labels
* token counts
* theme hits
* owner-response classification
* metadata preservation

Chunking uses:

* `tiktoken`
* overlap-aware segmentation
* deterministic filtering

---

## 3. Embedding + Pinecone Indexing

Script:

```bash id="k7zvmv"
python -m scripts.index_pinecone
```

Purpose:

* Generates OpenAI embeddings
* Creates/updates Pinecone index
* Stores vectors with metadata

Embedding model:

```text id="4ln51f"
text-embedding-3-small
```

Stored metadata includes:

* review IDs
* sentiment
* themes
* dates
* source
* owner-response flags
* original chunk text

---

## 4. Grounded Querying

Script:

```bash id="g4n2pa"
python -m scripts.query_bot
```

Purpose:

* Retrieves semantically relevant review chunks
* Filters and aggregates evidence
* Generates grounded responses using retrieved context

Example queries:

* “What recurring complaints exist around service speed?”
* “How do customers feel about pricing?”
* “Are cleanliness concerns recurring?”

Outputs:

* answer summaries
* recurring issues
* operational recommendations
* evidence-linked themes
* SMS-ready drafts

---

## 5. Evaluation

Script:

```bash id="95n4lq"
python -m scripts.eval
```

Purpose:

* Validates response schema
* Verifies grounding integrity
* Checks output constraints
* Tests recurring issue extraction

Validation includes:

* chunk grounding checks
* schema consistency
* SMS length validation
* evidence integrity

---

# Environment Setup

## Python Version

Recommended:

```text id="bxu1c0"
Python 3.10+
```

---

## Virtual Environment

### macOS / Linux

```bash id="wr7c4l"
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash id="ylxow6"
python -m venv venv
venv\Scripts\activate
```

---

# Installation

Install dependencies:

```bash id="9vrwfy"
pip install -r requirements.txt
```

Example `requirements.txt`:

```text id="7h0t2p"
python-dotenv
openai
pinecone
tiktoken
tqdm
nltk
```

---

# Environment Variables

Create a `.env` file:

```env id="izj95l"
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key

PINECONE_INDEX=reviews-index
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1

OPENAI_EMBED_MODEL=text-embedding-3-small

BUSINESS_NAME=Example Business
BUSINESS_LOCATION=New York
REVIEW_SOURCE=google
```

---

# Running the Pipeline

## Step 1 — Clean Reviews

```bash id="hn5q5u"
python -m scripts.clean_reviews \
  --in data/raw_reviews.json \
  --out data/cleaned_reviews.json
```

---

## Step 2 — Chunk Reviews

```bash id="6uhc0e"
python -m scripts.chunk_reviews \
  --in data/cleaned_reviews.json \
  --out data/chunks.jsonl
```

---

## Step 3 — Index Embeddings

```bash id="n4wn86"
python -m scripts.index_pinecone \
  --chunks data/chunks.jsonl \
  --reset
```

---

## Step 4 — Query the System

```bash id="yq4o3q"
python -m scripts.query_bot \
  --q "What operational issues recur most frequently?"
```

---

# Why the Project Uses `python -m`

The project imports internal modules using package-style imports:

```python id="2u3vut"
from app.util import normalize_review
```

To ensure Python resolves imports correctly, scripts must be executed as modules from the project root.

Correct:

```bash id="l7w2q8"
python -m scripts.chunk_reviews
```

Incorrect:

```bash id="gbskk0"
python scripts/chunk_reviews.py
```

Using `-m` ensures:

* package-relative imports work correctly
* the project root is added to Python’s module path
* scripts behave consistently across environments

---

# Design Notes

## Why JSONL for Chunks?

JSONL allows:

* streaming reads
* large dataset scalability
* append-friendly processing
* line-by-line embedding workflows

---

## Why Separate Owner Responses?

Owner replies can distort:

* sentiment analysis
* complaint frequency
* operational theme detection

The pipeline isolates them while preserving parent relationships.

---

## Why Chunk Reviews?

Embedding entire reviews reduces retrieval quality.

Chunking improves:

* semantic precision
* retrieval granularity
* context relevance
* grounding accuracy

---

# Future Extensions

Potential roadmap items:

* FastAPI service layer
* streaming responses
* dashboard/UI
* hybrid keyword + vector search
* reranking
* multi-tenant indexing
* review ingestion pipelines
* temporal trend analysis
* automated alerting

---

# Notes

This repository focuses on:

* grounded generation
* deterministic preprocessing
* retrieval quality
* operational explainability

The pipeline is intentionally modular so components can be replaced independently:

* embedding model
* vector database
* chunking strategy
* sentiment engine
* retrieval logic
* LLM provider
