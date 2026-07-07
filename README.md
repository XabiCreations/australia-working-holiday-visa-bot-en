# Australia Visa — Automation Bots

Two independent bots for managing the visa application process on the Australian immigration portal (ImmiAccount).

## Included bots

### `form-bot/` — Form bot
Automates navigation of the immigration portal form, periodically clicking the "Next" button and detecting step changes. Optionally notifies via Telegram and/or voice call (Twilio) when the form advances.

### `maintenance-bot/` — Maintenance bot
Monitors whether the portal is under maintenance and alerts as soon as it becomes available again. Optionally notifies via Telegram and/or voice call (Twilio).

---

## Project structure

```
.
├── form-bot/
│   ├── main.py            # Entry point
│   ├── config.py          # Credentials and configuration parameters
│   ├── form.py            # Form automation logic
│   ├── browser.py         # Chrome browser setup
│   ├── login.py           # Automatic login
│   ├── notifications.py   # Telegram and Twilio (optional)
│   ├── utils.py           # Logging
│   └── requirements.txt
│
└── maintenance-bot/
    ├── main.py            # Entry point
    ├── config.py          # Credentials and configuration parameters
    ├── monitor.py         # HTTP monitoring logic
    ├── notifications.py   # Telegram and Twilio (optional)
    ├── utils.py           # Logging and HTML parsing
    └── requirements.txt
```

---

## Prerequisites

- Python 3.10 or higher
- Google Chrome installed
- Telegram and/or Twilio *(optional — see [Notifications](#notifications) section)*

---

## Configuration

Edit the `config.py` file in the corresponding bot folder and fill in your values. Only the fields you configure will be used; the rest are silently ignored.

```python
# ── ImmiAccount (required) ────────────────────────────────────────────────────
IMMI_EMAIL    = "YOUR_EMAIL"
IMMI_PASSWORD = "YOUR_PASSWORD"

# ── Telegram (optional) ───────────────────────────────────────────────────────
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"

# ── Twilio (optional) ─────────────────────────────────────────────────────────
TWILIO_SID   = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM  = "+XXXXXXXXXXX"
TWILIO_TO    = "+XXXXXXXXXXX"
```

---

## Installation

```bash
# Form bot
cd form-bot
pip install -r requirements.txt

# Maintenance bot
cd maintenance-bot
pip install -r requirements.txt
```

---

## Usage

### Form bot

```bash
cd form-bot
python main.py
```

1. Chrome will open with the immigration portal.
2. The bot logs in automatically using the credentials in `config.py`.
3. Navigate to the form within the portal.
4. Press **ENTER** in the terminal to start the automation.
5. The bot will click "Next" automatically every 30–105 seconds.
6. If Telegram or Twilio is configured, you will receive notifications on each step change.
7. The bot stops automatically when it reaches the step defined in `FINAL_STEP` (`config.py`).

### Maintenance bot

```bash
cd maintenance-bot
python main.py
```

1. The bot will check the portal every 1–2 minutes.
2. If Telegram is configured, you will receive a message on each check.
3. As soon as the page is available, you will receive a notification and the bot will stop.

---

## Notifications

Both bots support three notification modes. The program automatically detects which services are configured and uses only those available.

### Mode 1 — Telegram only

Fill in only the Telegram fields. Twilio fields can be left with their default placeholder values.

```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"
TWILIO_SID     = "YOUR_TWILIO_ACCOUNT_SID"   # leave empty
TWILIO_TOKEN   = "YOUR_TWILIO_AUTH_TOKEN"    # leave empty
TWILIO_FROM    = "+XXXXXXXXXXX"              # leave empty
TWILIO_TO      = "+XXXXXXXXXXX"              # leave empty
```

### Mode 2 — Twilio only

Fill in only the Twilio fields. Telegram fields can be left with their default placeholder values.

```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # leave empty
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"    # leave empty
TWILIO_SID     = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_TOKEN   = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM    = "+15551234567"
TWILIO_TO      = "+44700000000"
```

### Mode 3 — Telegram and Twilio simultaneously

Fill in all fields. Both services will run in parallel.

```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"
TWILIO_SID     = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_TOKEN   = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM    = "+15551234567"
TWILIO_TO      = "+44700000000"
```

---

## Step-by-step setup

### Telegram

> 📺 **Video tutorial:** [How to set up a Telegram bot step by step](https://youtu.be/Qg5BaKTW1Uw?si=bByOrQt9kj_wKfoW)

#### 1. Create a bot with BotFather

1. Open Telegram and search for **@BotFather**.
2. Start a conversation and send the command `/newbot`.
3. Follow the instructions: choose a name for the bot (e.g. `My Visa Bot`) and a username ending in `bot` (e.g. `myvisabot_bot`).
4. BotFather will send you the **Bot Token**. It looks like this:
   ```
   YOUR_TELEGRAM_BOT_TOKEN
   ```

#### 2. Get your Chat ID

1. Start a conversation with your bot in Telegram by sending it any message.
2. Open this URL in your browser (replace `<TOKEN>` with your actual token):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
3. In the JSON response, look for the `"chat"` → `"id"` field. That number is your Chat ID:
   ```json
   "chat": { "id": 123456789, ... }
   ```

#### 3. Add credentials to the project

Edit `config.py` in the bot folder you want to use:

```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"
```

---

### Twilio

> 📺 **Video tutorial:** [How to set up Twilio step by step](https://www.youtube.com/watch?v=XxKciuSKLf0)

#### 1. Create an account

Sign up at [twilio.com](https://www.twilio.com). You can start with the free trial account.

#### 2. Get your Account SID and Auth Token

Once inside the Twilio dashboard, on the main **Console** page you will see:

- **Account SID**: starts with `AC`
- **Auth Token**: click the eye icon to reveal it

#### 3. Get a phone number

1. In the side menu go to **Phone Numbers → Manage → Buy a number**.
2. Filter by country and capability (select **Voice** to make calls).
3. Purchase the number. With a trial account Twilio provides one for free.
4. The number will be in E.164 format, for example `+15551234567`.

> **Note:** With trial accounts, the destination number (`TWILIO_TO`) must be **verified** in Twilio before it can receive calls. Go to **Phone Numbers → Manage → Verified Caller IDs** to add it.

#### 4. Add credentials to the project

Edit `config.py` in the bot folder you want to use:

```python
TWILIO_SID   = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM  = "+15551234567"   # your Twilio number
TWILIO_TO    = "+44700000000"   # your personal phone number
```

---

## Notes

- Logs are saved automatically to `form.log` and `maintenance.log` inside each bot folder.
- The `data.txt` file in the root is not used by any bot; it serves only as a manual reference.
