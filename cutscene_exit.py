# cutscene_exit.py
import turtle
from player import create_default_players
from stage4 import start_stage4

def play_exit_cutscene(screen, p1_health, p2_health):
    screen.clear()
    screen.bgpic("floor1.gif")
    screen.title("Exit Cutscene")
    screen.tracer(0)

    # START POSITIONS
    P1_START = (-400, -140)
    P2_START = (-390, -20)

    # TARGETS
    P1_TARGET = (-95, -140)
    P2_TARGET_1 = (30, -20)
    P2_TARGET_2 = (30, -140)

    # CREATE PLAYERS
    player1, player2 = create_default_players(P1_START, P2_START)

    # FACE RIGHT
    player1.facing = "right"
    player1.shape(player1.right_img)

    player2.facing = "right"
    player2.shape(player2.right_img)

    player1.showturtle()
    player2.showturtle()

    speed = 4

    p1_done = False
    p2_phase = 1

    def move_toward(t, tx, ty):
        x, y = t.xcor(), t.ycor()
        dx = tx - x
        dy = ty - y

        if abs(dx) < 1 and abs(dy) < 1:
            return True

        dist = (dx*dx + dy*dy) ** 0.5
        nx = x + (dx/dist) * speed
        ny = y + (dy/dist) * speed
        t.goto(nx, ny)
        return False

    def animate():
        nonlocal p1_done, p2_phase

        # ------------------------
        # PLAYER 1 — NO JITTER
        # ------------------------
        if not p1_done:
            tx, ty = P1_TARGET
            if move_toward(player1, tx, ty):
                player1.goto(tx, ty)
                player1.facing = "front"
                player1.shape(player1.front)
                p1_done = True

        # ------------------------
        # PLAYER 2 — TWO STEP WALK
        # ------------------------
        if p2_phase == 1:
            if move_toward(player2, P2_TARGET_1[0], P2_TARGET_1[1]):
                player2.facing = "front"
                player2.shape(player2.front)
                p2_phase = 2

        elif p2_phase == 2:
            if move_toward(player2, P2_TARGET_2[0], P2_TARGET_2[1]):
                # FINISHED CUTSCENE → GO TO STAGE 4
                start_stage4(screen, p1_health, p2_health)
                return  # STOP animation loop

        screen.update()
        screen.ontimer(animate, 20)

    animate()

    print("Cutscene running...")