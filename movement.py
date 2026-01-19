"""
Unified movement for ALL stages.
Handles boundaries, invisibility, sprite facing, and keybindings.
Stages only call:
    bind_player_controls(screen, p1, p2, game_state, extra_callback=None)
"""

import sys
sys.path.append('/usercode')

from collision import is_blocked

# Optional modules — safe fallback if not used in this stage
try:
    import notes
except:
    notes = None

try:
    import invisibility
except:
    invisibility = None


# ===== WORLD BOUNDS =====
HALF_W = 480
HALF_H = 270
MARGIN = 32

MIN_X = -HALF_W + MARGIN
MAX_X = HALF_W - MARGIN
MIN_Y = -HALF_H + MARGIN
MAX_Y = HALF_H - MARGIN


# ===================================================
# DIRECTION + SPRITES
# ===================================================

def update_sprite_direction(t, direction):
    """
    Updates the player's sprite and facing direction.
    If the player has invisibility mode, defer to invisibility handler.
    """
    t.facing = direction

    # invisibility stage handling
    if invisibility and hasattr(t, "is_invisible"):
        invisibility.update_player_direction(t, direction)
        return

    # normal sprite logic
    if direction == "back":
        t.shape(t.back)
    elif direction == "front":
        t.shape(t.front)
    elif direction == "left":
        t.shape(t.left_img)
    elif direction == "right":
        t.shape(t.right_img)


# ===================================================
# MOVEMENT HELPERS
# ===================================================

def allow_move(x, y):
    """Checks walls, notes restriction, and returns True/False."""
    if notes and not notes.can_move(x, y):
        return False
    if is_blocked(x, y):
        return False
    return True


def handle_invisibility_pickup(t):
    """Safe wrapper for invisibility drink pickup."""
    if invisibility:
        invisibility.check_drink_pickup(t)


# ===================================================
# MOVE FUNCTIONS
# ===================================================

def move_up(t, speed):
    update_sprite_direction(t, "back")
    nx, ny = t.xcor(), t.ycor() + speed
    if ny <= MAX_Y and allow_move(nx, ny):
        t.sety(ny)
        handle_invisibility_pickup(t)


def move_down(t, speed):
    update_sprite_direction(t, "front")
    nx, ny = t.xcor(), t.ycor() - speed
    if ny >= MIN_Y and allow_move(nx, ny):
        t.sety(ny)
        handle_invisibility_pickup(t)


def move_left(t, speed):
    update_sprite_direction(t, "left")
    nx, ny = t.xcor() - speed, t.ycor()
    if nx >= MIN_X and allow_move(nx, ny):
        t.setx(nx)
        handle_invisibility_pickup(t)


def move_right(t, speed):
    update_sprite_direction(t, "right")
    nx, ny = t.xcor() + speed, t.ycor()
    if nx <= MAX_X and allow_move(nx, ny):
        t.setx(nx)
        handle_invisibility_pickup(t)


# ===================================================
# MAIN BINDING FUNCTION
# ===================================================

def bind_player_controls(screen, player1, player2, game_state, extra_callback=None):
    speed = game_state["player_speed"]

    # helper wrapper: avoids repeating callback code
    def wrap(func):
        def inner():
            func()
            if extra_callback:
                extra_callback()
        return inner

    # P1 keys
    screen.onkey(wrap(lambda: move_up(player1, speed)),    "w")
    screen.onkey(wrap(lambda: move_down(player1, speed)),  "s")
    screen.onkey(wrap(lambda: move_left(player1, speed)),  "a")
    screen.onkey(wrap(lambda: move_right(player1, speed)), "d")

    # P2 keys
    screen.onkey(wrap(lambda: move_up(player2, speed)),    "Up")
    screen.onkey(wrap(lambda: move_down(player2, speed)),  "Down")
    screen.onkey(wrap(lambda: move_left(player2, speed)),  "Left")
    screen.onkey(wrap(lambda: move_right(player2, speed)), "Right")

    screen.listen()