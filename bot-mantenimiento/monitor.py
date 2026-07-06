import logging
import random
import time

import requests as req

from config import (
    INTERVALO_MAX,
    INTERVALO_MIN,
    MAX_REINTENTOS,
    PALABRAS_MANTENIMIENTO,
    TIMEOUT_SOLICITUD,
    URL_MONITOREO,
)
from notificaciones import enviar_telegram, hacer_llamada
from utils import es_mantenimiento, extraer_contenido, formatear_contenido, guardar_html

logger = logging.getLogger(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; MonitorVisado/1.0)"}


def obtener_pagina():
    for intento in range(1, MAX_REINTENTOS + 1):
        try:
            respuesta = req.get(URL_MONITOREO, timeout=TIMEOUT_SOLICITUD, headers=HEADERS)
            respuesta.raise_for_status()
            return respuesta.text
        except req.RequestException as e:
            logger.warning(f"⚠️ Intento {intento}/{MAX_REINTENTOS} fallido: {e}")
            if intento < MAX_REINTENTOS:
                time.sleep(10)
    return None


def iniciar_monitoreo():
    logger.info(f"🔍 Monitoreo iniciado → {URL_MONITOREO}")
    enviar_telegram(f"🔍 Monitoreo iniciado.\nURL: `{URL_MONITOREO}`")

    while True:
        hora = time.strftime("%Y-%m-%d %H:%M:%S")
        html = obtener_pagina()

        if html is None:
            msg = (
                f"❌ No se pudo obtener la página tras {MAX_REINTENTOS} intentos.\n"
                f"🕐 Hora: `{hora}`"
            )
            logger.error(msg)
            enviar_telegram(msg)

        else:
            guardar_html(html)
            contenido = extraer_contenido(html)

            if es_mantenimiento(contenido, PALABRAS_MANTENIMIENTO):
                msg = (
                    f"🔧 `[{hora}]`\n\n"
                    f"La página continúa en mantenimiento.\n\n"
                    f"{formatear_contenido(contenido)}"
                )
                logger.info(f"🔧 [{hora}] Página en mantenimiento.")
                enviar_telegram(msg)

            else:
                msg = (
                    f"✅ `[{hora}]`\n\n"
                    f"¡La página ya está disponible!\n\n"
                    f"{formatear_contenido(contenido)}"
                )
                logger.info(f"✅ [{hora}] ¡Página disponible!")
                enviar_telegram(msg)
                hacer_llamada(
                    "Atención. La página del visado de Australia ya está disponible. "
                    "Accede ahora para continuar con tu solicitud."
                )
                logger.info("✅ Monitoreo finalizado.")
                return

        intervalo = random.randint(INTERVALO_MIN, INTERVALO_MAX)
        minutos, segundos = divmod(intervalo, 60)
        logger.info(f"⏳ Próxima comprobación en {minutos}m {segundos}s...\n")
        time.sleep(intervalo)
