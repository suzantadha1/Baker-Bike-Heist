# professor_outside.py
"""
Professor spawning specifically for Stage 4 outside lawn.
"""

import turtle
from professor_ai import update_professor_sprite


def create_outside_professor():
    """
    Creates the professor for the outside lawn (Stage 4).
    Uses the same sprites as Stage 1, but with a lawn-friendly position.
    """
    prof = turtle.Turtle()
    prof.hideturtle()
    prof.penup()
    prof.speed(0)

    # These shapes are registered via register_all_sprites()
    prof.shape("stage_1/prof_front.gif")

    # You can tweak this starter position to wherever you like on the lawn
    prof.goto(-155, 85)
    update_professor_sprite(prof, "down")

    return prof