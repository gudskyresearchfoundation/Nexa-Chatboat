"""
src/backend/auth.py — SHA-256 authentication & user registry
Add or change users by editing ADMIN_USERS and ADMIN_INFO below.
"""

import hashlib
from typing import Dict, Optional

ADMIN_USERS: Dict[str, str] = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "demo":  hashlib.sha256("demo2024".encode()).hexdigest(),
}

ADMIN_INFO: Dict[str, Dict] = {
    "admin": {
        "full_name":   "Administrator",
        "role":        "Super Admin",
        "email":       "admin@localai.dev",
        "joined":      "2024-01-01",
        "avatar_init": "AD",
    },
    "demo": {
        "full_name":   "Demo User",
        "role":        "Analyst",
        "email":       "demo@localai.dev",
        "joined":      "2024-06-01",
        "avatar_init": "DU",
    },
}


def authenticate(username: str, password: str) -> Optional[Dict]:
    """Return user info dict on success, None on failure."""
    hashed = hashlib.sha256(password.encode()).hexdigest()
    if username in ADMIN_USERS and ADMIN_USERS[username] == hashed:
        return ADMIN_INFO.get(username)
    return None
