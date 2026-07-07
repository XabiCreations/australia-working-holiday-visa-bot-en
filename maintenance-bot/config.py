# ── Telegram ──────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"

# ── Twilio ────────────────────────────────────────────────────────────────────
TWILIO_SID   = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM  = "+XXXXXXXXXXX"
TWILIO_TO    = "+XXXXXXXXXXX"

# ── Monitoring ────────────────────────────────────────────────────────────────
MONITOR_URL  = "https://online.immi.gov.au/ola/app"
INTERVAL_MIN = 60    # 1 minute
INTERVAL_MAX = 120   # 2 minutes

# ── Network ───────────────────────────────────────────────────────────────────
REQUEST_TIMEOUT = 30   # seconds per HTTP request
MAX_RETRIES     = 3    # attempts before notifying network error

# ── Maintenance detection ─────────────────────────────────────────────────────
MAINTENANCE_KEYWORDS = [
    "maintenance",
    "planned system",
    "system maintenance",
    "unavailable",
    "we apologise",
    "apologize",
]
