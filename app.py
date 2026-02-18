import tkinter as tk
import random
import pygame

# ================= SETTINGS =================
WIDTH = 900
HEIGHT = 450
GROUND = 380
GRAVITY = 1
JUMP_POWER = -18
GAME_SPEED = 6  # initial speed

class SkyDashRunner:
    def __init__(self, root):
        self.root = root
        self.root.title("SkyDash Runner - Made with ❤️ by Ritesh Verma")
        self.root.resizable(False, False)

        # Canvas
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack()

        # Pygame mixer for music
        pygame.mixer.init()
        self.music_loaded = False
        try:
            pygame.mixer.music.load("music.mp3")
            self.music_loaded = True
        except:
            print("Music file 'music.mp3' not found!")

        # Start screen
        self.running = False
        self.show_start_screen()

    # ================= GRADIENT BACKGROUND =================
    def draw_gradient(self, color1, color2):
        self.canvas.delete("gradient")
        r1, g1, b1 = self.root.winfo_rgb(color1)
        r2, g2, b2 = self.root.winfo_rgb(color2)

        r_ratio = (r2 - r1) / HEIGHT
        g_ratio = (g2 - g1) / HEIGHT
        b_ratio = (b2 - b1) / HEIGHT

        for i in range(HEIGHT):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
            self.canvas.create_line(0, i, WIDTH, i, tags=("gradient",), fill=color)

    # ================= START SCREEN =================
    def show_start_screen(self):
        self.running = False
        self.canvas.delete("all")
        self.draw_gradient("#4facfe", "#00f2fe")

        self.canvas.create_text(WIDTH//2, 120,
                                text="SKYDASH RUNNER",
                                font=("Helvetica", 48, "bold"),
                                fill="white")

        self.canvas.create_text(WIDTH//2, 190,
                                text="Press SPACE to Jump",
                                font=("Arial", 20),
                                fill="black")

        # Buttons
        self.create_button("PLAY GAME", WIDTH//2, 260, self.start_game, "#00c853")
        self.create_button("CREDITS", WIDTH//2, 320, self.show_credits, "#2962ff")

    # ================= CUSTOM BUTTON =================
    def create_button(self, text, x, y, command, color):
        btn = tk.Button(self.root,
                        text=text,
                        font=("Arial", 16, "bold"),
                        bg=color,
                        fg="white",
                        activebackground="black",
                        activeforeground="white",
                        relief="flat",
                        bd=0,
                        padx=20,
                        pady=10,
                        command=command)
        self.canvas.create_window(x, y, window=btn)

    # ================= CREDITS =================
    def show_credits(self):
        self.canvas.delete("all")
        self.draw_gradient("#ff9a9e", "#fad0c4")

        self.canvas.create_text(WIDTH//2, 150,
                                text="CREDITS",
                                font=("Helvetica", 42, "bold"),
                                fill="white")

        self.canvas.create_text(WIDTH//2, 220,
                                text="Game Developed By",
                                font=("Arial", 20),
                                fill="black")

        self.canvas.create_text(WIDTH//2, 260,
                                text="Ritesh Verma",
                                font=("Comic Sans MS", 24, "bold"),
                                fill="purple")

        self.create_button("BACK", WIDTH//2, 330, self.show_start_screen, "#ff1744")

    # ================= GAME BACKGROUND =================
    def draw_game_background(self):
        self.draw_gradient("#87CEEB", "#b0e0ff")
        self.canvas.create_rectangle(0, GROUND, WIDTH, HEIGHT,
                                     fill="#2e7d32", outline="")
        # Clouds
        for i in range(5):
            x = random.randint(0, WIDTH)
            y = random.randint(50, 200)
            self.canvas.create_oval(x, y, x+60, y+40, fill="white", outline="")
            self.canvas.create_oval(x+20, y-20, x+80, y+40, fill="white", outline="")

    # ================= START GAME =================
    def start_game(self):
        global GAME_SPEED
        GAME_SPEED = 6  # reset speed
        self.canvas.delete("all")
        self.running = True
        self.score = 0
        self.jump_velocity = 0
        self.obstacles = []

        self.draw_game_background()

        # Character: triangle + legs
        self.player_body = self.canvas.create_polygon(
            150, GROUND-60, 190, GROUND-60, 170, GROUND-100,
            fill="yellow", outline="black", width=2
        )
        self.leg_left = self.canvas.create_line(160, GROUND-60, 160, GROUND-50, width=3)
        self.leg_right = self.canvas.create_line(180, GROUND-60, 180, GROUND-50, width=3)

        self.score_text = self.canvas.create_text(
            WIDTH-150, 40,
            text="Score: 0  Speed: 6",
            font=("Arial", 20, "bold"),
            fill="black"
        )

        self.root.bind("<space>", self.jump)

        # Start background music
        if self.music_loaded:
            pygame.mixer.music.play(-1)  # loop music
            pygame.mixer.music.set_volume(0.2)  # 20% volume

        self.spawn_obstacle()
        self.update_game()

    # ================= JUMP =================
    def jump(self, event):
        if self.running:
            coords = self.canvas.coords(self.player_body)
            y_max = max(coords[1], coords[3], coords[5])
            if y_max >= GROUND:
                self.jump_velocity = JUMP_POWER

    # ================= SPAWN OBSTACLE =================
    def spawn_obstacle(self):
        if not self.running:
            return

        obstacle_type = random.choice(["barrier", "bird"])
        if obstacle_type == "barrier":
            obstacle = self.canvas.create_rectangle(
                WIDTH, GROUND-50,
                WIDTH+40, GROUND,
                fill="red",
                outline="black",
                width=2
            )
        else:
            y = random.randint(250, 320)
            obstacle = self.canvas.create_oval(
                WIDTH, y,
                WIDTH+40, y+30,
                fill="purple",
                outline="black",
                width=2
            )

        self.obstacles.append(obstacle)
        self.root.after(random.randint(1500, 2500), self.spawn_obstacle)

    # ================= GAME LOOP =================
    def update_game(self):
        global GAME_SPEED
        if not self.running:
            return

        # Gravity and move character
        self.jump_velocity += GRAVITY
        self.canvas.move(self.player_body, 0, self.jump_velocity)
        self.canvas.move(self.leg_left, 0, self.jump_velocity)
        self.canvas.move(self.leg_right, 0, self.jump_velocity)

        coords = self.canvas.coords(self.player_body)
        y_max = max(coords[1], coords[3], coords[5])
        if y_max >= GROUND:
            diff = GROUND - y_max
            self.canvas.move(self.player_body, 0, diff)
            self.canvas.move(self.leg_left, 0, diff)
            self.canvas.move(self.leg_right, 0, diff)
            self.jump_velocity = 0

        # Move obstacles
        for obstacle in self.obstacles:
            self.canvas.move(obstacle, -GAME_SPEED, 0)
            if self.check_collision(self.player_body, obstacle):
                self.game_over()
                return

        self.obstacles = [obs for obs in self.obstacles if self.canvas.coords(obs)[2] > 0]

        # Score & Speed increase every 500 meters
        self.score += 1
        if self.score % 500 == 0:
            GAME_SPEED += 1

        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}  Speed: {GAME_SPEED}")

        self.root.after(30, self.update_game)

    # ================= COLLISION =================
    def check_collision(self, player, obstacle):
        p = self.canvas.bbox(player)
        o = self.canvas.bbox(obstacle)
        return not (p[2] < o[0] or p[0] > o[2] or p[3] < o[1] or p[1] > o[3])

    # ================= GAME OVER =================
    def game_over(self):
        self.running = False
        self.root.unbind("<space>")
        self.canvas.delete("all")

        # Stop music
        if self.music_loaded:
            pygame.mixer.music.stop()

        self.draw_gradient("#ff512f", "#dd2476")

        self.canvas.create_text(WIDTH//2, 150,
                                text="GAME OVER",
                                font=("Helvetica", 48, "bold"),
                                fill="white")

        self.canvas.create_text(WIDTH//2, 220,
                                text=f"Final Score: {self.score}",
                                font=("Arial", 22),
                                fill="black")

        self.create_button("PLAY AGAIN", WIDTH//2, 290, self.start_game, "#00c853")
        self.create_button("MAIN MENU", WIDTH//2, 350, self.show_start_screen, "#2962ff")


# ================= RUN GAME =================
root = tk.Tk()
game = SkyDashRunner(root)
root.mainloop()
