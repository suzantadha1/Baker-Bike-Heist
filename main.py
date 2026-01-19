import turtle
import sys
sys.path.append('/usercode')

from sprites import register_all_sprites
from start_screen import show_start_screen
from story_screens import show_story_1

# --------------------------------------
#   FIX: Avoid ghost turtle lag
# --------------------------------------
turtle.TurtleScreen._RUNNING = True

# --------------------------------------
#   CLEAN RESET FUNCTION
# --------------------------------------
def safe_reset_screen(scr):
    scr.tracer(False)
    for t in scr.turtles():
        try:
            t.hideturtle()
            t.clear()
            t.goto(2000, 2000)
            t._destroy()
        except:
            pass
    scr.tracer(True)

# --------------------------------------
#   SCREEN SETUP
# --------------------------------------
screen = turtle.Screen()
screen.setup(960, 540)
screen.setworldcoordinates(-480, -270, 480, 270)
screen.title("Fourth Floor Heist")

# --------------------------------------
#   LOAD ALL SPRITES ONCE
# --------------------------------------
register_all_sprites(screen)

# --------------------------------------
#   START GAME → STORY 1 → STAGE 1
# --------------------------------------
def start_game():
    show_story_1(screen)

show_start_screen(screen, start_game)

# --------------------------------------
# OPTIONAL DEBUG: Click to print coords
# --------------------------------------
def print_coords(x, y):
    print(f"Clicked at ({int(x)}, {int(y)})")

screen.onclick(print_coords)

# --------------------------------------
#   MAINLOOP
# --------------------------------------
turtle.mainloop()