# Autonomous Research Agent

A full-stack intelligent research platform that combines conversational AI with autonomous research capabilities. The agent can search the web, access academic databases, process documents, and generate comprehensive reports through an intuitive chat interface.

---

## 📋 Table of Contents

- [What is the Project?](#what-is-the-project)
- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)

---

## What is the Project?

The **Autonomous Research Agent** is an intelligent research platform designed to help users conduct comprehensive research through a conversational interface. It combines multiple data sources, document processing capabilities, and AI-powered synthesis to deliver detailed research reports and answers.

The system uses an agentic workflow that:
- Understands user queries and research intent
- Plans and executes research strategies autonomously
- Processes multiple document formats and sources
- Synthesizes findings into coherent reports
- Maintains conversation history for contextual research

---

## Features

### 🔍 **Multi-Source Research**
- **Web Search**: DuckDuckGo integration for real-time web results
- **Academic Research**: Arxiv integration for academic papers
- **News & Knowledge**: Wikipedia integration for reference data
- **Advanced Search**: Tavily search with enhanced capabilities

### 📄 **Document Processing**
- Support for **multiple formats**: PDF, Word, Excel, PowerPoint, CSV, images
- **Optical Character Recognition (OCR)**: Extract text from scanned PDFs and images
- **Table Extraction**: Intelligently parse and extract data from tables
- **Image Understanding**: Analyze and understand content in images
- **Automatic Chunking**: Smart document segmentation for better context retrieval

### 💬 **Intelligent Chat Interface**
- Conversational research interface
- Real-time streaming responses
- Context-aware follow-up questions
- Session-based conversation history

### 📊 **Report Generation**
- Auto-generate research reports from findings
- **Multi-format export**: PDF and DOCX formats
- Structured report with sources and citations
- Rich formatting and professional styling

### 🗂️ **Document Management**
- Upload and manage research documents
- Vector-based document search with semantic understanding
- Retrieval-Augmented Generation (RAG) for context enhancement
- Persistent storage and indexing

### 🤖 **Agentic Workflow**
- **Intelligent Routing**: Routes queries to appropriate tools and resources
- **Planning**: Develops research strategies before execution
- **Tool Execution**: Orchestrates multiple tools and data sources
- **Synthesis**: Combines findings into coherent responses

### 🧮 **Additional Tools**
- Built-in calculator for data analysis
- Extensible tool registry for custom tools

---

## Technologies

### Backend
- **Framework**: FastAPI (async Python web framework)
- **AI/ML**: LangChain, LLMs with streaming support
- **Database**: MongoDB (document storage & metadata)
- **Vector DB**: Chroma (semantic search & embeddings)
- **Document Processing**: 
  - PyMuPDF for PDF extraction
  - python-docx for Word documents
  - openpyxl for Excel
  - python-pptx for PowerPoint
  - pytesseract for OCR
  - Pillow for image processing
- **Search APIs**: DuckDuckGo, Tavily, Arxiv, Wikipedia
- **Task Management**: LangGraph (agentic workflows)

### Frontend
- **Framework**: React with TypeScript
- **Build Tool**: Vite (fast development server)
- **Styling**: TailwindCSS
- **Components**: shadcn/ui (accessible component library)
- **Routing**: TanStack Router

### DevOps
- **Static File Serving**: aiofiles for async file serving

---

## Getting Started

### ▶️ Local Development

1. **Start the backend**:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

2. **Start the frontend**:
```bash
cd frontend
npm install
npm run dev
```

3. **Access the application**:
   - Frontend: http://localhost:5173
   - API Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### 💻 Local Development Setup

#### Backend Only

1. **Create virtual environment**:
```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .\venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables** (create `.env`):
```env
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
MONGODB_URI=mongodb://localhost:27017
```

4. **Run the backend**:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

#### Frontend Only

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Start development server**:
```bash
npm run dev
```

Frontend will be available at: http://localhost:5173

#### Full Stack Local Development

Run both backend and frontend:
1. Start backend in one terminal (port 8000)
2. Start frontend in another terminal (port 5173)
3. Frontend will proxy API calls to backend

---

## Screenshots

> 📸 Add screenshots here:
> - Chat interface with example research queries
> - Document upload and processing
> - Generated report samples
> - Research results with citations
> - Multi-format export examples

---

## Future Improvements

### 🚀 Planned Features
- **Advanced Filtering**: Filter research results by source, date, relevance
- **Collaborative Research**: Multi-user workspaces for team research
- **Custom Tool Integration**: User-defined research tools and data sources
- **Real-time Collaboration**: Live updates across sessions
- **Advanced Analytics**: Research analytics and insights dashboard
- **Caching & Performance**: Intelligent result caching and query optimization
- **Mobile App**: Native mobile application for on-the-go research

### 🔧 Technical Improvements
- **Image Generation**: DALL-E integration for visual research synthesis
- **Video Processing**: Support for video content analysis
- **Multi-language Support**: Research in multiple languages
- **Advanced NLP**: Named entity recognition and sentiment analysis
- **Cost Optimization**: Implement caching strategies for API calls
- **Scalability**: Kubernetes deployment configurations
- **Advanced Monitoring**: Enhanced logging and performance metrics

### 📚 Documentation Enhancements
- API reference documentation
- Video tutorials for common tasks
- Prompt engineering guide for better research results
- Deployment guides for cloud providers

---

## Architecture Notes

The project uses a monorepo structure:

```
autonomous-research-agent/
├── backend/              # FastAPI application
│   ├── agents/          # LangGraph workflow definitions
│   ├── api/             # API endpoints
│   ├── core/            # Configuration and core utilities
│   ├── database/        # Repository patterns for data access
│   ├── rag/             # Retrieval-Augmented Generation
│   ├── services/        # Business logic
│   ├── tools/           # External tool integrations
│   └── storage/         # File storage (uploads, reports, images)
├── frontend/            # React + Vite + TypeScript
│   └── src/
│       ├── components/  # Reusable UI components
│       ├── routes/      # Page-level components
│       ├── hooks/       # Custom React hooks
│       └── lib/         # Utilities and API client
```

### Key Deployment Files
- **requirements.txt**: Python dependencies

---

## Configuration & Environment

Create a `.env` file in the root directory:

```env
# LLM Configuration
OPENAI_API_KEY=your_openai_key
MODEL_NAME=gpt-4-turbo

# Search APIs
TAVILY_API_KEY=your_tavily_key

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
