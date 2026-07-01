# SHL AI Conversational Assessment Recommender

## Overview

This project is a Conversational AI system that recommends SHL Individual Test Solutions based on user requirements. The application uses FastAPI, Retrieval-Augmented Generation (RAG), and Google Gemini to provide accurate and grounded assessment recommendations.

The assistant asks clarifying questions, retrieves relevant assessments from the SHL catalog, supports refinement of recommendations when user requirements change, and compares assessments using catalog data.

---

## Features

- FastAPI REST API
- GET /health endpoint
- POST /chat endpoint
- Conversational recommendation system
- Clarifying questions for vague requests
- SHL assessment recommendations
- Multi-turn conversation support
- Assessment comparison
- Remote assessment filtering
- Off-topic query handling
- Google Gemini integration
- Retrieval-Augmented Generation (RAG)

---

## Project Structure

```
shl-ai-recommender/
│
├── app.py
├── chatbot.py
├── retriever.py
├── gemini.py
├── scraper.py
├── utils.py
├── catalog.json
├── requirements.txt
├── README.md
├── .env
```

---

## Technologies Used

- Python 3.11+
- FastAPI
- Google Gemini API
- Retrieval-Augmented Generation (RAG)
- JSON Knowledge Base
- Uvicorn

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/shl-ai-recommender.git
cd shl-ai-recommender
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Run the Application

```bash
uvicorn app:app --reload
```

The application runs at:

```
http://127.0.0.1:8000
```

---

# API Endpoints

## Health Check

### GET

```
/health
```

Response

```json
{
    "status":"ok"
}
```

---

## Chat Endpoint

### POST

```
/chat
```

Example Request

```json
{
    "messages":[
        {
            "role":"user",
            "content":"I need assessments for a Java Developer."
        }
    ]
}
```

Example Response

```json
{
    "reply":"Here are the recommended SHL assessments.",
    "recommendations":[
        {
            "name":"Java 8 (New)",
            "url":"https://www.shl.com/...",
            "test_type":"Knowledge"
        }
    ],
    "end_of_conversation":false
}
```

---

## Conversational Features

The assistant supports:

- Clarifying vague user requests
- Assessment recommendations
- Multi-turn conversations
- Refinement based on changing requirements
- Assessment comparison
- SHL catalog grounded responses

---

## Retrieval Pipeline

1. Receive user request.
2. Search SHL catalog.
3. Retrieve relevant assessments.
4. Send retrieved data to Gemini.
5. Generate grounded recommendation.
6. Return structured JSON response.

---

## Evaluation

The project evaluates recommendation quality using:

- Retrieval Quality
- Recommendation Relevance
- Groundedness
- Response Accuracy
- Recall@10

---

## Future Improvements

- FAISS Vector Search
- ChromaDB Integration
- LangChain Support
- Better Ranking Algorithm
- Semantic Search
- Conversation Memory
- Hybrid Retrieval

---
