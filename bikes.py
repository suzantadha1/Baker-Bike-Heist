# bikes.py
"""
Bike hitbox definitions and helpers for Stage 4 (outside lawn).
"""

# ==========================
#  BIKE HITBOXES (OUTSIDE LAWN)
# ==========================
BIKES = {
    "top": {
        "x_min": 102, "x_max": 261,
        "y_min": 2,  "y_max": 82
    },
    "correct": {   # Baker's real bike
        "x_min": 102, "x_max": 261,
        "y_min": -83, "y_max": 5
    },
    "lower_mid": {
        "x_min": 102, "x_max": 261,
        "y_min": -158, "y_max": -80
    },
    "bottom": {
        "x_min": 102, "x_max": 261,
        "y_min": -250, "y_max": -160
    }
}


def in_box(player, box):
    """Return True if player's (x, y) is inside the given box dict."""
    x = player.xcor()
    y = player.ycor()
    return (box["x_min"] <= x <= box["x_max"] and
            box["y_min"] <= y <= box["y_max"])