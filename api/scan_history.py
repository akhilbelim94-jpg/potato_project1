# scan_history.py
# This file handles everything related to scan history
# 1. Save a new scan result to database (after every leaf scan)
# 2. Get all previous scans for a logged in farmer
# 3. Delete a scan from history

import os
import io
from PIL import Image
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Form
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from api.database import get_db
from api.models import ScanHistory, Farmer
from api.schemas import ScanHistoryResponse
from api.auth import get_current_farmer

# -------------------------------------------------------
# FOLDER WHERE LEAF IMAGES WILL BE SAVED
# -------------------------------------------------------
IMAGES_FOLDER = "scan_images"
os.makedirs(IMAGES_FOLDER, exist_ok=True)


# -------------------------------------------------------
# API ROUTER
# -------------------------------------------------------
router = APIRouter(
    prefix="/scans",
    tags=["scans"]
)


# -------------------------------------------------------
# ROUTE 1: SAVE SCAN RESULT
# POST /scans/save
# -------------------------------------------------------
@router.post("/save")
async def save_scan(
    result         : str   = Form(...),
    confidence     : float = Form(...),
    file           : UploadFile = File(...),
    db             : Session = Depends(get_db),
    current_farmer : Farmer  = Depends(get_current_farmer)
):
    # generate unique filename using timestamp
    timestamp  = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename   = f"farmer_{current_farmer.id}_{timestamp}.jpg"
    image_path = os.path.join(IMAGES_FOLDER, filename)

    # read image and convert to JPG using PIL
    # this fixes webp and other format issues
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    img = img.convert("RGB")
    img.save(image_path, "JPEG")

    # save scan result to database
    new_scan = ScanHistory(
        farmer_id  = current_farmer.id,
        image_path = image_path,
        result     = result,
        confidence = confidence
    )

    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)

    return {
        "message"   : "Scan saved successfully!",
        "scan_id"   : new_scan.id,
        "image_path": image_path,
        "result"    : result,
        "confidence": confidence
    }


# -------------------------------------------------------
# ROUTE 2: GET ALL SCANS FOR LOGGED IN FARMER
# GET /scans/history
# -------------------------------------------------------
@router.get("/history", response_model=List[ScanHistoryResponse])
def get_scan_history(
    db             : Session = Depends(get_db),
    current_farmer : Farmer  = Depends(get_current_farmer)
):
    scans = db.query(ScanHistory)\
              .filter(ScanHistory.farmer_id == current_farmer.id)\
              .order_by(ScanHistory.scanned_at.desc())\
              .all()

    if not scans:
        return []

    return scans


# -------------------------------------------------------
# ROUTE 3: DELETE A SCAN
# DELETE /scans/{scan_id}
# -------------------------------------------------------
@router.delete("/{scan_id}")
def delete_scan(
    scan_id        : int,
    db             : Session = Depends(get_db),
    current_farmer : Farmer  = Depends(get_current_farmer)
):
    scan = db.query(ScanHistory)\
             .filter(ScanHistory.id == scan_id)\
             .filter(ScanHistory.farmer_id == current_farmer.id)\
             .first()

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found."
        )

    # delete image file from folder
    if os.path.exists(scan.image_path):
        os.remove(scan.image_path)

    # delete from database
    db.delete(scan)
    db.commit()

    return {"message": "Scan deleted successfully!"}