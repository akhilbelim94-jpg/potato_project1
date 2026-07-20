from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from io import BytesIO
from PIL import Image
import numpy as np
import tensorflow as tf
from pathlib import Path
from sqlalchemy.orm import Session
from pathlib import Path


# import our files

from api.database import engine, get_db
from api.models import Farmer, ScanHistory
from api import models
from api import auth
from api import scan_history
from api.auth import get_current_farmer


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Grootify API",
    description="Potato Leaf Disease Detection API with farmer authentication",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/scan_images", StaticFiles(directory="scan_images"), name="scan_images")

app.include_router(auth.router)
app.include_router(scan_history.router)

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "traning"
    / "saved_models"
    / "potato_model"
    / "1"
    / "model_1.keras"
)

MODEL = tf.keras.models.load_model(MODEL_PATH)


CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


# -------------------------------------------------------
# GET /ping
# -------------------------------------------------------
@app.get("/ping")
async def ping():
    return {"message": "Grootify API is running!"}


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, axis=0)
    predictions = MODEL.predict(img_batch)
    confidence = float(np.max(predictions[0]))
    predicted_index = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[predicted_index]
    CONFIDENCE_THRESHOLD = 0.80

    # Print all probabilities for debugging
    print("Predictions:", predictions[0])
    print("Predicted Class:", predicted_class)
    print("Confidence:", confidence)

    # Reject low-confidence images
    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "class": "Unknown",
            "confidence": confidence,
            "message": "Unable to confidently identify the potato leaf disease.",
            "farmer_name": current_farmer.name
        }

    return {
        "class": predicted_class,
        "confidence": confidence,
        "farmer_name": current_farmer.name
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)