import requests

API_URL = "http://127.0.0.1:8000/command"

commands = [

    # ========================
    # SYSTEM INFO
    # ========================
    "cpu usage",
    "ram usage",
    "what is the time",

    # ========================
    # APPLICATION CONTROL
    # ========================
    "open youtube",
    "open notepad",
    "close notepad",

    # ========================
    # VOLUME CONTROL
    # ========================
    "volume up",
    "volume down",
    "mute",

    # ========================
    # SYSTEM POWER
    # ========================
    "shutdown",
    "restart",

    # ========================
    # CONTACT MANAGEMENT
    # ========================
    "add contact rahul number 919876543210",
    "add contact daddy number 919123456789",

    # ========================
    # WHATSAPP MESSAGES
    # ========================
    "send message to rahul saying hello",
    "send message to daddy saying how are you",

    # ========================
    # SCHEDULED MESSAGE
    # ========================
    "send message to rahul at 7 pm saying good evening",

    # ========================
    # TELUGU COMMANDS
    # ========================
    "rahul ki msg chey hello",
    "rahul number 919876543210 add chey",

    # ========================
    # AI COMPLEX QUERIES
    # ========================
    "analyze ai market trends",
    "compare python and kotlin",
    "summarize artificial intelligence",

    # ========================
    # GENERAL CHAT
    # ========================
    "tell me a joke",
    "who created you",
]

for cmd in commands:

    print("\n==============================")
    print("COMMAND:", cmd)

    try:
        response = requests.post(
            API_URL,
            json={"command": cmd}
        )

        data = response.json()

        print("RESPONSE:", data.get("response"))

    except Exception as e:
        print("ERROR:", e)