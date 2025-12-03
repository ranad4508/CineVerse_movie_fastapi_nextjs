#!/usr/bin/env python
"""
Generate a valid JWT token with all user data for testing
"""
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

print("\n" + "=" * 80)
print("JWT TOKEN GENERATOR WITH USER DATA")
print("=" * 80)

# Sample user data (like after login)
user_data = {
    "sub": "1",
    "email": "admin@example.com",
    "username": "admin",
    "full_name": "Admin User",
    "role": "admin",
    "is_active": True
}

# Generate expiration and issued-at times
iat = datetime.now(timezone.utc)
exp = iat + timedelta(hours=24)

# Create payload
payload = {
    **user_data,
    "iat": int(iat.timestamp()),
    "exp": int(exp.timestamp())
}

print("\n[PAYLOAD]")
print("-" * 80)
import json
print(json.dumps(payload, indent=2))

# Generate token with current SECRET_KEY
token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

print("\n[GENERATED TOKEN]")
print("-" * 80)
print(token)

# Verify the token
print("\n[VERIFICATION]")
print("-" * 80)
try:
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print("✓ Token signature: VALID")
    print("✓ Token decoding: SUCCESSFUL")
    print(f"✓ User ID: {decoded['sub']}")
    print(f"✓ Email: {decoded['email']}")
    print(f"✓ Username: {decoded['username']}")
    print(f"✓ Role: {decoded['role']}")
except jwt.InvalidTokenError as e:
    print(f"✗ Token verification failed: {e}")

print("\n[HOW TO USE]")
print("-" * 80)
print("1. Copy the token above")
print("2. Use in Authorization header:")
print(f"   Authorization: Bearer {token}")
print("\n3. Verify on jwt.io:")
print(f"   - Paste token in 'Encoded' field")
print(f"   - Paste this in 'Secret' field:")
print(f"     {settings.SECRET_KEY}")
print(f"   - You should see all the payload data!")

print("\n[PAYLOAD YOU'LL SEE IN JWT]")
print("-" * 80)
print(json.dumps(payload, indent=2, default=str))

print("\n[SECRET KEY BEING USED]")
print("-" * 80)
print(settings.SECRET_KEY)

print("\n" + "=" * 80)
print("Token is ready to use! Restart your app and test login to get a real token.")
print("=" * 80 + "\n")
