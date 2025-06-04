import requests
import time
import os
import logging

logger = logging.getLogger(__name__)


def get_ngrok_public_url(max_retries=30, retry_delay=2):
    """
    Fetch the public ngrok URL from ngrok's local API
    """
    for attempt in range(max_retries):
        try:
            # ngrok API endpoint (default port 4040)
            response = requests.get("http://ngrok:4040/api/tunnels", timeout=5)

            if response.status_code == 200:
                data = response.json()
                tunnels = data.get("tunnels", [])

                # Find the HTTPS tunnel
                for tunnel in tunnels:
                    if tunnel.get("proto") == "https":
                        public_url = tunnel.get("public_url")
                        if public_url:
                            logger.info(f"Found ngrok URL: {public_url}")
                            return public_url

                logger.warning(f"Attempt {attempt + 1}: No HTTPS tunnel found")

            else:
                logger.warning(
                    f"Attempt {attempt + 1}: ngrok API returned {response.status_code}"
                )

        except requests.exceptions.RequestException as e:
            logger.warning(
                f"Attempt {attempt + 1}: Failed to connect to ngrok API: {e}"
            )

        if attempt < max_retries - 1:
            time.sleep(retry_delay)

    raise Exception(f"Failed to get ngrok URL after {max_retries} attempts")


def wait_for_ngrok_and_update_webhook():
    """
    Wait for ngrok to be ready and update webhook URL
    """
    try:
        # Get dynamic ngrok URL
        public_url = get_ngrok_public_url()

        # Update environment variable
        os.environ["WEBHOOK_URL"] = public_url

        logger.info(f"Updated WEBHOOK_URL to: {public_url}")
        return public_url

    except Exception as e:
        logger.error(f"Failed to get ngrok URL: {e}")
        # Fallback to env file URL if available
        fallback_url = os.getenv("WEBHOOK_URL")
        if fallback_url:
            logger.warning(f"Using fallback URL from env: {fallback_url}")
            return fallback_url
        raise


# Global variable to store current webhook URL
current_webhook_url = None


def initialize_webhook():
    """Initialize and get the current webhook URL"""
    global current_webhook_url
    try:
        # Wait for ngrok and get dynamic URL
        current_webhook_url = wait_for_ngrok_and_update_webhook()
        logger.info(f"Webhook initialized with URL: {current_webhook_url}")

    except Exception as e:
        logger.error(f"Failed to initialize webhook: {e}")
        # Use fallback from env
        current_webhook_url = os.getenv("WEBHOOK_URL")


def get_webhook_url():
    """Get current webhook URL"""
    global current_webhook_url
    if not current_webhook_url:
        initialize_webhook()
    return current_webhook_url
