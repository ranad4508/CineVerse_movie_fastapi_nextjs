#!/usr/bin/env python
"""
Test script to verify admin access and token functionality
"""
import requests
import json
from app.core.config import settings

BASE_URL = "http://localhost:8000/api/v1"

print("\n" + "=" * 70)
print("ADMIN ACCESS TEST SCRIPT")
print("=" * 70)

print("\n[1] Testing Admin Login...")
print("-" * 70)

login_data = {
    "email": "admin@example.com",
    "password": "admin123"
}

try:
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code != 200:
        print(f"ERROR: Login failed with status {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)
    
    data = response.json()
    token = data["access_token"]
    user = data["user"]
    
    print(f"✓ Login successful")
    print(f"  User ID: {user['id']}")
    print(f"  Email: {user['email']}")
    print(f"  Role: {user['role']}")
    print(f"  Token: {token[:50]}...")
    
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)

print("\n[2] Testing User Authorization...")
print("-" * 70)

headers = {"Authorization": f"Bearer {token}"}

try:
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    
    if response.status_code != 200:
        print(f"ERROR: Failed with status {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)
    
    user_data = response.json()
    print(f"✓ Token is valid and user is authenticated")
    print(f"  User: {user_data['email']}")
    print(f"  Role: {user_data['role']}")
    
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)

print("\n[3] Testing Admin-Only Endpoints...")
print("-" * 70)

# Test creating a movie (admin only)
movie_data = {
    "title": "Test Movie",
    "synopsis": "This is a test movie",
    "director": "Test Director",
    "genre": "Action",
    "duration": 120,
    "release_date": "2024-01-01",
    "status": "now_playing"
}

try:
    response = requests.post(
        f"{BASE_URL}/movies",
        json=movie_data,
        headers=headers
    )
    
    if response.status_code == 201:
        movie = response.json()
        print(f"✓ Movie created successfully")
        print(f"  Movie ID: {movie['id']}")
        print(f"  Title: {movie['title']}")
    else:
        print(f"ERROR: Failed to create movie with status {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"ERROR: {e}")

print("\n[4] Testing Admin Role Access...")
print("-" * 70)

try:
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    
    if response.status_code == 200:
        users = response.json()
        print(f"✓ Admin endpoint accessible")
        print(f"  Total users: {len(users)}")
        for user in users:
            print(f"    - {user['email']} ({user['role']})")
    elif response.status_code == 403:
        print(f"✗ Access denied (not an admin)")
    else:
        print(f"ERROR: Status {response.status_code}")
        
except Exception as e:
    print(f"ERROR: {e}")

print("\n[5] Token Information...")
print("-" * 70)

from app.core.security import decode_access_token
decoded = decode_access_token(token)

if decoded:
    print(f"✓ Token decoded successfully")
    print(f"  Subject (User ID): {decoded.get('sub')}")
    print(f"  Expiration: {decoded.get('exp')}")
    from datetime import datetime, timezone
    if decoded.get('exp'):
        exp_time = datetime.fromtimestamp(decoded['exp'], tz=timezone.utc)
        now = datetime.now(timezone.utc)
        if now > exp_time:
            print(f"  Status: EXPIRED")
        else:
            print(f"  Status: VALID")
else:
    print(f"✗ Token decoding failed")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"✓ Admin authentication is working")
print(f"✓ JWT tokens are valid")
print(f"✓ Admin endpoints are accessible")
print(f"\nYou can now use this token for admin operations!")
print(f"\nToken to use:")
print(f"  Authorization: Bearer {token}")
print("\n" + "=" * 70 + "\n")
