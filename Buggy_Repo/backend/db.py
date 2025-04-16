from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, Optional
import os
from contextlib import asynccontextmanager

# Database configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "development_db")
MAX_POOL_SIZE = int(os.getenv("MONGO_MAX_POOL_SIZE", "10"))
MIN_POOL_SIZE = int(os.getenv("MONGO_MIN_POOL_SIZE", "1"))

# Global client instance
client: Optional[AsyncIOMotorClient] = None

async def connect_to_db() -> AsyncIOMotorClient:
    try:
        client = AsyncIOMotorClient(
            MONGO_URI,
            maxPoolSize=MAX_POOL_SIZE,
            minPoolSize=MIN_POOL_SIZE,
            serverSelectionTimeoutMS=5000
        )
        # Verify the connection
        await client.admin.command('ping')
        print("Successfully connected to the database")
        return client
    except Exception as e:
        print(f"Failed to connect to the database: {str(e)}")
        raise

async def close_db_connection():
    if client:
        client.close()
        print("Database connection closed")

@asynccontextmanager
async def get_db():
    """Context manager for database operations"""
    try:
        db = init_db()
        yield db
    finally:
        # Connection will be returned to the pool
        pass

def init_db() -> Dict:
    """Initialize database collections with error handling"""
    if not client:
        raise RuntimeError("Database client not initialized")
    
    try:
        db = client[DB_NAME]
        return {
            "items_collection": db["items"],
            "users_collection": db["users"]
        }
    except Exception as e:
        print(f"Failed to initialize database collections: {str(e)}")
        raise

# Startup and shutdown events
async def startup_db_client():
    """Initialize database connection on startup"""
    global client
    client = await connect_to_db()

async def shutdown_db_client():
    """Close database connection on shutdown"""
    await close_db_connection()

# Question for chocolate: How can we implement nosql syntax in mysql ???