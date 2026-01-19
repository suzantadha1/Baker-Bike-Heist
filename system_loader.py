import turtle
import time
from sprites import collect_all_sprite_paths, register_all_sprites_async


def start_real_loading(screen, next_stage="stage1", p1_health=100, p2_health=100):
    """
    Smooth, non-blocking loading screen that registers all sprites
    while showing a loading animation.
    """

    # ---------------------------
    #   LOADING UI
    # ---------------------------
    screen.clear()
    screen.bgcolor("black")
    screen.title("Fourth Floor Heist - Loading...")
    screen.tracer(0)

    loader = turtle.Turtle()
    loader.hideturtle()
    loader.penup()
    loader.color("white")
    loader.goto(0, 0)

    phases = ["Loading.", "Loading..", "Loading..."]
    idx = 0
    running = {"ok": True}

    def animate():
        if not running["ok"]:
            return
        nonlocal idx
        loader.clear()
        loader.write(phases[idx], align="center", font=("Arial", 26, "bold"))
        idx = (idx + 1) % len(phases)
        screen.update()
        screen.ontimer(animate, 250)

    animate()

    # ---------------------------
    #   SPRITE LOADING
    # ---------------------------
    sprite_paths = collect_all_sprite_paths()

    def all_done():
        running["ok"] = False
        loader.clear()
        loader.color("gold")
        loader.write("All systems ready!", align="center", font=("Arial", 28, "bold"))
        screen.update()
        time.sleep(0.3)

        # -------------------
        #   SWITCH STAGE
        # -------------------
        if next_stage == "stage1":
            from stage1 import start_stage1
            start_stage1(screen)

        elif next_stage == "stage2":
            from stage2 import start_stage2
            start_stage2(screen)

        elif next_stage == "stage3":
            from stage_3 import start_stage3
            start_stage3(screen, p1_health, p2_health)

        elif next_stage == "stage4":
            from stage4 import start_stage4
            start_stage4(screen, p1_health, p2_health)

    # async load prevents freezing
    register_all_sprites_async(screen, on_finish=all_done, chunk=6)