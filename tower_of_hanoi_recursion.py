import tkinter as tk
from tkinter import messagebox
import random

class TowerOfHanoiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi Animation")

        self.num_disks = 0
        self.pegs = {'A': [], 'B': [], 'C': []}
        self.disk_values = []
        self.disk_colors = []
        self.disk_order = []
        self.animation_index = 0
        self.moving_disk = None
        self.moving_text = None
        self.phase = None
        self.animation_speed = 20  # default average
        self.speed_up_speed = 1    # SPEED UP speed (very fast)
        self.average_speed = 20    # AVERAGE speed

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        # Input frame
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10, fill="x")

        # Left: number of plates
        left_frame = tk.Frame(self.input_frame)
        left_frame.pack(side="left", padx=20)
        tk.Label(left_frame, text="Number of plates (1-8):").pack(side="left")
        self.disk_entry = tk.Entry(left_frame, width=5)
        self.disk_entry.pack(side="left")

        # Center: START (blue) and RESET (red) buttons together
        center_frame = tk.Frame(self.input_frame)
        center_frame.pack(side="left", expand=True)

        self.start_btn = tk.Button(center_frame, text="START", width=10, bg="blue", fg="white", command=self.start_simulation)
        self.start_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(center_frame, text="RESET", width=10, bg="red", fg="white", command=self.reset_simulation)
        self.reset_btn.pack(side="left", padx=5)

        # Right: SPEED UP / AVERAGE buttons
        right_frame = tk.Frame(self.input_frame)
        right_frame.pack(side="right", padx=20)
        tk.Button(right_frame, text="SPEED UP", width=8, command=self.set_speed_up).pack(side="left", padx=5)
        tk.Button(right_frame, text="AVERAGE", width=8, command=self.set_average).pack(side="left", padx=5)

        self.peg_positions = {'A': 150, 'B': 300, 'C': 450}
        self.disk_height = 20

    def set_speed_up(self):
        self.animation_speed = self.speed_up_speed

    def set_average(self):
        self.animation_speed = self.average_speed

    def draw_pegs(self):
        self.canvas.delete("peg")
        for x in self.peg_positions.values():
            self.canvas.create_rectangle(x-5, 100, x+5, 300, fill="brown", tags="peg")

    def draw_disks(self, exclude_disk=None):
        self.canvas.delete("disk")
        for peg, disks in self.pegs.items():
            x_center = self.peg_positions[peg]
            for i, disk_index in enumerate(disks):
                if disk_index == exclude_disk:
                    continue
                max_width = 140
                min_width = 40
                step = (max_width - min_width) / (self.num_disks - 1) if self.num_disks > 1 else 0
                width = min_width + step * (disk_index-1)
                y = 300 - i*self.disk_height
                color = self.disk_colors[disk_index-1]
                self.canvas.create_rectangle(x_center-width//2, y-self.disk_height, x_center+width//2, y,
                                             fill=color, tags="disk")
                self.canvas.create_text(x_center, y - self.disk_height/2, text=str(self.disk_values[disk_index-1]),
                                        fill="white", font=("Arial", 12, "bold"), tags="disk")

    def solve_hanoi(self, n, source, aux, target):
        if n == 1:
            self.disk_order.append((source, target))
        else:
            self.solve_hanoi(n-1, source, target, aux)
            self.disk_order.append((source, target))
            self.solve_hanoi(n-1, aux, source, target)

    def animate_move(self):
        if self.animation_index >= len(self.disk_order):
            self.start_btn.config(state=tk.NORMAL)  # Re-enable start after finish
            return

        if self.moving_disk is None:
            source, target = self.disk_order[self.animation_index]
            self.disk = self.pegs[source].pop()
            max_width = 140
            min_width = 40
            step_width = (max_width - min_width) / (self.num_disks - 1) if self.num_disks > 1 else 0
            self.width = min_width + step_width * (self.disk-1)
            self.value = self.disk_values[self.disk-1]
            self.color = self.disk_colors[self.disk-1]

            self.start_x = self.peg_positions[source]
            self.start_y = 300 - len(self.pegs[source])*self.disk_height
            self.end_x = self.peg_positions[target]
            self.end_y = 300 - (len(self.pegs[target])+1)*self.disk_height
            self.current_x = self.start_x
            self.current_y = self.start_y

            self.phase = "up"

            self.moving_disk = self.canvas.create_rectangle(self.current_x-self.width//2,
                                                            self.current_y-self.disk_height,
                                                            self.current_x+self.width//2,
                                                            self.current_y,
                                                            fill=self.color)
            self.moving_text = self.canvas.create_text(self.current_x,
                                                       self.current_y - self.disk_height/2,
                                                       text=str(self.value),
                                                       fill="white", font=("Arial", 12, "bold"))

        step_pixels = 5
        if self.phase == "up":
            if self.current_y > 80:
                self.current_y -= step_pixels
            else:
                self.current_y = 80
                self.phase = "horizontal"
        elif self.phase == "horizontal":
            if abs(self.current_x - self.end_x) > step_pixels:
                self.current_x += step_pixels if self.end_x > self.current_x else -step_pixels
            else:
                self.current_x = self.end_x
                self.phase = "down"
        elif self.phase == "down":
            if self.current_y < self.end_y:
                self.current_y += step_pixels
            else:
                self.current_y = self.end_y
                self.canvas.delete(self.moving_disk)
                self.canvas.delete(self.moving_text)
                self.pegs[self.disk_order[self.animation_index][1]].append(self.disk)
                self.draw_disks()
                self.moving_disk = None
                self.animation_index += 1

        if self.moving_disk:
            self.canvas.coords(self.moving_disk,
                               self.current_x-self.width//2,
                               self.current_y-self.disk_height,
                               self.current_x+self.width//2,
                               self.current_y)
            self.canvas.coords(self.moving_text,
                               self.current_x,
                               self.current_y - self.disk_height/2)

        # Always use current animation_speed
        self.root.after(self.animation_speed, self.animate_move)

    def start_simulation(self):
        try:
            num = int(self.disk_entry.get())
            if 1 <= num <= 8:
                self.num_disks = num
                random_values = random.sample(range(10, 99), num)
                self.disk_values = sorted(random_values)
                base_colors = ['red','orange','yellow','green','blue','purple','black','gray']
                self.disk_colors = base_colors[:num]
                self.pegs = {'A': list(range(num,0,-1)), 'B': [], 'C': []}
                self.draw_pegs()
                self.draw_disks()
                self.disk_order = []
                self.animation_index = 0
                self.moving_disk = None
                self.start_btn.config(state=tk.DISABLED)  # Disable start
                self.disk_entry.config(state=tk.DISABLED)
                self.solve_hanoi(self.num_disks, 'A', 'B', 'C')
                self.root.after(self.animation_speed, self.animate_move)
            else:
                messagebox.showerror("Error", "Enter a number between 1 and 8")
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Enter a number.")

    def reset_simulation(self):
        # Clear canvas and reset everything
        self.canvas.delete("all")
        self.pegs = {'A': [], 'B': [], 'C': []}
        self.disk_values = []
        self.disk_colors = []
        self.disk_order = []
        self.animation_index = 0
        self.moving_disk = None
        self.moving_text = None
        self.phase = None
        self.start_btn.config(state=tk.NORMAL)  # Enable start button
        self.disk_entry.config(state=tk.NORMAL)
        self.disk_entry.delete(0, tk.END)

root = tk.Tk()
app = TowerOfHanoiGUI(root)
root.mainloop()
