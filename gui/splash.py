import tkinter as tk
from PIL import Image, ImageTk
import time

class SplashScreen:

    def __init__(self, gif_path, duration=4):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.configure(bg="black")

        self.duration = duration
        self.label = tk.Label(self.root, bg="black")
        self.label.pack()

        self.frames = []
        self.load_gif(gif_path)

        self.center_window(700, 700)

    def load_gif(self, path):
        gif = Image.open(path)
        try:
            while True:
                frame = ImageTk.PhotoImage(gif.copy())
                self.frames.append(frame)
                gif.seek(len(self.frames))
        except EOFError:
            pass

    def animate(self, index=0):
        frame = self.frames[index]
        self.label.configure(image=frame)
        index = (index + 1) % len(self.frames)
        self.root.after(40, self.animate, index)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show(self):
        self.animate()
        self.root.after(self.duration * 1000, self.root.destroy)
        self.root.mainloop()
