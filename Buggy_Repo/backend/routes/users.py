from fastapi import APIRouter, HTTPException, status
from models import User
from bson import ObjectId
from typing import List

router = APIRouter()

async def get_users_collection():
    from db import init_db
    return init_db()["users_collection"]

@router.get("/", response_model=List[dict], status_code=status.HTTP_200_OK)
async def get_users():
    try:
        collection = await get_users_collection()
        users = []
        async for user in collection.find():
            user["_id"] = str(user["_id"])
            users.append(user)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch users: {str(e)}"
        )

# whats ur favorite genre of music ??? mine is EDM
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    try:
        collection = await get_users_collection()
        result = await collection.insert_one(user.dict())
        return {"id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    try:
        collection = await get_users_collection()
        result = await collection.delete_one({"_id": ObjectId(user_id)})
        if not result.deleted_count:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )