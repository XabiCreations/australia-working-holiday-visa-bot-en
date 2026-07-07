import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import IMMI_EMAIL, IMMI_PASSWORD, TIMEOUT_ELEMENT, URL_POST_LOGIN

logger = logging.getLogger(__name__)


def login(driver):
    logger.info("🔐 Logging in automatically...")

    WebDriverWait(driver, TIMEOUT_ELEMENT).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    driver.find_element(By.ID, "username").send_keys(IMMI_EMAIL)
    driver.find_element(By.ID, "password").send_keys(IMMI_PASSWORD)
    driver.find_element(By.XPATH, "//button[@name='login' and not(@tabindex='-1')]").click()

    logger.info("✅ Credentials submitted.")
    time.sleep(0.1)

    driver.get(URL_POST_LOGIN)
    logger.info(f"🌐 Redirected to {URL_POST_LOGIN}")
