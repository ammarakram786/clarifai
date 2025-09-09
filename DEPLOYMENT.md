# Clarifai Image Analysis API - Deployment Guide

## Security Updates Completed ✅

1. **Removed all hardcoded secrets** from `main.py` and `docker-compose.yml`
2. **Environment variables only** - all credentials must be provided via environment variables
3. **Added validation** - app will fail to start if required environment variables are missing
4. **Generated new secure API token** for authentication

## Required Environment Variables

Set these environment variables in your deployment platform:

```
CLARIFAI_PAT=your_new_clarifai_pat_here
CLARIFAI_USER_ID=your_clarifai_user_id
CLARIFAI_APP_ID=your_clarifai_app_id
CLARIFAI_MODEL_ID=your_clarifai_model_id
CLARIFAI_MODEL_VERSION_ID=your_clarifai_model_version_id
API_BEARER_TOKEN=xeZWXMpeCKcsV54hdkguzjgZszICEkJF9nIkJTSB
```

## API Endpoints

- **Health Check**: `GET /health`
- **API Documentation**: `GET /docs`
- **Analyze Image Upload**: `POST /analyze-image` (requires Bearer token)
- **Analyze Image URL**: `POST /analyze-image-url` (requires Bearer token)

## Authentication

- **Format**: `Authorization: Bearer <token>`
- **Test Token**: `xeZWXMpeCKcsV54hdkguzjgZszICEkJF9nIkJTSB`

## CORS Configuration

- **Origins**: `*` (configure as needed for production)
- **Methods**: All methods allowed
- **Headers**: All headers allowed
- **Credentials**: Enabled

## Deployment Platforms

### Render
1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Deploy using the Procfile

### Railway
1. Connect your GitHub repository
2. Set environment variables in Railway dashboard
3. Deploy automatically

### Fly.io
1. Install flyctl
2. Run `fly launch`
3. Set secrets with `fly secrets set`
4. Deploy with `fly deploy`

## Files Included

- `main.py` - Main application (secrets removed)
- `main_clean.py` - Clean version for private sharing
- `requirements.txt` - Python dependencies
- `Procfile` - For platform deployment
- `Dockerfile` - For containerized deployment
- `docker-compose.yml` - For local development (secrets removed)
- `env_template.txt` - Environment variables template
