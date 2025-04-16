from fastapi import APIRouter, HTTPException, status
from models import Item
from bson import ObjectId, errors as bson_errors
from typing import List, Dict
from db import get_db
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[Dict], status_code=status.HTTP_200_OK)
async def get_items():
    try:
        async with get_db() as db:
            collection = db["items_collection"]
            items = []
            async for item in collection.find():
                item["_id"] = str(item["_id"])
                items.append(item)
            logger.info(f"Successfully retrieved {len(items)} items")
            return items
    except RuntimeError as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not available"
        )
    except Exception as e:
        logger.error(f"Error fetching items: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch items: {str(e)}"
        )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    try:
        async with get_db() as db:
            collection = db["items_collection"]
            item_dict = item.dict()
            result = await collection.insert_one(item_dict)
            logger.info(f"Successfully created item with ID: {result.inserted_id}")
            return {"id": str(result.inserted_id)}
    except RuntimeError as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not available"
        )
    except Exception as e:
        logger.error(f"Error creating item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create item: {str(e)}"
        )

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str):
    try:
        async with get_db() as db:
            collection = db["items_collection"]
            try:
                object_id = ObjectId(item_id)
            except bson_errors.InvalidId:
                logger.error(f"Invalid item ID format: {item_id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid item ID format"
                )
            
            result = await collection.delete_one({"_id": object_id})
            if not result.deleted_count:
                logger.warning(f"Item not found with ID: {item_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Item not found"
                )
            logger.info(f"Successfully deleted item with ID: {item_id}")
    except RuntimeError as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not available"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete item: {str(e)}"
        )