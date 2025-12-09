from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"



engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=False
)

def get_db_connection():
    """Get database connection"""
    return engine.connect()

def close_db():
    """Close all connections"""
    engine.dispose()
