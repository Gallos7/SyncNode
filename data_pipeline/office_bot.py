import requests
import time
import random
from sqlalchemy import create_engine, text
from faker import Faker

# Initialize Faker for dynamic payloads
fake = Faker()

# ==========================================
# PHASE 1: THE BOOTSTRAPPER (Runs Once)
# ==========================================
print("🔌 Connecting to the database to map the users...")

# We use localhost:3307 because this script runs on your Windows host
DATABASE_URL = "mysql+pymysql://root:ena123456789@localhost:3307/syncnode"
engine = create_engine(DATABASE_URL)

valid_users = []

# Open connection and grab both email AND role
with engine.connect() as conn:
    result = conn.execute(text("SELECT email, role FROM users WHERE role != 'superadmin'"))
    
    for row in result:
        # Save as a dictionary so the bot knows its permissions
        valid_users.append({
            "email": row[0],
            "role": row[1]
        })

print(f"✅ Successfully loaded {len(valid_users)} employees into memory!")
print("🚀 Starting the Office Bot Simulation... Press CTRL+C to stop.\n")

# ==========================================
# PHASE 2: THE SIMULATION (Infinite Loop)
# ==========================================
BASE_URL = 'http://localhost:8000'
iteration = 1

try:
    while True:
        # --- 1. PICK A RANDOM WORKER ---
        current_worker = random.choice(valid_users)
        worker_email = current_worker["email"]
        worker_role = current_worker["role"]
        
        print(f"[{iteration}] 🤖 Bot woke up as: {worker_email} (Role: {worker_role})")

        # --- 2. LOG IN & GET TOKEN ---
        login_resp = requests.post(
            f"{BASE_URL}/auth/login",
            data={"username": worker_email, "password": "password123"}
        )
        
        if login_resp.status_code != 200:
            print(f"   ❌ Login failed! Server said: {login_resp.status_code}. Skipping turn.")
            time.sleep(2)
            continue
            
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # --- 3. THE ACTION DECIDER ---
        action = random.choices(
            population=[
                "create_issue", 
                "update_issue", 
                "browse_board", 
                "update_profile", 
                "invite_user",
                "delete_issue" # <-- Added here!
            ], 
            # 40 + 27 + 20 + 8 + 2 + 3 = 100%
            weights=[40, 27, 20, 8, 2, 3], 
            k=1
        )[0]

        # ------------------------------------------
        # ACTION: CREATE ISSUE
        # ------------------------------------------
        if action == "create_issue":
            print("   🔨 Action: Creating a new issue...")
            payload = {
                "title": fake.catch_phrase(),
                "description": fake.paragraph(),
                "priority": random.choice(["low", "medium", "high"]),
                "type": random.choice(["bug", "task"])
            }
            resp = requests.post(f"{BASE_URL}/issues/", json=payload, headers=headers)
            print(f"   ↳ Result: {resp.status_code}")

        # ------------------------------------------
        # ACTION: UPDATE ISSUE
        # ------------------------------------------
        elif action == "update_issue":
            print("   📝 Action: Updating an existing issue...")
            fetch_resp = requests.get(f"{BASE_URL}/issues/", headers=headers)
            
            if fetch_resp.status_code == 200 and len(fetch_resp.json()) > 0:
                target = random.choice(fetch_resp.json())
                target_id = target["id"]
                
                payload = {"status": random.choice(["in_progress", "done"])}
                update_resp = requests.put(f"{BASE_URL}/issues/{target_id}", json=payload, headers=headers)
                print(f"   ↳ Result: Changed Issue {target_id[:8]} to {payload['status']} (Status: {update_resp.status_code})")
            else:
                print("   ↳ Result: No issues available to update.")

        # ------------------------------------------
        # ACTION: BROWSE BOARD
        # ------------------------------------------
        elif action == "browse_board":
            print("   👀 Action: Browsing the board and checking logs...")
            fetch_resp = requests.get(f"{BASE_URL}/issues/", headers=headers)
            
            if fetch_resp.status_code == 200 and len(fetch_resp.json()) > 0:
                target = random.choice(fetch_resp.json())
                log_resp = requests.get(f"{BASE_URL}/issues/{target['id']}/logs", headers=headers)
                print(f"   ↳ Result: Read logs for issue {target['id'][:8]} (Status: {log_resp.status_code})")
            else:
                print("   ↳ Result: Board is empty.")

        # ------------------------------------------
        # ACTION: UPDATE PROFILE
        # ------------------------------------------
        elif action == "update_profile":
            print("   👤 Action: Updating user profile settings...")
            payload = {
                "presence": random.choice(["online", "away", "busy", "offline"]),
                "phone": fake.phone_number()[:20] # Keep it under standard DB limits
            }
            resp = requests.put(f"{BASE_URL}/users/profile", json=payload, headers=headers)
            print(f"   ↳ Result: {resp.status_code}")

        # ------------------------------------------
        # ACTION: INVITE USER (Admin/IT/Owner Only)
        # ------------------------------------------
        elif action == "invite_user":
            if worker_role in ["admin", "owner", "it"]:
                print("   👔 Action: High-privilege user is inviting a new employee...")
                f_name = fake.first_name()
                payload = {
                    "first_name": f_name,
                    "last_name": fake.last_name(),
                    "email": f"{f_name.lower()}@{fake.domain_name()}",
                    "password": "Password123!", # Satisfies your strict regex validator!
                    "role": "developer"
                }
                resp = requests.post(f"{BASE_URL}/users/", json=payload, headers=headers)
                print(f"   ↳ Result: {resp.status_code}")
            else:
                print("   🚫 Action Skipped: Bot tried to invite a user, but lacks Admin privileges.")

        # ------------------------------------------
        # ACTION: DELETE ISSUE (Managers & Above Only)
        # ------------------------------------------
        elif action == "delete_issue":
            # Based on your seed script, 'admin' and 'owner' definitely pass the >= 50 weight check
            if worker_role in ["admin", "owner"]:
                print("   🗑️ Action: High-privilege user is cleaning up the board (Deleting an issue)...")
                
                # First, fetch the issues to find one to delete
                fetch_resp = requests.get(f"{BASE_URL}/issues/", headers=headers)
                
                if fetch_resp.status_code == 200 and len(fetch_resp.json()) > 0:
                    target = random.choice(fetch_resp.json())
                    target_id = target["id"]
                    
                    # Send the DELETE request
                    delete_resp = requests.delete(f"{BASE_URL}/issues/{target_id}", headers=headers)
                    print(f"   ↳ Result: Deleted Issue {target_id[:8]} (Status: {delete_resp.status_code})")
                else:
                    print("   ↳ Result: Board is already empty, nothing to delete.")
            else:
                print(f"   🚫 Action Skipped: {worker_email} ({worker_role}) tried to delete an issue, but lacks Manager privileges.")

        # --- 4. COOL DOWN ---
        iteration += 1
        print("-" * 50)
        time.sleep(random.uniform(1.5, 3.5)) # Random sleep between 1.5 and 3.5 seconds

except KeyboardInterrupt:
    print("\n🛑 Simulation stopped by user. Great testing session!")