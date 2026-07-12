"""
Database Seeding Utility.
Populates the database with realistic dummy data (Tenants, Users, Issues, Logs) 
to facilitate local development and QA testing.
"""
from faker import Faker
import json
import random

from app.db.session import SessionLocal
from app.models.auth import UserAuth
from app.models.company import Company
from app.models.issues import Issue
from app.models.user import User
from app.models.logs import IssueLog
from app.utils import hash_password 

db = SessionLocal()
fake = Faker()

def seed_data():
    print("🌱 Initiating database seeding...")
    # ---------------------------------------------------------
    # 1. COMPANIES (Tenants)
    # ---------------------------------------------------------
    companies = []

    # Adding the superadmin company first
    companies.append(Company(name="SyncNode System", subscription_plan="enterprise"))

    # Generate 10 random companies
    for i in range(10):
        companies.append(
            Company(
                name=fake.company(), 
                subscription_plan=random.choices(
                    population=["free", "pro", "enterprise"], 
                    weights=[50, 30, 20], 
                    k=1)[0]
                )
            )
        
    
    db.add_all(companies)
    db.commit()

    # Create an empty memory list to store the IDs of all the new companies
    company_ids = []

    for company in companies:
        db.refresh(company)
        company_ids.append(company.id)

    print(f"✅ Created 11 Companies. IDs saved: {company_ids}")

    # ---------------------------------------------------------
    # 2. USERS & AUTHENTICATION 
    # ---------------------------------------------------------
    
    # --- SUPERADMIN ---
    superadmin = User(
        company_id=company_ids[0],
        first_name="System",
        last_name="Administrator",
        email="superadmin@syncnode.com",
        role="superadmin",
        avatar_url="https://ui-avatars.com/api/?name=System+Admin&background=000000&color=fff"
    )
    db.add(superadmin)
    db.commit()
    db.refresh(superadmin)

    default_password = hash_password("password123")
    db.add(UserAuth(user_id=superadmin.id, password_hash=default_password))
    db.commit()

    users = []
    auth_profiles = []
    # default_password = hash_password("password123")

    # Skip company_ids[0] because that is the System HQ
    for current_company_id in company_ids[1:]:

        # Randomly decide this company has between 5 and 15 employees
        num_employees = random.randint(5, 15)
        company_user_ids = []

        for _ in range(num_employees):
            f_name = fake.first_name()
            l_name = fake.last_name()

            assigned_role = random.choices(
                population=["developer", "IT", "admin", "owner"], 
                weights=[60, 20, 15, 5], 
                k=1
            )[0]

            users.append(User(
                company_id=current_company_id,
                first_name=f_name,
                last_name=l_name,
                email=f"{f_name.lower()}.{l_name.lower()}@{fake.domain_name()}",
                role=assigned_role,
                avatar_url=f"https://ui-avatars.com/api/?name={f_name}+{l_name}&background=random&color=fff"
            ))

        db.add_all(users)
        db.commit()


        for u in users:
            db.refresh(u)
            company_user_ids.append(u.id)
            auth_profiles.append(UserAuth(user_id=u.id, password_hash=default_password))

        db.add_all(auth_profiles)
        db.commit()

        users.clear()
        auth_profiles.clear()

        # ---------------------------------------------------------
        # 3. ISSUES
        # ---------------------------------------------------------

        company_issues = []
        num_issues = random.randint(10, 30)

        for _ in range(num_issues):
            company_issues.append(Issue(
            title=fake.catch_phrase(),
            description=fake.paragraph(),
            priority=random.choice(["low", "medium", "high"]),
            status=random.choice(["open", "in_progress", "done"]),
            type=random.choice(["bug", "task"]),
            company_id=current_company_id,
            creator_id=random.choice(company_user_ids),
            assignee_id=random.choices([random.choice(company_user_ids), None], weights=[80, 20], k=1)[0], # 20% chance the issue is unassigned (None)
            git_url=f"https://github.com/{fake.word()}/{fake.word()}/issues/{random.randint(1, 100)}"
        ))

        db.add_all(company_issues)
        db.commit()

        issue_logs = []
        for issue in company_issues:
            db.refresh(issue)

            issue_logs.append(IssueLog(
                company_id=current_company_id,
                issue_id=issue.id,
                actor_id=issue.creator_id,
                action="created_issue",
                old_value=None,
                new_value=issue.status
            ))

        db.add_all(issue_logs)
        db.commit()
        company_issues.clear()
        issue_logs.clear()

    print("🚀 Seeding Complete! You can now log in.")

if __name__ == "__main__":
    seed_data()