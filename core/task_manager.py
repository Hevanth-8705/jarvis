import threading
import time
import psutil


class TaskManager:

    def __init__(self, speak):
        self.speak = speak
        self.running_tasks = {}

    def reminder(self, seconds, message):
        def task():
            time.sleep(seconds)
            self.speak(f"Reminder: {message}")

        t = threading.Thread(target=task, daemon=True)
        t.start()
        self.running_tasks["reminder"] = t

    def monitor_cpu(self, threshold=80):
        def task():
            self.speak("CPU monitoring started.")
            while True:
                cpu = psutil.cpu_percent(interval=5)
                if cpu > threshold:
                    self.speak(f"Warning. CPU usage is {cpu} percent.")

        t = threading.Thread(target=task, daemon=True)
        t.start()
        self.running_tasks["cpu"] = t
