"""Quick script to exchange Zoho auth code for tokens"""

import httpx
import os
from pathlib import Path
from dotenv import load_dotenv, set_key

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# The authorization code from the URL
AUTH_CODE = "1000.131e11075fea6a04ac539f4251b6051.3d34b53d282e35d4210a24c.b85927a"

client_id = os.getenv('ZOHO_CLIENT_ID')
client_secret = os.getenv('ZOHO_CLIENT_SECRET')
redirect_uri = "http://localhost:3000/api/auth/zoho/callback"

url = "https://accounts.zoho.com/oauth/v2/token"

data = {
    "grant_type": "authorization_code",
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": redirect_uri,
    "code": AUTH_CODE
}

print("🔄 Exchanging authorization code for tokens...")
print(f"   Client ID: {client_id[:20]}...")

with httpx.Client() as client:
    response = client.post(url, data=data)
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Response: {result}")
    
    if 'refresh_token' in result:
        refresh_token = result['refresh_token']
        set_key(env_path, "ZOHO_REFRESH_TOKEN", refresh_token)
        print(f"\n✅ SUCCESS!")
        print(f"   Refresh Token: {refresh_token[:30]}...")
        print(f"   Saved to .env file!")
    elif 'access_token' in result:
        print(f"\n⚠️  Got access token but no refresh token")
        print(f"   Access Token: {result['access_token'][:30]}...")
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error')}")

