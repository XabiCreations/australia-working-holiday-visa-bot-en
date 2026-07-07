import logging

import requests
from twilio.rest import Client as TwilioClient

from config import CHAT_ID, TELEGRAM_TOKEN, TWILIO_FROM, TWILIO_SID, TWILIO_TO, TWILIO_TOKEN

logger = logging.getLogger(__name__)

_PLACEHOLDERS = {
    "", "YOUR_TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_CHAT_ID",
    "YOUR_TWILIO_ACCOUNT_SID", "YOUR_TWILIO_AUTH_TOKEN", "+XXXXXXXXXXX",
}


def _telegram_configured():
    return (
        TELEGRAM_TOKEN not in _PLACEHOLDERS
        and str(CHAT_ID) not in _PLACEHOLDERS
    )


def _twilio_configured():
    return (
        TWILIO_SID not in _PLACEHOLDERS
        and TWILIO_TOKEN not in _PLACEHOLDERS
        and TWILIO_FROM not in _PLACEHOLDERS
        and TWILIO_TO not in _PLACEHOLDERS
    )


def send_telegram(message):
    if not _telegram_configured():
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            logger.info("📩 Telegram message sent.")
        else:
            logger.error(f"❌ Telegram error ({response.status_code}): {response.text}")
    except requests.RequestException as e:
        logger.error(f"❌ Network error sending Telegram message: {e}")


def make_call(voice_message):
    if not _twilio_configured():
        return
    try:
        client = TwilioClient(TWILIO_SID, TWILIO_TOKEN)
        twiml = (
            f"<Response>"
            f'<Say language="en-US" voice="alice">{voice_message}</Say>'
            f'<Pause length="1"/>'
            f'<Say language="en-US" voice="alice">{voice_message}</Say>'
            f"</Response>"
        )
        client.calls.create(twiml=twiml, to=TWILIO_TO, from_=TWILIO_FROM)
        logger.info("📞 Call made.")
    except Exception as e:
        logger.error(f"❌ Error making Twilio call: {e}")
        send_telegram(f"❌ Could not make Twilio call: `{e}`")
