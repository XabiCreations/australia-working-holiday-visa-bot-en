import logging
import sys

from browser import create_driver
from config import FORM_URL
from form import start_automation
from login import login
from notifications import send_telegram
from utils import configure_logging

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    configure_logging()
    logger = logging.getLogger(__name__)

    driver = create_driver()
    driver.get(FORM_URL)

    login(driver)

    input("📋 Navigate to the form and press ENTER to start...\n")

    try:
        start_automation(driver)
    except KeyboardInterrupt:
        logger.info("🛑 Program stopped by user.")
        send_telegram("🛑 Program manually stopped by user.")
    finally:
        driver.quit()
