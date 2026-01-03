"""
Database models and CRUD operations for LeadQual AI
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, field, asdict
from .connection import execute_query, execute_one, execute_insert


@dataclass
class Lead:
    """Lead model"""
    id: Optional[str] = None
    user_id: Optional[str] = None
    config_id: Optional[str] = None
    email: str = ""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    source: Optional[str] = None
    source_details: Dict = field(default_factory=dict)
    status: str = "new"
    score: int = 0
    qualification_data: Dict = field(default_factory=dict)
    zoho_lead_id: Optional[str] = None
    zoho_synced_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    qualified_at: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        parts = [self.first_name, self.last_name]
        return " ".join(p for p in parts if p) or "Unknown"
    
    @property
    def is_qualified(self) -> bool:
        return self.status == "qualified"
    
    def to_dict(self) -> Dict:
        return asdict(self)


class LeadRepository:
    """CRUD operations for leads"""
    
    @staticmethod
    def create(lead: Lead) -> Lead:
        """Create a new lead"""
        query = """
            INSERT INTO leads (user_id, config_id, email, first_name, last_name, 
                company, job_title, phone, website, source, source_details, status, score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        import json
        result = execute_insert(query, (
            lead.user_id, lead.config_id, lead.email, lead.first_name, lead.last_name,
            lead.company, lead.job_title, lead.phone, lead.website, lead.source,
            json.dumps(lead.source_details), lead.status, lead.score
        ))
        return Lead(**result) if result else None
    
    @staticmethod
    def get_by_id(lead_id: str) -> Optional[Lead]:
        """Get lead by ID"""
        query = "SELECT * FROM leads WHERE id = %s"
        result = execute_one(query, (lead_id,))
        return Lead(**result) if result else None
    
    @staticmethod
    def get_by_email(user_id: str, email: str) -> Optional[Lead]:
        """Get lead by email for a user"""
        query = "SELECT * FROM leads WHERE user_id = %s AND email = %s"
        result = execute_one(query, (user_id, email))
        return Lead(**result) if result else None
    
    @staticmethod
    def get_by_user(user_id: str, status: str = None, limit: int = 100) -> List[Lead]:
        """Get leads for a user"""
        if status:
            query = "SELECT * FROM leads WHERE user_id = %s AND status = %s ORDER BY created_at DESC LIMIT %s"
            results = execute_query(query, (user_id, status, limit))
        else:
            query = "SELECT * FROM leads WHERE user_id = %s ORDER BY created_at DESC LIMIT %s"
            results = execute_query(query, (user_id, limit))
        return [Lead(**r) for r in results]
    
    @staticmethod
    def update(lead_id: str, **updates) -> Optional[Lead]:
        """Update a lead"""
        if not updates:
            return LeadRepository.get_by_id(lead_id)
        
        import json
        set_clauses = []
        values = []
        
        for key, value in updates.items():
            set_clauses.append(f"{key} = %s")
            if isinstance(value, dict):
                values.append(json.dumps(value))
            else:
                values.append(value)
        
        set_clauses.append("updated_at = NOW()")
        values.append(lead_id)
        
        query = f"UPDATE leads SET {', '.join(set_clauses)} WHERE id = %s RETURNING *"
        result = execute_insert(query, tuple(values))
        return Lead(**result) if result else None
    
    @staticmethod
    def update_score(lead_id: str, score: int, status: str = None) -> Optional[Lead]:
        """Update lead score and optionally status"""
        updates = {'score': score}
        if status:
            updates['status'] = status
            if status == 'qualified':
                updates['qualified_at'] = 'NOW()'
        return LeadRepository.update(lead_id, **updates)
    
    @staticmethod
    def update_zoho_sync(lead_id: str, zoho_lead_id: str) -> Optional[Lead]:
        """Update Zoho sync info"""
        query = """
            UPDATE leads SET zoho_lead_id = %s, zoho_synced_at = NOW(), updated_at = NOW()
            WHERE id = %s RETURNING *
        """
        result = execute_insert(query, (zoho_lead_id, lead_id))
        return Lead(**result) if result else None
    
    @staticmethod
    def count_by_user(user_id: str, since: datetime = None) -> int:
        """Count leads for a user"""
        if since:
            query = "SELECT COUNT(*) as count FROM leads WHERE user_id = %s AND created_at >= %s"
            result = execute_one(query, (user_id, since))
        else:
            query = "SELECT COUNT(*) as count FROM leads WHERE user_id = %s"
            result = execute_one(query, (user_id,))
        return result['count'] if result else 0

