#!/usr/bin/env python
import jwt
from app.core.config import settings
from app.core.security import decode_access_token

print("\n" + "=" * 70)
print("JWT TOKEN VERIFICATION & DEBUGGING TOOL")
print("=" * 70)

# Display current settings
print(f"\n[CONFIG]")
print(f"SECRET_KEY: {settings.SECRET_KEY}")
print(f"ALGORITHM: {settings.ALGORITHM}")
print(f"Token Expiry: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes")

# Get token from user
token = input("\nPaste your JWT token here: ").strip()

if not token:
    print("No token provided!")
    exit(1)

print("\n[DECODING TOKEN]")
print("-" * 70)

try:
    # Decode without verification first (to see header/payload structure)
    parts = token.split('.')
    if len(parts) != 3:
        print("ERROR: Invalid token format. Token must have 3 parts separated by dots")
        exit(1)
    
    import base64
    import json
    
    # Add padding if needed
    def decode_part(part):
        padding = 4 - len(part) % 4
        if padding != 4:
            part += '=' * padding
        return json.loads(base64.urlsafe_b64decode(part))
    
    header = decode_part(parts[0])
    payload = decode_part(parts[1])
    
    print("\n[HEADER]")
    print(json.dumps(header, indent=2))
    
    print("\n[PAYLOAD]")
    print(json.dumps(payload, indent=2, default=str))
    
    # Now decode with verification
    print("\n[VERIFICATION]")
    print("-" * 70)
    
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print("✓ Token signature is VALID")
    print(f"✓ User ID (sub): {decoded.get('sub')}")
    print(f"✓ Expiration: {decoded.get('exp')}")
    
    # Check if expired
    from datetime import datetime, timezone
    if decoded.get('exp'):
        exp_time = datetime.fromtimestamp(decoded['exp'], tz=timezone.utc)
        now = datetime.now(timezone.utc)
        if now > exp_time:
            print(f"✗ Token EXPIRED at {exp_time}")
        else:
            print(f"✓ Token valid until {exp_time}")
    
    print("\n[HOW TO USE THIS TOKEN]")
    print("-" * 70)
    print(f"Authorization Header:")
    print(f"  Authorization: Bearer {token}")
    print(f"\nExample curl command:")
    print(f'  curl -X GET "http://localhost:8000/api/v1/users/me" \\')
    print(f'    -H "Authorization: Bearer {token}"')
    
except jwt.ExpiredSignatureError:
    print("✗ Token has EXPIRED")
    exit(1)
except jwt.InvalidTokenError as e:
    print(f"✗ Token verification FAILED: {e}")
    print("\nPossible causes:")
    print("  1. Wrong SECRET_KEY in .env file")
    print("  2. Token was generated with a different secret key")
    print("  3. Token is corrupted")
    exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

print("\n" + "=" * 70)
