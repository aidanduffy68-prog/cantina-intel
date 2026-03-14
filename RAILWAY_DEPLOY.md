# Deploy to Railway - Get Permanent Public URL 🚂

## Why Railway?

- ✅ **No compatibility issues** (works on any macOS)
- ✅ **Permanent URL** (doesn't change like ngrok)
- ✅ **Free tier** available
- ✅ **Easy deployment** from GitHub
- ✅ **Professional solution**

## Quick Deployment (5 minutes)

### Step 1: Create GitHub Repo

```bash
cd /Users/AidanMDuffy/Desktop/cantina-intel

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Crypto Exploit Intelligence API"

# Create repo on GitHub.com, then:
git remote add origin https://github.com/YOUR_USERNAME/cantina-intel.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Railway

1. **Go to**: https://railway.app
2. **Sign up** (use GitHub account - easiest!)
3. **Click**: "New Project"
4. **Select**: "Deploy from GitHub repo"
5. **Choose**: Your `cantina-intel` repo
6. **Railway will auto-detect** FastAPI and start deploying

### Step 3: Add Environment Variable

1. In Railway project, click on your service
2. Go to **"Variables"** tab
3. Click **"New Variable"**
4. Add:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key
5. Railway will automatically redeploy

### Step 4: Get Your Public URL

1. In Railway project, click on your service
2. Go to **"Settings"** tab
3. Click **"Generate Domain"** (or use the default one)
4. **Copy the URL** (e.g., `https://cantina-intel-production.up.railway.app`)

### Step 5: Use in Zapier

In your Zapier Zap, use:
```
https://YOUR_RAILWAY_URL/generate-brief
```

Replace `YOUR_RAILWAY_URL` with your Railway domain.

## What Railway Does Automatically

- ✅ Detects FastAPI
- ✅ Installs dependencies from `requirements.txt`
- ✅ Runs `uvicorn app.main:app`
- ✅ Provides HTTPS URL
- ✅ Handles scaling

## Testing Your Deployment

Once deployed, test it:

```bash
curl -X POST https://YOUR_RAILWAY_URL/generate-brief \
  -H "Content-Type: application/json" \
  -d '{"text": "Euler Finance exploit involving flash loans and a donation attack that manipulated collateral accounting."}'
```

## Railway vs ngrok

| Feature | Railway | ngrok |
|---------|---------|-------|
| URL | Permanent | Changes on restart |
| Compatibility | Works everywhere | Issues on older macOS |
| Setup | 5 minutes | 2 minutes (when working) |
| Cost | Free tier | Free tier |
| Best for | Production/Demo | Quick testing |

## Troubleshooting

**Deployment fails:**
- Check that `requirements.txt` is correct
- Verify `OPENAI_API_KEY` is set
- Check Railway logs for errors

**API not responding:**
- Wait 1-2 minutes for deployment to complete
- Check Railway logs
- Verify the endpoint: `/generate-brief`

## You're Done! 🎉

Once deployed, you'll have a permanent URL like:
```
https://cantina-intel-production.up.railway.app
```

Use this in Zapier - it will never change!
