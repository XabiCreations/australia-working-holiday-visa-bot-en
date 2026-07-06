# ── Telegram ──────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"

# ── Twilio ────────────────────────────────────────────────────────────────────
TWILIO_SID   = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM  = "+XXXXXXXXXXX"
TWILIO_TO    = "+XXXXXXXXXXX"

# ── Monitoreo ─────────────────────────────────────────────────────────────────
URL_MONITOREO = "https://online.immi.gov.au/ola/app"
INTERVALO_MIN = 60    # 1 minuto
INTERVALO_MAX = 120   # 2 minutos

# ── Red ───────────────────────────────────────────────────────────────────────
TIMEOUT_SOLICITUD = 30   # segundos por petición HTTP
MAX_REINTENTOS    = 3    # intentos antes de notificar error de red

# ── Detección de mantenimiento ────────────────────────────────────────────────
PALABRAS_MANTENIMIENTO = [
    "maintenance",
    "planned system",
    "system maintenance",
    "unavailable",
    "we apologise",
    "apologize",
]
