from app.database import SessionLocal
from app import models
from datetime import datetime, timezone
import requests
import time

def fetch_tasks_for_system(system: str, api_key: str):
    #Calling API logic can be called here 
    """if system == "Salesforce":
        url = "https://api.salesforce.com/v1/tasks"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    elif system == "Asana":
        # Asana-specific API logic
        ... """
    # Simulated response for demo purposes
    if system == "Salesforce":
        return [
            {"task_name": "Renwew contract", "due_date": "2024-09-01", "status": "Pending"},
            {"task_name": "Update Jersey", "due_date": "2026-07-15", "status": "Pending"},
        ]
    # Add more integrations here
    return []

def sync_tasks_from_integration(integration, db):
    tasks = fetch_tasks_for_system(integration.system, integration.api_key)

    inserted_count = 0

    for task_data in tasks:
        task = models.Task(
            sponsor_id=integration.sponsor_id,
            source=integration.system,
            task_name=task_data["task_name"],
            due_date=task_data["due_date"],
            status=task_data["status"],
            synced_at=datetime.utcnow()
        )
        db.add(task)
        inserted_count += 1

    integration.last_synced_at = datetime.now(timezone.utc)
    db.commit()
    print(f" Synced {inserted_count} tasks for sponsor '{integration.sponsor.name}' from {integration.system}")

def run_periodic_sync():
    db = SessionLocal()
    integrations = db.query(models.Integration).all()
    for integration in integrations:
        sync_tasks_from_integration(integration, db)
    db.close()

if __name__ == "__main__":
    print(" Starting background sync every 1 hour...")
    while True:
        run_periodic_sync()
        time.sleep(3600)  # sync every hour
