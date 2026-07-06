from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def crear_driver():
    opciones = Options()
    opciones.add_argument("--start-maximized")
    opciones.add_argument("--disable-blink-features=AutomationControlled")
    opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
    opciones.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(options=opciones)
