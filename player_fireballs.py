# player_fireballs.py — LAG-FREE VERSION
import turtle
import math
import os


# ---------------------------------------------------------
#  LOAD SHAPES WITHOUT RE-REGISTERING (main loads all GIFs)
# ---------------------------------------------------------
def load_player_fireball_shapes(screen):
    """
    Returns {"pink": [...], "blue": [...]} without re-registering shapes.
    """
    frames = {"pink": [], "blue": []}

    # Pink frames
    for i in range(1, 6):
        path = f"fireball/pink_fireball_{i}.gif"
        if os.path.exists(path):
            frames["pink"].append(path)

    # Blue frames
    for i in range(1, 6):
        path = f"fireball/blue_fireball_{i}.gif"
        if os.path.exists(path):
            frames["blue"].append(path)

    return frames


# ---------------------------------------------------------
#  PLAYER FIREBALL — smooth, no leaks
# ---------------------------------------------------------
def spawn_player_fireball(screen, player, boss, frames, on_hit=None):

    if not frames:
        frames = ["prof_final.gif"]  # fallback

    fb = turtle.Turtle()
    fb.hideturtle()
    fb.penup()
    fb.speed(0)
    fb.shape(frames[0])
    fb.goto(player.xcor(), player.ycor())
    fb.showturtle()

    step = 22
    frame_i = 0
    alive = True

    # -----------------------------------------------------
    #  DESTROY TURTLE PROPERLY (no lingering objects)
    # -----------------------------------------------------
    def destroy():
        nonlocal alive
        alive = False
        fb.hideturtle()
        fb.clear()
        try:
            fb._destroy()
        except:
            pass

    # -----------------------------------------------------
    #  MOVEMENT & ANIMATION LOOP
    # -----------------------------------------------------
    def move():
        nonlocal frame_i, alive

        if not alive:
            return

        # Animate
        fb.shape(frames[frame_i])
        frame_i = (frame_i + 1) % len(frames)

        # Aim toward boss CURRENT position
        bx, by = boss.xcor(), boss.ycor()
        angle = math.atan2(by - fb.ycor(), bx - fb.xcor())

        nx = fb.xcor() + step * math.cos(angle)
        ny = fb.ycor() + step * math.sin(angle)
        fb.goto(nx, ny)

        # HIT BOSS
        if fb.distance(boss) < 25:
            destroy()
            if on_hit:
                on_hit()
            return

        # OFF SCREEN
        if abs(nx) > 520 or abs(ny) > 320:
            destroy()
            return

        screen.ontimer(move, 30)

    move()