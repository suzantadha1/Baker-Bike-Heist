# story_screens.py
import turtle
from system_loader import start_real_loading

# ----------------------------------------------------
#   BUTTON FACTORY (NO NEW SCREEN)
# ----------------------------------------------------
def make_button(screen, path, x, y):
    try:
        screen.addshape(path)
    except:
        pass

    t = turtle.Turtle()
    t.penup()
    t.goto(x, y)
    t.shape(path)
    t.showturtle()
    return t


# ----------------------------------------------------
#   STORY SCREEN 1
# ----------------------------------------------------
def show_story_1(screen):
    screen.onclick(None)
    screen.clear()
    screen.bgpic("1story_screen.gif")

    next_btn = make_button(screen, "next_button.gif", 0, -200)

    def handle_click(x, y):
        if next_btn.distance(x, y) < 80:
            next_btn.hideturtle()
            show_story_2(screen)

    next_btn.onclick(handle_click)


# ----------------------------------------------------
#   STORY SCREEN 2
# ----------------------------------------------------
def show_story_2(screen):
    screen.onclick(None)
    screen.clear()
    screen.bgpic("2story_screen.gif")

    next_btn = make_button(screen, "next_button.gif", 0, -200)

    def handle_click(x, y):
        if next_btn.distance(x, y) < 80:
            next_btn.hideturtle()
            show_story_3(screen)

    next_btn.onclick(handle_click)


# ----------------------------------------------------
#   STORY SCREEN 3 — start Stage 1
# ----------------------------------------------------
def show_story_3(screen):
    screen.onclick(None)
    screen.clear()
    screen.bgpic("3story_screen.gif")

    start_btn = make_button(screen, "start_stage_button.gif", 0, -220)

    def handle_click(x, y):
        if start_btn.distance(x, y) < 80:
            start_btn.hideturtle()
            start_real_loading(screen, "stage1")

    start_btn.onclick(handle_click)


# ----------------------------------------------------
#   STORY SCREEN 4 — start Stage 2
# ----------------------------------------------------
def show_story_4(screen):
    screen.onclick(None)
    screen.clear()
    screen.bgpic("4story_screen.gif")

    start_btn = make_button(screen, "start_stage_button.gif", 0, -200)

    def handle_click(x, y):
        if start_btn.distance(x, y) < 80:
            start_btn.hideturtle()
            start_real_loading(screen, "stage2")

    start_btn.onclick(handle_click)


# ----------------------------------------------------
#   STORY SCREEN 5 — start Stage 3 (needs p1/p2)
# ----------------------------------------------------
def show_story_5(screen, p1, p2):
    screen.onclick(None)
    screen.clear()
    screen.bgpic("5story_screen.gif")

    start_btn = make_button(screen, "start_stage_button.gif", 300, 0)

    def handle_click(x, y):
        if start_btn.distance(x, y) < 80:
            start_btn.hideturtle()
            start_real_loading(screen, "stage3", p1, p2)

    start_btn.onclick(handle_click)


# ----------------------------------------------------
#   STORY SCREEN 6 — start Stage 4
# ----------------------------------------------------
def show_story_6(screen, p1, p2):
    screen.onclick(None)
    screen.clear()
    screen.bgpic("6story_screen.gif")

    start_btn = make_button(screen, "start_stage_button.gif", 0, -200)

    def handle_click(x, y):
        if start_btn.distance(x, y) < 80:
            start_btn.hideturtle()
            start_real_loading(screen, "stage4", p1, p2)

    start_btn.onclick(handle_click)