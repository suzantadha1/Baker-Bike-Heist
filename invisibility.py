# invisibility.py
import turtle

# --- Globals ---
drinks = []        # list of drink turtles (or None after used)
players = []       # [player1, player2]
screen_ref = None  # Screen reference
INVIS_DURATION = 30000  # 30 seconds

# -------------------------------------------------
# SETUP DRINKS (NO KEY BINDINGS HERE)
# -------------------------------------------------
def setup_drinks(screen, player1, player2, positions):
    """
    Create drink turtles at given positions.
    DOES NOT bind keys. Keys are handled in notes.py
    """
    global drinks, players, screen_ref
    screen_ref = screen
    players = [player1, player2]

    drinks = []
    i = 0
    while i < len(positions):
        pos = positions[i]
        drink = turtle.Turtle()
        drink.penup()
        drink.goto(pos)
        drink.shape("invisible_players/drink.gif")
        drinks.append(drink)
        i = i + 1

    # Make sure players have invisibility flags
    j = 0
    while j < len(players):
        p = players[j]
        if not hasattr(p, "is_invisible"):
            p.is_invisible = False
        if not hasattr(p, "facing"):
            p.facing = "front"
        j = j + 1

    # NOTE: keys are handled in notes.handle_space / handle_return
    # by calling invisibility.check_drink_pickup(player)
    # So nothing else here.


# -------------------------------------------------
# PUBLIC: check_drink_pickup(player)
# Called from notes.handle_space / handle_return
# -------------------------------------------------
def check_drink_pickup(player):
    """
    Called when player presses space/return in notes.handle_space/handle_return.
    If the player is close to a drink, they drink it and become invisible.
    """
    # Find which index this player is (0 or 1)
    index = -1
    k = 0
    while k < len(players):
        if players[k] is player:
            index = k
            break
        k = k + 1

    if index == -1:
        return   # player not found

    i = 0
    while i < len(drinks):
        drink = drinks[i]
        if drink is not None:
            dx = player.xcor() - drink.xcor()
            dy = player.ycor() - drink.ycor()
            if dx > -60 and dx < 60 and dy > -60 and dy < 60:
                # Player is close enough: drink it
                player.is_invisible = True
                set_invisible_sprite(player)

                # Change drink sprite to empty
                drink.shape("invisible_players/empty_drink.gif")
                drinks[i] = None  # mark as used

                # Schedule invisibility end after 30 seconds
                if index == 0:
                    turtle.ontimer(remove_invisibility_p1, INVIS_DURATION)
                elif index == 1:
                    turtle.ontimer(remove_invisibility_p2, INVIS_DURATION)
                return
        i = i + 1


# -------------------------------------------------
# Helper: schedule remove for each player index
# -------------------------------------------------
def remove_invisibility_p1():
    if len(players) > 0:
        remove_invisibility(players[0])


def remove_invisibility_p2():
    if len(players) > 1:
        remove_invisibility(players[1])


# -------------------------------------------------
# SPRITE HANDLING
# -------------------------------------------------
def set_invisible_sprite(player):
    """
    Sets invisible sprite based on player index and facing.
    """
    # Find player index
    index = -1
    i = 0
    while i < len(players):
        if players[i] is player:
            index = i
            break
        i = i + 1

    if index == -1:
        return

    facing = player.facing

    # shape map for each player
    if index == 0:
        if facing == "front":
            player.shape("invisible_players/p1_invisibility_front.gif")
        elif facing == "back":
            player.shape("invisible_players/p1_invisibility_back.gif")
        elif facing == "left":
            player.shape("invisible_players/p1_invisibility_left.gif")
        elif facing == "right":
            player.shape("invisible_players/p1_invisibility_right.gif")
    elif index == 1:
        if facing == "front":
            player.shape("invisible_players/p2_invisibility_front.gif")
        elif facing == "back":
            player.shape("invisible_players/p2_invisibility_back.gif")
        elif facing == "left":
            player.shape("invisible_players/p2_invisibility_left.gif")
        elif facing == "right":
            player.shape("invisible_players/p2_invisibility_right.gif")


def update_player_direction(player, direction):
    """
    Called by movement.py when player moves.
    If invisible: update invisible sprite.
    If not invisible: use original sprites.
    """
    player.facing = direction

    if player.is_invisible:
        set_invisible_sprite(player)
    else:
        # back to normal sprites
        if hasattr(player, "front"):
            if direction == "front":
                player.shape(player.front)
            elif direction == "back":
                player.shape(player.back)
            elif direction == "left":
                player.shape(player.left_img)
            elif direction == "right":
                player.shape(player.right_img)


def remove_invisibility(player):
    """
    Revert to normal sprites after timer.
    """
    if player.is_invisible:
        player.is_invisible = False
        update_player_direction(player, player.facing)
