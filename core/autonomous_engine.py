import psutil
import time


class AutonomousEngine:

    def __init__(self):
        self.last_action_time = 0
        self.cooldown = 60  # seconds between actions

    def evaluate(self):

        now = time.time()

        # Prevent spam
        if now - self.last_action_time < self.cooldown:
            return None

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        # 1️⃣ Critical CPU
        if cpu > 95:
            self.last_action_time = now
            return {
                "type": "alert",
                "message": "CPU usage extremely high. Consider closing heavy applications."
            }

        # 2️⃣ Critical RAM
        if ram > 95:
            self.last_action_time = now
            return {
                "type": "alert",
                "message": "RAM usage extremely high. System may slow down."
            }

        return None