#!/bin/bash

# Quick Test Script for Humanoid Robotics Chatbot
# This script performs quick API tests without indexing

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║       🧪 QUICK CHATBOT TEST - Book Related Questions 🧪                  ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

BASE_URL="http://localhost:8000"

# Test 1: Health Check
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  Health Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s $BASE_URL/health | python3 -m json.tool
echo ""

# Test 2: Collection Info
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  Vector Database Collection Info"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s $BASE_URL/chat/collection-info | python3 -m json.tool
echo ""

# Test 3: Sample Questions (only if documents are indexed)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  Testing Sample Questions"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Question 1: About ROS 2
echo "📝 Question 1: What is ROS 2?"
echo "────────────────────────────────────────────────────────────────────────────"
curl -s -X POST $BASE_URL/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is ROS 2 and why is it important?"}' \
  | python3 -m json.tool
echo ""
sleep 2

# Question 2: About Physical AI
echo "📝 Question 2: What is Physical AI?"
echo "────────────────────────────────────────────────────────────────────────────"
curl -s -X POST $BASE_URL/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Physical AI?"}' \
  | python3 -m json.tool
echo ""
sleep 2

# Question 3: About NVIDIA Isaac
echo "📝 Question 3: What is NVIDIA Isaac?"
echo "────────────────────────────────────────────────────────────────────────────"
curl -s -X POST $BASE_URL/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is NVIDIA Isaac and what does it do?"}' \
  | python3 -m json.tool
echo ""
sleep 2

# Question 4: About course modules
echo "📝 Question 4: Course Structure"
echo "────────────────────────────────────────────────────────────────────────────"
curl -s -X POST $BASE_URL/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main modules in this robotics course?"}' \
  | python3 -m json.tool
echo ""

# Test 4: Query with Selection
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  Testing Query with Text Selection"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Selected Text: 'ROS 2 provides nodes, topics, and services...'"
echo "Question: 'Explain these concepts in simple terms'"
echo "────────────────────────────────────────────────────────────────────────────"

curl -s -X POST $BASE_URL/chat/query-selection \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain these concepts in simple terms",
    "selected_text": "ROS 2 provides nodes, topics, and services for robot communication. Nodes are individual processes, topics are named buses for message passing, and services provide request-reply interactions."
  }' \
  | python3 -m json.tool

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Tests Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 View full API docs: http://localhost:8000/docs"
echo "❤️  Health check: http://localhost:8000/health"
echo ""
