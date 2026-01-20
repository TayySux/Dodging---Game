import tkinter as tk
import random

# Window setup
WIDTH = 700
HEIGHT = 450
FPS = 60

root = tk.Tk()
root.title("Dodging Game")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0b0f1a")
canvas.pack()

# Game state
game_state = "menu"  # menu | playing

# Game variables
player_size = 40
player_speed = 6
enemy_size = 35
enemy_speed = 4
lives = 3
score = 0
game_over = False
paused = False

# Key states (SMOOTH MOVEMENT)
keys = {"Left": False, "Right": False}

# Background stars
stars = []
for _ in range(90):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    r = random.randint(1, 2)
    stars.append(canvas.create_oval(x, y, x + r, y + r, fill="white", outline=""))

def move_stars():
    for star in stars:
        canvas.move(star, 0, 1)
        if canvas.coords(star)[1] > HEIGHT:
            x = random.randint(0, WIDTH)
            canvas.coords(star, x, 0, x + 2, 2)

# Player
player = canvas.create_rectangle(
    WIDTH // 2 - player_size // 2,
    HEIGHT - 70,
    WIDTH // 2 + player_size // 2,
    HEIGHT - 30,
    fill="#00bfff",
    outline=""
)

# Enemies
enemies = []
for _ in range(3):
    x = random.randint(0, WIDTH - enemy_size)
    enemies.append(
        canvas.create_rectangle(
            x, -enemy_size,
            x + enemy_size, 0,
            fill="#ff4c4c",
            outline=""
        )
    )

# UI
score_text = canvas.create_text(10, 10, anchor="nw", fill="white", font=("Arial", 14, "bold"))
lives_text = canvas.create_text(10, 30, anchor="nw", fill="white", font=("Arial", 14, "bold"))

# Menu UI
canvas.create_text(
    WIDTH // 2, HEIGHT // 2 - 40,
    text="DODGING GAME",
    fill="white",
    font=("Arial", 36, "bold"),
    tags="menu"
)

canvas.create_text(
    WIDTH // 2, HEIGHT // 2 + 20,
    text="Press ENTER to Start",
    fill="white",
    font=("Arial", 16),
    tags="menu"
)

def update_ui():
    canvas.itemconfig(score_text, text=f"Score: {score}")
    canvas.itemconfig(lives_text, text=f"Lives: {lives}")

# Collision
def collision(a, b):
    ax1, ay1, ax2, ay2 = canvas.coords(a)
    bx1, by1, bx2, by2 = canvas.coords(b)
    return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)

def reset_enemy(enemy):
    x = random.randint(0, WIDTH - enemy_size)
    canvas.coords(enemy, x, -enemy_size, x + enemy_size, 0)

def start_game(event=None):
    global game_state
    game_state = "playing"
    canvas.delete("menu")

def restart_game(event=None):
    global lives, score, enemy_speed, game_over
    lives = 3
    score = 0
    enemy_speed = 4
    game_over = False
    canvas.delete("gameover")

    canvas.coords(
        player,
        WIDTH // 2 - player_size // 2,
        HEIGHT - 70,
        WIDTH // 2 + player_size // 2,
        HEIGHT - 30
    )

    for enemy in enemies:
        reset_enemy(enemy)

# Key handling
def key_down(event):
    if event.keysym in keys:
        keys[event.keysym] = True
    if event.keysym == "Return" and game_state == "menu":
        start_game()

def key_up(event):
    if event.keysym in keys:
        keys[event.keysym] = False

# Main game loop
def game_loop():
    global score, lives, enemy_speed

    move_stars()

    if game_state == "playing" and not game_over:

        # SMOOTH MOVEMENT (ONLY CHANGE)
        if keys["Left"]:
            canvas.move(player, -player_speed, 0)
        if keys["Right"]:
            canvas.move(player, player_speed, 0)

        # Keep player in bounds
        x1, _, x2, _ = canvas.coords(player)
        if x1 < 0:
            canvas.move(player, -x1, 0)
        if x2 > WIDTH:
            canvas.move(player, WIDTH - x2, 0)

        # Enemies
        for enemy in enemies:
            canvas.move(enemy, 0, enemy_speed)

            if collision(player, enemy):
                lives -= 1
                reset_enemy(enemy)

                if lives <= 0:
                    canvas.create_text(
                        WIDTH // 2, HEIGHT // 2,
                        text="GAME OVER\nPress R to Restart",
                        fill="white",
                        font=("Arial", 30, "bold"),
                        tags="gameover"
                    )
                    game_over = True
                    return

            if canvas.coords(enemy)[1] > HEIGHT:
                reset_enemy(enemy)
                score += 1
                enemy_speed += 0.2

        update_ui()

    root.after(int(1000 / FPS), game_loop)

# Bindings
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
root.bind("r", restart_game)
root.bind("R", restart_game)

# Start
update_ui()
game_loop()
root.mainloop()
