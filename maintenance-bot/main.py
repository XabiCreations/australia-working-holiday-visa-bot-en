import logging
import sys

from utils import configure_logging
from monitor import start_monitoring

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    configure_logging()
    logger = logging.getLogger(__name__)

    try:
        start_monitoring()
    except KeyboardInterrupt:
        logger.info("\n🛑 Monitoring stopped by user.")
