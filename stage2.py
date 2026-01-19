# stage2.py  — CLEAN VERSION (Moderate Cleanup)
import turtle

from sprites import healthbar_images
from movement import bind_player_controls
from professor_ai import create_professor, move_professor
from collision import add_block
from camera import start_camera
from notes import setup_notes
import invisibility


# ---------------------------------------------------
# CONSTANTS
# ---------------------------------------------------
HALF_W = 480
HALF_H = 270
SPRITE_MARGIN = 32

MIN_X = -HALF_W + SPRITE_MARGIN
MAX_X = HALF_W - SPRITE_MARGIN
MIN_Y = -HALF_H + SPRITE_MARGIN
MAX_Y = HALF_H - SPRITE_MARGIN


# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------
def clamp_x(x): return max(MIN_X, min(MAX_X, x))
def clamp_y(y): return max(MIN_Y, min(MAX_Y, y))


def load_character(screen, x, y, front, back, left, right):
    """Registers sprite frames & returns a configured turtle."""
    for img in (front, back, left, right):
        screen.register_shape(img)

    t = turtle.Turtle()
    t.penup()
    t.goto(x, y)

    t.front = front
    t.back = back
    t.left_img = left
    t.right_img = right

    t.shape(front)
    t.facing = "front"
    t.is_invisible = False
    return t


def get_hp_image(hp):
    """Returns correct HP bar sprite for given HP."""
    for level in sorted(healthbar_images.keys(), reverse=True):
        if hp >= level:
            return healthbar_images[level]
    return healthbar_images[min(healthbar_images.keys())]


# ---------------------------------------------------
# MAIN STAGE FUNCTION
# ---------------------------------------------------
def start_stage2(screen):

    # Reset
    from collision import blocked_area
    blocked_area.clear()

    screen.clear()
    screen.bgcolor("black")
    screen.tracer(0)

    # Hide ALL previous turtles
    for t in screen.turtles():
        t.hideturtle()
        t.clear()
    screen.update()

    # ---------------------------------------------------
    # STAGE BACKGROUND
    # ---------------------------------------------------
    screen.bgpic("stage_2.gif")
    screen.setworldcoordinates(-480, -270, 480, 270)
    screen.title("Baker Bike Heist - Stage 2")

    # ---------------------------------------------------
    # PLAYERS
    # ---------------------------------------------------
    player1 = load_character(
        screen, -50.64, -215.86,
        "stage_1/P1_front.gif", "stage_1/P1_back.gif",
        "stage_1/P1_left.gif", "stage_1/P1_right.gif"
    )
    player2 = load_character(
        screen, 24.25, -213.69,
        "stage_1/P2_front.gif", "stage_1/P2_back.gif",
        "stage_1/P2_left.gif", "stage_1/P2_right.gif"
    )

    # ---------------------------------------------------
    # HEALTHBARS
    # ---------------------------------------------------
    p1_hp = 100
    p2_hp = 100

    # register HP bar shapes once
    for img in healthbar_images.values():
        screen.register_shape(img)

    hp1 = turtle.Turtle()
    hp1.penup()
    hp1.goto(-400, 250)
    hp1.shape(get_hp_image(p1_hp))

    hp2 = turtle.Turtle()
    hp2.penup()
    hp2.goto(300, 250)
    hp2.shape(get_hp_image(p2_hp))

    # ---------------------------------------------------
    # SHARED STATE
    # ---------------------------------------------------
    stage2_state = {
        "player_speed": 15,
        "professor_speed": 4,
        "p1_health": p1_hp,
        "p2_health": p2_hp,
        "game_over": False,
        "professor_damage_cooldown": 0,
        "victory": False
    }

    # Elevator exit zone
    END_X_MIN, END_X_MAX = -46, 38
    END_Y_MIN, END_Y_MAX = 169, 268

    # ---------------------------------------------------
    # WALL HITBOXES (unchanged)
    # ---------------------------------------------------
    stage2_blocks = [
        (-432.94205, -259.78609, -410.08915, 70.64171),
        (-420.08915, 50.64171, -99.12333, 71.36363),
        (-114.84398, -66.31016, -94.13075, 71.36363),
        (-400.13372, -70.64171, -378.70728, 57.64705),
        (-254.63595, -70.64171, -234.63595, -50.64171),
        (-253.92273, 23.20855, -233.92273, 43.20855),
        (-393.71471, -123.34224, -327.35512, -91.79144),
        (-395.85438, -183.98395, -330.20802, -159.65240),
        (-226.82020, -77.13903, -206.82020, 2.05882),
        (-190.44576, -72.80748, -170.44576, 4.94652),
        (-223.25408, -16.49732, -170.44576, 4.94652),
        (-116.27043, 158.20855, -94.84398, 287.94117),
        (-429.37592, 265.05347, -94.84398, 287.94117),
        (-430.08915, 51.36363, -410.08915, 71.36363),
        (-350.20802, 103.34224, -330.20802, 194.09090),
        (-224.68053, 108.39572, -204.68053, 189.75935),
        (-346.64190, 172.64705, -204.68053, 189.75935),
        (83.43239, 212.35294, 108.42496, 286.49732),
        (388.13372, 263.60962, 109.13818, 286.49732),
        (323.07578, 179.14438, 344.50222, 255.45454),
        (375.14115, 182.75401, 400.13372, 256.89839),
        (158.32095, 163.26203, 178.32095, 209.25133),
        (268.87072, 163.26203, 296.00297, 212.86096),
        (163.31352, 197.19251, 296.00297, 212.86096),
        (385.56017, 60.74866, 85.57206, 84.35828),
        (83.43239, -141.39037, 113.43239, -98.28877),
        (390.13372, -120.45454, 89.13818, -100.45454),
        (181.14413, -199.14438, 202.57057, -149.54545),
        (285.27488, -195.53475, 305.27488, -153.15508),
        (191.12927, -176.04278, 305.27488, -153.15508),
        (311.66419, -205.64171, 331.66419, -135.10695),
        (368.72213, -196.25668, 388.72213, -136.55080),
        (313.09063, -156.55080, 388.72213, -136.55080),
    ]

    for x1, y1, x2, y2 in stage2_blocks:
        add_block(x1, y1, x2, y2)

    # ---------------------------------------------------
    # NOTES (must load BEFORE professor)
    # ---------------------------------------------------
    msg = turtle.Turtle()
    msg.hideturtle()
    msg.penup()
    msg.color("white")
    msg.goto(0, 200)

    setup_notes(screen, player1, player2, hp1, hp2, msg)

    # ---------------------------------------------------
    # PROFESSOR AI
    # ---------------------------------------------------
    for img in [
        "stage_1/prof_front.gif", "stage_1/prof_back.gif",
        "stage_1/prof_left.gif", "stage_1/prof_right.gif"
    ]:
        screen.register_shape(img)

    prof = create_professor()
    prof.goto(-0.71, 135.72)

    def update_hp(gs, hp1_t, hp2_t):
        hp1_t.shape(get_hp_image(gs["p1_health"]))
        hp2_t.shape(get_hp_image(gs["p2_health"]))

    move_professor(
        screen, prof,
        player1, player2,
        stage2_state,
        hp1, hp2,
        msg,
        update_hp
    )

    # ---------------------------------------------------
    # ELEVATOR / STAGE 2 WIN CHECK
    # ---------------------------------------------------
    def check_stage2_win():
        if stage2_state["victory"]:
            return

        x1, y1 = player1.position()
        x2, y2 = player2.position()

        p1_ready = END_X_MIN <= x1 <= END_X_MAX and END_Y_MIN <= y1 <= END_Y_MAX and player1.is_invisible
        p2_ready = END_X_MIN <= x2 <= END_X_MAX and END_Y_MIN <= y2 <= END_Y_MAX and player2.is_invisible

        msg.clear()

        if p1_ready and p2_ready:
            stage2_state["victory"] = True
            stage2_victory()
            return

        if p1_ready ^ p2_ready:
            msg.write(
                "Waiting for other player...",
                align="center", font=("Arial", 20, "bold")
            )

    # ---------------------------------------------------
    # VICTORY HANDLER
    # ---------------------------------------------------
    def stage2_victory():
        stage2_state["game_over"] = True

        # disable keys
        for key in ["w", "a", "s", "d", "Up", "Down", "Left", "Right", "space", "Return", "e"]:
            screen.onkeypress(None, key)

        player1.hideturtle()
        player2.hideturtle()
        msg.clear()

        # save HP for stage 3
        p1, p2 = stage2_state["p1_health"], stage2_state["p2_health"]

        from story_screens import show_story_5
        show_story_5(screen, p1, p2)

    # ---------------------------------------------------
    # CAMERA + DAMAGE SYSTEM
    # ---------------------------------------------------
    start_camera(
        screen,
        player1, player2,
        hp1, hp2,
        get_hp_image,
        stage2_state,
        update_hp,
        speed=5,
        damage_distance=100,
        damage_amount=10,
        image_left="camera_left_small.gif",
        image_right="camera_right_small.gif"
    )

    # ---------------------------------------------------
    # INVISIBILITY DRINKS
    # ---------------------------------------------------
    drink_positions = [
        (-335.215, -111.176),
        (-170.460, -62.807)
    ]

    invis_sprites = [
        "invisible_players/drink.gif",
        "invisible_players/empty_drink.gif",
        "invisible_players/p1_invisibility_front.gif",
        "invisible_players/p1_invisibility_back.gif",
        "invisible_players/p1_invisibility_left.gif",
        "invisible_players/p1_invisibility_right.gif",
        "invisible_players/p2_invisibility_front.gif",
        "invisible_players/p2_invisibility_back.gif",
        "invisible_players/p2_invisibility_left.gif",
        "invisible_players/p2_invisibility_right.gif"
    ]

    for s in invis_sprites:
        screen.register_shape(s)

    bind_player_controls(screen, player1, player2, stage2_state, extra_callback=check_stage2_win)
    invisibility.setup_drinks(screen, player1, player2, drink_positions)

    # ---------------------------------------------------
    # FINAL SHOW
    # ---------------------------------------------------
    player1.showturtle()
    player2.showturtle()
    prof.showturtle()
    hp1.showturtle()
    hp2.showturtle()

    screen.tracer(1)
    screen.update()