import logging
import random
import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import (
    FINAL_STEP,
    INTERVAL_MAX,
    INTERVAL_MIN,
    TIMEOUT_ELEMENT,
    TIMEOUT_STEP,
    XPATH_BUTTON,
    XPATH_STEP,
)
from notifications import send_telegram, make_call

logger = logging.getLogger(__name__)


def get_step(driver):
    element = WebDriverWait(driver, TIMEOUT_ELEMENT).until(
        EC.presence_of_element_located((By.XPATH, XPATH_STEP))
    )
    return element.text.strip()


def click_next(driver):
    button = WebDriverWait(driver, TIMEOUT_ELEMENT).until(
        EC.element_to_be_clickable((By.XPATH, XPATH_BUTTON))
    )
    button.click()


def wait_for_step_change(driver, previous_step):
    """Returns the new step if the form advanced, or None if no change."""
    try:
        WebDriverWait(driver, TIMEOUT_STEP).until(
            lambda d: d.find_element(By.XPATH, XPATH_STEP).text.strip() != previous_step
        )
        return driver.find_element(By.XPATH, XPATH_STEP).text.strip()
    except TimeoutException:
        return None


def run_cycle(driver):
    """Runs one full cycle: reads the step, clicks Next, and waits for a change."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    current_step = get_step(driver)
    logger.info(f"[{timestamp}] Current step: {current_step}")

    click_next(driver)
    logger.info(f"[{timestamp}] ✅ 'Next' button clicked.")

    new_step = wait_for_step_change(driver, current_step)

    if new_step:
        logger.info(f"✅ Form advanced to step: {new_step}")
        make_call(
            f"Attention. The visa form has advanced to step {new_step}. "
            f"Please access the application to continue."
        )
        send_telegram(f"✅ The form has advanced to the next step: *{new_step}*")
    else:
        msg = (
            f"⚠️ No step change after clicking Next.\n"
            f"🕐 Time: `{timestamp}`\n"
            f"📍 Current step: `{current_step}`"
        )
        logger.warning(msg)
        send_telegram(msg)

    return new_step or current_step


def start_automation(driver):
    logger.info("🤖 Form automation started.")

    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            step = run_cycle(driver)

            if FINAL_STEP in step:
                logger.info(f"🎯 Form reached step {FINAL_STEP}. Stopping.")
                send_telegram(f"🎯 Form reached step *{FINAL_STEP}*. Closing in 5 seconds.")
                time.sleep(5)
                return

        except TimeoutException:
            msg = f"⏱ Timeout: button or step not found.\nTime: `{timestamp}`"
            logger.warning(msg)
            send_telegram(msg)

        except NoSuchElementException:
            msg = f"❌ Element not found on the page.\nTime: `{timestamp}`"
            logger.error(msg)
            send_telegram(msg)

        except WebDriverException as e:
            msg = f"❗ Browser error: `{e}`\nTime: `{timestamp}`"
            logger.error(msg)
            send_telegram(msg)

        except Exception as e:
            msg = f"❗ Unexpected error: `{e}`\nTime: `{timestamp}`"
            logger.error(msg)
            send_telegram(msg)

        interval = random.randint(INTERVAL_MIN, INTERVAL_MAX)
        minutes, seconds = divmod(interval, 60)
        logger.info(f"⏳ Next attempt in {minutes}m {seconds}s...\n")
        time.sleep(interval)
