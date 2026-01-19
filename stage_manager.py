import turtle

def check_stage_complete(
    screen, game_state,
    player1, player2,
    professor, message_turtle,
    prepare_for_stage2_callback
):
    """
    Checks exit conditions for Stage 1.
    Handles waiting messages, key checks, and safe transition.
    """

    # ===== EXIT DOOR HITBOX =====
    x_min, x_max = 155, 245
    y_min, y_max = -300, -155

    p1_in = x_min <= player1.xcor() <= x_max and y_min <= player1.ycor() <= y_max
    p2_in = x_min <= player2.xcor() <= x_max and y_min <= player2.ycor() <= y_max

    # ===== Key checks (safe) =====
    p1_inv = game_state.get("inventory_p1", [])
    p2_inv = game_state.get("inventory_p2", [])

    has_exit_key = ("Exit Key" in p1_inv) or ("Exit Key" in p2_inv)
    has_bike_key = ("Bike Key" in p1_inv) or ("Bike Key" in p2_inv)

    # Clear previous message
    message_turtle.clear()
    message_turtle.color("white")

    # ===== One player inside, the other not =====
    if p1_in ^ p2_in:
        message_turtle.write(
            "⏳ Waiting for the other player...",
            align="center", font=("Arial", 16, "bold")
        )
        return

    # ===== Both players inside =====
    if p1_in and p2_in:

        # Reset message position ALWAYS
        message_turtle.clear()
        message_turtle.goto(0, 140)

        # ---- Missing keys ----
        if not has_exit_key or not has_bike_key:
            message_turtle.color("white")
            message_turtle.write(
                "❗ You need BOTH keys to leave!",
                align="center", font=("Arial", 18, "bold")
            )
            return

        # ===== Use Exit Key (safe remove) =====
        used_by = ""
        if "Exit Key" in p1_inv:
            p1_inv.remove("Exit Key")
            used_by = "Player 1"
        elif "Exit Key" in p2_inv:
            p2_inv.remove("Exit Key")
            used_by = "Player 2"

        # ===== Display messages =====
        message_turtle.color("yellow")
        message_turtle.goto(0, 140)
        message_turtle.write(
            f"🔓 {used_by} used the Exit Key!",
            align="center", font=("Arial", 16, "bold")
        )

        message_turtle.goto(0, 0)
        message_turtle.color("gold")
        message_turtle.write(
            "Stage 1 Complete!\nPreparing Stage 2...",
            align="center", font=("Arial", 26, "bold")
        )

        # Stop professor + freeze logic
        professor.hideturtle()
        game_state["game_over"] = True

        # ===== Move to next stage =====
        screen.ontimer(prepare_for_stage2_callback, 2500)