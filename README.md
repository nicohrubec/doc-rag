# Doc-RAG: Document Retrieval-Augmented Generation System

## Overview
Doc-RAG is a specialized question-answering system that uses Retrieval-Augmented Generation (RAG) to provide accurate answers about technical software documentation. The system currently supports two tools:
- ArchiCAD
- RFEM

## Architecture

The system consists of three main components:

1. **Frontend Service** (Port 9000)
   - Web interface for user interactions
   - Built with Flask and simple HTML/CSS
   - Communicates with backend service via REST API

2. **Backend Service** (Port 8000)
   - Core RAG implementation
   - Handles document embedding and retrieval
   - Integrates with OpenAI for response generation
   - Uses Pinecone for vector storage

3. **ETL Pipeline**
   - Processes PDF documentation
   - Generates embeddings using sentence-transformers
   - Indexes documents in Pinecone database

## Prerequisites

- Python 3.9
- Docker and Docker Compose
- Pinecone API credentials
- OpenAI API key

## Running the application

1. Create a `.env` file in the root directory with:

```
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_pinecone_environment
OPENAI_API_KEY=your_openai_key
```

2. Run using docker compose:

```
docker compose up --build
```

This will start the frontend and backend services. The frontend can then be accessed at `http://localhost:9000`.


## Adding new Documents

To add new documentation:

1. Place PDF documentation in the `docs` directory
2. Run the ETL process:

```
python3 etl.py <pdf_path> <tool_name>
```

Where `tool_name` is currently either `archicad` or `rfem`. This will extract the text from the PDF and embed it using sentence-transformers. The embeddings are then stored in Pinecone.

## System Components

### Frontend
- Simple web interface with tool selection
- Chat-like interface for questions and answers

### Backend
- API endpoint for processing queries
- Vector similarity search using Pinecone
- Context-aware response generation using GPT-3.5-turbo
- Sentence transformer embeddings (all-MiniLM-L6-v2)

### ETL Pipeline
- PDF text extraction using PyMuPDF
- Text chunking with sentence splitting
- Document embedding generation
- Vector database indexing
