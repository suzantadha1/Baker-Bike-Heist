import turtle
import time
import math
from collision import is_blocked

# =====================================================
#  GLOBAL FLAG — used by stages to pause AI if needed
# =====================================================
PROFESSOR_AI_ENABLED = True


# =====================================================
#  PROFESSOR INITIALIZATION
# =====================================================
def create_professor():
    prof = turtle.Turtle()
    prof.hideturtle()
    prof.penup()
    prof.speed(0)
    prof.shape("stage_1/prof_front.gif")
    prof.goto(-155, 85)
    return prof


# =====================================================
#  SPRITE LOGIC
# =====================================================
def update_professor_sprite(professor, direction):
    if direction == "up":
        professor.shape("stage_1/prof_back.gif")
    elif direction == "down":
        professor.shape("stage_1/prof_front.gif")
    elif direction == "left":
        professor.shape("stage_1/prof_left.gif")
    elif direction == "right":
        professor.shape("stage_1/prof_right.gif")


def update_professor_sprite_by_heading(professor):
    h = professor.heading()

    if 45 < h <= 135:
        update_professor_sprite(professor, "up")
    elif 135 < h <= 225:
        update_professor_sprite(professor, "left")
    elif 225 < h <= 315:
        update_professor_sprite(professor, "down")
    else:
        update_professor_sprite(professor, "right")


# =====================================================
#  NON-BLOCKING WALK
# =====================================================
def walk_points(screen, professor, points, on_finish, pause=18):
    """
    Walk through multiple points asynchronously.
    Calls on_finish ONLY when last point is reached.
    """

    if not points:
        on_finish()
        return

    px, py = points[0]

    def step():
        # Arrived at this waypoint
        if professor.distance(px, py) <= 5:
            professor.goto(px, py)
            screen.ontimer(
                lambda: walk_points(screen, professor, points[1:], on_finish, pause),
                20
            )
            return

        angle = professor.towards(px, py)
        professor.setheading(angle)
        update_professor_sprite_by_heading(professor)

        nx = professor.xcor() + 4 * math.cos(math.radians(angle))
        ny = professor.ycor() + 4 * math.sin(math.radians(angle))

        if not is_blocked(nx, ny):
            professor.goto(nx, ny)

        screen.ontimer(step, pause)

    step()


# =====================================================
#  ENTRY SEQUENCE
# =====================================================
def professor_stays(screen, professor, msg, move_callback):
    professor.showturtle()
    update_professor_sprite(professor, "down")
    professor.goto(-135, 65)

    msg.clear()
    msg.write("👨‍🏫 Professor is still in the room...",
              align="center", font=("Arial", 14, "bold"))

    screen.ontimer(
        lambda: professor_leaves(screen, professor, msg, move_callback),
        2500
    )


def professor_leaves(screen, professor, msg, move_callback):

    msg.clear()
    msg.write("🚶‍♂️ Professor leaves to refill his bottle...",
              align="center", font=("Arial", 14, "bold"))

    path_to_fountain = [
        (-65, 65),
        (-65, -30),
        (180, -30),
        (180, 140),
    ]

    # After reaching fountain
    def reached_fountain():
        msg.clear()
        msg.write("🥤 Professor is refilling his bottle...",
                  align="center", font=("Arial", 14, "bold"))

        # ★ 5-SECOND REFILL TIME ★
        screen.ontimer(
            lambda: professor_returns(screen, professor, msg, move_callback),
            5000
        )

    walk_points(screen, professor, path_to_fountain, reached_fountain)


def professor_returns(screen, professor, msg, move_callback):

    msg.clear()
    msg.write("😈 Professor returns and starts chasing!",
              align="center", font=("Arial", 14, "bold"))

    final_path = [
        (180, 140),
        (180, -30),
        (0, -30),
        (-6, -30),     # ★ Chase STARTS only after this point ★
    ]

    def start_chase():
        update_professor_sprite(professor, "left")
        professor.showturtle()
        if PROFESSOR_AI_ENABLED:
            move_callback()

    walk_points(screen, professor, final_path, start_chase)


# =====================================================
#  CHASE LOGIC
# =====================================================
def move_professor(
    screen, professor, player1, player2,
    game_state, p1_hpbar, p2_hpbar,
    msg, update_hp
):
    if game_state["game_over"] or not PROFESSOR_AI_ENABLED:
        return

    # invisibility freeze
    if getattr(player1, "is_invisible", False) and getattr(player2, "is_invisible", False):
        screen.ontimer(lambda:
            move_professor(screen, professor, player1, player2,
                           game_state, p1_hpbar, p2_hpbar,
                           msg, update_hp),
            60
        )
        return

    # chase closest player
    target = player1 if professor.distance(player1) < professor.distance(player2) else player2

    angle = professor.towards(target.xcor(), target.ycor())
    professor.setheading(angle)

    step = game_state["professor_speed"]

    nx = professor.xcor() + step * math.cos(math.radians(angle))
    ny = professor.ycor() + step * math.sin(math.radians(angle))

    free = not is_blocked(nx, ny)
    slide_x = not is_blocked(nx, professor.ycor())
    slide_y = not is_blocked(professor.xcor(), ny)

    if free:
        professor.goto(nx, ny)
    else:
        moved = False

        if slide_x:
            professor.goto(nx, professor.ycor())
            moved = True
        if slide_y:
            professor.goto(professor.xcor(), ny)
            moved = True

        if not moved:
            for offset in (10, -10, 20, -20):
                t_angle = angle + offset
                tx = professor.xcor() + step * math.cos(math.radians(t_angle))
                ty = professor.ycor() + step * math.sin(math.radians(t_angle))
                if not is_blocked(tx, ty):
                    professor.setheading(t_angle)
                    professor.goto(tx, ty)
                    moved = True
                    break

        if not moved:
            return

    update_professor_sprite_by_heading(professor)

    # damage
    if game_state.get("outside_damage_enabled", True):

        if game_state["professor_damage_cooldown"] > 0:
            game_state["professor_damage_cooldown"] -= 1

        else:
            hit = False
            if professor.distance(player1) < 35:
                game_state["p1_health"] -= 5
                hit = True
            if professor.distance(player2) < 35:
                game_state["p2_health"] -= 5
                hit = True

            if hit:
                game_state["professor_damage_cooldown"] = 10

    update_hp(game_state, p1_hpbar, p2_hpbar)

    if game_state["p1_health"] <= 0 or game_state["p2_health"] <= 0:
        game_state["game_over"] = True
        from game_over import show_game_over
        show_game_over(screen)
        return

    screen.ontimer(lambda:
        move_professor(screen, professor, player1, player2,
                       game_state, p1_hpbar, p2_hpbar,
                       msg, update_hp),
        60
    )