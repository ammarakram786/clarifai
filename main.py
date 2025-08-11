import os
import base64
from fastapi import FastAPI, UploadFile, File, requests, HTTPException
from fastapi.responses import JSONResponse

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from pydantic import BaseModel

# Clarifai credentials
PAT = "7607dc924f7d48cb9498d01f28fcb71d"
USER_ID = "nxi9k6mtpija"
APP_ID = "ScreenSnapp-Vision"
MODEL_ID = "set-2"
MODEL_VERSION_ID = "f2fb3217afa341ce87545e1ba7bf0b64"

# Setup Clarifai gRPC
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)
user_data = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

app = FastAPI()

@app.post("/analyze-image")
async def predict_from_image(file: UploadFile = File(...)):
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



class ImageURL(BaseModel):
    url: str

@app.post("/analyze-image-url")
async def predict_from_url(image_url: ImageURL):
    try:
        # Fetch the image from the URL
        response = requests.get(image_url.url)
        response.raise_for_status()
        image_bytes = response.content
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching image: {e}")

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