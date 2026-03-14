# Zapier Automation Setup Guide

## Overview

Zapier can automate your exploit analysis workflow by connecting triggers (like new emails, form submissions, webhooks) to your FastAPI endpoint.

## Prerequisites

1. **Zapier Account**: Sign up at https://zapier.com (free tier available)
2. **FastAPI Running**: Your server should be accessible (see options below)
3. **Public URL** (if using Zapier cloud): Your FastAPI needs to be publicly accessible

## Making FastAPI Publicly Accessible

### Deploy to Railway (Recommended)

See `RAILWAY_DEPLOY.md` for detailed deployment instructions.

Railway provides:
- Permanent public URL
- Free tier available
- Easy GitHub integration
- Automatic deployments

### Option 3: Use Zapier Webhooks (Advanced)

Set up a webhook that Zapier can call, which then forwards to your local API.

## Creating Your Zap

### Step 1: Choose a Trigger

**Popular Options:**
- **Webhook by Zapier** (Catch Hook) - Receive data via webhook
- **Gmail** - New email with specific subject
- **Google Forms** - New form submission
- **Slack** - New message in channel
- **Schedule** - Run on a schedule
- **Manual Trigger** - Test manually

### Step 2: Set Up the Action

1. Search for **"Webhooks by Zapier"**
2. Choose **"POST"** action
3. Configure:
   - **URL**: `http://localhost:8001/analyze-exploit` (if local) or your public URL
   - **Method**: `POST`
   - **Data Pass-Through**: `No`
   - **Headers**: 
     ```
     Content-Type: application/json
     ```
   - **Payload Type**: `json`
   - **Body**: 
     ```json
     {
       "exploit_text": "{{trigger_field}}"
     }
     ```
     Replace `{{trigger_field}}` with the field from your trigger that contains the exploit text

### Step 3: Test Your Zap

1. Click **"Test"** button
2. Check the response - you should see:
   ```json
   {
     "protocol_name": "...",
     "exploit_type": "...",
     "vulnerability_pattern": "...",
     "root_cause": "...",
     "affected_smart_contract_component": "...",
     "risk_category": "..."
   }
   ```

### Step 4: Add Additional Actions (Optional)

After getting the analysis, you can:
- **Send to Slack** - Post results to a channel
- **Save to Google Sheets** - Log all analyses
- **Send Email** - Alert on critical exploits
- **Create Notion Page** - Document the exploit
- **Send to Discord** - Team notifications

## Example Zap Configurations

### Configuration 1: Webhook Trigger → FastAPI → Slack

**Trigger**: Webhook by Zapier (Catch Hook)
- URL: Copy the webhook URL Zapier provides
- Send exploit text to this URL

**Action 1**: Webhooks by Zapier (POST)
- URL: `https://your-api.ngrok.io/analyze-exploit`
- Body: `{"exploit_text": "{{1}}"}`
- Headers: `Content-Type: application/json`

**Action 2**: Slack (Send Channel Message)
- Channel: `#security-alerts`
- Message: 
  ```
  🚨 Exploit Analysis
  
  Protocol: {{action1_protocol_name}}
  Type: {{action1_exploit_type}}
  Risk: {{action1_risk_category}}
  
  Root Cause: {{action1_root_cause}}
  ```

### Configuration 2: Gmail → FastAPI → Google Sheets

**Trigger**: Gmail (New Email)
- Search: `subject:"exploit report"`

**Action 1**: Webhooks by Zapier (POST)
- Extract email body and send to FastAPI

**Action 2**: Google Sheets (Create Spreadsheet Row)
- Log all analysis results

### Configuration 3: Manual Trigger → FastAPI → Multiple Actions

**Trigger**: Manual (for testing)

**Action 1**: Webhooks by Zapier (POST)
- Send test exploit text

**Action 2**: Filter by Zapier
- Only continue if `risk_category` contains "Critical"

**Action 3**: Slack (if Critical)
- Send alert

**Action 4**: Email (if Critical)
- Send detailed report

## Testing Your Setup

### Test with curl (if using ngrok):

```bash
curl -X POST https://your-zapier-webhook-url.com/catch/12345/abcde \
  -H "Content-Type: application/json" \
  -d '{"exploit_text": "Euler Finance Exploit - March 2023..."}'
```

### Test in Zapier:

1. Go to your Zap
2. Click "Test" on the trigger
3. Enter test data
4. Watch it flow through each step
5. Check the results

## Troubleshooting

**Zapier can't reach your API:**
- Make sure FastAPI is running
- If local, use ngrok to create a public URL
- Check firewall settings

**Getting 422 errors:**
- Verify JSON format matches FastAPI expectations
- Check that `exploit_text` field is being sent correctly

**Timeout errors:**
- OpenAI API calls can take 10-30 seconds
- Increase Zapier timeout settings if possible
- Consider adding a delay step

## Quick Start Checklist

- [ ] Sign up for Zapier account
- [ ] Start FastAPI: `uvicorn app.main:app --reload --port 8001`
- [ ] Set up ngrok: `ngrok http 8001` (get public URL)
- [ ] Create new Zap in Zapier
- [ ] Choose trigger (Webhook, Gmail, etc.)
- [ ] Add Webhook POST action pointing to your API
- [ ] Test the Zap
- [ ] Add additional actions (Slack, Email, etc.)
- [ ] Turn on the Zap!

## Cost

- **Zapier Free Tier**: 100 tasks/month, 5 Zaps
- **Zapier Starter**: $19.99/month - 750 tasks, unlimited Zaps
- **ngrok Free**: Unlimited tunnels, but URLs change on restart

For this project, the free tier should be sufficient for testing!
