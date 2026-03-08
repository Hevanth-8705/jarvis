import os
import sys
import threading
import time
import keyboard
import queue
from dotenv import load_dotenv

from PyQt6.QtWidgets import QApplication
from gui.app import JarvisGUI

from core.voice import speak, listen
from core.wake_word import WakeWordDetector
from core.engine import JarvisEngine
from core.intent_router import IntentRouter
from core.skill_executor import SkillExecutor
from core.memory_store import MemoryStore
from core.langchain_planner import LangChainPlanner
from core.plugin_loader import PluginLoader
from core.vector_memory import VectorMemory
from core.graph_planner import GraphPlanner
from core.autonomous_engine import AutonomousEngine


# ===============================
# LOAD ENVIRONMENT
# ===============================

load_dotenv()

if not os.getenv("PORCUPINE_ACCESS_KEY"):
    print("PORCUPINE_ACCESS_KEY missing.")
    sys.exit(1)


# ===============================
# GLOBAL STATE
# ===============================

task_queue = queue.Queue()
last_monitor_alert = 0


# ===============================
# TASK WORKER
# ===============================

def task_worker():

    while True:

        task = task_queue.get()

        if task is None:
            break

        try:
            task()

        except Exception as e:
            print("Task error:", e)

        finally:
            task_queue.task_done()


# ===============================
# COMPLEX QUERY DETECTOR
# ===============================

def is_complex_query(command: str):

    keywords = [
        "if", "when", "after", "before",
        "analyze", "compare", "summarize",
        "plan", "evaluate", "strategy",
        "explain deeply"
    ]

    return any(word in command.lower() for word in keywords)


# ===============================
# AUTONOMOUS BACKGROUND MONITOR
# ===============================

def autonomous_monitor(gui, shutdown_event, vector_memory):

    auto_engine = AutonomousEngine()

    while not shutdown_event.is_set():

        decision = auto_engine.evaluate()

        if decision:

            if decision["type"] == "alert":

                speak(decision["message"])
                gui.output_signal.emit("Autonomous", decision["message"])

                vector_memory.add("Autonomous Decision")
                vector_memory.add(decision["message"])

        time.sleep(5)


# ===============================
# JARVIS MAIN LOOP
# ===============================

def jarvis_loop(gui, shutdown_event, executor, vector_memory):

    wake = WakeWordDetector(os.getenv("PORCUPINE_ACCESS_KEY"))

    router = IntentRouter()
    engine = JarvisEngine()
    memory = MemoryStore()
    planner = LangChainPlanner()
    plugins = PluginLoader()
    graph_planner = GraphPlanner(planner)

    print("JARVIS SYSTEM ACTIVE")

    gui.status_signal.emit("Waiting for wake word...")

    while True:

        if shutdown_event.is_set():
            break

        try:

            # ESC = force shutdown
            if keyboard.is_pressed("esc"):
                shutdown_event.set()
                break

            # Wake word or manual trigger
            detected = False

            try:
                detected = keyboard.is_pressed("F9") or wake.listen(shutdown_event)
            except:
                detected = False

            if not detected:
                time.sleep(0.2)
                continue

            wake.pause()

            gui.status_signal.emit("Listening...")

            speak("Yes?")

            time.sleep(0.5)

            command = listen()

            if not command or command == "none":
                wake.resume()
                gui.status_signal.emit("Waiting for wake word...")
                continue

            if command.lower() in ["exit", "quit", "stop assistant"]:
                shutdown_event.set()
                break

            gui.status_signal.emit("Processing...")

            def execute_single():

                try:
                    memory.track_command(command)
                except:
                    pass

                plugin_response = plugins.handle(command)

                if plugin_response:

                    speak(plugin_response)
                    gui.output_signal.emit(command, plugin_response)

                    vector_memory.add(f"User: {command}")
                    vector_memory.add(f"Assistant: {plugin_response}")

                    return

                intent = router.route(command)

                response = executor.execute(intent)

                if not response and is_complex_query(command):

                    gui.status_signal.emit("Planning...")

                    steps = graph_planner.generate_plan(command)

                    if not steps:
                        response = planner.plan(command)

                    else:

                        results = []

                        for step in steps:

                            try:

                                step_intent = router.route(step)
                                step_result = executor.execute(step_intent)

                                if not step_result:
                                    step_result = engine.handle(step)

                                results.append(step_result)

                                vector_memory.add(f"Step: {step}")
                                vector_memory.add(f"Result: {step_result}")

                            except Exception:
                                results.append("Step failed")

                        response = "\n".join(results)

                if not response:
                    response = engine.handle(command)

                vector_memory.add(f"User: {command}")
                vector_memory.add(f"Assistant: {response}")

                speak(response)

                gui.output_signal.emit(command, response)

            task_queue.put(execute_single)

            task_queue.join()

            gui.status_signal.emit("Waiting for wake word...")

            wake.resume()

        except Exception as e:

            print("Loop error:", e)

            time.sleep(1)

    wake.shutdown()

    print("Assistant stopped cleanly.")


# ===============================
# MAIN
# ===============================

def main():

    app = QApplication(sys.argv)

    gui = JarvisGUI()

    gui.show()

    shutdown_event = threading.Event()

    executor = SkillExecutor()

    vector_memory = VectorMemory()

    worker_thread = threading.Thread(
        target=task_worker,
        daemon=True
    )

    worker_thread.start()

    assistant_thread = threading.Thread(
        target=jarvis_loop,
        args=(gui, shutdown_event, executor, vector_memory),
        daemon=False
    )

    assistant_thread.start()

    autonomous_thread = threading.Thread(
        target=autonomous_monitor,
        args=(gui, shutdown_event, vector_memory),
        daemon=True
    )

    autonomous_thread.start()

    def on_exit():

        shutdown_event.set()

        task_queue.put(None)

        assistant_thread.join()

        worker_thread.join()

    app.aboutToQuit.connect(on_exit)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()