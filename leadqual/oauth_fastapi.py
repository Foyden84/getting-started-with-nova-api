"""FastAPI OAuth callback server for Zoho"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import httpx
import os
import uvicorn
from pathlib import Path
from dotenv import load_dotenv, set_key

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

app = FastAPI()

client_id = os.getenv('ZOHO_CLIENT_ID')
client_secret = os.getenv('ZOHO_CLIENT_SECRET')
redirect_uri = "http://localhost:3000/api/auth/zoho/callback"


@app.get("/api/auth/zoho/callback")
async def zoho_callback(code: str = None, error: str = None):
    if error:
        return HTMLResponse(f"<h1>Error: {error}</h1>")
    
    if not code:
        return HTMLResponse("<h1>No code received</h1>")
    
    print(f"\n✅ Received authorization code: {code[:30]}...")
    
    # Exchange code for tokens
    url = "https://accounts.zoho.com/oauth/v2/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": code
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)
        result = response.json()
    
    print(f"   Token response: {result}")
    
    if 'refresh_token' in result:
        set_key(env_path, "ZOHO_REFRESH_TOKEN", result['refresh_token'])
        print(f"\n✅ SUCCESS! Refresh token saved!")
        print(f"   Refresh Token: {result['refresh_token'][:30]}...")
        return HTMLResponse("""
            <html>
            <body style="font-family: Arial; text-align: center; padding: 50px; background: #1a1a2e; color: white;">
                <h1 style="color: #4ade80;">✅ Success!</h1>
                <p>Zoho authorization complete!</p>
                <p>Refresh token has been saved to your .env file.</p>
                <p style="color: #888;">You can close this window.</p>
            </body>
            </html>
        """)
    else:
        error_msg = result.get('error', 'Unknown error')
        return HTMLResponse(f"""
            <html>
            <body style="font-family: Arial; text-align: center; padding: 50px; background: #1a1a2e; color: white;">
                <h1 style="color: #f87171;">❌ Error</h1>
                <p>{error_msg}</p>
            </body>
            </html>
        """)


@app.get("/")
async def home():
    from urllib.parse import urlencode
    scopes = "ZohoCRM.modules.ALL,ZohoCRM.settings.ALL,ZohoCRM.users.READ,ZohoMail.messages.ALL,ZohoMail.accounts.READ"
    auth_url = f"https://accounts.zoho.com/oauth/v2/auth?{urlencode({
        'client_id': client_id,
        'response_type': 'code',
        'access_type': 'offline',
        'redirect_uri': redirect_uri,
        'scope': scopes,
        'prompt': 'consent'
    })}"
    return HTMLResponse(f"""
        <html>
        <body style="font-family: Arial; text-align: center; padding: 50px; background: #1a1a2e; color: white;">
            <h1>🔐 LeadQual AI - Zoho OAuth</h1>
            <p>Click the button below to authorize Zoho access:</p>
            <a href="{auth_url}" style="display: inline-block; margin-top: 20px; padding: 15px 30px; background: #3b82f6; color: white; text-decoration: none; border-radius: 8px; font-size: 18px;">
                Connect Zoho Account
            </a>
        </body>
        </html>
    """)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔐 ZOHO OAUTH SERVER")
    print("="*60)
    print("\n📡 Starting server at http://localhost:3000")
    print("\n👉 Open http://localhost:3000 in your browser")
    print("   Then click 'Connect Zoho Account'\n")
    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="warning")

