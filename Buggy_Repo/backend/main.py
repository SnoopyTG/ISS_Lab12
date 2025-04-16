from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes.items import router as items_router
from routes.analytics import router as analytics_router
from routes.quiz import router as quiz_router
from routes.users import router as users_router
from db import startup_db_client, shutdown_db_client
import uvicorn

app = FastAPI(
    title="Multi-Page FastAPI App",
    description="A simple FastAPI app with multiple pages",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handling middleware
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "message": str(e)}
        )

# Include routers
app.include_router(items_router, prefix="/items", tags=["Items"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(quiz_router, prefix="/quiz", tags=["Quiz"])
app.include_router(users_router, prefix="/users", tags=["Users"])

@app.get("/")
@app.get("/home")
async def get_home():
    return {"message": "Welcome to the Multi-Page FastAPI App!"}

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    await startup_db_client()

@app.on_event("shutdown")
async def shutdown_event():
    await shutdown_db_client()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)