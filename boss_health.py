import turtle

def create_boss_healthbar():
    bar = turtle.Turtle()
    bar.hideturtle()
    bar.penup()
    bar.speed(0)

    bar.goto(-50, -230)
    bar.showturtle()

    return bar

def update_boss_healthbar(bar, boss_hp):
    """
    boss_hp: integer 0–12
    """
    if boss_hp < 0:
        boss_hp = 0
    if boss_hp > 12:
        boss_hp = 12

    bar.shape(f"boss_hp/boss_hp_{boss_hp}.gif")