# ── Telegram ──────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"

# ── Twilio ────────────────────────────────────────────────────────────────────
TWILIO_SID   = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM  = "+XXXXXXXXXXX"
TWILIO_TO    = "+XXXXXXXXXXX"

# ── Selenium ──────────────────────────────────────────────────────────────────
URL_VISADO  = "https://online.immi.gov.au/elp/app"
XPATH_PASO  = "//span[@class='wc-label' and contains(text(), '/17')]"
XPATH_BOTON = "//button[.//span[text()='Next']]"

# ── Lógica ────────────────────────────────────────────────────────────────────
PASO_FINAL = "6/17"

# ── Intervalos y timeouts ─────────────────────────────────────────────────────
INTERVALO_MIN = 30    # segundos entre ciclos (mínimo)
INTERVALO_MAX = 105   # segundos entre ciclos (máximo)
TIMEOUT_BOTON = 10    # segundos esperando que aparezca el botón o el paso
TIMEOUT_PASO  = 30    # segundos esperando que el formulario cambie de paso
