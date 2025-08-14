#!/bin/bash

# Smart City AI Dashboard - Development Startup Script

echo "🏙️  Starting Smart City AI Dashboard..."
echo "======================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/smartcity

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production

# API Keys (optional)
WEATHER_API_KEY=
TRAFFIC_API_KEY=

# Environment
ENVIRONMENT=development
EOF
fi

echo "🚀 Starting services with Docker Compose..."

# Start the services
docker-compose up -d db redis

echo "⏳ Waiting for database to be ready..."
sleep 10

# Start backend and frontend
docker-compose up backend frontend

echo ""
echo "✅ Smart City AI Dashboard is now running!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "To stop the services, press Ctrl+C or run: docker-compose down"