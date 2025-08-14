#!/bin/bash

echo "🚀 Starting Smart Task Manager - Hackathon Winner Project"
echo "=================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are available"
echo ""

# Build and start the services
echo "🔨 Building and starting services..."
docker-compose up --build -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "🎉 Smart Task Manager is now running!"
    echo ""
    echo "📱 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo ""
    echo "💡 Tips:"
    echo "  - Open multiple browser tabs to see real-time updates"
    echo "  - Try creating tasks with keywords like 'meeting', 'urgent', 'deadline'"
    echo "  - Watch the AI automatically categorize and prioritize tasks"
    echo ""
    echo "🛑 To stop the application, run: docker-compose down"
    echo ""
else
    echo "❌ Failed to start services. Check the logs with: docker-compose logs"
    exit 1
fi