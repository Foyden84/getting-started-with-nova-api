"""
Zoho OAuth Handler for LeadQual AI
Handles OAuth 2.0 flow to get access and refresh tokens
"""

import os
import httpx
import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse
from pathlib import Path
from dotenv import load_dotenv, set_key

# Load environment
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)


class ZohoOAuth:
    """Handle Zoho OAuth 2.0 authentication"""
    
    ACCOUNTS_URL = "https://accounts.zoho.com"
    
    # Scopes needed for CRM and Mail
    SCOPES = [
        "ZohoCRM.modules.ALL",
        "ZohoCRM.settings.ALL", 
        "ZohoCRM.users.READ",
        "ZohoMail.messages.ALL",
        "ZohoMail.accounts.READ"
    ]
    
    def __init__(self):
        self.client_id = os.getenv('ZOHO_CLIENT_ID')
        self.client_secret = os.getenv('ZOHO_CLIENT_SECRET')
        self.redirect_uri = "http://localhost:3000/api/auth/zoho/callback"
        
        if not self.client_id or not self.client_secret:
            raise ValueError("ZOHO_CLIENT_ID and ZOHO_CLIENT_SECRET required")
    
    def get_authorization_url(self) -> str:
        """Generate the authorization URL for user consent"""
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "access_type": "offline",  # Required to get refresh token
            "redirect_uri": self.redirect_uri,
            "scope": ",".join(self.SCOPES),
            "prompt": "consent"  # Force consent to get refresh token
        }
        return f"{self.ACCOUNTS_URL}/oauth/v2/auth?{urlencode(params)}"
    
    def exchange_code_for_tokens(self, authorization_code: str) -> dict:
        """Exchange authorization code for access and refresh tokens"""
        url = f"{self.ACCOUNTS_URL}/oauth/v2/token"
        
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": authorization_code
        }
        
        with httpx.Client() as client:
            response = client.post(url, data=data)
            response.raise_for_status()
            return response.json()
    
    def refresh_access_token(self, refresh_token: str) -> dict:
        """Get a new access token using refresh token"""
        url = f"{self.ACCOUNTS_URL}/oauth/v2/token"
        
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token
        }
        
        with httpx.Client() as client:
            response = client.post(url, data=data)
            response.raise_for_status()
            return response.json()
    
    def save_refresh_token(self, refresh_token: str):
        """Save refresh token to .env file"""
        set_key(env_path, "ZOHO_REFRESH_TOKEN", refresh_token)
        print(f"✅ Refresh token saved to .env file")
    
    def start_oauth_flow(self):
        """Start the OAuth flow - opens browser for authorization"""
        auth_url = self.get_authorization_url()
        print("\n" + "="*60)
        print("🔐 ZOHO OAUTH AUTHORIZATION")
        print("="*60)
        print("\n1. Opening browser for Zoho authorization...")
        print("\n2. After authorizing, you'll be redirected to a URL like:")
        print("   http://localhost:3000/api/auth/zoho/callback?code=XXXXX")
        print("\n3. Copy the 'code' parameter from that URL")
        print("\n" + "="*60)
        
        webbrowser.open(auth_url)
        
        # Wait for user to paste the code
        print("\n📋 Paste the authorization code here:")
        code = input("Code: ").strip()
        
        if not code:
            print("❌ No code provided")
            return None
        
        try:
            print("\n🔄 Exchanging code for tokens...")
            tokens = self.exchange_code_for_tokens(code)
            
            if 'refresh_token' in tokens:
                self.save_refresh_token(tokens['refresh_token'])
                print(f"\n✅ Access Token: {tokens['access_token'][:20]}...")
                print(f"✅ Refresh Token: {tokens['refresh_token'][:20]}...")
                print(f"✅ Expires In: {tokens.get('expires_in', 'N/A')} seconds")
                return tokens
            else:
                print(f"⚠️  No refresh token in response: {tokens}")
                return tokens
                
        except Exception as e:
            print(f"❌ Error exchanging code: {e}")
            return None


def main():
    """Run OAuth flow from command line"""
    oauth = ZohoOAuth()
    oauth.start_oauth_flow()


if __name__ == "__main__":
    main()

