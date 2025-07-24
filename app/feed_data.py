from app.database import SessionLocal
from app import models
from app.auth import get_password_hash

db = SessionLocal()

# Check if integration already exists
sponsor = db.query(models.Sponsor).filter(models.Sponsor.name == "Nike").first()
integration = db.query(models.Integration).filter_by(system="Salesforce", sponsor_id=sponsor.id).first()

if not integration:
    integration = models.Integration(
        sponsor_id=sponsor.id,
        system="Salesforce",
        api_key="mock-key-123",  # Simulated
        last_synced_at=None
    )
    db.add(integration)
    db.commit()
    print(" Added Salesforce integration for sponsor Nike")
# # Fetch the user and sponsor
# user = db.query(models.User).filter(models.User.username == "user1").first()
# sponsor = db.query(models.Sponsor).filter(models.Sponsor.name == "Nike").first()

# # Link if not already linked
# if user and sponsor and sponsor not in user.sponsors:
#     user.sponsors.append(sponsor)
#     db.commit()
#     print(f" Linked user '{user.username}' to sponsor '{sponsor.name}'")
# else:
#     print("⚠️ Either user or sponsor does not exist, or already linked.")

db.close()
# # Create or fetch sponsor
# sponsor = db.query(models.Sponsor).filter(models.Sponsor.name == "Nike").first()
# if not sponsor:
#     sponsor = models.Sponsor(name="Nike")
#     db.add(sponsor)
#     db.commit()
#     db.refresh(sponsor)

# # Create 3 tasks for each source
# sources = ["Salesforce", "Asana", "Google Calendar"]
# for source in sources:
#     for i in range(1, 4):
#         task = models.Task(
#             sponsor_id=sponsor.id,
#             source=source,
#             task_name=f"{source} Task {i}",
#             due_date=f"2025-08-{i+10:02d}",
#             status="Pending" if i % 2 == 0 else "In Progress"
#         )
#         db.add(task)

# # Create or fetch demo user
# user = db.query(models.User).filter(models.User.username == "demo").first()
# if not user:
#     user = models.User(
#         username="demo",
#         email="demo@example.com",
#         hashed_password=get_password_hash("test123")
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)

# # Link user to sponsor if not already linked
# if sponsor not in user.sponsors:
#     user.sponsors.append(sponsor)
#     db.commit()

# db.close()
print(f" Seeded sponsor, tasks, and user.")
