from flask import Blueprint, request, session
from ..services.db_service import get_db_connection

auth_bp = Blueprint("auth_routes", __name__)

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return {"error": "Email and password are required"}, 400
        
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
    conn.close()
    
    if user:
        return {
            "success": True,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "role": user["role"]
            }
        }
    
    return {"error": "Invalid credentials"}, 401
