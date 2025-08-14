# 🏗️ Smart City AI Dashboard - Technical Architecture

## 🎯 System Overview

The Smart City AI Dashboard is a modern, scalable, AI-powered platform designed to provide real-time insights and predictive analytics for urban management. Built with microservices architecture and containerized deployment.

## 📊 High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │   ML Services   │
│                 │    │                 │    │                 │
│ • TypeScript    │◄──►│ • Python 3.11   │◄──►│ • TensorFlow    │
│ • Tailwind CSS  │    │ • Async/Await   │    │ • Scikit-learn  │
│ • Framer Motion │    │ • WebSockets    │    │ • Pandas/NumPy  │
│ • Recharts      │    │ • Pydantic      │    │ • Predictive AI │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Nginx        │    │   PostgreSQL    │    │     Redis       │
│                 │    │                 │    │                 │
│ • Load Balancer │    │ • Primary DB    │    │ • Caching       │
│ • SSL Termination│    │ • Time Series   │    │ • Session Store │
│ • Static Assets │    │ • Geospatial    │    │ • Real-time Data│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Technology Stack

### Frontend Layer
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS with custom design system
- **State Management**: React Context + Custom Hooks
- **Animations**: Framer Motion for smooth transitions
- **Charts**: Recharts for data visualization
- **Maps**: Custom SVG-based visualization (extensible to Leaflet)
- **Build Tool**: Vite for fast development and optimized builds

### Backend Layer
- **Framework**: FastAPI (Python 3.11)
- **API Documentation**: Auto-generated OpenAPI/Swagger
- **Async Processing**: Native Python asyncio
- **WebSockets**: Real-time bidirectional communication
- **Data Validation**: Pydantic models with type safety
- **Authentication**: JWT-based with optional OAuth2

### AI/ML Layer
- **Traffic Prediction**: Random Forest Regressor
- **Air Quality Forecasting**: Gradient Boosting Regressor
- **Feature Engineering**: Time-series, weather, and contextual data
- **Model Training**: Automated retraining pipelines
- **Inference**: Real-time prediction endpoints
- **Model Storage**: Pickle serialization with versioning

### Data Layer
- **Primary Database**: PostgreSQL 15 with TimescaleDB extension
- **Caching**: Redis 7 for session storage and real-time data
- **Data Processing**: Pandas for ETL operations
- **Geospatial**: PostGIS for location-based queries
- **Time Series**: Optimized for IoT sensor data storage

### Infrastructure Layer
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose for development
- **Reverse Proxy**: Nginx for production deployment
- **SSL/TLS**: Let's Encrypt integration
- **Monitoring**: Health checks and logging

## 🏛️ System Components

### 1. Frontend Application (`/frontend`)

```
src/
├── components/          # Reusable UI components
│   ├── Header.tsx      # Navigation and theme toggle
│   ├── Sidebar.tsx     # Navigation menu
│   ├── MetricCard.tsx  # KPI display cards
│   ├── Chart.tsx       # Data visualization
│   └── Map.tsx         # Interactive city map
├── pages/              # Route-based page components
│   ├── Dashboard.tsx   # Main overview page
│   ├── Traffic.tsx     # Traffic management
│   ├── AirQuality.tsx  # Environmental monitoring
│   ├── Energy.tsx      # Smart grid management
│   ├── Emergency.tsx   # Emergency response
│   └── Analytics.tsx   # Advanced analytics
├── hooks/              # Custom React hooks
│   └── useWebSocket.ts # Real-time data connection
├── context/            # React context providers
│   └── ThemeContext.tsx # Dark/light mode
└── utils/              # Helper functions and utilities
```

### 2. Backend API (`/backend`)

```
app/
├── api/                # API route handlers
│   ├── traffic.py      # Traffic management endpoints
│   ├── air_quality.py  # Environmental data endpoints
│   ├── energy.py       # Smart grid endpoints
│   └── emergency.py    # Emergency services endpoints
├── core/               # Core configuration
│   └── config.py       # Environment settings
├── models/             # Data models and schemas
│   └── schemas.py      # Pydantic models
├── ml/                 # Machine learning components
│   ├── traffic_predictor.py     # Traffic ML model
│   └── air_quality_predictor.py # Air quality ML model
├── services/           # Business logic services
│   └── websocket_manager.py     # WebSocket connections
└── main.py             # FastAPI application entry point
```

### 3. ML Models (`/ml-models`)

```
models/
├── traffic/            # Traffic prediction models
│   ├── model.pkl       # Trained Random Forest model
│   ├── scaler.pkl      # Feature scaler
│   └── metadata.json   # Model metadata and metrics
├── air_quality/        # Air quality forecasting models
│   ├── model.pkl       # Trained Gradient Boosting model
│   ├── scaler.pkl      # Feature scaler
│   └── metadata.json   # Model metadata and metrics
└── training/           # Training scripts and data
    ├── train_traffic.py    # Traffic model training
    ├── train_air_quality.py # Air quality model training
    └── data/               # Training datasets
```

## 🔄 Data Flow Architecture

### Real-time Data Pipeline

```
IoT Sensors → API Gateway → FastAPI → WebSocket → React Frontend
     ↓              ↓           ↓          ↓            ↓
City Systems → Data Validation → Redis → Real-time UI → User Actions
     ↓              ↓           ↓          ↓            ↓
External APIs → ML Processing → PostgreSQL → Analytics → Insights
```

### Prediction Pipeline

```
Historical Data → Feature Engineering → ML Models → Predictions → API Response
       ↓                  ↓               ↓           ↓          ↓
   PostgreSQL → Pandas DataFrames → TensorFlow → JSON → Frontend Charts
```

## 🚀 API Architecture

### RESTful Endpoints

```
GET  /api/dashboard/overview        # City-wide metrics summary
GET  /api/predictions/traffic       # 24-hour traffic forecast
GET  /api/analytics/city-health     # AI-generated city health score
GET  /api/ml/model-status          # ML model performance metrics

GET  /api/traffic/live             # Real-time traffic data
GET  /api/traffic/predict          # Traffic predictions
GET  /api/traffic/optimize         # Signal optimization

GET  /api/air-quality/current      # Current air quality
GET  /api/air-quality/forecast     # 7-day forecast
GET  /api/air-quality/sources      # Pollution source analysis

GET  /api/energy/grid-status       # Smart grid status
GET  /api/energy/consumption-forecast # Energy demand forecast
GET  /api/energy/optimization      # Grid optimization recommendations

GET  /api/emergency/incidents      # Active incidents
GET  /api/emergency/response-optimization # Route optimization
GET  /api/emergency/risk-assessment # City risk analysis
```

### WebSocket Endpoints

```
WS   /ws/realtime                  # Real-time data streaming
     → Traffic updates every 5s
     → Air quality updates every 30s
     → Energy grid updates every 10s
     → Emergency alerts real-time
```

## 🔒 Security Architecture

### Authentication & Authorization
- **JWT Tokens**: Stateless authentication
- **Role-Based Access**: Admin, Operator, Viewer roles
- **API Rate Limiting**: Prevent abuse and ensure fair usage
- **CORS Configuration**: Secure cross-origin requests

### Data Security
- **Input Validation**: Pydantic models prevent injection
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- **XSS Prevention**: React's built-in escaping
- **HTTPS Enforcement**: SSL/TLS for all communications

### Infrastructure Security
- **Container Security**: Non-root users, minimal base images
- **Environment Variables**: Secrets management
- **Network Isolation**: Docker networks for service communication
- **Regular Updates**: Automated dependency updates

## 📈 Scalability & Performance

### Horizontal Scaling
- **Stateless Services**: Easy to replicate and load balance
- **Database Sharding**: Partition data by city/region
- **CDN Integration**: Static asset delivery
- **Microservices**: Independent scaling of components

### Performance Optimizations
- **Async Processing**: Non-blocking I/O operations
- **Database Indexing**: Optimized queries for time-series data
- **Redis Caching**: Reduce database load
- **Connection Pooling**: Efficient database connections

### Monitoring & Observability
- **Health Checks**: Automated service monitoring
- **Metrics Collection**: Performance and usage analytics
- **Error Tracking**: Centralized error reporting
- **Log Aggregation**: Structured logging with correlation IDs

## 🔧 Development & Deployment

### Local Development
```bash
# Start all services
./start.sh

# Individual services
docker-compose up backend
docker-compose up frontend
docker-compose up db redis
```

### Production Deployment
```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# With Nginx reverse proxy
docker-compose --profile production up -d
```

### CI/CD Pipeline
```yaml
# GitHub Actions workflow
Build → Test → Security Scan → Deploy → Health Check
  ↓       ↓         ↓           ↓         ↓
Docker → PyTest → Bandit → K8s → Monitoring
```

## 🧪 Testing Strategy

### Frontend Testing
- **Unit Tests**: Jest + React Testing Library
- **Integration Tests**: Cypress for E2E testing
- **Visual Regression**: Chromatic for UI testing
- **Performance Tests**: Lighthouse CI

### Backend Testing
- **Unit Tests**: PyTest with fixtures
- **Integration Tests**: FastAPI TestClient
- **Load Testing**: Locust for performance testing
- **API Testing**: Automated OpenAPI validation

### ML Model Testing
- **Model Validation**: Cross-validation and holdout testing
- **Data Quality**: Automated data validation pipelines
- **Performance Monitoring**: Model drift detection
- **A/B Testing**: Compare model versions in production

## 🌐 Deployment Architectures

### Development Environment
```
Developer Machine
├── Frontend (Vite dev server)
├── Backend (FastAPI with reload)
├── PostgreSQL (Docker)
├── Redis (Docker)
└── Hot reloading enabled
```

### Production Environment
```
Load Balancer (Nginx)
├── Frontend Cluster (3 replicas)
├── Backend Cluster (5 replicas)
├── Database Cluster (Primary + Replicas)
├── Redis Cluster (3 nodes)
└── ML Service Cluster (2 replicas)
```

## 📊 Monitoring & Analytics

### Application Metrics
- **Response Times**: API endpoint performance
- **Error Rates**: 4xx/5xx response tracking
- **Throughput**: Requests per second
- **WebSocket Connections**: Real-time connection health

### Business Metrics
- **User Engagement**: Dashboard usage patterns
- **Prediction Accuracy**: ML model performance
- **City Performance**: Traffic, air quality improvements
- **Cost Optimization**: Infrastructure efficiency

### Infrastructure Metrics
- **Resource Usage**: CPU, memory, disk utilization
- **Database Performance**: Query times, connection pools
- **Network Performance**: Latency, bandwidth usage
- **Container Health**: Docker container status

This architecture provides a solid foundation for a scalable, maintainable, and performant smart city management platform that can grow with the needs of modern urban environments.