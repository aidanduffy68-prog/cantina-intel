"""
Exploit analyzer module for extracting intelligence from exploit reports.
"""
from pydantic import BaseModel
from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
project_root = Path(__file__).parent.parent
load_dotenv(dotenv_path=project_root / ".env")


class ExploitAnalysis(BaseModel):
    """Structured analysis of an exploit."""
    protocol_name: str
    exploit_type: str
    vulnerability_pattern: str
    root_cause: str
    affected_smart_contract_component: str
    risk_category: str


class ExploitAnalyzer:
    """Analyzes exploit reports using OpenAI."""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        # Initialize OpenAI client with explicit parameters
        self.client = OpenAI(
            api_key=api_key,
            timeout=60.0
        )
    
    def analyze(self, exploit_text: str) -> ExploitAnalysis:
        """
        Analyze exploit text and extract structured intelligence.
        
        Args:
            exploit_text: Raw exploit report text
            
        Returns:
            ExploitAnalysis object with extracted information
        """
        prompt = f"""As a blockchain security researcher, perform a deep technical analysis of the following exploit report. 
Extract and categorize the exploit with precision and technical accuracy.

EXPLOIT REPORT:
{exploit_text}

ANALYSIS REQUIREMENTS:

1. protocol_name: The name of the blockchain protocol, DeFi protocol, or smart contract system being exploited (e.g., "Uniswap V3", "Compound", "Ethereum L2 Bridge")

2. exploit_type: Classify the exploit type using standard blockchain security taxonomy. Common types include:
   - Reentrancy (single-function, cross-function, cross-contract)
   - Flash loan attack
   - Oracle manipulation
   - Access control violation
   - Integer overflow/underflow
   - Logic error
   - Front-running/MEV
   - Price manipulation
   - Token standard vulnerability (ERC-20/721/1155)
   - Governance attack
   - Bridge exploit
   - If none match exactly, provide a specific technical classification

3. vulnerability_pattern: Identify the specific vulnerability pattern or weakness. Be precise about the pattern:
   - State inconsistency
   - Missing checks (e.g., zero-address, balance, reentrancy guard)
   - Incorrect state updates
   - Unchecked external calls
   - Improper access control
   - Arithmetic errors
   - Design flaw in protocol logic
   - Provide specific technical details about the pattern

4. root_cause: Identify the fundamental root cause of the vulnerability. Explain WHY the exploit was possible:
   - Was it a missing security check?
   - Incorrect assumption about state?
   - Flawed business logic?
   - Inadequate validation?
   - Provide a clear, technical explanation of the underlying issue

5. affected_smart_contract_component: Specify which component(s) of the smart contract system were affected:
   - Function name(s) if identifiable
   - Contract name(s) or module
   - Protocol layer (e.g., "Liquidity Pool", "Oracle", "Governance", "Bridge Contract")
   - If specific components aren't clear, describe the affected functionality

6. risk_category: Classify the risk category based on impact and exploitability:
   - Critical: Complete fund drainage, protocol shutdown, or systemic risk
   - High: Significant fund loss, major functionality compromise
   - Medium: Moderate impact, limited scope
   - Low: Minor impact, edge case
   - Consider both the actual impact and potential worst-case scenario

Return ONLY valid JSON with these exact keys: protocol_name, exploit_type, vulnerability_pattern, root_cause, affected_smart_contract_component, risk_category"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert blockchain security researcher with deep expertise in smart contract vulnerabilities, DeFi protocols, and crypto exploit analysis. You have extensive knowledge of common vulnerability patterns (reentrancy, flash loans, oracle manipulation, etc.), smart contract security best practices, and the technical mechanics of blockchain exploits. Your analysis is precise, technically accurate, and follows established security research methodologies. You think like a security auditor and categorize exploits using standard industry taxonomies."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return ExploitAnalysis(
                protocol_name=result.get("protocol_name", "Unknown"),
                exploit_type=result.get("exploit_type", "Unknown"),
                vulnerability_pattern=result.get("vulnerability_pattern", "Unknown"),
                root_cause=result.get("root_cause", "Unknown"),
                affected_smart_contract_component=result.get("affected_smart_contract_component", "Unknown"),
                risk_category=result.get("risk_category", "Unknown")
            )
        except Exception as e:
            raise ValueError(f"Failed to analyze exploit: {str(e)}")
