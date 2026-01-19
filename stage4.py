# stage4.py — FINAL CLEAN VERSION (Outside → Boss Transition FIXED)
import turtle

from movement import bind_player_controls
from player import (
    create_default_players,
    create_healthbars,
    update_healthbars
)
from collision import add_block
from professor_ai import move_professor
from professor_outside import create_outside_professor
from bikes import BIKES, in_box
from stage4_bossfight import start_boss_fight


def start_stage4(screen, p1_health, p2_health):

    # --------------------------------------------
    # FULL OUTSIDE RESET
    # --------------------------------------------
    screen.clear()
    from collision import blocked_area
    blocked_area.clear()
    screen.setworldcoordinates(-480, -270, 480, 270)

    screen.title("Fourth Floor Heist – Stage 4 (Outside Lawn)")
    screen.bgpic("stage_4_outside.gif")
    screen.listen()

    # --------------------------------------------
    # SPAWN PLAYERS
    # --------------------------------------------
    P1_START = (-449, 124)
    P2_START = (-363, 124)
    player1, player2 = create_default_players(P1_START, P2_START)

    # --------------------------------------------
    # GAME STATE FOR OUTSIDE
    # --------------------------------------------
    game_state = {
        "player_speed": 25,
        "professor_speed": 3,
        "game_over": False,             # IMPORTANT → outside loop stops here
        "p1_health": p1_health,
        "p2_health": p2_health,
        "outside_damage_enabled": True,
        "professor_damage_cooldown": 0,
    }

    # --------------------------------------------
    # PLAYER CONTROLS
    # --------------------------------------------
    bind_player_controls(screen, player1, player2, game_state)

    # --------------------------------------------
    # HEALTHBARS
    # --------------------------------------------
    p2_bar, p1_bar = create_healthbars()
    update_healthbars(game_state, p1_bar, p2_bar)

    p1_bar.showturtle()
    p2_bar.showturtle()

    # --------------------------------------------
    # OUTSIDE PROFESSOR + MESSAGE TURTLE
    # --------------------------------------------
    prof = create_outside_professor()
    prof.showturtle()

    msg = turtle.Turtle()
    msg.hideturtle()
    msg.penup()
    msg.goto(0, 220)

    # --------------------------------------------
    # OUTSIDE PROFESSOR CHASE LOOP
    # --------------------------------------------
    def professor_update():
        if game_state["game_over"]:
            return      # STOPS LOOP IMMEDIATELY

        move_professor(
            screen,
            prof,
            player1,
            player2,
            game_state,
            p1_bar,
            p2_bar,
            msg,
            update_healthbars
        )

        screen.ontimer(professor_update, 80)

    professor_update()   # start loop

    # --------------------------------------------
    # BIKE PICKING → ENTER BOSS ARENA
    # --------------------------------------------
    def correct_bike_selected():
        # STOP ALL OUTSIDE LOGIC
        game_state["game_over"] = True   # ← THE FIX
        game_state["outside_damage_enabled"] = False

        # hide outside professor + UI
        prof.hideturtle()
        msg.clear()

        # START BOSS FIGHT with carried-over HP
        start_boss_fight(
            screen,
            game_state["p1_health"],
            game_state["p2_health"]
        )

    def pick_bike_for_player(player_label, player_turtle):
        for name, box in BIKES.items():
            if in_box(player_turtle, box):
                print(player_label, "picked:", name)

                if name == "correct":
                    correct_bike_selected()
                else:
                    print("❌ Wrong bike.")
                return

        print(player_label, "not on bike.")

    # keybinds for picking bikes
    def pick_bike_p1():
        pick_bike_for_player("P1", player1)

    def pick_bike_p2():
        pick_bike_for_player("P2", player2)

    screen.onkey(pick_bike_p1, "space")
    screen.onkey(pick_bike_p2, "Return")
    screen.listen()

    # show players
    player1.showturtle()
    player2.showturtle()

    print("Stage 4 (Outside Lawn) Loaded ✔")
    print("P1: WASD + SPACE to pick bike")
    print("P2: Arrows + ENTER to pick bike")