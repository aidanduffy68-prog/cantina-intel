"""
Security intelligence brief generator.
"""
from pydantic import BaseModel
from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv
from .analyzer import ExploitAnalysis

# Load .env from project root
project_root = Path(__file__).parent.parent
load_dotenv(dotenv_path=project_root / ".env")


class SecurityBrief(BaseModel):
    """Security Intelligence Brief model."""
    title: str
    executive_summary: str
    threat_level: str
    recommendations: list[str]
    brief: str


class BriefGenerator:
    """Generates security intelligence briefs from exploit analysis."""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        # Initialize OpenAI client with explicit parameters
        self.client = OpenAI(
            api_key=api_key,
            timeout=60.0
        )
    
    def generate_brief(self, analysis: ExploitAnalysis) -> SecurityBrief:
        """
        Generate a security intelligence brief from exploit analysis.
        
        Args:
            analysis: ExploitAnalysis object with extracted intelligence
            
        Returns:
            SecurityBrief object with generated brief
        """
        prompt = f"""Generate a Security Intelligence Brief based on the following exploit analysis:

Protocol: {analysis.protocol_name}
Exploit Type: {analysis.exploit_type}
Vulnerability Pattern: {analysis.vulnerability_pattern}
Root Cause: {analysis.root_cause}
Affected Component: {analysis.affected_smart_contract_component}
Risk Category: {analysis.risk_category}

Create a comprehensive security intelligence brief in JSON format with:
1. title: A concise title for the brief
2. executive_summary: A 2-3 sentence executive summary
3. threat_level: One of: Low, Medium, High, Critical (should align with the risk_category provided)
4. recommendations: A list of 3-5 security recommendations (as an array of strings)
5. brief: A detailed 3-4 paragraph intelligence brief covering the threat, impact, root cause analysis, and mitigation strategies

Return only valid JSON with these exact keys."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a security intelligence analyst creating briefs for security teams. Generate professional, actionable intelligence briefs."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return SecurityBrief(
                title=result.get("title", "Security Intelligence Brief"),
                executive_summary=result.get("executive_summary", ""),
                threat_level=result.get("threat_level", "Unknown"),
                recommendations=result.get("recommendations", []),
                brief=result.get("brief", "")
            )
        except Exception as e:
            raise ValueError(f"Failed to generate brief: {str(e)}")
