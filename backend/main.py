from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import List, Optional
import json
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Smart Task Manager API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    priority = Column(String, default="medium")
    category = Column(String, default="general")
    status = Column(String, default="pending")
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_completed = Column(Boolean, default=False)
    user_id = Column(String, default="default")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    category: Optional[str] = "general"
    due_date: Optional[datetime] = None
    user_id: Optional[str] = "default"

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    category: str
    status: str
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    is_completed: bool
    user_id: str

    class Config:
        from_attributes = True

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# AI-powered task categorization
def categorize_task(title: str, description: str = "") -> str:
    """Simple AI-like categorization based on keywords"""
    text = (title + " " + description).lower()
    
    categories = {
        "work": ["meeting", "report", "project", "deadline", "client", "business"],
        "personal": ["family", "friend", "birthday", "anniversary", "home", "garden"],
        "health": ["exercise", "doctor", "gym", "diet", "meditation", "sleep"],
        "learning": ["study", "course", "book", "tutorial", "practice", "skill"],
        "finance": ["bill", "payment", "budget", "investment", "tax", "expense"]
    }
    
    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category
    
    return "general"

def suggest_priority(title: str, description: str = "", due_date: Optional[datetime] = None) -> str:
    """AI-like priority suggestion"""
    text = (title + " " + description).lower()
    
    # High priority keywords
    high_priority = ["urgent", "asap", "emergency", "critical", "deadline", "important"]
    if any(word in text for word in high_priority):
        return "high"
    
    # Check due date proximity
    if due_date:
        days_until_due = (due_date - datetime.now()).days
        if days_until_due <= 1:
            return "high"
        elif days_until_due <= 3:
            return "medium"
    
    return "medium"

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Smart Task Manager API", "version": "1.0.0"}

@app.post("/tasks/", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # AI-powered categorization and priority
    category = categorize_task(task.title, task.description)
    priority = suggest_priority(task.title, task.description, task.due_date)
    
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=priority,
        category=category,
        due_date=task.due_date,
        user_id=task.user_id
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Broadcast to all connected clients
    await manager.broadcast(json.dumps({
        "type": "task_created",
        "task": {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "priority": db_task.priority,
            "category": db_task.category,
            "status": db_task.status,
            "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
            "created_at": db_task.created_at.isoformat(),
            "updated_at": db_task.updated_at.isoformat(),
            "is_completed": db_task.is_completed,
            "user_id": db_task.user_id
        }
    }))
    
    return db_task

@app.get("/tasks/", response_model=List[TaskResponse])
async def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db_task.updated_at = datetime.now()
    db.commit()
    db.refresh(db_task)
    
    # Broadcast update
    await manager.broadcast(json.dumps({
        "type": "task_updated",
        "task": {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "priority": db_task.priority,
            "category": db_task.category,
            "status": db_task.status,
            "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
            "created_at": db_task.created_at.isoformat(),
            "updated_at": db_task.updated_at.isoformat(),
            "is_completed": db_task.is_completed,
            "user_id": db_task.user_id
        }
    }))
    
    return db_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    
    # Broadcast deletion
    await manager.broadcast(json.dumps({
        "type": "task_deleted",
        "task_id": task_id
    }))
    
    return {"message": "Task deleted successfully"}

@app.get("/tasks/category/{category}")
async def get_tasks_by_category(category: str, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.category == category).all()
    return tasks

@app.get("/tasks/priority/{priority}")
async def get_tasks_by_priority(priority: str, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.priority == priority).all()
    return tasks

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for testing
            await manager.send_personal_message(f"Message received: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)