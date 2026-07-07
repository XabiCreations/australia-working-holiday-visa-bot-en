# ── Telegram ──────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"

# ── Twilio ────────────────────────────────────────────────────────────────────
TWILIO_SID   = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM  = "+XXXXXXXXXXX"
TWILIO_TO    = "+XXXXXXXXXXX"

# ── ImmiAccount ───────────────────────────────────────────────────────────────
IMMI_EMAIL    = "YOUR_EMAIL"
IMMI_PASSWORD = "YOUR_PASSWORD"

# ── Selenium ──────────────────────────────────────────────────────────────────
FORM_URL       = "https://online.immi.gov.au/elp/app"
URL_POST_LOGIN = "https://online.immi.gov.au"
XPATH_STEP     = "//span[@class='wc-label' and contains(text(), '/17')]"
XPATH_BUTTON   = "//button[.//span[text()='Next']]"

# ── Logic ─────────────────────────────────────────────────────────────────────
FINAL_STEP = "6/17"

# ── Intervals and timeouts ────────────────────────────────────────────────────
INTERVAL_MIN     = 30    # minimum seconds between cycles
INTERVAL_MAX     = 105   # maximum seconds between cycles
TIMEOUT_ELEMENT  = 10    # seconds waiting for button or step to appear
TIMEOUT_STEP     = 30    # seconds waiting for form to change step
