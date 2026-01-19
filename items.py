# items.py
import turtle
import random
from inventory import debug_print_inventories


def create_drawers():
    drawers = []
    drawer_positions = [(-450, 220), (-370, 220), (-290, 220),
                        (-210, 220), (-120, 220)]
    for pos in drawer_positions:
        d = turtle.Turtle()
        d.hideturtle()
        d.shape("blank")    # prevents triangle flashing
        d.penup()
        d.goto(pos)
        drawers.append(d)
    return drawers


def create_bagpack():
    bag = turtle.Turtle()
    bag.hideturtle()
    bag.shape("blank")      # prevents triangle flashing
    bag.penup()
    bag.goto(-295, -110)
    return bag


def create_keys(drawers, bagpack):
    key_turtle = turtle.Turtle()
    key_turtle.hideturtle()
    key_turtle.shape("blank")                        # invisible at start
    key_turtle.real_shape = "stage_1/exit_door_key.gif"
    key_turtle.penup()
    key_drawer = random.choice(drawers)
    key_turtle.goto(key_drawer.xcor(), key_drawer.ycor())

    bike_key = turtle.Turtle()
    bike_key.hideturtle()
    bike_key.shape("blank")                          # invisible at start
    bike_key.real_shape = "stage_1/exit_door_key.gif"
    bike_key.penup()
    bike_key.goto(bagpack.xcor(), bagpack.ycor() + 25)

    return key_turtle, key_drawer, bike_key


def search_drawers_for_player(player, drawers, key_drawer, key_turtle,
                              message_turtle, game_state):
    for d in drawers:
        if player.distance(d) < 50:
            message_turtle.clear()
            if "exit key" not in game_state["keys_collected"]:
                if d == key_drawer:
                    game_state["keys_collected"].append("exit key")

                    # reveal exit key using correct shape
                    key_turtle.shape(key_turtle.real_shape)
                    key_turtle.goto(d.xcor(), d.ycor() + 25)
                    key_turtle.showturtle()

                    message_turtle.write(
                        "✅ Exit key found!",
                        align="center",
                        font=("Arial", 16, "bold"),
                    )
                else:
                    message_turtle.write(
                        "🗄️ Nothing here...",
                        align="center",
                        font=("Arial", 16, "bold"),
                    )
            else:
                message_turtle.write(
                    "🗄️ Drawer already checked.",
                    align="center",
                    font=("Arial", 16, "bold"),
                )
            return

    message_turtle.clear()
    message_turtle.write(
        "Not near a drawer!",
        align="center",
        font=("Arial", 16, "bold"),
    )


def open_bagpack_if_close(player, bagpack, bike_key, message_turtle, game_state):
    if player.distance(bagpack) < 90:
        message_turtle.clear()
        if "bike key" not in game_state["keys_collected"]:

            # reveal bike key using its real shape
            bike_key.shape(bike_key.real_shape)
            bike_key.showturtle()

            message_turtle.write(
                "🎒 You opened the bagpack... found a key inside!",
                align="center",
                font=("Arial", 16, "bold"),
            )
        else:
            message_turtle.write(
                "🎒 The bagpack is empty now.",
                align="center",
                font=("Arial", 16, "bold"),
            )
    else:
        message_turtle.clear()
        message_turtle.write(
            "You're too far from the bagpack.",
            align="center",
            font=("Arial", 16, "bold"),
        )


def open_near_bagpack(player1, player2, bagpack, bike_key, message_turtle, game_state):
    if player1.distance(bagpack) < 90:
        open_bagpack_if_close(player1, bagpack, bike_key, message_turtle, game_state)
    elif player2.distance(bagpack) < 90:
        open_bagpack_if_close(player2, bagpack, bike_key, message_turtle, game_state)
    else:
        message_turtle.clear()
        message_turtle.write(
            "You're too far from the bagpack.",
            align="center",
            font=("Arial", 16, "bold"),
        )


def _pick_up_item_core(player, inventory, key_turtle, bike_key,
                       message_turtle, game_state, update_inventory_ui_func):

    # Exit key pickup
    if key_turtle.isvisible() and player.distance(key_turtle) < 70:
        key_turtle.hideturtle()
        inventory.append("Exit Key")
        game_state["keys_collected"].append("exit key")
        message_turtle.clear()
        message_turtle.write(
            "🗝️ Exit Key picked up!",
            align="center",
            font=("Arial", 16, "bold"),
        )
        debug_print_inventories(game_state["inventory_p1"], game_state["inventory_p2"])
        update_inventory_ui_func(game_state)
        return

    # Bike key pickup
    if bike_key.isvisible() and player.distance(bike_key) < 60:
        bike_key.hideturtle()
        inventory.append("Bike Key")
        game_state["keys_collected"].append("bike key")
        message_turtle.clear()
        message_turtle.write(
            "🔑 Bike Key picked up!",
            align="center",
            font=("Arial", 16, "bold"),
        )
        debug_print_inventories(game_state["inventory_p1"], game_state["inventory_p2"])
        update_inventory_ui_func(game_state)
        return

    message_turtle.clear()
    message_turtle.write(
        "Nothing to pick up here.",
        align="center",
        font=("Arial", 16, "bold"),
    )


def pick_up_near_item(player1, player2,
                      key_turtle, bike_key,
                      message_turtle, game_state, update_inventory_ui_func):

    if key_turtle.isvisible():
        if player1.distance(key_turtle) < 90:
            _pick_up_item_core(player1, game_state["inventory_p1"],
                               key_turtle, bike_key, message_turtle,
                               game_state, update_inventory_ui_func)
            return
        elif player2.distance(key_turtle) < 90:
            _pick_up_item_core(player2, game_state["inventory_p2"],
                               key_turtle, bike_key, message_turtle,
                               game_state, update_inventory_ui_func)
            return

    if bike_key.isvisible():
        if player1.distance(bike_key) < 90:
            _pick_up_item_core(player1, game_state["inventory_p1"],
                               key_turtle, bike_key, message_turtle,
                               game_state, update_inventory_ui_func)
            return
        elif player2.distance(bike_key) < 90:
            _pick_up_item_core(player2, game_state["inventory_p2"],
                               key_turtle, bike_key, message_turtle,
                               game_state, update_inventory_ui_func)
            return

    message_turtle.clear()
    message_turtle.write(
        "Nothing to pick up here.",
        align="center",
        font=("Arial", 16, "bold"),
    )