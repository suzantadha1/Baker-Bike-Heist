# animation_evolve.py
"""
Optimized evolution animation.
- NO duplicate sprite loading (uses global cache)
- Reuses pre-registered shapes from main loader
- Clean, smooth animation timing
"""

import turtle
import os


def play_evolution_animation(screen, final_callback,
                             start_x=-50, start_y=90,
                             frame_delay=120):
    """
    Plays the evolution animation ONCE, then calls final_callback(turtle).
    """

    # ---------------------------------------------
    # 1. COLLECT FRAMES (NO NEW REGISTRATION)
    # ---------------------------------------------
    frames = []
    for i in range(1, 200):
        path = f"prof_evolve/prof_evolve_{i}.gif"
        if os.path.exists(path):
            frames.append(path)
        else:
            break

    if not frames:
        print("❌ No evolution frames found!")
        final_callback(None)
        return

    # ---------------------------------------------
    # 2. CREATE ANIMATION TURTLE
    # ---------------------------------------------
    evo = turtle.Turtle()
    evo.hideturtle()
    evo.penup()
    evo.speed(0)
    evo.goto(start_x, start_y)

    # ensure start frame is visible
    evo.shape(frames[0])
    evo.showturtle()

    # ---------------------------------------------
    # 3. NON-BLOCKING ANIMATION LOOP
    # ---------------------------------------------
    state = {"index": 0}

    def animate():
        i = state["index"]

        if i < len(frames):
            evo.shape(frames[i])
            state["index"] = i + 1
            screen.ontimer(animate, frame_delay)
        else:
            # animation DONE → return turtle to callback
            final_callback(evo)

    animate()