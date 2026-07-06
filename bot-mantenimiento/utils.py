import logging
import os
import sys
from bs4 import BeautifulSoup

LOG_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DUMP = os.path.join(LOG_DIR, "ultima_pagina.html")

# lxml es más rápido; html.parser es el fallback incluido en Python (sin instalar nada)
try:
    import lxml  # noqa: F401
    HTML_PARSER = "lxml"
except ImportError:
    HTML_PARSER = "html.parser"


def configurar_logs():
    log_path = os.path.join(LOG_DIR, "mantenimiento.log")
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # En Windows el StreamHandler hereda el stdout ya reconfigurado en main.py
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, stream_handler])


def extraer_contenido(html):
    soup = BeautifulSoup(html, HTML_PARSER)

    h1 = soup.find("h1")
    h2 = soup.find("h2")
    h3 = soup.find("h3")

    parrafos = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
    parrafo = max(parrafos, key=len) if parrafos else ""

    return {
        "h1": h1.get_text(strip=True) if h1 else "",
        "h2": h2.get_text(strip=True) if h2 else "",
        "h3": h3.get_text(strip=True) if h3 else "",
        "p":  parrafo,
    }


def es_mantenimiento(contenido, palabras_clave):
    texto = " ".join(contenido.values()).lower()
    return any(p.lower() in texto for p in palabras_clave)


def guardar_html(html):
    with open(HTML_DUMP, "w", encoding="utf-8") as f:
        f.write(html)


def formatear_contenido(contenido):
    return (
        f"H1: {contenido['h1'] or '(vacío)'}\n"
        f"H2: {contenido['h2'] or '(vacío)'}\n"
        f"H3: {contenido['h3'] or '(vacío)'}\n"
        f"P:  {contenido['p']  or '(vacío)'}"
    )
