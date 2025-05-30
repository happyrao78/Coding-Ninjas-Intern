from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.faq_routes import voice_router
from routes.info_routes import voice_router as info_router
from routes.api_routes import api_router
import sys
import os
from dotenv import load_dotenv

# Set console encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Calling Agent API",
    description="Voice-based calling agent for data collection",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(voice_router)
app.include_router(api_router)
app.include_router(info_router)

@app.get("/")
def read_root():
    return {"status": "Calling agent server is running"}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy", "message": "Call Agent is operational"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)