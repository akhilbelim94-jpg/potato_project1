from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from io import BytesIO
from PIL import Image
import numpy as np
import tensorflow as tf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pathlib import Path
MODEL_PATH = Path(r"C:\Users\akhil\My_projects\potato_project\code\potato_project1\traning\saved_models\potato_model\1\model_1.keras")
MODEL = tf.keras.models.load_model(MODEL_PATH)

CLASS_NAMES = ["Early blight", "Late Blight", "Healthy"]

@app.get("/ping")
async def ping():
    return "Hello I am ON"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, axis=0)
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions)]
    confidence =  np.max(predictions[0])
    print(predicted_class, confidence)
    return {
        "class": predicted_class, 
        "confidence": float(confidence)
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)