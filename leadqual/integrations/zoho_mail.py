"""
Zoho Mail Integration for LeadQual AI
Handles sending qualification emails via Zoho Mail API
"""

import os
import httpx
from typing import Optional, Dict, Any, List
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta

env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)


class ZohoMail:
    """Zoho Mail API client for sending qualification emails"""
    
    ACCOUNTS_URL = "https://accounts.zoho.com"
    MAIL_API_URL = "https://mail.zoho.com/api"
    
    def __init__(self):
        self.client_id = os.getenv('ZOHO_CLIENT_ID')
        self.client_secret = os.getenv('ZOHO_CLIENT_SECRET')
        self.refresh_token = os.getenv('ZOHO_REFRESH_TOKEN', '').strip("'\"")
        self.account_id = os.getenv('ZOHO_MAIL_ACCOUNT_ID')
        self.access_token = None
        self.token_expires_at = None
        
        if not all([self.client_id, self.client_secret, self.refresh_token]):
            raise ValueError("Zoho credentials not configured")
    
    async def _get_access_token(self) -> str:
        """Get a fresh access token using refresh token"""
        url = f"{self.ACCOUNTS_URL}/oauth/v2/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data)
            result = response.json()
        
        if "access_token" in result:
            self.access_token = result["access_token"]
            self.token_expires_at = datetime.now() + timedelta(seconds=result.get("expires_in", 3600))
            return self.access_token
        else:
            raise ValueError(f"Failed to get access token: {result}")
    
    async def _ensure_access_token(self) -> str:
        """Ensure we have a valid access token"""
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at - timedelta(minutes=5):
                return self.access_token
        return await self._get_access_token()
    
    async def get_account_id(self) -> str:
        """Get the mail account ID (needed for sending emails)"""
        if self.account_id:
            return self.account_id
        
        token = await self._ensure_access_token()
        url = f"{self.MAIL_API_URL}/accounts"
        headers = {"Authorization": f"Zoho-oauthtoken {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            result = response.json()
        
        if "data" in result and len(result["data"]) > 0:
            self.account_id = result["data"][0]["accountId"]
            return self.account_id
        else:
            raise ValueError(f"No mail accounts found: {result}")
    
    async def send_email(
        self,
        to_address: str,
        subject: str,
        html_content: str,
        from_address: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send an email via Zoho Mail"""
        token = await self._ensure_access_token()
        account_id = await self.get_account_id()
        
        url = f"{self.MAIL_API_URL}/accounts/{account_id}/messages"
        headers = {
            "Authorization": f"Zoho-oauthtoken {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "toAddress": to_address,
            "subject": subject,
            "content": html_content,
            "mailFormat": "html"
        }
        
        if from_address:
            payload["fromAddress"] = from_address
        if cc:
            payload["ccAddress"] = ",".join(cc)
        if bcc:
            payload["bccAddress"] = ",".join(bcc)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            result = response.json()
        
        return result
    
    async def test_connection(self) -> bool:
        """Test mail connection by fetching account info"""
        try:
            account_id = await self.get_account_id()
            print(f"✅ Zoho Mail connected! Account ID: {account_id}")
            return True
        except Exception as e:
            print(f"❌ Zoho Mail connection failed: {e}")
            return False


async def test():
    """Test Zoho Mail connection"""
    mail = ZohoMail()
    await mail.test_connection()


if __name__ == "__main__":
    import asyncio
    asyncio.run(test())

