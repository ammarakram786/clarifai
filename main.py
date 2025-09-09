import os
import base64
from fastapi import FastAPI, UploadFile, File, requests, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get port from environment variable (Railway sets this)
PORT = int(os.getenv("PORT", 8000))

# Clarifai credentials - all must be provided via environment variables
PAT = os.getenv("CLARIFAI_PAT")
USER_ID = os.getenv("CLARIFAI_USER_ID")
APP_ID = os.getenv("CLARIFAI_APP_ID")
MODEL_ID = os.getenv("CLARIFAI_MODEL_ID")
MODEL_VERSION_ID = os.getenv("CLARIFAI_MODEL_VERSION_ID")

# Bearer token for authentication - must be provided via environment variable
BEARER_TOKEN = os.getenv("API_BEARER_TOKEN")

# Validate required environment variables
required_vars = {
    "CLARIFAI_PAT": PAT,
    "CLARIFAI_USER_ID": USER_ID,
    "CLARIFAI_APP_ID": APP_ID,
    "CLARIFAI_MODEL_ID": MODEL_ID,
    "CLARIFAI_MODEL_VERSION_ID": MODEL_VERSION_ID,
    "API_BEARER_TOKEN": BEARER_TOKEN
}

missing_vars = [var for var, value in required_vars.items() if not value]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Setup Clarifai gRPC
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)
user_data = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

# Security scheme
security = HTTPBearer()

app = FastAPI(
    title="Clarifai Image Analysis API",
    description="API for analyzing images using Clarifai AI models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify the Bearer token"""
    if credentials.credentials != BEARER_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Clarifai Image Analysis API",
        "version": "1.0.0",
        "auth_enabled": True,
        "token_source": "environment" if os.getenv("API_BEARER_TOKEN") else "default"
    }

@app.post("/analyze-image")
async def predict_from_image(
    file: UploadFile = File(...),
    token: str = Depends(verify_token)
):
    print("Received file: ")
    # Read image and encode
    image_bytes = await file.read()

    # Send image to Clarifai
    response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=user_data,
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(base64=image_bytes)
                    )
                )
            ]
        ),
        metadata=metadata
    )

    # Check for errors
    if response.status.code != status_code_pb2.SUCCESS:
        return JSONResponse(
            status_code=500,
            content={"error": response.status.description}
        )

    # Extract predictions
    predictions = []
    for concept in response.outputs[0].data.concepts:
        predictions.append({
            "name": concept.name,
            "confidence": round(concept.value, 4)
        })

    return {"predictions": predictions}



import base64

class ImageURL(BaseModel):
    url: str

@app.post("/analyze-image-url")
async def predict_from_url(
    image_url: ImageURL,
    token: str = Depends(verify_token)
):
    try:
        # Fetch the image from the URL
        response = requests.get(image_url.url)
        response.raise_for_status()
        image_bytes = response.content

        # Encode the image bytes to base64
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching or encoding image: {e}")

    # Send image to Clarifai
    response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=user_data,
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(base64=image_base64)
                    )
                )
            ]
        ),
        metadata=metadata
    )

    # Check for errors
    if response.status.code != status_code_pb2.SUCCESS:
        return JSONResponse(
            status_code=500,
            content={"error": response.status.description}
        )

    # Extract predictions
    predictions = []
    for concept in response.outputs[0].data.concepts:
        predictions.append({
            "name": concept.name,
            "confidence": round(concept.value, 4)
        })

    return {"predictions": predictions}