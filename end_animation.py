import turtle
import time

def play_end_animation(screen, bike_sprite, background_sprite, on_finish=None):

    # FULL SCREEN RESET (safe)
    screen.clear()
    screen.clearscreen()

    # Restore coordinate system & window
    screen.setworldcoordinates(-480, -270, 480, 270)
    screen.setup(960, 540)
    screen.title("Fourth Floor Heist – Ending")
    screen.tracer(0)

    # Register shapes safely
    try:
        screen.register_shape(background_sprite)
    except:
        print("Could not register:", background_sprite)

    try:
        screen.register_shape(bike_sprite)
    except:
        print("Could not register:", bike_sprite)

    # Background
    screen.bgpic(background_sprite)

    # Bike turtle
    bike = turtle.Turtle()
    bike.penup()
    bike.speed(0)
    bike.shape(bike_sprite)

    # Movement values
    x, y = 0, -200
    end_y = 100

    bike.goto(x, y)
    bike.showturtle()

    # ----------------------------------
    # ANIMATION LOOP
    # ----------------------------------
    def animate():
        nonlocal y

        if y < end_y:
            y += 4
            bike.goto(x, y)
            screen.update()
            screen.ontimer(animate, 20)

        else:
            show_final_screen()

    # ----------------------------------
    # FINAL MESSAGE SCREEN
    # ----------------------------------
    def show_final_screen():
        # Display final image
        try:
            screen.register_shape("end_message.gif")
        except:
            pass

        screen.bgpic("end_message.gif")
        bike.hideturtle()
        screen.update()

        if on_finish:
            on_finish()

    animate()