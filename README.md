Sponsorship Task Sync Platform

This project simulates a simplified sponsorship task management system with support for:

User authentication via JWT

Role-based access to sponsor tasks

Dynamic integration with external systems (Salesforce, Asana, Google Calendar)

Periodic ETL-style background sync jobs

🚀 Features

JWT Authentication: Secure login using OAuth2 password flow

Sponsor Access Control: Users only see tasks for sponsors they're linked to

Integration Table: Stores sponsor connections to third-party systems

Task Filtering: Filter synced tasks by status

Sync Worker: Background job to auto-fetch tasks from simulated APIs

REST API Docs: Fully interactive Swagger UI at /docs

🧠 Architecture Overview

User ⇄ FastAPI ⇄ Database
                     ⇓
       [Integration Table]
             ⇓
     sync_worker.py (ETL)
             ⇓
  External APIs (simulated)

Core Models

User ↔ Sponsor (many-to-many)

Sponsor ↔ Task (one-to-many)

Sponsor ↔ Integration (one-to-many)

🛠️ Setup

# Clone & activate environment
uvicorn app.main:app --reload  # run API
python -m app.feed_data        # seed sponsor, user, integration
python -m app.sync_worker      # run sync ETL job

📦 API Endpoints

Endpoint

Method

Description

/token

POST

Get access token with username/password

/users/

POST

Register a new user

/sync-tasks

POST

Get tasks for sponsor (if authorized)

/update-status

PATCH

Update task status (optional bonus)

🔁 Periodic Sync

app/sync_worker.py:

Uses fetch_tasks_for_system(system, api_key)

Mocks real API calls (can be replaced with requests)

Populates Task table every hour

To test instantly:

# Inside sync_worker.py
run_periodic_sync()  # one-time run

🔐 Security Notes

Passwords hashed using passlib (bcrypt)

JWT-based authentication and Depends(get_current_user) on all protected routes

Authorization enforced using user-sponsor link check

📈 Scaling & Extensibility

Swap mock integrations with real APIs using requests or httpx

Use Celery + Redis for distributed ETL sync

Add webhook support for real-time task sync

Cache task responses using Redis

Add frontend dashboard (React/Vue) for visualization

🤖 Future AI Features (Ideas)

Use LLM to auto-summarize tasks across sponsors

Recommend task priorities using fine-tuned GPT

Predict overdue risk using historical sync patterns

👨‍💻 Credits

Built with ❤️ using FastAPI, SQLAlchemy, and Python by Smith.
