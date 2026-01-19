# game_over.py
import turtle

def show_game_over(screen, message="GAME OVER"):
    """
    Universal Game Over screen for all stages.
    Clears the screen, displays a message,
    and enables 'q' to quit the entire game.
    """

    # wipe everything
    screen.clear()
    screen.bgcolor("black")
    screen.title("Fourth Floor Heist - Game Over")

    t = turtle.Turtle()
    t.hideturtle()
    t.color("red")
    t.penup()
    t.goto(0, 50)
    t.write(message, align="center", font=("Arial", 48, "bold"))

    # Press Q to quit
    q = turtle.Turtle()
    q.hideturtle()
    q.color("white")
    q.penup()
    q.goto(0, -50)
    #q.write("Press Q to quit", align="center", font=("Arial", 20, "normal"))

    # Enable quitting the program
    def quit_game():
        turtle.bye()     # closes the Turtle window completely

    screen.listen()
    screen.onkey(quit_game, "q")