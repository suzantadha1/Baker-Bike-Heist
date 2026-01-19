# boss_fireball.py — LAG-FREE VERSION
import turtle
import math
from player import update_healthbars


# ---------------------------------------------------------
#  DO NOT REGISTER SHAPES HERE — main already handles it
# ---------------------------------------------------------
def load_fireball_shapes(screen):
    """
    Returns list of fireball frame paths WITHOUT re-registering.
    """
    frames = []

    for i in range(1, 6):
        path = f"fireball/fireball_{i}.gif"
        # Only append — shapes are already preloaded by main
        if path:
            frames.append(path)

    if not frames:
        frames = ["fireball/fireball_1.gif"]

    return frames


# ---------------------------------------------------------
#  FIREBALL SPAWNER — smooth, no leaks, no lag
# ---------------------------------------------------------
def spawn_boss_fireball(boss, target, frames,
                        game_state, p1, p2, p1_bar, p2_bar):
    """
    Creates and animates a boss fireball while minimizing lag.
    """

    fb = turtle.Turtle()
    fb.hideturtle()
    fb.penup()
    fb.speed(0)

    # First frame (no registration needed)
    fb.shape(frames[0])
    fb.goto(boss.xcor(), boss.ycor())
    fb.showturtle()

    frame_i = 0
    alive = True
    step = 14

    # snapshot target position (aim where the player WAS)
    tx, ty = target.xcor(), target.ycor()
    angle = math.atan2(ty - boss.ycor(), tx - boss.xcor())
    vx = step * math.cos(angle)
    vy = step * math.sin(angle)

    # -----------------------------------------------------
    #  DAMAGE
    # -----------------------------------------------------
    def on_hit():
        if target == p1:
            game_state["p1_health"] = max(0, game_state["p1_health"] - 10)
        else:
            game_state["p2_health"] = max(0, game_state["p2_health"] - 10)

        update_healthbars(game_state, p1_bar, p2_bar)

    # -----------------------------------------------------
    #  DESTROY TURTLE CLEANLY (important!)
    # -----------------------------------------------------
    def destroy():
        nonlocal alive
        alive = False
        fb.hideturtle()
        fb.clear()
        try:
            fb._destroy()  # hard remove from screen/turtle list
        except:
            pass

    # -----------------------------------------------------
    #  FIREBALL MOVEMENT + ANIMATION
    # -----------------------------------------------------
    def move():
        nonlocal frame_i, alive

        if not alive:
            return

        # animate
        fb.shape(frames[frame_i])
        frame_i = (frame_i + 1) % len(frames)

        # move step
        nx = fb.xcor() + vx
        ny = fb.ycor() + vy
        fb.goto(nx, ny)

        # HIT PLAYER
        if fb.distance(target) < 25:
            destroy()
            on_hit()
            return

        # OFF SCREEN
        if abs(nx) > 600 or abs(ny) > 400:
            destroy()
            return

        # continue animation
        fb.getscreen().ontimer(move, 30)

    move()