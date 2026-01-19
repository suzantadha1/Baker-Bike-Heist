# projectile_manager.py
import turtle
import math

# ================================
# GLOBAL STATE
# ================================
PROJECTILES = []
PROJECTILE_FRAMES = {}

FPS = 60
FRAME_TIME = int(1000 / FPS)


# ================================
# FRAME REGISTRATION
# ================================
def register_frames(name, frames):
    """Register animation frames for a projectile category."""
    PROJECTILE_FRAMES[name] = frames


# ================================
# REQUIRED BY STAGE 4
# ================================
def projectile_manager_add(p):
    """Add projectile (compat name)."""
    PROJECTILES.append(p)


def projectile_manager_clear():
    """Clear everything — used on stage load."""
    for p in PROJECTILES:
        try:
            p["turtle"].hideturtle()
        except:
            pass
    PROJECTILES.clear()


# ================================
# LEGACY SUPPORT (OPTIONAL)
# ================================
# Your old function name still works
add_projectile = projectile_manager_add


# ================================
# MAIN UPDATE LOOP
# ================================
def update_all(screen, game_state):
    """Updates animation + collisions for all projectiles."""

    if game_state.get("game_over", False):
        projectile_manager_clear()
        return

    remove_list = []

    for p in PROJECTILES:
        t = p["turtle"]

        # ---- Animation ----
        frames = PROJECTILE_FRAMES[p["frame_key"]]
        p["frame_i"] = (p["frame_i"] + 1) % len(frames)
        t.shape(frames[p["frame_i"]])

        # ---- Movement ----
        t.goto(t.xcor() + p["vx"], t.ycor() + p["vy"])

        # ---- Hit Detection ----
        target = p.get("target")
        if target and t.distance(target) < 25:
            if p["on_hit"]:
                p["on_hit"]()
            remove_list.append(p)
            continue

        # ---- Lifetime ----
        p["life"] -= 1
        if p["life"] <= 0:
            remove_list.append(p)
            continue

        # ---- Offscreen ----
        if abs(t.xcor()) > 700 or abs(t.ycor()) > 500:
            remove_list.append(p)
            continue

    # ---- Cleanup ----
    for p in remove_list:
        try:
            p["turtle"].hideturtle()
        except:
            pass
        if p in PROJECTILES:
            PROJECTILES.remove(p)

    # Schedule next update
    screen.ontimer(lambda: update_all(screen, game_state), FRAME_TIME)


# ================================
# ENTRY POINT CALLED AT STAGE START
# ================================
def start_projectile_manager(screen, game_state):
    """Starts the 40 FPS update loop."""
    update_all(screen, game_state)