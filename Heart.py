import tkinter as tk
from math import sin, cos, pi
import random

class HeartFormationAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("Анимация формирования сердечка")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-transparent', 'black')
        self.canvas = tk.Canvas(self.root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.size = min(self.width, self.height) // 40
        self.num_points = 800
        self.points = []
        self.target_points = []
        self.current_step = 0
        self.max_steps = 40
        self.create_random_points()
        self.create_heart_target_points()
        self.create_stars()
        self.animate_chaos()
        self.root.bind('<Escape>', self.close_window)
        self.pulse_step = 0
        self.pulse_direction = 1

    def create_random_points(self):
        for _ in range(self.num_points):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            point = self.canvas.create_oval(x, y, x + 3, y + 3, fill='white', outline='')
            self.points.append((point, x, y))

    def create_heart_target_points(self):
        num_points = self.num_points
        for i in range(num_points):
            angle = 2 * pi * i / num_points
            x = self.size * 16 * (pow(sin(angle), 3))
            y = -self.size * (13 * cos(angle) - 5 * cos(2 * angle) - 2 * cos(3 * angle) - cos(4 * angle))
            x += self.center_x
            y += self.center_y
            self.target_points.append((x, y))

    def create_stars(self):
        for _ in range(200):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(1, 3)
            self.canvas.create_oval(x, y, x + size, y + size, fill='white', outline='')

    def animate_chaos(self):
        if self.current_step < self.max_steps:
            for i, (point, x, y) in enumerate(self.points):
                dx = random.randint(-5, 5)
                dy = random.randint(-5, 5)
                new_x = x + dx
                new_y = y + dy
                self.canvas.move(point, dx, dy)
                self.points[i] = (point, new_x, new_y)
            self.current_step += 1
            self.root.after(50, self.animate_chaos)
        else:
            self.current_step = 0
            self.animate_formation()

    def animate_formation(self):
        if self.current_step < self.max_steps:
            for i, (point, x, y) in enumerate(self.points):
                target_x, target_y = self.target_points[i]
                dx = (target_x - x) / (self.max_steps - self.current_step)
                dy = (target_y - y) / (self.max_steps - self.current_step)
                new_x = x + dx
                new_y = y + dy
                self.canvas.move(point, dx, dy)
                self.points[i] = (point, new_x, new_y)
            self.current_step += 1
            self.root.after(20, self.animate_formation)
        else:
            self.color_gradient_index = 0
            self.blink_heart_gradient()
            self.start_pulse()

    def blink_heart_gradient(self):
        gradient_colors = [
            "#FF0000", "#FF0A4D", "#FF1493", "#FF40B4", "#FF69B4",
            "#FF87C1", "#FFB6C1", "#FF87C1", "#FF69B4", "#FF40B4",
            "#FF1493", "#FF0A4D", "#FF0000"
        ]
        current_color = gradient_colors[self.color_gradient_index % len(gradient_colors)]
        for point, _, _ in self.points:
            self.canvas.itemconfig(point, fill=current_color)
        self.color_gradient_index += 1
        self.root.after(30, self.blink_heart_gradient)

    def start_pulse(self):
        if self.pulse_step < 10:
            scale = 1 + self.pulse_step * 0.02 * self.pulse_direction
            for i, (point, x, y) in enumerate(self.points):
                target_x, target_y = self.target_points[i]
                new_x = self.center_x + (target_x - self.center_x) * scale
                new_y = self.center_y + (target_y - self.center_y) * scale
                self.canvas.coords(point, new_x, new_y, new_x + 3, new_y + 3)
            self.pulse_step += 1
            self.root.after(50, self.start_pulse)
        else:
            self.pulse_direction *= -1
            self.pulse_step = 0
            self.root.after(50, self.start_pulse)

    def close_window(self, event=None):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HeartFormationAnimation(root)
    root.mainloop()
