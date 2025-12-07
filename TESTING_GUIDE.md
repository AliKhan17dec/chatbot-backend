# 🧪 How to Test the Chatbot with Book-Related Questions

## Quick Start

Your chatbot backend is running at **http://localhost:8000**

## ⚠️ IMPORTANT: Before Testing

**You MUST index the documents first!** The chatbot needs to load and process your book's content before it can answer questions.

---

## 📋 Step-by-Step Testing Guide

### Step 1: Index the Book Documents

This is **required** before asking any questions. Run ONE of these methods:

#### Method A: Using Browser (Easiest)
1. Open http://localhost:8000/docs
2. Find `POST /chat/index` endpoint
3. Click "Try it out"
4. Click "Execute"
5. Wait 5-10 minutes for indexing to complete

#### Method B: Using curl
```bash
curl -X POST http://localhost:8000/chat/index \
  -H "Content-Type: application/json" \
  -d '{"force_reindex": false}'
```

#### Method C: Using Python test script
```bash
cd /Users/ammadkhan/coding/giaic-robotics-book-hackathon/chatbot/backend
source venv/bin/activate
python test_chatbot.py
```

**What happens during indexing:**
- Loads 25 MDX files from `humanoid-robotics-book/docs/`
- Splits into ~249 text chunks
- Generates embeddings using Gemini
- Stores in Qdrant vector database
- **Time required:** 5-10 minutes

---

### Step 2: Verify Indexing is Complete

Check if documents are indexed:

```bash
curl http://localhost:8000/chat/collection-info
```

You should see `points_count` > 0 (should be around 249).

---

### Step 3: Ask Questions About the Book

Now you can test with book-related questions!

## 📚 Sample Questions by Module

### Module 1: ROS 2 Questions

```bash
# What is ROS 2?
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is ROS 2 and why is it important for robotics?"}'

# ROS 2 Components
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain ROS 2 nodes, topics, and services"}'

# URDF
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is URDF and how is it used in robotics?"}'
```

### Module 2: Digital Twin Questions

```bash
# Digital Twin Concept
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a digital twin in robotics?"}'

# Gazebo vs Unity
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the differences between Gazebo and Unity for robot simulation?"}'

# Sensor Simulation
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How do you simulate sensors like LiDAR and cameras?"}'
```

### Module 3: NVIDIA Isaac Questions

```bash
# Isaac Sim
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is NVIDIA Isaac Sim and what is it used for?"}'

# Isaac ROS
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What does Isaac ROS provide for robotics development?"}'

# Navigation
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Nav2 and how does it help with robot navigation?"}'
```

### Module 4: Vision-Language-Action Questions

```bash
# VLA Concept
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Vision-Language-Action (VLA) in robotics?"}'

# Voice Commands
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How can OpenAI Whisper be used for voice commands in robots?"}'

# LLM Planning
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How can LLMs be used for robot task planning?"}'
```

### General Course Questions

```bash
# Physical AI
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Physical AI?"}'

# Course Structure
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main modules in this robotics course?"}'

# Hardware Requirements
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What hardware is required for this course?"}'

# Learning Outcomes
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the learning outcomes of this course?"}'
```

---

## 🎯 Testing with Text Selection

This feature allows users to select text from the book and ask questions about it:

```bash
curl -X POST http://localhost:8000/chat/query-selection \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain this in simpler terms",
    "selected_text": "ROS 2 (Robot Operating System 2) is a middleware framework for robot control. It provides nodes, topics, and services for communication between different components."
  }'
```

---

## 🚀 Quick Test Methods

### Method 1: Use the Test Scripts

We've created test scripts for you:

```bash
# Quick bash test
cd /Users/ammadkhan/coding/giaic-robotics-book-hackathon/chatbot/backend
./quick_test.sh

# Comprehensive Python test
python test_chatbot.py
```

### Method 2: Use Swagger UI (Easiest)

1. Open http://localhost:8000/docs
2. Try each endpoint interactively
3. See responses in real-time
4. No command line needed!

### Method 3: Use curl Commands

Copy and paste the curl commands above directly into your terminal.

---

## 📊 Understanding the Response

When you ask a question, you get:

```json
{
  "answer": "Generated answer based on the book content",
  "sources": [
    {
      "title": "Module 1: ROS 2 Architecture",
      "content": "Relevant text snippet...",
      "similarity_score": 0.89,
      "metadata": {...}
    }
  ],
  "session_id": null,
  "timestamp": "2025-12-07T10:00:00"
}
```

- **answer**: AI-generated response based on book content
- **sources**: Which book sections were used (with relevance scores)
- **similarity_score**: How relevant each source is (0-1)

---

## ⚙️ Configuration

### Adjusting Response Quality

Edit `/Users/ammadkhan/coding/giaic-robotics-book-hackathon/chatbot/backend/config.py`:

```python
# RAG Configuration
top_k_results: int = 5          # Number of context chunks to retrieve
similarity_threshold: float = 0.7  # Minimum relevance score (0-1)
```

- **Higher top_k_results** = More context, longer but more comprehensive answers
- **Lower similarity_threshold** = More lenient matching, more sources included

---

## 🐛 Troubleshooting

### Problem: "I couldn't find relevant information"

**Solution:** Documents aren't indexed yet.
```bash
# Index documents
curl -X POST http://localhost:8000/chat/index \
  -H "Content-Type: application/json" \
  -d '{"force_reindex": false}'
```

### Problem: Indexing times out

**Solution:** It's normal! Indexing takes 5-10 minutes. Check logs:
```bash
tail -f /Users/ammadkhan/coding/giaic-robotics-book-hackathon/chatbot/backend/server.log
```

### Problem: "Model not found" error

**Solution:** Fixed! We updated the model name to `gemini-1.5-flash-latest` in `.env`

### Problem: Server not responding

**Solution:** Restart the server:
```bash
cd /Users/ammadkhan/coding/giaic-robotics-book-hackathon/chatbot/backend
source venv/bin/activate
pkill -f "python main.py"
nohup python main.py > server.log 2>&1 &
```

---

## 📈 Advanced Testing

### Test Different Question Types

1. **Factual Questions**
   - "What is ROS 2?"
   - "List the course modules"

2. **Conceptual Questions**
   - "Why is Physical AI important?"
   - "How does a digital twin help in robotics?"

3. **Procedural Questions**
   - "How do I set up Isaac Sim?"
   - "What steps are needed to create a ROS 2 node?"

4. **Comparative Questions**
   - "What's the difference between Gazebo and Unity?"
   - "ROS 1 vs ROS 2 differences?"

---

## 🎓 Example Testing Session

```bash
# 1. Start fresh terminal
cd /Users/ammadkhan/coding/giaic-robotics-book-hackathon/chatbot/backend

# 2. Check server health
curl http://localhost:8000/health

# 3. Check if documents are indexed
curl http://localhost:8000/chat/collection-info

# 4. If not indexed, index now (wait 5-10 min)
curl -X POST http://localhost:8000/chat/index \
  -H "Content-Type: application/json" \
  -d '{"force_reindex": false}'

# 5. Ask your first question
curl -X POST http://localhost:8000/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Physical AI?"}' \
  | python3 -m json.tool

# 6. Try more questions!
```

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Server Logs**: `tail -f chatbot/backend/server.log`

---

## ✅ Success Criteria

Your chatbot is working correctly if:

1. ✓ Health check returns `"status": "healthy"`
2. ✓ Collection info shows `points_count` > 0
3. ✓ Questions return relevant answers with sources
4. ✓ Sources have high similarity scores (> 0.7)
5. ✓ Answers reference actual book content

---

## 🎉 You're Ready!

Now you can:
1. ✅ Test the chatbot thoroughly
2. ✅ Integrate it with your Docusaurus book frontend
3. ✅ Demo it for the hackathon
4. ✅ Deploy it to production

Happy testing! 🚀
