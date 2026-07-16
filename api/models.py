# models.py
# This file defines the actual tables in our MySQL database
# Each class here = one table in MySQL
# Each variable inside the class = one column in that table

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from api.database import Base   # Base we created in database.py


# -------------------------------------------------------
# TABLE 1: farmers
# This table stores all registered farmers
# -------------------------------------------------------
class Farmer(Base):

    __tablename__ = "farmers"   # this will be the table name in MySQL

    # Each column in the farmers table:
    id       = Column(Integer, primary_key=True, index=True)  # auto-increment unique ID
    name     = Column(String(100), nullable=False)            # farmer full name
    email    = Column(String(100), unique=True, nullable=False) # email must be unique
    password = Column(String(255), nullable=False)            # hashed password (never plain text)
    created_at = Column(DateTime, default=datetime.utcnow)   # when they registered

    # This connects Farmer to ScanHistory
    # One farmer can have MANY scan histories
    scans = relationship("ScanHistory", back_populates="farmer")


# -------------------------------------------------------
# TABLE 2: scan_history
# This table stores every scan done by every farmer
# -------------------------------------------------------
class ScanHistory(Base):

    __tablename__ = "scan_history"  # table name in MySQL

    # Each column in the scan_history table:
    id             = Column(Integer, primary_key=True, index=True)  # unique scan ID
    farmer_id      = Column(Integer, ForeignKey("farmers.id"))       # which farmer did this scan
    image_path     = Column(String(255), nullable=False)            # path where image is saved
    result         = Column(String(100), nullable=False)            # Early Blight / Late Blight / Healthy
    confidence     = Column(Float, nullable=False)                  # confidence percentage
    scanned_at     = Column(DateTime, default=datetime.utcnow)     # when the scan was done

    # This connects ScanHistory back to Farmer
    farmer = relationship("Farmer", back_populates="scans")
