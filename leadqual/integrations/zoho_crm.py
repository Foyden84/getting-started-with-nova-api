"""
Zoho CRM Integration for LeadQual AI
Handles pushing qualified leads to Zoho CRM
"""

import os
import httpx
from typing import Optional, Dict, Any, List
from pathlib import Path
from dotenv import load_dotenv, set_key
from datetime import datetime, timedelta

env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)


class ZohoCRM:
    """Zoho CRM API client"""
    
    ACCOUNTS_URL = "https://accounts.zoho.com"
    API_URL = "https://www.zohoapis.com/crm/v3"
    
    def __init__(self):
        self.client_id = os.getenv('ZOHO_CLIENT_ID')
        self.client_secret = os.getenv('ZOHO_CLIENT_SECRET')
        self.refresh_token = os.getenv('ZOHO_REFRESH_TOKEN', '').strip("'\"")
        self.access_token = None
        self.token_expires_at = None
        
        if not all([self.client_id, self.client_secret, self.refresh_token]):
            raise ValueError("Zoho credentials not configured")
    
    async def _ensure_access_token(self):
        """Get or refresh access token"""
        if self.access_token and self.token_expires_at and datetime.now() < self.token_expires_at:
            return self.access_token
        
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
        
        if 'access_token' in result:
            self.access_token = result['access_token']
            expires_in = result.get('expires_in', 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            return self.access_token
        else:
            raise Exception(f"Failed to get access token: {result}")
    
    async def _request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make authenticated API request"""
        token = await self._ensure_access_token()
        url = f"{self.API_URL}/{endpoint}"
        headers = {
            "Authorization": f"Zoho-oauthtoken {token}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, headers=headers)
            elif method == "POST":
                response = await client.post(url, headers=headers, json=data)
            elif method == "PUT":
                response = await client.put(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
        
        return response.json()
    
    async def create_lead(self, lead_data: Dict[str, Any]) -> Dict:
        """Create a lead in Zoho CRM"""
        # Map our lead fields to Zoho fields
        zoho_lead = {
            "First_Name": lead_data.get('first_name', ''),
            "Last_Name": lead_data.get('last_name', 'Unknown'),
            "Email": lead_data.get('email'),
            "Company": lead_data.get('company', 'Unknown'),
            "Phone": lead_data.get('phone', ''),
            "Website": lead_data.get('website', ''),
            "Designation": lead_data.get('job_title', ''),
            "Lead_Source": lead_data.get('source', 'LeadQual AI'),
            "Lead_Status": "Qualified",
            "Description": self._build_description(lead_data)
        }
        
        # Remove empty values
        zoho_lead = {k: v for k, v in zoho_lead.items() if v}
        
        payload = {"data": [zoho_lead]}
        result = await self._request("POST", "Leads", payload)
        
        return result
    
    def _build_description(self, lead_data: Dict) -> str:
        """Build description from qualification data"""
        lines = ["=== LeadQual AI Qualification ==="]
        lines.append(f"Score: {lead_data.get('score', 0)}/100")
        lines.append(f"Status: {lead_data.get('status', 'unknown')}")
        
        qual_data = lead_data.get('qualification_data', {})
        if qual_data:
            lines.append("\n--- Qualification Responses ---")
            for q, a in qual_data.items():
                lines.append(f"{q}: {a}")
        
        return "\n".join(lines)
    
    async def get_users(self) -> List[Dict]:
        """Get CRM users (for testing connection)"""
        result = await self._request("GET", "users?type=AllUsers")
        return result.get('users', [])
    
    async def test_connection(self) -> bool:
        """Test CRM connection"""
        try:
            users = await self.get_users()
            print(f"✅ Zoho CRM connected! Found {len(users)} users.")
            return True
        except Exception as e:
            print(f"❌ Zoho CRM connection failed: {e}")
            return False


async def test():
    """Test Zoho CRM connection"""
    crm = ZohoCRM()
    await crm.test_connection()


if __name__ == "__main__":
    import asyncio
    asyncio.run(test())

