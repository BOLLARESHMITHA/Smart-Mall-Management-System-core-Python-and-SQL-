# src/service/auth_service.py
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import hashlib

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE = "users"  # <-- updated table name

def signup_user(email, password, role):
    # Hash password (optional but recommended)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Check if user already exists
    existing = supabase.table(TABLE).select("*").eq("email", email).execute()
    if existing.data:
        raise ValueError("Email already registered")

    # Insert new user
    supabase.table(TABLE).insert({
        "email": email,
        "password": hashed_password,
        "role": role
    }).execute()
    return {"email": email, "role": role}


def login_user(email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    response = supabase.table(TABLE).select("*").eq("email", email).eq("password", hashed_password).execute()
    if not response.data:
        raise ValueError("Invalid email or password")
    return response.data[0]
