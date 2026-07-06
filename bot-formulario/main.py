import logging
import sys

from browser import crear_driver
from config import URL_VISADO
from formulario import iniciar_automatizacion
from notificaciones import enviar_telegram
from utils import configurar_logs

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    configurar_logs()
    logger = logging.getLogger(__name__)

    driver = crear_driver()
    driver.get(URL_VISADO)

    input("🔐 Inicia sesión y navega al formulario. Presiona ENTER para comenzar...\n")

    try:
        iniciar_automatizacion(driver)
    except KeyboardInterrupt:
        logger.info("🛑 Programa detenido por el usuario.")
        enviar_telegram("🛑 Programa detenido manualmente por el usuario.")
    finally:
        driver.quit()
