#!/usr/bin/env python3
"""
Demo Data Script for Smart Task Manager
Populates the database with sample tasks to showcase AI features
"""

import requests
import json
from datetime import datetime, timedelta

API_BASE = "http://localhost:8000"

# Sample tasks that will demonstrate AI categorization and priority
DEMO_TASKS = [
    {
        "title": "Urgent client meeting tomorrow",
        "description": "Discuss Q4 project requirements with ABC Corp team",
        "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "user_id": "demo_user"
    },
    {
        "title": "Gym workout session",
        "description": "Cardio and strength training at local fitness center",
        "due_date": (datetime.now() + timedelta(days=0)).isoformat(),
        "user_id": "demo_user"
    },
    {
        "title": "Study React hooks and context",
        "description": "Complete online course on advanced React patterns",
        "due_date": (datetime.now() + timedelta(days=3)).isoformat(),
        "user_id": "demo_user"
    },
    {
        "title": "Pay electricity bill",
        "description": "Due date approaching, need to process payment",
        "due_date": (datetime.now() + timedelta(days=2)).isoformat(),
        "user_id": "demo_user"
    },
    {
        "title": "Family dinner planning",
        "description": "Organize weekend family gathering and meal prep",
        "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
        "user_id": "demo_user"
    },
    {
        "title": "Critical project deadline",
        "description": "Submit final deliverables for hackathon project",
        "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "user_id": "demo_user"
    },
    {
        "title": "Doctor appointment",
        "description": "Annual health checkup and blood work",
        "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "user_id": "demo_user"
    },
    {
        "title": "Learn Python FastAPI",
        "description": "Complete tutorial on building REST APIs with FastAPI",
        "due_date": (datetime.now() + timedelta(days=4)).isoformat(),
        "user_id": "demo_user"
    },
    {
        "title": "Budget review meeting",
        "description": "Monthly financial planning session with team",
        "due_date": (datetime.now() + timedelta(days=2)).isoformat(),
        "user_id": "demo_user"
    },
    {
        "title": "Home maintenance",
        "description": "Fix leaky faucet and clean gutters",
        "due_date": (datetime.now() + timedelta(days=6)).isoformat(),
        "user_id": "demo_user"
    }
]

def create_demo_tasks():
    """Create demo tasks to showcase AI features"""
    print("🚀 Creating demo tasks to showcase AI features...")
    print("=" * 50)
    
    created_tasks = []
    
    for i, task_data in enumerate(DEMO_TASKS, 1):
        try:
            print(f"Creating task {i}/{len(DEMO_TASKS)}: {task_data['title']}")
            
            response = requests.post(f"{API_BASE}/tasks/", json=task_data)
            
            if response.status_code == 200:
                task = response.json()
                print(f"  ✅ Created successfully")
                print(f"  📍 AI Category: {task['category']}")
                print(f"  🚨 AI Priority: {task['priority']}")
                print(f"  📅 Due: {task['due_date']}")
                print()
                created_tasks.append(task)
            else:
                print(f"  ❌ Failed to create: {response.status_code}")
                print(f"  Error: {response.text}")
                print()
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to the API. Make sure the backend is running.")
            print("Run: docker-compose up --build")
            return
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            print()
    
    print("🎉 Demo data creation completed!")
    print(f"📊 Created {len(created_tasks)} tasks")
    print()
    
    # Show AI categorization summary
    categories = {}
    priorities = {}
    
    for task in created_tasks:
        cat = task['category']
        pri = task['priority']
        
        categories[cat] = categories.get(cat, 0) + 1
        priorities[pri] = priorities.get(pri, 0) + 1
    
    print("🧠 AI Categorization Results:")
    print("-" * 30)
    for category, count in categories.items():
        print(f"  {category.capitalize()}: {count} tasks")
    
    print()
    print("🚨 AI Priority Suggestions:")
    print("-" * 30)
    for priority, count in priorities.items():
        print(f"  {priority.capitalize()}: {count} tasks")
    
    print()
    print("💡 Demo Tips:")
    print("-" * 30)
    print("• Open multiple browser tabs to see real-time updates")
    print("• Try filtering by category or priority")
    print("• Search for specific keywords")
    print("• Watch how AI automatically organizes your tasks")
    print()
    print("🌐 Access your app at: http://localhost:3000")

if __name__ == "__main__":
    create_demo_tasks()