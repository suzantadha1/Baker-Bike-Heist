# stage_3.py
import turtle

def start_stage3(screen, p1_health, p2_health):

    # ---------- RESET SCREEN ----------
    screen.onclick(None)
    screen.clear()
    screen.bgcolor("black")
    screen.bgpic("img/classroom.gif")
    screen.title("Fourth Floor Heist - Stage 3")

    # ---------- GIF SIZE ----------
    gif_width = 1350
    gif_height = 770

    # ---------- MAP BOUNDARIES ----------
    x_min, x_max = -gif_width//2, gif_width//2
    y_min, y_max = -gif_height//2, gif_height//2

    # ---------- PLAYER SPEED ----------
    player_speed = 20

    # ---------- REGISTER PLAYER SHAPES ----------
    player_shapes = {
        "P1": {
            "front": "stage_1/P1_front.gif",
            "back": "stage_1/P1_back.gif",
            "left": "stage_1/P1_left.gif",
            "right": "stage_1/P1_right.gif"
        },
        "P2": {
            "front": "stage_1/P2_front.gif",
            "back": "stage_1/P2_back.gif",
            "left": "stage_1/P2_left.gif",
            "right": "stage_1/P2_right.gif"
        }
    }

    for key in player_shapes:
        for shape in player_shapes[key].values():
            screen.register_shape(shape)

    # ---------- CREATE PLAYERS ----------
    player1 = turtle.Turtle()
    player1.shape(player_shapes["P1"]["front"])
    player1.penup()
    player1.goto(0, 0)

    player2 = turtle.Turtle()
    player2.shape(player_shapes["P2"]["front"])
    player2.penup()
    player2.goto(80, 0)

    players = [player1, player2]

    # ---------- CLAMP ----------
    def clamp_player(player):
        x = min(max(player.xcor(), x_min), x_max)
        y = min(max(player.ycor(), y_min), y_max)
        player.goto(x, y)

    # ---------- MOVEMENT ----------
    def move_up_p1():
        player1.shape(player_shapes["P1"]["back"])
        player1.sety(player1.ycor() + player_speed)
        clamp_player(player1)

    def move_down_p1():
        player1.shape(player_shapes["P1"]["front"])
        player1.sety(player1.ycor() - player_speed)
        clamp_player(player1)

    def move_left_p1():
        player1.shape(player_shapes["P1"]["left"])
        player1.setx(player1.xcor() - player_speed)
        clamp_player(player1)

    def move_right_p1():
        player1.shape(player_shapes["P1"]["right"])
        player1.setx(player1.xcor() + player_speed)
        clamp_player(player1)

    def move_up_p2():
        player2.shape(player_shapes["P2"]["back"])
        player2.sety(player2.ycor() + player_speed)
        clamp_player(player2)

    def move_down_p2():
        player2.shape(player_shapes["P2"]["front"])
        player2.sety(player2.ycor() - player_speed)
        clamp_player(player2)

    def move_left_p2():
        player2.shape(player_shapes["P2"]["left"])
        player2.setx(player2.xcor() - player_speed)
        clamp_player(player2)

    def move_right_p2():
        player2.shape(player_shapes["P2"]["right"])
        player2.setx(player2.xcor() + player_speed)
        clamp_player(player2)

    # ---------- KEY BINDINGS ----------
    screen.listen()
    screen.onkey(move_up_p1, "w")
    screen.onkey(move_down_p1, "s")
    screen.onkey(move_left_p1, "a")
    screen.onkey(move_right_p1, "d")
    screen.onkey(move_up_p2, "Up")
    screen.onkey(move_down_p2, "Down")
    screen.onkey(move_left_p2, "Left")
    screen.onkey(move_right_p2, "Right")

    # ==========================================
    # MESSAGE SYSTEM
    # ==========================================
    message_turtle = turtle.Turtle()
    message_turtle.hideturtle()
    message_turtle.penup()
    message_turtle.color("white")
    message_turtle.goto(0, -350)

    def show_message(text, color="white"):
        message_turtle.clear()
        message_turtle.color(color)
        message_turtle.write(text, align="center", font=("Arial", 24, "bold"))
        screen.ontimer(message_turtle.clear, 1500)

    # ==========================================
    # HEALTHBARS
    # ==========================================
    healthbar_images = {}
    for hp in [00, 20, 40, 50, 60, 70, 80, 90, 100]:
        hp_str = f"{hp:02}"
        path = f"stage_1/healthbars/hp{hp_str}_small.gif"
        screen.addshape(path)
        healthbar_images[hp] = path

    p1_hp = p1_health
    p2_hp = p2_health

    def get_hp_image(hp):
        hp = max(0, min(100, hp))
        nearest = max([h for h in healthbar_images if h <= hp])
        return healthbar_images[nearest]

    hp1 = turtle.Turtle()
    hp1.penup()
    hp1.goto(-600, 350)
    hp1.shape(get_hp_image(p1_hp))

    hp2 = turtle.Turtle()
    hp2.penup()
    hp2.goto(600, 350)
    hp2.shape(get_hp_image(p2_hp))

    def update_health_bar():
        hp1.shape(get_hp_image(p1_hp))
        hp2.shape(get_hp_image(p2_hp))

    def apply_wrong_code_damage():
        nonlocal p1_hp, p2_hp
        p1_hp -= 10
        p2_hp -= 10
        update_health_bar()

    # ==========================================
    # DOOR SYSTEM
    # ==========================================
    DOOR_LEFT   = -463
    DOOR_RIGHT  = -293
    DOOR_BOTTOM = 78
    DOOR_TOP    = 274

    def player_in_door(player):
        x, y = player.position()
        return (DOOR_LEFT <= x <= DOOR_RIGHT and
                DOOR_BOTTOM <= y <= DOOR_TOP)

    SECRET_CODE = "203520"
    MAX_ATTEMPTS = 10
    door_attempts = 0

    def ask_door_code(player):
        nonlocal door_attempts
        user_input = screen.textinput("Door Code", "Enter door code:")

        if user_input == SECRET_CODE:
            from story_screens import show_story_6

            # 🔥 STOP AI COMPLETELY before showing story
            from professor_ai import PROFESSOR_AI_ENABLED
            PROFESSOR_AI_ENABLED = False

            # 🔥 ONLY show the story screen
            #    Stage 4 will start WHEN USER CLICKS THE BUTTON
            show_story_6(screen, p1_hp, p2_hp)

            return
 
        door_attempts += 1
        apply_wrong_code_damage()
        show_message("Wrong code!", "red")

        if door_attempts < MAX_ATTEMPTS:
            ask_door_code(player)


    # ==========================================
    # INTERACTABLES
    # ==========================================
    screen.register_shape("img/whiteboard_overlay.gif")
    screen.register_shape("img/paper_overlay.gif")
    screen.register_shape("img/announcement_overlay.gif")

    whiteboard_overlay = turtle.Turtle()
    paper_overlay = turtle.Turtle()
    announcement_overlay = turtle.Turtle()

    for overlay in [whiteboard_overlay, paper_overlay, announcement_overlay]:
        overlay.hideturtle()
        overlay.penup()

    whiteboard_center = (0, 240)
    whiteboard_size = (700, 100)

    paper_center = (0, -100)
    paper_size = (300, 200)

    announcement_center = (450, 250)
    announcement_size = (240, 240)

    def try_open_interactable():
        for player in players:
            px, py = player.position()

            # WHITEBOARD
            left = whiteboard_center[0] - whiteboard_size[0]/2
            right = whiteboard_center[0] + whiteboard_size[0]/2
            bottom = whiteboard_center[1] - whiteboard_size[1]/2
            top = whiteboard_center[1] + whiteboard_size[1]/2

            if left <= px <= right and bottom <= py <= top:
                whiteboard_overlay.goto(0, 0)
                whiteboard_overlay.shape("img/whiteboard_overlay.gif")
                whiteboard_overlay.showturtle()
                return

            # PAPER
            left = paper_center[0] - paper_size[0]/2
            right = paper_center[0] + paper_size[0]/2
            bottom = paper_center[1] - paper_size[1]/2
            top = paper_center[1] + paper_size[1]/2

            if left <= px <= right and bottom <= py <= top:
                paper_overlay.goto(0, 0)
                paper_overlay.shape("img/paper_overlay.gif")
                paper_overlay.showturtle()
                return

            # ANNOUNCEMENT
            left = announcement_center[0] - announcement_size[0]/2
            right = announcement_center[0] + announcement_size[0]/2
            bottom = announcement_center[1] - announcement_size[1]/2
            top = announcement_center[1] + announcement_size[1]/2

            if left <= px <= right and bottom <= py <= top:
                announcement_overlay.goto(0, 0)
                announcement_overlay.shape("img/announcement_overlay.gif")
                announcement_overlay.showturtle()
                return

            # DOOR
            if player_in_door(player):
                ask_door_code(player)
                return

    screen.onkey(try_open_interactable, "e")

    # CLOSE overlays with Q
    def close_any_overlay():
        whiteboard_overlay.hideturtle()
        paper_overlay.hideturtle()
        announcement_overlay.hideturtle()

    screen.onkey(close_any_overlay, "q")

    show_message("Find the code and escape the classroom!")
