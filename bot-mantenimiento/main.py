import logging
import sys
from utils import configurar_logs
from monitor import iniciar_monitoreo

if __name__ == "__main__":
    # Forzar UTF-8 en la consola de Windows (CMD / PowerShell)
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    configurar_logs()
    logger = logging.getLogger(__name__)

    try:
        iniciar_monitoreo()
    except KeyboardInterrupt:
        logger.info("\n🛑 Monitoreo detenido por el usuario.")
