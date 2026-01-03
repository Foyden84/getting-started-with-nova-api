"""
Simple OAuth callback server for Zoho
Captures the auth code and exchanges it for tokens automatically
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import httpx
import os
import webbrowser
from pathlib import Path
from dotenv import load_dotenv, set_key

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

client_id = os.getenv('ZOHO_CLIENT_ID')
client_secret = os.getenv('ZOHO_CLIENT_SECRET')
redirect_uri = "http://localhost:3000/api/auth/zoho/callback"

SCOPES = [
    "ZohoCRM.modules.ALL",
    "ZohoCRM.settings.ALL", 
    "ZohoCRM.users.READ",
    "ZohoMail.messages.ALL",
    "ZohoMail.accounts.READ"
]


class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/api/auth/zoho/callback':
            params = parse_qs(parsed.query)
            code = params.get('code', [None])[0]
            
            if code:
                print(f"\n✅ Received authorization code!")
                print(f"   Code: {code[:30]}...")
                
                # Exchange code for tokens
                tokens = self.exchange_code(code)
                
                if tokens and 'refresh_token' in tokens:
                    set_key(env_path, "ZOHO_REFRESH_TOKEN", tokens['refresh_token'])
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"""
                        <html><body style="font-family: Arial; text-align: center; padding: 50px;">
                        <h1 style="color: green;">Success!</h1>
                        <p>Zoho authorization complete. You can close this window.</p>
                        </body></html>
                    """)
                    print(f"\n✅ SUCCESS! Refresh token saved to .env")
                    print(f"   Refresh Token: {tokens['refresh_token'][:30]}...")
                    print(f"\n🛑 You can stop this server now (Ctrl+C)")
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    error_msg = tokens.get('error', 'Unknown error') if tokens else 'No response'
                    self.wfile.write(f"<html><body><h1>Error: {error_msg}</h1></body></html>".encode())
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def exchange_code(self, code):
        url = "https://accounts.zoho.com/oauth/v2/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code
        }
        try:
            with httpx.Client() as client:
                response = client.post(url, data=data)
                return response.json()
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def log_message(self, format, *args):
        pass  # Suppress default logging


def main():
    from urllib.parse import urlencode
    
    auth_url = f"https://accounts.zoho.com/oauth/v2/auth?{urlencode({
        'client_id': client_id,
        'response_type': 'code',
        'access_type': 'offline',
        'redirect_uri': redirect_uri,
        'scope': ','.join(SCOPES),
        'prompt': 'consent'
    })}"
    
    print("="*60)
    print("🔐 ZOHO OAUTH SERVER")
    print("="*60)
    print(f"\n📡 Starting server on http://localhost:3000")
    print(f"\n🌐 Opening browser for authorization...")
    
    server = HTTPServer(('localhost', 3000), OAuthHandler)
    webbrowser.open(auth_url)
    
    print("\n⏳ Waiting for authorization...")
    server.handle_request()  # Handle one request then exit


if __name__ == "__main__":
    main()

