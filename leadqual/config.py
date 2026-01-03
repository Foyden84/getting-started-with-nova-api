"""
Configuration management for LeadQual AI
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


class Config:
    """Application configuration"""
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    DEBUG = ENVIRONMENT == 'development'
    
    # Amazon Nova
    NOVA_API_KEY = os.getenv('NOVA_API_KEY')
    NOVA_BASE_URL = "https://api.nova.amazon.com/v1"
    NOVA_MODEL = "nova-2-lite-v1"  # Use lite for cost efficiency
    NOVA_MODEL_PRO = "nova-2-pro-v1"  # For complex reasoning
    
    # Database
    DATABASE_URL = os.getenv('NEON_DATABASE_URL', '').strip("'\"")
    
    # Clerk Auth
    CLERK_PUBLISHABLE_KEY = os.getenv('CLERK_PUBLISHABLE_KEY')
    CLERK_SECRET_KEY = os.getenv('CLERK_SECRET_KEY')
    
    # Stripe
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    # Zoho
    ZOHO_CLIENT_ID = os.getenv('ZOHO_CLIENT_ID')
    ZOHO_CLIENT_SECRET = os.getenv('ZOHO_CLIENT_SECRET')
    ZOHO_REFRESH_TOKEN = os.getenv('ZOHO_REFRESH_TOKEN')
    ZOHO_ORG_ID = os.getenv('ZOHO_ORG_ID')
    ZOHO_ACCOUNTS_URL = "https://accounts.zoho.com"
    ZOHO_CRM_API_URL = "https://www.zohoapis.com/crm/v3"
    ZOHO_MAIL_API_URL = "https://mail.zoho.com/api"
    
    # Gmail
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_REFRESH_TOKEN = os.getenv('GOOGLE_REFRESH_TOKEN')
    
    # App Settings
    APP_NAME = "LeadQual AI"
    APP_URL = os.getenv('APP_URL', 'http://localhost:3000')
    
    # Subscription Tiers
    TIERS = {
        'free': {'leads_limit': 25, 'price': 0},
        'starter': {'leads_limit': 200, 'price': 49},
        'pro': {'leads_limit': 1000, 'price': 149},
        'agency': {'leads_limit': 5000, 'price': 299}
    }
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = ['NOVA_API_KEY', 'DATABASE_URL']
        missing = [key for key in required if not getattr(cls, key)]
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        return True
    
    @classmethod
    def get_tier_limit(cls, tier: str) -> int:
        """Get leads limit for a subscription tier"""
        return cls.TIERS.get(tier, cls.TIERS['free'])['leads_limit']


# Validate on import
try:
    Config.validate()
except ValueError as e:
    print(f"⚠️  Configuration warning: {e}")

