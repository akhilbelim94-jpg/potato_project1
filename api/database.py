# database.py
# This file creates the connection between our FastAPI backend and MySQL database
# SQLAlchemy is the library we use to talk to MySQL from Python

from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------------
# DATABASE URL FORMAT:
# mysql+pymysql://username:password@host:port/database_name
# Change YOUR_PASSWORD to your actual MySQL root password
# -------------------------------------------------------
DATABASE_URL = "mysql+pymysql://root:AKKiSipahi2003@localhost:3306/grootify"

# create_engine = creates the actual connection to MySQL
# pool_pre_ping=True means it checks connection is alive before using it
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal = each farmer request gets its own database session
# autocommit=False = we manually save changes (safer)
# autoflush=False  = changes are not sent to DB until we say so
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = all our database table classes will inherit from this
# Think of it as the parent of all tables
Base = declarative_base()


# -------------------------------------------------------
# This function gives us a database session for each request
# and automatically closes it when the request is done
# We will use this in every API route that needs the database
# -------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db          # give the session to the route
    finally:
        db.close()        # always close after request is done
