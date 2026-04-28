from src.database.config import supabase

import bcrypt

def hash_pass(password):
    # Hash the password using bcrypt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def check_password(password, hashed):    
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode(), hashed.encode())

def check_teacher_exists(username):
    # Check for unique username, returns false when username is already taken

    response = supabase.table("teachers").select("username").eq("username", username).execute()

    return len(response.data) > 0

def create_teacher(username, password, name):

    data = {"username" : username,
            "password" : hash_pass(password),
            "name" : name}
    
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):

    response = supabase.table("teachers").select("*").eq("username", username).execute()

    if response.data:
        teacher = response.data[0]
        if check_password(password, teacher["password"]):
            return teacher
    return None


def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data


