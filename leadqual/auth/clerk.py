"""
Clerk Authentication for FastAPI
Validates JWT tokens from Clerk frontend SDK
"""

import os
from typing import Optional
from pathlib import Path
from functools import lru_cache

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)


class ClerkUser(BaseModel):
    """Authenticated user from Clerk"""
    user_id: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization_id: Optional[str] = None


# Bearer token security scheme
bearer_scheme = HTTPBearer(auto_error=False)


@lru_cache()
def get_clerk_secret_key() -> str:
    """Get Clerk secret key from environment"""
    secret = os.getenv('CLERK_SECRET_KEY')
    if not secret:
        raise ValueError("CLERK_SECRET_KEY not configured in environment")
    return secret


def _extract_user_from_payload(payload: dict) -> ClerkUser:
    """Extract user info from Clerk JWT payload"""
    return ClerkUser(
        user_id=payload.get('sub', ''),
        email=payload.get('email'),
        first_name=payload.get('first_name'),
        last_name=payload.get('last_name'),
        organization_id=payload.get('org_id')
    )


async def clerk_auth(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)
) -> ClerkUser:
    """
    Dependency for authenticating requests with Clerk JWT tokens.
    
    Usage:
        @app.get("/protected")
        async def protected_route(user: ClerkUser = Depends(clerk_auth)):
            return {"user_id": user.user_id}
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = credentials.credentials
    
    try:
        # Import Clerk SDK (lazy import to handle optional dependency)
        from clerk_backend_api import Clerk
        from clerk_backend_api.security import authenticate_request
        from clerk_backend_api.security.types import AuthenticateRequestOptions
        import httpx
        
        # Build httpx request from FastAPI request
        httpx_request = httpx.Request(
            method=request.method,
            url=str(request.url),
            headers=dict(request.headers)
        )
        
        # Initialize Clerk SDK
        clerk = Clerk(bearer_auth=get_clerk_secret_key())
        
        # Get authorized parties from env (comma-separated list)
        authorized_parties = os.getenv('CLERK_AUTHORIZED_PARTIES', '').split(',')
        authorized_parties = [p.strip() for p in authorized_parties if p.strip()]
        
        # Authenticate the request
        request_state = clerk.authenticate_request(
            httpx_request,
            AuthenticateRequestOptions(
                authorized_parties=authorized_parties if authorized_parties else None
            )
        )
        
        if not request_state.is_signed_in:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token verification failed: {request_state.reason}",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Extract user from payload
        return _extract_user_from_payload(request_state.payload)
        
    except ImportError:
        # Fallback: Manual JWT verification if clerk-backend-api not installed
        return await _manual_jwt_verify(token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def _manual_jwt_verify(token: str) -> ClerkUser:
    """Fallback JWT verification without Clerk SDK"""
    import jwt
    import httpx
    
    # Get Clerk publishable key to determine JWKS URL
    clerk_pub_key = os.getenv('CLERK_PUBLISHABLE_KEY', '')
    
    # Extract frontend API from publishable key (pk_test_xxx or pk_live_xxx)
    # The key contains the frontend API subdomain
    if not clerk_pub_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="CLERK_PUBLISHABLE_KEY not configured"
        )
    
    try:
        # Decode without verification first to get issuer
        unverified = jwt.decode(token, options={"verify_signature": False})
        issuer = unverified.get('iss', '')
        
        # Fetch JWKS from Clerk
        jwks_url = f"{issuer}/.well-known/jwks.json"
        async with httpx.AsyncClient() as client:
            resp = await client.get(jwks_url)
            jwks = resp.json()
        
        # Get the signing key
        from jwt import PyJWKClient
        jwk_client = PyJWKClient(jwks_url)
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        
        # Verify and decode
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False}
        )
        
        return _extract_user_from_payload(payload)
        
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )


# Convenience alias
get_current_user = clerk_auth

