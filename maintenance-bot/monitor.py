import logging
import random
import time

import requests as req

from config import (
    INTERVAL_MAX,
    INTERVAL_MIN,
    MAINTENANCE_KEYWORDS,
    MAX_RETRIES,
    MONITOR_URL,
    REQUEST_TIMEOUT,
)
from notifications import send_telegram, make_call
from utils import is_maintenance, extract_content, format_content, save_html

logger = logging.getLogger(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; VisaMonitor/1.0)"}


def fetch_page():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = req.get(MONITOR_URL, timeout=REQUEST_TIMEOUT, headers=HEADERS)
            response.raise_for_status()
            return response.text
        except req.RequestException as e:
            logger.warning(f"⚠️ Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(10)
    return None


def start_monitoring():
    logger.info(f"🔍 Monitoring started → {MONITOR_URL}")
    send_telegram(f"🔍 Monitoring started.\nURL: `{MONITOR_URL}`")

    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        html = fetch_page()

        if html is None:
            msg = (
                f"❌ Could not retrieve the page after {MAX_RETRIES} attempts.\n"
                f"🕐 Time: `{timestamp}`"
            )
            logger.error(msg)
            send_telegram(msg)

        else:
            save_html(html)
            content = extract_content(html)

            if is_maintenance(content, MAINTENANCE_KEYWORDS):
                msg = (
                    f"🔧 `[{timestamp}]`\n\n"
                    f"The page is still under maintenance.\n\n"
                    f"{format_content(content)}"
                )
                logger.info(f"🔧 [{timestamp}] Page under maintenance.")
                send_telegram(msg)

            else:
                msg = (
                    f"✅ `[{timestamp}]`\n\n"
                    f"The page is now available!\n\n"
                    f"{format_content(content)}"
                )
                logger.info(f"✅ [{timestamp}] Page available!")
                send_telegram(msg)
                make_call(
                    "Attention. The Australian visa page is now available. "
                    "Access it now to continue with your application."
                )
                logger.info("✅ Monitoring complete.")
                return

        interval = random.randint(INTERVAL_MIN, INTERVAL_MAX)
        minutes, seconds = divmod(interval, 60)
        logger.info(f"⏳ Next check in {minutes}m {seconds}s...\n")
        time.sleep(interval)
