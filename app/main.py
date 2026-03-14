"""
FastAPI application for crypto exploit intelligence reporting.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .analyzer import ExploitAnalyzer, ExploitAnalysis
from .briefing import BriefGenerator, SecurityBrief

app = FastAPI(
    title="Crypto Exploit Intelligence API",
    description="API for analyzing crypto exploits and generating security intelligence briefs",
    version="1.0.0"
)

# Add CORS middleware for Zapier and other external services
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy initialization - will be created on first use
_analyzer = None
_brief_generator = None

def get_analyzer():
    global _analyzer
    if _analyzer is None:
        _analyzer = ExploitAnalyzer()
    return _analyzer

def get_brief_generator():
    global _brief_generator
    if _brief_generator is None:
        _brief_generator = BriefGenerator()
    return _brief_generator


class ExploitReportRequest(BaseModel):
    """Request model for exploit analysis."""
    exploit_text: str


class BriefRequest(BaseModel):
    """Request model for brief generation."""
    protocol_name: str
    exploit_type: str
    vulnerability_pattern: str
    root_cause: str
    affected_smart_contract_component: str
    risk_category: str


class SimpleBriefRequest(BaseModel):
    """Simplified request model - just text, does analysis + brief."""
    text: str


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Crypto Exploit Intelligence API",
        "endpoints": {
            "analyze": "/analyze-exploit",
            "brief": "/generate-brief",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Zapier and monitoring."""
    return {
        "status": "healthy",
        "service": "Crypto Exploit Intelligence API",
        "version": "1.0.0"
    }


@app.post("/analyze-exploit", response_model=ExploitAnalysis)
async def analyze_exploit(request: ExploitReportRequest):
    """
    Analyze exploit report text and extract structured intelligence.
    
    Args:
        request: ExploitReportRequest containing exploit_text
        
    Returns:
        ExploitAnalysis with extracted information
    """
    try:
        if not request.exploit_text or not request.exploit_text.strip():
            raise HTTPException(status_code=400, detail="exploit_text cannot be empty")
        
        analysis = get_analyzer().analyze(request.exploit_text)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/generate-brief", response_model=SecurityBrief)
async def generate_brief_simple(request: SimpleBriefRequest):
    """
    Generate a Security Intelligence Brief from exploit text.
    Does analysis first, then generates brief.
    
    Args:
        request: SimpleBriefRequest with text field
        
    Returns:
        SecurityBrief with generated intelligence brief
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(status_code=400, detail="text field cannot be empty")
        
        # First analyze the exploit
        analysis = get_analyzer().analyze(request.text)
        # Then generate brief from analysis
        brief = get_brief_generator().generate_brief(analysis)
        return brief
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/generate-brief-full", response_model=SecurityBrief)
async def generate_brief_full(request: BriefRequest):
    """
    Generate a Security Intelligence Brief from full exploit analysis data.
    
    Args:
        request: BriefRequest containing all exploit analysis fields
        
    Returns:
        SecurityBrief with generated intelligence brief
    """
    try:
        analysis = ExploitAnalysis(
            protocol_name=request.protocol_name,
            exploit_type=request.exploit_type,
            vulnerability_pattern=request.vulnerability_pattern,
            root_cause=request.root_cause,
            affected_smart_contract_component=request.affected_smart_contract_component,
            risk_category=request.risk_category
        )
        brief = get_brief_generator().generate_brief(analysis)
        return brief
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
