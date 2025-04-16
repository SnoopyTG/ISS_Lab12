from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes.items import router as items_router
from routes.analytics import router as analytics_router
from routes.quiz import router as quiz_router


app = FastAPI(
    title="Multi-Page FastAPI App",
    description="A simple FastAPI app with multiple pages",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "message": str(e)}
        )
        
app.include_router(items_router, prefix="/items", tags=["Items"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(quiz_router, prefix="/quiz", tags=["Quiz"])

# why the hell did I write this function?
@app.get("/home")
async def get_home():
    return {"message": "Welcome to the Multi-Page FastAPI App!"}