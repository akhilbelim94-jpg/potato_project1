# main.py
# This is the main entry point of our FastAPI backend
# It connects everything together:
# 1. Database connection
# 2. Creates MySQL tables automatically
# 3. Includes auth routes (register, login)
# 4. Includes scan history routes
# 5. The predict route (AI model prediction)

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


# import our files

from api.database import engine, get_db
from api.models import Farmer, ScanHistory
from api import models
from api import auth
from api import scan_history
from api.auth import get_current_farmer

# -------------------------------------------------------
# CREATE ALL TABLES IN MYSQL AUTOMATICALLY
# When you run main.py for the first time,
# it will create "farmers" and "scan_history" tables
# in your grootify database automatically!
# No need to manually create tables in MySQL!
# -------------------------------------------------------
models.Base.metadata.create_all(bind=engine)


# -------------------------------------------------------
# CREATE FASTAPI APP
# -------------------------------------------------------
app = FastAPI(
    title="Grootify API",
    description="Potato Leaf Disease Detection API with farmer authentication",
    version="2.0.0"
)


# -------------------------------------------------------
# CORS MIDDLEWARE
# Allows our frontend (HTML files) to talk to this backend
# Without this, browser will block all requests
# -------------------------------------------------------
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

# -------------------------------------------------------
# SERVE SCAN IMAGES AS STATIC FILES
# This allows frontend to display saved leaf images
# Example: http://localhost:8000/scan_images/farmer_1_xxx.jpg
# -------------------------------------------------------
app.mount("/scan_images", StaticFiles(directory="scan_images"), name="scan_images")


# -------------------------------------------------------
# INCLUDE ROUTERS
# This connects auth.py and scan_history.py routes to our app
# auth routes:         /auth/register, /auth/login, /auth/me
# scan history routes: /scans/save, /scans/history, /scans/{id}
# -------------------------------------------------------
app.include_router(auth.router)
app.include_router(scan_history.router)


# -------------------------------------------------------
# LOAD AI MODEL
# -------------------------------------------------------
MODEL_PATH = Path(r"C:\Users\akhil\My_projects\potato_project2\traning\saved_models\potato_model\1\model_1.keras")
MODEL = tf.keras.models.load_model(MODEL_PATH)

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]


# -------------------------------------------------------
# HELPER FUNCTION
# Converts uploaded image bytes to numpy array for model
# -------------------------------------------------------
def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


# -------------------------------------------------------
# ROUTE: PING (test if server is running)
# GET /ping
# -------------------------------------------------------
@app.get("/ping")
async def ping():
    return {"message": "Grootify API is running!"}


# -------------------------------------------------------
# ROUTE: PREDICT (AI prediction - requires login)
# POST /predict
# Farmer must be logged in to use scan feature
# Receives: leaf image
# Returns: disease class + confidence
# -------------------------------------------------------
@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    # Read uploaded image
    image = read_file_as_image(await file.read())

    # Add batch dimension
    img_batch = np.expand_dims(image, axis=0)

    # Make prediction
    predictions = MODEL.predict(img_batch)

    # Get highest confidence
    confidence = float(np.max(predictions[0]))

    # Get predicted class index
    predicted_index = np.argmax(predictions[0])

    # Get class name
    predicted_class = CLASS_NAMES[predicted_index]

    # Temporary threshold
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