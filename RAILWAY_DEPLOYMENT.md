# Railway Deployment Guide

## Quick Deploy to Railway

### Option 1: Deploy via Railway Dashboard (Recommended)

1. **Go to Railway**: https://railway.app
2. **Sign in** with your GitHub account
3. **Click "New Project"** → **"Deploy from GitHub repo"**
4. **Select your repository** (or fork this one)
5. **Railway will automatically detect** it's a Python app

### Option 2: Deploy via Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

## Environment Variables Setup

In your Railway dashboard, go to **Variables** tab and add:

```
CLARIFAI_PAT=your_new_clarifai_pat_here
CLARIFAI_USER_ID=your_clarifai_user_id
CLARIFAI_APP_ID=your_clarifai_app_id
CLARIFAI_MODEL_ID=your_clarifai_model_id
CLARIFAI_MODEL_VERSION_ID=your_clarifai_model_version_id
API_BEARER_TOKEN=xeZWXMpeCKcsV54hdkguzjgZszICEkJF9nIkJTSB
```

## Important Security Notes

⚠️ **CRITICAL**: You MUST rotate your Clarifai PAT token:

1. Go to https://portal.clarifai.com/
2. Navigate to **Settings** → **API Keys**
3. **Generate a new PAT** and replace the old one
4. Update the `CLARIFAI_PAT` environment variable in Railway

## After Deployment

Once deployed, Railway will provide you with:
- **Base URL**: `https://your-app-name.railway.app`
- **Health Check**: `https://your-app-name.railway.app/health`
- **API Docs**: `https://your-app-name.railway.app/docs`

## Testing the API

### Health Check
```bash
curl https://your-app-name.railway.app/health
```

### Test Image Analysis (with auth)
```bash
curl -X POST "https://your-app-name.railway.app/analyze-image" \
  -H "Authorization: Bearer xeZWXMpeCKcsV54hdkguzjgZszICEkJF9nIkJTSB" \
  -F "file=@your-image.jpg"
```

## Files Ready for Deployment

✅ `main.py` - Main application (secrets removed)
✅ `requirements.txt` - Python dependencies  
✅ `railway.json` - Railway configuration
✅ `Procfile` - Alternative deployment method
✅ `Dockerfile` - Container deployment option

## CORS Configuration

- **Origins**: `*` (allows all origins)
- **Methods**: All HTTP methods
- **Headers**: All headers
- **Credentials**: Enabled

## Authentication Format

```
Authorization: Bearer xeZWXMpeCKcsV54hdkguzjgZszICEkJF9nIkJTSB
```

## Next Steps

1. Deploy to Railway using the dashboard
2. Set all environment variables
3. Rotate your Clarifai PAT token
4. Test the endpoints
5. Share the live URLs for testing
