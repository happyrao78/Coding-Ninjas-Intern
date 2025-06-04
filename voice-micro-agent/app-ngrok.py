from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.faq_routes import voice_router
from routes.info_routes import voice_router as info_router
from routes.api_routes import api_router
import sys
import os
import logging
import time
from dotenv import load_dotenv
from ngrok_helper import initialize_webhook, get_webhook_url

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set console encoding to UTF-8
sys.stdout.reconfigure(encoding="utf-8")

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Calling Agent API",
    description="Voice-based calling agent for data collection",
    version="1.0.0",
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


@app.on_event("startup")
async def startup_event():
    """Initialize webhook URL on startup"""
    logger.info("Starting application...")

    # Wait a bit for ngrok to be ready (only in Docker)
    if os.getenv("DOCKER_ENV"):
        logger.info("Docker environment detected, waiting for ngrok...")
        time.sleep(10)

        try:
            initialize_webhook()
            logger.info(f"Webhook URL initialized: {get_webhook_url()}")
        except Exception as e:
            logger.error(f"Failed to initialize webhook: {e}")


@app.get("/")
def read_root():
    return {"status": "Calling agent server is running"}


@app.get("/healthcheck")
def healthcheck():
    webhook_url = get_webhook_url()
    return {
        "status": "healthy",
        "message": "Call Agent is operational",
        "webhook_url": webhook_url,
    }


@app.get("/current-webhook")
def current_webhook():
    """Get current webhook URL"""
    return {"webhook_url": get_webhook_url(), "status": "active"}


@app.post("/refresh-webhook")
def refresh_webhook():
    """Manually refresh webhook URL"""
    try:
        initialize_webhook()
        return {"status": "refreshed", "webhook_url": get_webhook_url()}
    except Exception as e:
        return {"error": str(e), "status": "failed"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
