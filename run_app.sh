#!/bin/bash


if [ ! -d "venv" ]; then
    echo "❌ Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found"
    source venv/bin/activate
fi

echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🔧 Creating database..."
python -c "from app.models.database import create_tables; create_tables()"

echo ""
echo "🌐 Starting server..."
echo "📖 Documentation available at: http://localhost:8000/docs"
echo "📋 ReDoc available at: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 