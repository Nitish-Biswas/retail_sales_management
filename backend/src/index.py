from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import api
from src.services.db import close_db

app = FastAPI(
    title="TruEstate Sales Management API",
    description="Backend API for Sales Management System (Database Version)",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(api.router, prefix="/api", tags=["transactions"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
