# Crypto Exploit Intelligence API

A FastAPI-based service for analyzing crypto exploits and generating structured security intelligence briefs using AI-powered analysis.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
   - Copy `.env` and set your `OPENAI_API_KEY`

3. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /analyze-exploit
Analyzes exploit report text and extracts structured intelligence.

**Request Body:**
```json
{
  "exploit_text": "Your exploit report text here..."
}
```

**Response:**
```json
{
  "protocol_name": "Protocol Name",
  "exploit_type": "Exploit Type",
  "vulnerability_pattern": "Vulnerability Pattern",
  "root_cause": "Root cause explanation",
  "affected_smart_contract_component": "Component name/function",
  "risk_category": "Critical|High|Medium|Low"
}
```

### POST /generate-brief
Generates a Security Intelligence Brief from exploit text. Automatically performs analysis first, then generates the brief.

**Request Body:**
```json
{
  "text": "Your exploit report text here..."
}
```

**Response:**
```json
{
  "title": "Brief Title",
  "executive_summary": "Executive summary...",
  "threat_level": "High",
  "recommendations": ["Recommendation 1", "Recommendation 2"],
  "brief": "Detailed brief..."
}
```

## Testing

### Quick Test

1. Open `http://localhost:8000/docs` in your browser
2. Navigate to `POST /generate-brief`
3. Click "Try it out"
4. Use the example payload:
   ```json
   {
     "text": "Euler Finance exploit involving flash loans and a donation attack that manipulated collateral accounting."
   }
   ```
5. Click "Execute"

The API will return a structured security intelligence brief with analysis and recommendations.

## Deployment

Deploy to Railway:
1. Push to GitHub
2. Connect Railway to your GitHub repo
3. Add `OPENAI_API_KEY` environment variable
4. Railway auto-detects FastAPI and deploys

## Automation

The API can be integrated with automation tools like Zapier:
- Use webhook triggers to send exploit text
- POST to `/generate-brief` endpoint
- Receive structured security intelligence briefs

See `ZAPIER_WORKFLOW_FINAL.json` for example workflow configuration.

## Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
