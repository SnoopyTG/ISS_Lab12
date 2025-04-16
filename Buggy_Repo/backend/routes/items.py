from fastapi import APIRouter, HTTPException, status
from models import Item
from bson import ObjectId
from typing import List

router = APIRouter()

async def get_items_collection():
    from db import init_db
    return init_db()["items_collection"]

@router.get("/", response_model=List[dict], status_code=status.HTTP_200_OK)
async def get_items():
    try:
        collection = await get_items_collection()
        items = []
        async for item in collection.find():
            item["_id"] = str(item["_id"])
            items.append(item)
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch items: {str(e)}"
        )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    try:
        collection = await get_items_collection()
        result = await collection.insert_one(item.dict())
        return {"id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create item: {str(e)}"
        )

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str):
    try:
        collection = await get_items_collection()
        result = await collection.delete_one({"_id": ObjectId(item_id)})
        if not result.deleted_count:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete item: {str(e)}"
        )