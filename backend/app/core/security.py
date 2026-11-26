from datetime import datetime, timedelta, timezone
import hashlib, secrets
import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from .config import settings

password_hash = PasswordHash((Argon2Hasher(),))
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)

def create_access_token(subject: str, role: str):
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_minutes)
    return jwt.encode({"sub": subject, "role": role, "type":"access", "exp": exp}, settings.jwt_secret, algorithm=ALGORITHM)

def create_refresh_token():
    return secrets.token_urlsafe(48)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def decode_access_token(token: str):
    return jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
