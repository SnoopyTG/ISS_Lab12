from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, Optional, Any, Union
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
    """Connect to MongoDB and initialize the database"""
    try:
        global client
        print(f"Connecting to MongoDB at {MONGO_URI}...")
        
        client = AsyncIOMotorClient(
            MONGO_URI,
            maxPoolSize=MAX_POOL_SIZE,
            minPoolSize=MIN_POOL_SIZE,
            serverSelectionTimeoutMS=5000
        )
        
        # Verify the connection
        await client.admin.command('ping')
        print("Successfully connected to MongoDB")
        
        # Initialize database and collections
        db = client[DB_NAME]
        
        # Ensure indexes and collections exist
        await db.items.create_index("name")
        await db.users.create_index("username")
        await db.quiz.create_index("_id")
        
        print(f"Successfully initialized database '{DB_NAME}'")
        return client
    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
        if client:
            await client.close()
            client = None
        raise

async def close_db_connection():
    """Close the MongoDB connection"""
    global client
    if client:
        try:
            await client.close()
            print("MongoDB connection closed")
        except Exception as e:
            print(f"Error closing MongoDB connection: {str(e)}")
        finally:
            client = None

@asynccontextmanager
async def get_db():
    """Context manager for database operations"""
    global client
    if not client:
        try:
            await startup_db_client()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize database client: {str(e)}")
    
    try:
        db = init_db()
        yield db
    except Exception as e:
        print(f"Error in database operation: {str(e)}")
        raise
    finally:
        # Connection will be returned to the pool
        pass

def init_db() -> Dict[str, Any]:
    """Initialize database collections"""
    global client
    if not client:
        raise RuntimeError("Database client not initialized")
    
    try:
        db = client[DB_NAME]
        collections = {
            "items_collection": db.items,
            "users_collection": db.users,
            "quiz_collection": db.quiz
        }
        return collections
    except Exception as e:
        print(f"Failed to initialize database collections: {str(e)}")
        raise

async def startup_db_client():
    """Initialize database connection on startup"""
    global client
    if not client:
        client = await connect_to_db()
    else:
        try:
            await client.admin.command('ping')
        except Exception:
            client = await connect_to_db()

async def shutdown_db_client():
    """Close database connection on shutdown"""
    await close_db_connection()

# Question for chocolate: How can we implement nosql syntax in mysql ???