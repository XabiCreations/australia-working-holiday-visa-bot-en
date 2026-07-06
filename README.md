# Visado Australia — Bots de Automatización

Dos bots independientes para gestionar la solicitud de visado en el portal de inmigración australiana (ImmiAccount).

## Bots incluidos

### `bot-formulario/` — Bot de formulario
Automatiza la navegación del formulario del portal de inmigración, pulsando el botón "Next" periódicamente y detectando el avance de paso. Notifica por Telegram y llamada de voz (Twilio) cuando el formulario avanza de paso.

### `bot-mantenimiento/` — Bot de mantenimiento
Monitorea si el portal está en mantenimiento y avisa en cuanto vuelva a estar disponible. Envía un mensaje de Telegram en cada comprobación e inicia una llamada de voz cuando la página se recupera.

---

## Estructura del proyecto

```
.
├── bot-formulario/
│   ├── main.py            # Punto de entrada
│   ├── config.py          # Credenciales y parámetros de configuración
│   ├── formulario.py      # Lógica de automatización del formulario
│   ├── browser.py         # Configuración del navegador Chrome
│   ├── notificaciones.py  # Telegram y Twilio
│   ├── utils.py           # Logging
│   └── requirements.txt
│
└── bot-mantenimiento/
    ├── main.py            # Punto de entrada
    ├── config.py          # Credenciales y parámetros de configuración
    ├── monitor.py         # Lógica de monitoreo HTTP
    ├── notificaciones.py  # Telegram y Twilio
    ├── utils.py           # Logging y parsing HTML
    └── requirements.txt
```

---

## Requisitos previos

- Python 3.10 o superior
- Google Chrome instalado
- Una cuenta de Telegram con un bot creado (`@BotFather`)
- Una cuenta de Twilio con un número de teléfono activo

---

## Configuración

Antes de ejecutar cualquier bot, edita el archivo `config.py` de la carpeta correspondiente y rellena los valores con tus credenciales:

```python
# Telegram
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"   # Token de tu bot de Telegram
CHAT_ID        = "YOUR_TELEGRAM_CHAT_ID"     # ID del chat donde recibir los mensajes

# Twilio
TWILIO_SID   = "YOUR_TWILIO_ACCOUNT_SID"    # Account SID de Twilio
TWILIO_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"     # Auth Token de Twilio
TWILIO_FROM  = "+XXXXXXXXXXX"               # Número Twilio emisor (formato E.164)
TWILIO_TO    = "+XXXXXXXXXXX"               # Tu número de teléfono (formato E.164)
```

---

## Instalación

```bash
# Bot de formulario
cd bot-formulario
pip install -r requirements.txt

# Bot de monitoreo
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
2. Inicia sesión manualmente en ImmiAccount y navega al formulario.
3. Pulsa **ENTER** en la terminal para iniciar la automatización.
4. El bot pulsará "Next" automáticamente cada 30–105 segundos.
5. Recibirás una notificación en Telegram y una llamada de voz cada vez que el formulario avance de paso.
6. El bot se detiene automáticamente al alcanzar el paso configurado en `PASO_FINAL` (`config.py`).

### Bot de monitoreo

```bash
cd bot-mantenimiento
python main.py
```

1. El bot comprobará el portal cada 1–2 minutos.
2. Mientras esté en mantenimiento, enviará un mensaje de Telegram en cada comprobación.
3. En cuanto la página esté disponible, recibirás un mensaje de Telegram y una llamada de voz, y el bot finalizará.

---

## Notificaciones

| Canal | Cuándo se activa |
|---|---|
| Telegram | En cada comprobación, cambio de paso y error |
| Llamada de voz (Twilio) | Solo cuando se detecta un evento importante |

---

## Notas

- Los logs se guardan automáticamente en `formulario.log` y `mantenimiento.log` dentro de cada carpeta.
- Para cuentas Twilio en modo trial, el número de destino debe estar verificado en el panel de Twilio.
- El archivo `datos.txt` de la raíz no es usado por ningún bot; sirve únicamente como referencia manual.
