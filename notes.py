# notes.py
import turtle
import random
from PIL import Image
from collision import add_block, blocked_area

# ===== FILE I/O: READ CODE FROM FILE =====
f = open("note_code.txt", "r")
NOTE_CODE = f.read().strip()
f.close()

correct_keypad_code = NOTE_CODE

correct_keypad_code = "1121"

note_image = "note_small.gif"
popup_note_image = "note_popup.gif"

note_positions = [
    (-333, 148),
    (357, 164),
    (320, -30),
    (344, -194)
]

# globals
screen = None
player1 = None
player2 = None
message_turtle = None

notes = []
note_state = []     # "hidden" or "revealed"
note_digits = []    # shuffled digits from NOTE_CODE
DOOR_BLOCK = (-140, -260, -60, -60)
keypad_pad = None   # yellow square trigger

# door / keypad popup
storage_locked = True
popup_open = False
entered_code = ""
popup_bg = None
popup_title = None
popup_digits = None

# ========== STAGE 2 SAFE MOVEMENT ==========
def can_move(x, y):
    # For Stage 2, allow movement everywhere except blocked walls.
    return True

# ======================================
# SIMPLE MESSAGE
# ======================================
def show_message(text, duration=2000):
    message_turtle.clear()
    message_turtle.write(text, align="center", font=("Arial", 18, "bold"))
    screen.ontimer(message_turtle.clear, duration)


# ======================================
# NOTES: REVEAL + OPEN
# ======================================
def reveal_note(player):
    px = player.xcor()
    py = player.ycor()

    i = 0
    while i < len(notes):
        nx = notes[i].xcor()
        ny = notes[i].ycor()

        if px > nx - 50 and px < nx + 50 and py > ny - 50 and py < ny + 50:
            if note_state[i] == "hidden":
                notes[i].showturtle()
                note_state[i] = "revealed"
                show_message("Press O to open the note.", 1500)
            return True
        i += 1

    return False


def open_note():
    # check both players
    p_index = 0
    while p_index < 2:
        if p_index == 0:
            p = player1
        else:
            p = player2

        px = p.xcor()
        py = p.ycor()

        i = 0
        while i < len(notes):
            if note_state[i] == "revealed":
                nx = notes[i].xcor()
                ny = notes[i].ycor()
                if px > nx - 50 and px < nx + 50 and py > ny - 50 and py < ny + 50:
                    show_note_popup(note_digits[i])
                    return
            i += 1

        p_index += 1


def show_note_popup(digit):
    t = turtle.Turtle()
    t.penup()
    t.hideturtle()
    t.goto(0, 0)

    try:
        if popup_note_image not in screen.getshapes():
            screen.register_shape(popup_note_image)
        t.shape(popup_note_image)
        t.showturtle()
    except:
        t.write("NOTE", align="center", font=("Arial", 30, "bold"))

    t.write("\n" + str(digit), align="center", font=("Arial", 26, "bold"))

    def remove():
        t.clear()
        t.hideturtle()

    screen.ontimer(remove, 3000)


# ======================================
# MOVEMENT FILTER FOR movement.py
# (right now we let everything pass; walls are collision.add_block)
# ======================================
def can_move(x, y):
    return True


# ======================================
# KEYPAD TRIGGER (YELLOW PAD)
# ======================================
def try_open_keypad(player):
    if not storage_locked:
        return False

    px = player.xcor()
    py = player.ycor()

    kx = keypad_pad.xcor()
    ky = keypad_pad.ycor()

    if px > kx - 100 and px < kx + 100 and py > ky - 100 and py < ky + 100:
        open_code_popup()
        return True

    return False


# ======================================
# CODE POPUP 
# ======================================
def open_code_popup():
    global popup_open, entered_code
    global popup_bg, popup_title, popup_digits

    if popup_open:
        return

    popup_open = True
    entered_code = ""

    # gray background
    popup_bg = turtle.Turtle()
    popup_bg.penup()
    popup_bg.hideturtle()
    popup_bg.shape("square")
    popup_bg.color("lightgray")
    popup_bg.shapesize(10, 14)
    popup_bg.goto(0, 0)
    popup_bg.showturtle()

    # title
    popup_title = turtle.Turtle()
    popup_title.penup()
    popup_title.hideturtle()
    popup_title.color("black")
    popup_title.goto(0, 30)

    # check if all notes are revealed
    all_revealed = True
    i = 0
    while i < len(note_state):
        if note_state[i] == "hidden":
            all_revealed = False
        i += 1

    if all_revealed:
        title = "ENTER 4-DIGIT CODE\n(Hint: Professor's favorite numbers)"
    else:
        title = "ENTER 4-DIGIT CODE\n Find notes for a hint!"

    popup_title.write(title, align="center", font=("Arial", 14, "bold"))

    # digits display
    popup_digits = turtle.Turtle()
    popup_digits.penup()
    popup_digits.hideturtle()
    popup_digits.color("black")
    popup_digits.goto(0, -10)
    popup_digits.write("____", align="center", font=("Arial", 26, "bold"))

    # bind digits WITHOUT lambda
    bind_digit_keys()
    screen.listen()


def bind_digit_keys():
    screen.onkey(record_digit_0, "0")
    screen.onkey(record_digit_1, "1")
    screen.onkey(record_digit_2, "2")
    screen.onkey(record_digit_3, "3")
    screen.onkey(record_digit_4, "4")
    screen.onkey(record_digit_5, "5")
    screen.onkey(record_digit_6, "6")
    screen.onkey(record_digit_7, "7")
    screen.onkey(record_digit_8, "8")
    screen.onkey(record_digit_9, "9")


def record_digit_0():
    type_digit("0")


def record_digit_1():
    type_digit("1")


def record_digit_2():
    type_digit("2")


def record_digit_3():
    type_digit("3")


def record_digit_4():
    type_digit("4")


def record_digit_5():
    type_digit("5")


def record_digit_6():
    type_digit("6")


def record_digit_7():
    type_digit("7")


def record_digit_8():
    type_digit("8")


def record_digit_9():
    type_digit("9")


def type_digit(d):
    global entered_code

    if not popup_open:
        return

    entered_code = entered_code + d

    popup_digits.clear()
    popup_digits.write(entered_code, align="center", font=("Arial", 26, "bold"))

    if len(entered_code) == 4:
        if entered_code == correct_keypad_code:
            unlock_storage()
        else:
            popup_digits.goto(0, -40)
            popup_digits.write("WRONG", align="center", font=("Arial", 20, "bold"))
            screen.ontimer(close_code_popup, 1000)


def unlock_storage():
    global storage_locked
    storage_locked = False
    #remove teh door block
    if DOOR_BLOCK in blocked_area:
        blocked_area.remove(DOOR_BLOCK)  # remove door block
    
    
    show_message("Door unlocked!", 2000)
    close_code_popup()


def close_code_popup():
    global popup_open

    popup_open = False

    try:
        popup_bg.clear()
        popup_bg.hideturtle()
        popup_title.clear()
        popup_digits.clear()
    except:
        pass


# ======================================
# SPACE / RETURN HANDLERS
# ======================================
def handle_space():
    # P1: keypad → note → drink
    if try_open_keypad(player1):
        return
    if reveal_note(player1):
        return

    try:
        import invisibility
        invisibility.check_drink_pickup(player1)
    except:
        pass


def handle_return():
    # P2: keypad → note → drink
    if try_open_keypad(player2):
        return
    if reveal_note(player2):
        return

    try:
        import invisibility
        invisibility.check_drink_pickup(player2)
    except:
        pass


# ======================================
# SETUP (CALL FROM stage2)
# ======================================
def setup_notes(scr, p1, p2, hp1, hp2, msg_turtle):
    global screen, player1, player2, message_turtle
    global notes, note_state, keypad_pad, note_digits

    screen = scr
    player1 = p1
    player2 = p2
    message_turtle = msg_turtle

    # shuffle digits from "1121"
    digits = list(NOTE_CODE)
    random.shuffle(digits)
    note_digits = digits[:]

    # register note sprite
    if note_image not in screen.getshapes():
        screen.register_shape(note_image)

    # spawn notes (hidden)
    notes[:] = []
    note_state[:] = []

    i = 0
    while i < len(note_positions):
        pos = note_positions[i]
        n = turtle.Turtle()
        n.penup()
        n.goto(pos)
        n.shape(note_image)
        n.hideturtle()
        notes.append(n)
        note_state.append("hidden")
        i += 1

    # storage door block (collision rectangle)
    add_block(*DOOR_BLOCK)

    
    # === KEYPAD TRIGGER USING keypad.gif ===
    if "keypad/keypad.gif" not in screen.getshapes():
        screen.register_shape("keypad/keypad.gif")

    keypad_pad = turtle.Turtle()
    keypad_pad.penup()
    keypad_pad.shape("keypad/keypad.gif")
    keypad_pad.goto(-116.2555720653789, -225.24064171122996)

  
    
    # key bindings
    screen.onkey(handle_space, "space")
    screen.onkey(handle_return, "Return")
    screen.onkey(open_note, "o")

    screen.listen()

    print("Notes initialized. Digits:", note_digits)
