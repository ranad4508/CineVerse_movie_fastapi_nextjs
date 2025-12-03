import secrets
import jwt
from datetime import datetime, timedelta, timezone

print("=" * 60)
print("JWT SECRET KEY GENERATOR")
print("=" * 60)

# Generate a secure random secret key
secret_key = secrets.token_urlsafe(32)
print(f"\nGenerated Secret Key:\n{secret_key}\n")

# Create a sample token
sample_data = {"sub": 1, "email": "user@example.com"}
expiration = datetime.now(timezone.utc) + timedelta(hours=24)
sample_data["exp"] = expiration

token = jwt.encode(sample_data, secret_key, algorithm="HS256")
print(f"Sample Token:\n{token}\n")

# Verify the token
try:
    decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
    print(f"Decoded Token:\n{decoded}\n")
except jwt.InvalidTokenError as e:
    print(f"Error: {e}")

print("=" * 60)
print("INSTRUCTIONS:")
print("=" * 60)
print(f"1. Update your .env file:")
print(f"   OLD: SECRET_KEY=your_super_secret_key_here")
print(f"   NEW: SECRET_KEY={secret_key}")
print(f"\n2. Restart your FastAPI application")
print(f"\n3. Login again to get a new token")
print(f"\n4. Use the new token to authorize requests")
print("=" * 60)
