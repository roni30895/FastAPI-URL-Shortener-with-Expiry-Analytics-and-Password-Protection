import hashlib
from datetime import datetime, timedelta
from typing import Optional


def generate_shorten_url(original_url: str) -> str:
    if not isinstance(original_url, str):
        original_url = str(original_url)
    hash_object = hashlib.md5(original_url.encode())
    return hash_object.hexdigest()[:6]


def get_current_time() -> str:
    return datetime.utcnow().isoformat()

def get_expiry_time(hours: str) -> str:
    return (datetime.utcnow() + timedelta(hours=hours)).isoformat()

def is_expired(exp_timestamp: str) -> bool:
    return datetime.utcnow() > datetime.fromisoformat(exp_timestamp)

def hash_password(password: Optional[str]) -> Optional[str]:
    if password:
        return hashlib.sha256(password.encode()).hexdigest()
    return None

def verify_password(stored_hash: Optional[str], password: Optional[str]) -> bool:
    if not stored_hash or not password:
        return False
    return stored_hash == hashlib.sha256(password.encode()).hexdigest()
