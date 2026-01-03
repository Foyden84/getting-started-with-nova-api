"""
FastAPI Application for LeadQual AI
Main API endpoints for lead qualification
"""

import os
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List, Any
from pathlib import Path
from dotenv import load_dotenv

# Load env from project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

from .agent.qualifier import LeadQualifierAgent
from .integrations.zoho_crm import ZohoCRM
from .integrations.zoho_mail import ZohoMail
from .auth import clerk_auth, ClerkUser

app = FastAPI(
    title="LeadQual AI",
    description="AI-powered lead qualification with Amazon Nova",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
agent = None
zoho = None


def get_agent() -> LeadQualifierAgent:
    global agent
    if agent is None:
        agent = LeadQualifierAgent()
    return agent


def get_zoho() -> ZohoCRM:
    global zoho
    if zoho is None:
        zoho = ZohoCRM()
    return zoho


# Request/Response Models
class LeadCreate(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[str] = "Website"


class LeadResponse(BaseModel):
    lead_email: EmailStr
    response_text: str


class GenerateEmailRequest(BaseModel):
    lead_email: EmailStr
    lead_name: Optional[str] = None
    company: Optional[str] = None
    conversation_history: Optional[str] = ""
    current_score: Optional[int] = 0
    custom_questions: Optional[str] = ""


# Endpoints
@app.get("/")
async def root():
    return {"message": "LeadQual AI is running!", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy", "services": {"agent": agent is not None, "zoho": zoho is not None}}


@app.post("/api/leads/generate-email")
async def generate_qualification_email(
    request: GenerateEmailRequest,
    user: ClerkUser = Depends(clerk_auth)
):
    """Generate a qualification email for a lead (requires authentication)"""
    try:
        qualifier = get_agent()
        result = qualifier.generate_qualification_email(
            lead_name=request.lead_name,
            lead_email=request.lead_email,
            lead_company=request.company or "Unknown",
            conversation_history=request.conversation_history,
            current_score=request.current_score,
            custom_questions=request.custom_questions
        )
        return {"success": True, "data": result, "user_id": user.user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/leads/analyze-response")
async def analyze_lead_response(
    request: LeadResponse,
    user: ClerkUser = Depends(clerk_auth)
):
    """Analyze a lead's email response (requires authentication)"""
    try:
        qualifier = get_agent()
        result = qualifier.analyze_response(response_text=request.response_text)
        return {"success": True, "data": result, "user_id": user.user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/leads/push-to-crm")
async def push_lead_to_crm(
    lead_data: Dict[str, Any],
    user: ClerkUser = Depends(clerk_auth)
):
    """Push a qualified lead to Zoho CRM (requires authentication)"""
    try:
        crm = get_zoho()
        result = await crm.create_lead(lead_data)
        return {"success": True, "data": result, "user_id": user.user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/zoho/test")
async def test_zoho_connection(user: ClerkUser = Depends(clerk_auth)):
    """Test Zoho CRM connection (requires authentication)"""
    try:
        crm = get_zoho()
        connected = await crm.test_connection()
        return {"success": connected, "user_id": user.user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/me")
async def get_current_user_info(user: ClerkUser = Depends(clerk_auth)):
    """Get current authenticated user info"""
    return {
        "user_id": user.user_id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "organization_id": user.organization_id
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

