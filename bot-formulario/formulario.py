import logging
import random
import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import (
    INTERVALO_MAX,
    INTERVALO_MIN,
    PASO_FINAL,
    TIMEOUT_BOTON,
    TIMEOUT_PASO,
    XPATH_BOTON,
    XPATH_PASO,
)
from notificaciones import enviar_telegram, hacer_llamada

logger = logging.getLogger(__name__)


def obtener_paso(driver):
    elemento = WebDriverWait(driver, TIMEOUT_BOTON).until(
        EC.presence_of_element_located((By.XPATH, XPATH_PASO))
    )
    return elemento.text.strip()


def pulsar_siguiente(driver):
    boton = WebDriverWait(driver, TIMEOUT_BOTON).until(
        EC.element_to_be_clickable((By.XPATH, XPATH_BOTON))
    )
    boton.click()


def esperar_cambio_paso(driver, paso_anterior):
    """Devuelve el nuevo paso si el formulario avanzó, o None si no hubo cambio."""
    try:
        WebDriverWait(driver, TIMEOUT_PASO).until(
            lambda d: d.find_element(By.XPATH, XPATH_PASO).text.strip() != paso_anterior
        )
        return driver.find_element(By.XPATH, XPATH_PASO).text.strip()
    except TimeoutException:
        return None


def ejecutar_ciclo(driver):
    """Ejecuta un ciclo completo: lee el paso, pulsa Next y espera el cambio."""
    hora = time.strftime("%Y-%m-%d %H:%M:%S")

    paso_actual = obtener_paso(driver)
    logger.info(f"[{hora}] Paso actual: {paso_actual}")

    pulsar_siguiente(driver)
    logger.info(f"[{hora}] ✅ Botón 'Next' pulsado.")

    nuevo_paso = esperar_cambio_paso(driver, paso_actual)

    if nuevo_paso:
        logger.info(f"✅ Formulario avanzó al paso: {nuevo_paso}")
        hacer_llamada(
            f"Atención. El formulario de visado ha avanzado al paso {nuevo_paso}. "
            f"Accede a la aplicación para continuar."
        )
        enviar_telegram(f"✅ ¡El formulario avanzó al siguiente paso!: *{nuevo_paso}*")
    else:
        msg = (
            f"⚠️ Sin cambio de paso tras pulsar Next.\n"
            f"🕐 Hora: `{hora}`\n"
            f"📍 Paso actual: `{paso_actual}`"
        )
        logger.warning(msg)
        enviar_telegram(msg)

    return nuevo_paso or paso_actual


def iniciar_automatizacion(driver):
    logger.info("🤖 Automatización del formulario iniciada.")

    while True:
        hora = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            paso = ejecutar_ciclo(driver)

            if PASO_FINAL in paso:
                logger.info(f"🎯 Formulario alcanzó el paso {PASO_FINAL}. Finalizando.")
                enviar_telegram(f"🎯 Formulario alcanzó el paso *{PASO_FINAL}*. Cerrando en 5 segundos.")
                time.sleep(5)
                return

        except TimeoutException:
            msg = f"⏱ Timeout: botón o paso no encontrado.\nHora: `{hora}`"
            logger.warning(msg)
            enviar_telegram(msg)

        except NoSuchElementException:
            msg = f"❌ Elemento no encontrado en la página.\nHora: `{hora}`"
            logger.error(msg)
            enviar_telegram(msg)

        except WebDriverException as e:
            msg = f"❗ Error del navegador: `{e}`\nHora: `{hora}`"
            logger.error(msg)
            enviar_telegram(msg)

        except Exception as e:
            msg = f"❗ Error inesperado: `{e}`\nHora: `{hora}`"
            logger.error(msg)
            enviar_telegram(msg)

        intervalo = random.randint(INTERVALO_MIN, INTERVALO_MAX)
        minutos, segundos = divmod(intervalo, 60)
        logger.info(f"⏳ Próximo intento en {minutos}m {segundos}s...\n")
        time.sleep(intervalo)
