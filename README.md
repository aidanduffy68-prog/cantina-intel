# Crypto Exploit Intelligence API

A FastAPI-based service for analyzing crypto exploits and generating security intelligence briefs.

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

### Example: Euler Finance Exploit

Test the API with a famous exploit. Copy the text from `test_exploit_euler.txt` or use the JSON payload from `test_payload.json`.

**Quick Test:**
1. Open `http://localhost:8000/docs` in your browser
2. Navigate to `POST /analyze-exploit`
3. Click "Try it out"
4. Paste the Euler Finance exploit text (from `test_exploit_euler.txt`) into the `exploit_text` field
5. Click "Execute"

**Expected Response:**
The API will analyze the exploit and return structured intelligence including:
- Protocol name: "Euler Finance"
- Exploit type: "Flash loan attack" or "Donation attack"
- Vulnerability pattern: Details about the accounting manipulation
- Root cause: Missing checks in donation mechanism
- Affected component: "donateToReserves function" or similar
- Risk category: "Critical"

## Deployment

See `RAILWAY_DEPLOY.md` for deployment instructions to Railway.

## Automation

See `ZAPIER_SETUP.md` for Zapier automation setup.

## Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
