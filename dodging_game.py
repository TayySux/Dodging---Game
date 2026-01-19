import tkinter as tk
import random

# Window setup
WIDTH = 700
HEIGHT = 450

root = tk.Tk()
root.title("Dodging Game")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0b0f1a")
canvas.pack()

# Game variables
player_size = 40
player_speed = 25
enemy_size = 35
enemy_speed = 4
lives = 3
score = 0
game_over = False

# Background (stars)
stars = []
for _ in range(90):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    r = random.randint(1, 2)
    star = canvas.create_oval(
        x, y, x + r, y + r,
        fill="white", outline=""
    )
    stars.append(star)

def move_stars():
    for star in stars:
        canvas.move(star, 0, 1)
        _, y1, _, y2 = canvas.coords(star)
        if y1 > HEIGHT:
            x = random.randint(0, WIDTH)
            canvas.coords(star, x, 0, x + 2, 2)
    root.after(50, move_stars)

# Player
player = canvas.create_rectangle(
    WIDTH // 2 - player_size // 2,
    HEIGHT - 70,
    WIDTH // 2 + player_size // 2,
    HEIGHT - 30,
    fill="#00bfff", outline=""
)

# Enemies
enemies = []
for _ in range(3):
    x = random.randint(0, WIDTH - enemy_size)
    enemy = canvas.create_rectangle(
        x, -enemy_size,
        x + enemy_size, 0,
        fill="#ff4c4c", outline=""
    )
    enemies.append(enemy)

# UI
score_text = canvas.create_text(
    10, 10, anchor="nw",
    font=("Arial", 14, "bold"),
    fill="white"
)
lives_text = canvas.create_text(
    10, 30, anchor="nw",
    font=("Arial", 14, "bold"),
    fill="white"
)

def update_ui():
    canvas.itemconfig(score_text, text=f"Score: {score}")
    canvas.itemconfig(lives_text, text=f"Lives: {lives}")

# Controls
def move_left(event):
    x1, _, _, _ = canvas.coords(player)
    if x1 > 0:
        canvas.move(player, -player_speed, 0)

def move_right(event):
    _, _, x2, _ = canvas.coords(player)
    if x2 < WIDTH:
        canvas.move(player, player_speed, 0)

# Game logic
def collision(a, b):
    ax1, ay1, ax2, ay2 = canvas.coords(a)
    bx1, by1, bx2, by2 = canvas.coords(b)
    return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)

def reset_enemy(enemy):
    x = random.randint(0, WIDTH - enemy_size)
    canvas.coords(enemy, x, -enemy_size, x + enemy_size, 0)

def restart_game(event=None):
    global lives, score, enemy_speed, game_over
    lives = 4
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

    update_game()

def update_game():
    global score, lives, enemy_speed, game_over

    if game_over:
        return

    for enemy in enemies:
        canvas.move(enemy, 0, enemy_speed)

        if collision(player, enemy):
            lives -= 1
            reset_enemy(enemy)

            if lives <= 0:
                canvas.create_text(
                    WIDTH // 2, HEIGHT // 2,
                    text="GAME OVER\nPress R to Restart",
                    font=("Arial", 30, "bold"),
                    fill="white",
                    tags="gameover"
                )
                game_over = True
                return

        _, y1, _, _ = canvas.coords(enemy)
        if y1 > HEIGHT:
            reset_enemy(enemy)
            score += 1
            enemy_speed += 0.2

    update_ui()
    root.after(30, update_game)

# Key bindings
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("r", restart_game)
root.bind("R", restart_game)

# Start game
update_ui()
move_stars()
update_game()
root.mainloop()
