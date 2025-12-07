#!/bin/bash

# Chatbot Backend Setup Verification Script

echo "🔍 Humanoid Robotics Book Chatbot - Setup Verification"
echo "======================================================="
echo ""

# Check Python
echo "1️⃣  Python Environment:"
if [ -d "venv" ]; then
    echo "   ✓ Virtual environment exists"
    PYTHON_PATH="$(pwd)/venv/bin/python"
    VERSION=$($PYTHON_PATH --version 2>&1)
    echo "   ✓ Python: $VERSION"
else
    echo "   ✗ Virtual environment not found"
    exit 1
fi

# Check dependencies
echo ""
echo "2️⃣  Dependencies:"
source venv/bin/activate
PACKAGES=$(python -m pip list | grep -E "fastapi|google-generativeai|qdrant-client|pydantic" | wc -l)
if [ "$PACKAGES" -ge 4 ]; then
    echo "   ✓ All core packages installed"
else
    echo "   ✗ Some packages missing"
fi

# Check main files
echo ""
echo "3️⃣  Project Files:"
FILES=("main.py" "config.py" "requirements.txt" ".env" "README.md")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file missing"
    fi
done

# Check subdirectories
echo ""
echo "4️⃣  Subdirectories:"
DIRS=("services" "routers" "models" "utils")
for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        FILE_COUNT=$(find "$dir" -name "*.py" | wc -l)
        echo "   ✓ $dir/ ($FILE_COUNT Python files)"
    else
        echo "   ✗ $dir/ missing"
    fi
done

# Check imports
echo ""
echo "5️⃣  Import Check:"
python -c "from main import app; from config import settings; from services.rag_service import rag_service" 2>/dev/null && echo "   ✓ All imports work" || echo "   ✗ Import failed"

# Environment variables
echo ""
echo "6️⃣  Environment Variables:"
if grep -q "GEMINI_API_KEY=your_gemini_api_key_here" .env; then
    echo "   ⚠️  GEMINI_API_KEY not configured"
else
    echo "   ✓ GEMINI_API_KEY configured"
fi

if grep -q "QDRANT_URL=https://your-cluster" .env; then
    echo "   ⚠️  QDRANT_URL not configured"
else
    echo "   ✓ QDRANT_URL configured"
fi

echo ""
echo "======================================================="
echo "✅ Setup Complete!"
echo ""
echo "Next Steps:"
echo "1. Configure API keys in .env file:"
echo "   - GEMINI_API_KEY (from https://aistudio.google.com/app/apikey)"
echo "   - QDRANT_URL & QDRANT_API_KEY (from https://cloud.qdrant.io/)"
echo ""
echo "2. Start the server:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "3. Visit:"
echo "   - API: http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs"
echo ""
