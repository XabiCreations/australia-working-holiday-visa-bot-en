import logging
import os
import sys
from bs4 import BeautifulSoup

LOG_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DUMP = os.path.join(LOG_DIR, "last_page.html")

# lxml is faster; html.parser is the built-in Python fallback (no install needed)
try:
    import lxml  # noqa: F401
    HTML_PARSER = "lxml"
except ImportError:
    HTML_PARSER = "html.parser"


def configure_logging():
    log_path = os.path.join(LOG_DIR, "maintenance.log")
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # On Windows the StreamHandler inherits the stdout already reconfigured in main.py
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, stream_handler])


def extract_content(html):
    soup = BeautifulSoup(html, HTML_PARSER)

    h1 = soup.find("h1")
    h2 = soup.find("h2")
    h3 = soup.find("h3")

    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
    paragraph = max(paragraphs, key=len) if paragraphs else ""

    return {
        "h1": h1.get_text(strip=True) if h1 else "",
        "h2": h2.get_text(strip=True) if h2 else "",
        "h3": h3.get_text(strip=True) if h3 else "",
        "p":  paragraph,
    }


def is_maintenance(content, keywords):
    text = " ".join(content.values()).lower()
    return any(k.lower() in text for k in keywords)


def save_html(html):
    with open(HTML_DUMP, "w", encoding="utf-8") as f:
        f.write(html)


def format_content(content):
    return (
        f"H1: {content['h1'] or '(empty)'}\n"
        f"H2: {content['h2'] or '(empty)'}\n"
        f"H3: {content['h3'] or '(empty)'}\n"
        f"P:  {content['p']  or '(empty)'}"
    )
