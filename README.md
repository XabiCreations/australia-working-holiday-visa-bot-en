# Visado Australia — Bots de Automatización

Dos bots independientes para gestionar la solicitud de visado en el portal de inmigración australiana (ImmiAccount).

## Bots incluidos

### `bot-formulario/` — Bot de formulario
Automatiza la navegación del formulario del portal de inmigración, pulsando el botón "Next" periódicamente y detectando el avance de paso. Notifica opcionalmente por Telegram y/o llamada de voz (Twilio) cuando el formulario avanza de paso.

### `bot-mantenimiento/` — Bot de mantenimiento
Monitorea si el portal está en mantenimiento y avisa en cuanto vuelva a estar disponible. Notifica opcionalmente por Telegram y/o llamada de voz (Twilio).

---

## Estructura del proyecto

```
.
├── bot-formulario/
│   ├── main.py            # Punto de entrada
│   ├── config.py          # Credenciales y parámetros de configuración
│   ├── formulario.py      # Lógica de automatización del formulario
│   ├── browser.py         # Configuración del navegador Chrome
│   ├── login.py           # Inicio de sesión automático
│   ├── notificaciones.py  # Telegram y Twilio (opcionales)
│   ├── utils.py           # Logging
│   └── requirements.txt
│
└── bot-mantenimiento/
    ├── main.py            # Punto de entrada
    ├── config.py          # Credenciales y parámetros de configuración
    ├── monitor.py         # Lógica de monitoreo HTTP
    ├── notificaciones.py  # Telegram y Twilio (opcionales)
    ├── utils.py           # Logging y parsing HTML
    └── requirements.txt
```

---

## Requisitos previos

- Python 3.10 o superior
- Google Chrome instalado
- Telegram y/o Twilio *(opcionales — ver sección [Notificaciones](#notificaciones))*

---

## Configuración

Edita el archivo `config.py` de la carpeta correspondiente y rellena los valores que necesites. Solo los campos que configures se utilizarán; el resto se ignora automáticamente.

```python
# ── ImmiAccount (obligatorio) ─────────────────────────────────────────────────
IMMI_EMAIL    = "YOUR_EMAIL"
IMMI_PASSWORD = "YOUR_PASSWORD"

# ── Telegram (opcional) ───────────────────────────────────────────────────────
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"

# ── Twilio (opcional) ─────────────────────────────────────────────────────────
TWILIO_SID   = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM  = "+XXXXXXXXXXX"
TWILIO_TO    = "+XXXXXXXXXXX"
```

---

## Instalación

```bash
# Bot de formulario
cd bot-formulario
pip install -r requirements.txt

# Bot de mantenimiento
cd bot-mantenimiento
pip install -r requirements.txt
```

---

## Uso

### Bot de formulario

```bash
cd bot-formulario
python main.py
```

1. Se abrirá Chrome con el portal de inmigración.
2. El bot inicia sesión automáticamente con las credenciales de `config.py`.
3. Navega al formulario dentro del portal.
4. Pulsa **ENTER** en la terminal para iniciar la automatización.
5. El bot pulsará "Next" automáticamente cada 30–105 segundos.
6. Si tienes Telegram o Twilio configurados, recibirás notificaciones en cada cambio de paso.
7. El bot se detiene automáticamente al alcanzar el paso configurado en `PASO_FINAL` (`config.py`).

### Bot de mantenimiento

```bash
cd bot-mantenimiento
python main.py
```

1. El bot comprobará el portal cada 1–2 minutos.
2. Si tienes Telegram configurado, recibirás un mensaje en cada comprobación.
3. En cuanto la página esté disponible, recibirás una notificación y el bot finalizará.

---

## Notificaciones

Ambos bots admiten tres modos de notificación. El programa detecta automáticamente qué servicios están configurados y usa solo los disponibles.

### Modo 1 — Solo Telegram

Rellena únicamente los campos de Telegram. Los de Twilio pueden dejarse con sus valores por defecto.

```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"
TWILIO_SID     = "YOUR_TWILIO_ACCOUNT_SID"   # sin rellenar
TWILIO_TOKEN   = "YOUR_TWILIO_AUTH_TOKEN"    # sin rellenar
TWILIO_FROM    = "+XXXXXXXXXXX"              # sin rellenar
TWILIO_TO      = "+XXXXXXXXXXX"              # sin rellenar
```

### Modo 2 — Solo Twilio

Rellena únicamente los campos de Twilio. Los de Telegram pueden dejarse con sus valores por defecto.

```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # sin rellenar
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"    # sin rellenar
TWILIO_SID     = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_TOKEN   = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM    = "+15551234567"
TWILIO_TO      = "+34600123456"
```

### Modo 3 — Telegram y Twilio simultáneamente

Rellena todos los campos. Ambos servicios funcionarán en paralelo.

```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"
TWILIO_SID     = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_TOKEN   = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM    = "+15551234567"
TWILIO_TO      = "+34600123456"
```

---

## Configuración paso a paso

### Telegram

> 📺 **Video tutorial:** [Cómo configurar un bot de Telegram paso a paso](https://youtu.be/Qg5BaKTW1Uw?si=bByOrQt9kj_wKfoW)

#### 1. Crear un bot con BotFather

1. Abre Telegram y busca **@BotFather**.
2. Inicia una conversación y envía el comando `/newbot`.
3. Sigue las instrucciones: elige un nombre para el bot (p. ej. `Mi Bot Visado`) y un nombre de usuario que termine en `bot` (p. ej. `mibotvisado_bot`).
4. BotFather te enviará el **Bot Token**. Tiene este formato:
   ```
   YOUR_TELEGRAM_BOT_TOKEN
   ```

#### 2. Obtener el Chat ID

1. Inicia una conversación con tu bot en Telegram enviándole cualquier mensaje.
2. Abre esta URL en el navegador (sustituye `<TOKEN>` por tu token real):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
3. En la respuesta JSON busca el campo `"chat"` → `"id"`. Ese número es tu Chat ID:
   ```json
   "chat": { "id": 123456789, ... }
   ```

#### 3. Colocar las credenciales en el proyecto

Edita `config.py` de la carpeta del bot que vayas a usar:

```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"
```

---

### Twilio

> 📺 **Video tutorial:** [Cómo configurar Twilio paso a paso](https://www.youtube.com/watch?v=XxKciuSKLf0)

#### 1. Crear una cuenta

Regístrate en [twilio.com](https://www.twilio.com). Puedes empezar con la cuenta gratuita (trial).

#### 2. Obtener el Account SID y el Auth Token

Una vez dentro del panel de Twilio, en la página principal (**Console Dashboard**) verás directamente:

- **Account SID**: empieza por `AC`, por ejemplo `YOUR_TWILIO_ACCOUNT_SID`
- **Auth Token**: haz clic en el icono del ojo para mostrarlo

#### 3. Obtener un número de teléfono

1. En el menú lateral ve a **Phone Numbers → Manage → Buy a number**.
2. Filtra por país y capacidad (selecciona **Voice** para poder hacer llamadas).
3. Compra el número. Con la cuenta trial Twilio te proporciona uno gratuito.
4. El número tendrá formato E.164, por ejemplo `+15551234567`.

> **Nota:** Con cuentas trial, el número de destino (`TWILIO_TO`) debe estar **verificado** en Twilio antes de poder recibir llamadas. Ve a **Phone Numbers → Manage → Verified Caller IDs** para añadirlo.

#### 4. Colocar las credenciales en el proyecto

Edita `config.py` de la carpeta del bot que vayas a usar:

```python
TWILIO_SID   = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM  = "+15551234567"   # tu número de Twilio
TWILIO_TO    = "+34600123456"   # tu teléfono personal
```

---

## Notas

- Los logs se guardan automáticamente en `formulario.log` y `mantenimiento.log` dentro de cada carpeta.
- El archivo `datos.txt` de la raíz no es usado por ningún bot; sirve únicamente como referencia manual.
