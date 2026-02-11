import base64
import sys

# Read the cookies file
with open('backend/cookies.txt', 'rb') as f:
    cookies_content = f.read()

# Encode to base64
encoded = base64.b64encode(cookies_content).decode('utf-8')

print("=" * 80)
print("BASE64 ENCODED COOKIES FOR RENDER")
print("=" * 80)
print()
print("Copy the text below and paste it into Render's YOUTUBE_COOKIES_BASE64 environment variable:")
print()
print(encoded)
print()
print("=" * 80)
print(f"Total length: {len(encoded)} characters")
print("=" * 80)
