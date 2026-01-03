"""
Lead Qualification Agent powered by Amazon Nova
"""

import os
import json
from typing import Dict, Any, Optional, List
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

from .prompts import SYSTEM_PROMPT, QUALIFICATION_PROMPT, SCORING_PROMPT, SUMMARY_PROMPT

env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)


class LeadQualifierAgent:
    """AI Agent for qualifying leads using Amazon Nova"""
    
    def __init__(self):
        api_key = os.getenv('NOVA_API_KEY')
        if not api_key:
            raise ValueError("NOVA_API_KEY not configured")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.nova.amazon.com/v1"
        )
        self.model = "nova-2-lite-v1"
        self.model_pro = "nova-2-pro-v1"
    
    def _call_nova(self, messages: List[Dict], use_pro: bool = False) -> str:
        """Call Amazon Nova API"""
        model = self.model_pro if use_pro else self.model
        
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON from Nova response"""
        # Try to extract JSON from response
        try:
            # Find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # Return default structure if parsing fails
        return {"error": "Failed to parse response", "raw": response}
    
    def generate_qualification_email(
        self,
        lead_name: str,
        lead_email: str,
        lead_company: str = "Unknown",
        lead_source: str = "Website",
        questions_asked: List[str] = None,
        current_score: int = 0,
        missing_info: List[str] = None,
        conversation_history: str = "",
        custom_questions: str = ""
    ) -> Dict[str, Any]:
        """Generate the next qualification email for a lead"""
        
        if questions_asked is None:
            questions_asked = []
        if missing_info is None:
            missing_info = ["budget", "authority", "need", "timeline"]
        
        prompt = QUALIFICATION_PROMPT.format(
            lead_name=lead_name or "there",
            lead_email=lead_email,
            lead_company=lead_company,
            lead_source=lead_source,
            questions_asked=", ".join(questions_asked) if questions_asked else "None yet",
            current_score=current_score,
            missing_info=", ".join(missing_info),
            conversation_history=conversation_history or "No previous conversation",
            custom_questions=custom_questions or "Use standard BANT questions"
        )
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_nova(messages)
        return self._parse_json_response(response)
    
    def analyze_response(
        self,
        response_text: str,
        current_scores: Dict[str, int] = None,
        previous_analysis: str = ""
    ) -> Dict[str, Any]:
        """Analyze a lead's response and update scores"""
        
        if current_scores is None:
            current_scores = {
                "budget": 0, "authority": 0, "need": 0, "timeline": 0
            }
        
        prompt = SCORING_PROMPT.format(
            response=response_text,
            budget_score=current_scores.get("budget", 0),
            authority_score=current_scores.get("authority", 0),
            need_score=current_scores.get("need", 0),
            timeline_score=current_scores.get("timeline", 0),
            total_score=sum(current_scores.values()),
            previous_analysis=previous_analysis or "No previous analysis"
        )
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_nova(messages, use_pro=True)  # Use pro for analysis
        return self._parse_json_response(response)
    
    def generate_summary(
        self,
        lead_name: str,
        lead_email: str,
        lead_company: str,
        score: int,
        qualification_data: Dict,
        conversation_summary: str
    ) -> str:
        """Generate a summary for the sales team"""
        
        prompt = SUMMARY_PROMPT.format(
            lead_name=lead_name,
            lead_email=lead_email,
            lead_company=lead_company,
            score=score,
            qualification_data=json.dumps(qualification_data, indent=2),
            conversation_summary=conversation_summary
        )
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        return self._call_nova(messages)

