import turtle
import time

from movement import bind_player_controls
from player import create_default_players, create_healthbars, update_healthbars
from professor_ai import create_professor, professor_stays, move_professor
from items import (
    create_drawers, create_bagpack, create_keys,
    search_drawers_for_player, open_near_bagpack,
    pick_up_near_item,
)
from inventory import create_inventories
from ui_inventory import create_inventory_ui, update_inventory_ui
from stage_manager import check_stage_complete
from game_over import show_game_over
from collision import add_block


def start_stage1(screen):

    screen.clear()
    screen.bgcolor("black")
    screen.title("Stage 1")
    screen.tracer(0)

    # ----- COLLISION WALLS -----
    add_block(-40, 277, 14, 0)
    add_block(-40, -70, 14, -195)
    add_block(-430, 70, -180, 180)
    add_block(-481, -269, -17, -150)
    add_block(10, -265, 147, -150)
    add_block(264, -265, 480, -150)
    add_block(-332, -136, -265, -50)
    add_block(-213, -149, -141, -40)

    # ----- PLAYERS -----
    player1, player2 = create_default_players((-350, 0), (-250, 0))

    game_state = {
        "p1_health": 100,
        "p2_health": 100,
        "player_speed": 25,
        "professor_speed": 5,
        "keys_collected": [],
        "inventory_p1": [],
        "inventory_p2": [],
        "game_over": False,
        "total_keys": 2,
        "start_time": time.time(),
        "professor_damage_cooldown": 0,
    }

    def handle_game_over():
        game_state["game_over"] = True
        show_game_over(screen)
        for key in ["w","a","s","d","Up","Down","Left","Right"]:
            screen.onkeypress(None, key)

    message = turtle.Turtle()
    message.hideturtle()
    message.penup()
    message.goto(0, 200)
    message.color("white")

    # ----- INVENTORY -----
    inventory_ui = create_inventory_ui()
    inv_p1, inv_p2 = create_inventories()
    game_state["inventory_p1"] = inv_p1
    game_state["inventory_p2"] = inv_p2

    def update_inv(gs):
        update_inventory_ui(gs, inventory_ui)

    # ----- HEALTHBARS -----
    p2_healthbar, p1_healthbar = create_healthbars()

    # ----- PROFESSOR -----
    professor = create_professor()
    professor.hideturtle()

    # ----- ITEMS -----
    drawers = create_drawers()
    bagpack = create_bagpack()
    key_turtle, key_drawer, bike_key = create_keys(drawers, bagpack)

    def prepare_for_stage2():
        from story_screens import show_story_4
        show_story_4(screen)

    def check_exit():
        if not game_state["game_over"]:
            check_stage_complete(
                screen, game_state,
                player1, player2,
                professor, message,
                prepare_for_stage2
            )

    # ----- ACTION KEYS -----
    def p1_search():
        if not game_state["game_over"]:
            search_drawers_for_player(player1, drawers, key_drawer, key_turtle, message, game_state)

    def p2_search():
        if not game_state["game_over"]:
            search_drawers_for_player(player2, drawers, key_drawer, key_turtle, message, game_state)

    def open_bag():
        if not game_state["game_over"]:
            open_near_bagpack(player1, player2, bagpack, bike_key, message, game_state)

    def pickup_item():
        if not game_state["game_over"]:
            pick_up_near_item(player1, player2, key_turtle, bike_key, message, game_state, update_inv)

    # ----- PROFESSOR MOVEMENT -----
    def ai_tick():
        move_professor(
            screen, professor,
            player1, player2,
            game_state, p1_healthbar, p2_healthbar,
            message, update_healthbars
        )

        if game_state["p1_health"] <= 0 or game_state["p2_health"] <= 0:
            handle_game_over()

    professor_stays(screen, professor, message, ai_tick)

    # ----- CONTROLS -----
    bind_player_controls(screen, player1, player2, game_state, extra_callback=check_exit)

    screen.onkey(p1_search, "space")
    screen.onkey(p2_search, "Return")
    screen.onkey(open_bag, "o")
    screen.onkey(pickup_item, "p")

    # ----- START AREA DELAY -----
    for key in ["w","a","s","d","Up","Down","Left","Right"]:
        screen.onkeypress(None, key)

    def unlock():
        bind_player_controls(screen, player1, player2, game_state, extra_callback=check_exit)

    screen.ontimer(unlock, 2500)

    # ----- SHOW EVERYTHING -----
    screen.bgpic("stage_1/stage_1.gif")
    screen.title("Stage 1")

    for obj in [player1, player2, professor, *drawers, bagpack, p1_healthbar, p2_healthbar, inventory_ui]:
        obj.showturtle()

    screen.tracer(1)
    screen.update()