# Autonomous Research Agent

A full-stack research and analytics platform that combines GPT-style conversational Q&A with tool-backed retrieval, multi-modal RAG, and automated report generation.

This project supports three primary user workflows:
- **Chat**: answer general and domain-specific questions using an LLM, with tool support for external research when needed.
- **RAG**: upload documents and ask questions over text, images, tables, PDFs, Word, Excel, PPTX, and CSV files.
- **Research**: generate structured analytical reports from a single prompt, with evidence synthesis from multiple sources.

Built for enterprise-style research, this system uses a planner-executor LangGraph agent, a FastAPI REST backend, and a polished React 19 + TypeScript frontend.

---

## 📋 Table of Contents

- [Problem Statement](#problem-statement)
- [What is the Project?](#what-is-the-project)
- [How it Works](#how-it-works)
- [Objectives](#objectives)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)

---

## Problem Statement

The organization requires an AI system capable of conducting structured research tasks and generating comprehensive analytical reports autonomously.

The system must decompose tasks, retrieve relevant information from multiple sources, synthesize findings, and produce structured reports.

---

## What is the Project?

The **Autonomous Research Agent** is an intelligent research platform that combines conversational Q&A, multi-source retrieval, document-driven RAG, and report generation.

It can act as a chat assistant for general questions, use external tools and search APIs when needed, and answer questions grounded in uploaded documents.

The platform also supports full research workflows that create downloadable analytical reports from user prompts.

This repository includes a FastAPI REST backend, a React 19 + TypeScript frontend with Tailwind CSS v4, shadcn/ui components, TanStack Start, and a document ingestion pipeline for multi-format content.

---

## How it Works

- **Chat Mode**: users ask questions and receive LLM-generated answers. The agent can optionally leverage external tools for improved factual accuracy.
- **RAG Mode**: users upload documents and query them directly. The system retrieves relevant content from indexed documents and answers using both retrieval and LLM synthesis.
- **Research Mode**: users submit a research prompt, then the LangGraph workflow plans, retrieves, synthesizes, and writes a structured report.

The agent maintains reasoning state across steps and supports multi-modal content such as images, tables, and text.

---

## Objectives

- Implement a multi-stage LangGraph workflow
- Integrate RAG for research document retrieval with multi-modal support
- Enable document upload and domain-aware answers from uploaded files
- Maintain state across reasoning steps
- Generate structured research reports
- Build a FastAPI REST backend
- Develop a frontend interface using React 19 + TypeScript, Tailwind CSS v4, shadcn/ui, and TanStack Start

---

## Features

### 🧠 Multi-Stage Agent Workflow
- Planner-executor architecture implemented with **LangGraph**
- Nodes for planning, research, synthesis, and report writing
- Maintains state across each reasoning step via shared graph state
- Automates tool selection and route execution for research tasks

### 🔍 Multi-Modal RAG Research
- **RAG** with semantic retrieval from a Chroma vector store
- Supports **text documents, scanned PDFs, images, tables, Word, Excel, PPTX, CSV**
- Document upload + indexing pipeline with:
  - OCR for images and scanned PDFs
  - Table extraction
  - Image understanding and captioning
  - Chunking and semantic embeddings
- Query documents directly through the frontend with source-aware answers

### 🌐 Multi-Source Retrieval
- Integrated search tools for multiple external sources:
  - **DuckDuckGo** for general web search
  - **Arxiv** for academic papers
  - **Wikipedia** for factual knowledge
  - **Tavily** for advanced search capabilities
- Uses tool-based retrieval to collect diverse evidence before synthesis

### 💬 Conversational Research Interface
- Session-based chat for follow-up questions and contextual research
- Manage multiple sessions and conversation history
- Chat API that routes queries through the research agent

### 📑 Report Generation
- Generate structured research reports from natural language prompts
- Save reports as **PDF** and **DOCX**
- Download generated reports from the frontend
- Reports include synthesized analysis and source references

### 📂 Document Management
- Upload documents from the browser
- View indexed documents in a document library
- Delete uploaded documents and regenerate indexes
- Ask questions against uploaded documents using RAG

---

## Architecture

### Backend
- **FastAPI** REST API with endpoints for:
  - `/api/chat` — conversational chat sessions
  - `/api/rag/upload` — document upload and processing
  - `/api/rag/query` — RAG-powered document query
  - `/api/rag/documents` — list/delete document metadata
  - `/api/reports/generate-report` — generate research reports
  - `/api/sessions` — manage chat sessions
- **LangGraph** workflow in `backend/agents/graph.py` with planner, researcher, synthesizer, and report_writer nodes
- **RAG pipeline** in `backend/rag/` for ingestion, embeddings, retrieval, and multi-modal document understanding
- **Persistent state** via MongoDB repositories for chat sessions, documents, messages, and reports
- **Report generation** using ReportLab and python-docx in `backend/storage/reports`

### Frontend
- Built with **React + TypeScript** and **Vite**
- Uses **TanStack Router** for page navigation and **React Query** for data fetching
- Includes dedicated UI pages for:
  - Research report generation
  - Document upload and RAG querying
  - Chat sessions and conversational research
- Provides file upload, query input, result preview, and report download

---

## Technologies

### Backend
- **Framework**: FastAPI
- **Agent orchestration**: LangGraph
- **Database**: MongoDB
- **Vector DB**: Chroma
- **Embeddings**: HuggingFaceEmbeddings (BAAI/bge-large-en-v1.5)
- **LLM provider**: Groq via `langchain-groq`
- **Document processing**:
  - PDF, DOCX, PPTX, XLSX, CSV, image loaders
  - OCR and scanned PDF handling
  - Table extraction and chunk creation
  - Image understanding and caption generation
- **Search APIs**: DuckDuckGo, Arxiv, Wikipedia, Tavily
- **Report export**: ReportLab, python-docx

### Frontend
- **Framework**: React + TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **Routing**: TanStack Router
- **Data fetching**: React Query
- **UI primitives**: shadcn/ui

---

## Getting Started

### ▶️ Local Development

1. Start the backend:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

2. Start the frontend:
```bash
cd frontend
npm install
npm run dev
```

3. Access the application:
   - Frontend: http://localhost:5173
   - API Docs: http://localhost:8000/docs

### Backend Setup

1. Create a Python virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_key
MODEL_NAME=gpt-4-turbo
TAVILY_API_KEY=your_tavily_key
MONGODB_URI=mongodb://localhost:27017
```

### Frontend Setup

1. Navigate to the frontend folder:
```bash
cd frontend
```

2. Install dependencies and run the dev server:
```bash
npm install
npm run dev
```

---

## Screenshots

> Add screenshots for:
> - Research report generation
> - Document upload and indexing
> - RAG query results with source citations
> - Chat session interaction
> - Report downloads

---

## Architecture Notes

Project structure:

```
autonomous-research-agent/
├── backend/              # FastAPI application
│   ├── agents/          # LangGraph workflow definitions
│   ├── api/             # REST endpoints
│   ├── core/            # app configuration and logging
│   ├── database/        # MongoDB repository layer
│   ├── rag/             # multi-modal retrieval and ingestion pipeline
│   ├── services/        # business logic and orchestration
│   ├── storage/         # file and report exporters
│   └── tools/           # external tool adapters
├── frontend/            # React + Vite + TypeScript UI
│   └── src/
│       ├── components/  # reusable UI components
│       ├── routes/      # page routes and views
│       ├── hooks/       # custom React hooks
│       └── lib/         # API client and utilities
```

---

## Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=gpt-4-turbo
TAVILY_API_KEY=your_tavily_key
MONGODB_URI=mongodb://localhost:27017
```

# Database
MONGODB_URI=mongodb://mongo:27017
MONGO_DB_NAME=research_agent

# Chroma Vector DB
CHROMA_HOST=chroma
CHROMA_PORT=8000

# Server
DEBUG=false
```

> ⚠️ **Security**: Never commit `.env` files. Use your orchestration system or secret management service in production.

---

## Common Issues & Troubleshooting

### PDF/Image Processing Issues
Some Python packages (PyMuPDF, Tesseract, EasyOCR) require system-level dependencies. Install the required system packages on your machine for full feature support.

### MongoDB Connection Issues
Ensure MongoDB is running and accessible at the configured URI.

### API Key Configuration
All API keys (OpenAI, Tavily, etc.) must be set in environment variables before starting the application.

---

## Contributing

Contributions are welcome! Please ensure:
- Code follows project conventions
- API documentation is updated
- New features include appropriate error handling
- Environment setup is documented

---

## License

See [LICENSE](LICENSE) file for details.
