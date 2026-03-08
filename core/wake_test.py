# wake_test.py

import os
from dotenv import load_dotenv
from core.wake_word import WakeWordDetector

load_dotenv()

access_key = os.getenv("PORCUPINE_ACCESS_KEY")

if not access_key:
    print("PORCUPINE_ACCESS_KEY missing.")
    exit()

wake = WakeWordDetector(access_key)

print("Say 'Jarvis'...")

wake.listen()

wake.stop()

print("Wake test finished.")