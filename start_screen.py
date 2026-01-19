# start_screen.py
import turtle

def show_start_screen(screen, on_start):
    screen.clear()
    screen.bgpic("")
    screen.bgcolor("black")
    screen.title("Baker Bike Heist")
    screen.tracer(0)

    # Background
    try:
        screen.addshape("start_image.gif")
    except:
        print("⚠️ Missing: start_image.gif")

    bg = turtle.Turtle()
    bg.penup()
    bg.goto(0, 0)
    bg.shape("start_image.gif")

    # First START button
    try:
        screen.addshape("start_button.gif")
    except:
        print("⚠️ Missing: start_button.gif")

    start_btn = turtle.Turtle()
    start_btn.penup()
    start_btn.goto(0, -180)
    start_btn.shape("start_button.gif")

    # Click handler
    def clicked(x, y):
        if start_btn.distance(x, y) < 80:
            start_btn.hideturtle()
            bg.hideturtle()
            screen.onclick(None)
            on_start()

    start_btn.onclick(clicked)
    screen.update()