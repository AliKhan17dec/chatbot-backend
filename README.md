# Humanoid Robotics Book Chatbot Backend

RAG-based chatbot backend for the Physical AI & Humanoid Robotics textbook. Built with FastAPI, Google Gemini, Qdrant, and Neon Postgres.

## 🚀 Features

- **RAG (Retrieval-Augmented Generation)**: Answers questions using content from the robotics textbook
- **Context-based Queries**: Retrieve relevant sections and generate accurate answers
- **Text Selection Support**: Ask questions about specific text selections
- **Vector Search**: Fast semantic search using Qdrant vector database
- **Gemini Integration**: Powered by Google's Gemini API for embeddings and generation
- **FastAPI**: High-performance async API with automatic documentation

## 📋 Prerequisites

- Python 3.10 or higher
- Google Gemini API key
- Qdrant Cloud account (free tier)
- Neon Serverless Postgres (optional)

## 🛠️ Setup Instructions

### 1. Clone and Navigate

```bash
cd chatbot/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# Get Gemini API key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Create Qdrant cluster at: https://cloud.qdrant.io/
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here

# Optional: Neon Postgres from: https://neon.tech/
DATABASE_URL=postgresql://user:password@host/db

# Application settings
APP_ENV=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 5. Get Your API Keys

#### Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy and paste into `.env`

#### Qdrant Cloud
1. Visit [Qdrant Cloud](https://cloud.qdrant.io/)
2. Sign up for free account
3. Create a new cluster (free tier available)
4. Copy cluster URL and API key to `.env`

#### Neon Postgres (Optional)
1. Visit [Neon](https://neon.tech/)
2. Sign up and create a project
3. Copy connection string to `.env`

## 🎯 Running the Application

### Start the Server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Index the Book Content

Before using the chatbot, you need to index the book documents:

```bash
# Using curl
curl -X POST http://localhost:8000/chat/index \
  -H "Content-Type: application/json" \
  -d '{"force_reindex": false}'

# Or use the Swagger UI at http://localhost:8000/docs
```

This will:
1. Load all MDX files from the book
2. Split them into chunks
3. Generate embeddings using Gemini
4. Store them in Qdrant

**Note**: Initial indexing may take 5-10 minutes depending on the number of documents.

## 📡 API Endpoints

### Health Check
```http
GET /health
```

Check if all services are running properly.

### Query Chatbot
```http
POST /chat/query
Content-Type: application/json

{
  "question": "What is ROS 2 and why is it important?",
  "session_id": "optional-session-id"
}
```

### Query with Text Selection
```http
POST /chat/query-selection
Content-Type: application/json

{
  "question": "Explain this in simpler terms",
  "selected_text": "ROS 2 nodes communicate via topics...",
  "session_id": "optional-session-id"
}
```

### Index Documents
```http
POST /chat/index
Content-Type: application/json

{
  "force_reindex": false
}
```

### Collection Info
```http
GET /chat/collection-info
```

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example           # Example environment variables
├── models/
│   └── schemas.py         # Pydantic models for request/response
├── routers/
│   └── chat.py           # Chat endpoints
├── services/
│   ├── gemini_service.py  # Gemini API integration
│   ├── qdrant_service.py  # Qdrant vector database
│   └── rag_service.py     # RAG pipeline
└── utils/
    └── document_loader.py # Document loading and chunking
```

## 🧪 Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the main modules in this course?"
  }'

# Query with selection
curl -X POST http://localhost:8000/chat/query-selection \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain this concept",
    "selected_text": "NVIDIA Isaac Sim is an Omniverse application..."
  }'
```

### Using Python

```python
import requests

# Query the chatbot
response = requests.post(
    "http://localhost:8000/chat/query",
    json={"question": "What is Physical AI?"}
)

print(response.json())
```

## 🔧 Configuration Options

Edit `config.py` or `.env` to customize:

```python
# RAG Configuration
chunk_size: int = 1000          # Size of text chunks
chunk_overlap: int = 200        # Overlap between chunks
top_k_results: int = 5          # Number of results to retrieve
similarity_threshold: float = 0.7  # Minimum similarity score

# Model Configuration
embedding_model = "models/text-embedding-004"
generation_model = "gemini-1.5-flash"
```

## 🐛 Troubleshooting

### Import Errors
Make sure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Qdrant Connection Failed
- Check your `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Ensure your Qdrant cluster is running
- Check firewall/network settings

### Gemini API Errors
- Verify your `GEMINI_API_KEY` is correct
- Check API quota limits
- Ensure you're using a valid model name

### No Documents Found
- Verify `BOOK_DOCS_PATH` points to the correct location
- Check that MDX files exist in the docs directory
- Review logs for file loading errors

## 📝 Development

### Adding New Endpoints

1. Create new router in `routers/`
2. Add to `main.py`:
```python
from routers import your_router
app.include_router(your_router.router)
```

### Modifying RAG Pipeline

Edit `services/rag_service.py` to customize:
- Context retrieval logic
- Answer generation prompts
- Source formatting

### Changing Chunking Strategy

Edit `utils/document_loader.py` to modify:
- Chunk size and overlap
- Text splitting logic
- Metadata extraction

## 🚀 Deployment

### Environment Variables for Production

```env
APP_ENV=production
CORS_ORIGINS=https://your-book-domain.com
# ... other production settings
```

### Using Docker (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t robotics-chatbot .
docker run -p 8000:8000 --env-file .env robotics-chatbot
```

## 📚 Next Steps

1. **Index the documents**: Run the `/chat/index` endpoint
2. **Test queries**: Use Swagger UI at `/docs`
3. **Integrate with frontend**: Connect your book's UI to this API
4. **Monitor performance**: Check logs and response times
5. **Optimize**: Adjust chunk size, top_k, and similarity threshold

## 🔗 Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 📄 License

This project is part of the GIAIC Humanoid Robotics Book Hackathon.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API logs
3. Test with Swagger UI at `/docs`
4. Check environment variables

---

Built with ❤️ for the Physical AI & Humanoid Robotics Course
