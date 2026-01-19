

# player.py
import turtle
from sprites import healthbar_images

# ============================================
#  PLAYER CREATION (UNIVERSAL)
# ============================================
def create_player(front, back, left_img, right_img, start_x, start_y):
   """
   Creates a player with 4-direction sprite support.
   """
   t = turtle.Turtle()
   t.hideturtle()
   t.penup()
   t.speed(0)


   t.front = front
   t.back = back
   t.left_img = left_img
   t.right_img = right_img


   t.shape(front)
   t.goto(start_x, start_y)
   t.showturtle()


   return t




# ============================================
#  BASIC WALL BOUNDARIES
# ============================================
def handle_wall_collision(t, x_min=-480, x_max=480, y_min=-270, y_max=270):
   if t.xcor() < x_min:
       t.setx(x_min)
   if t.xcor() > x_max:
       t.setx(x_max)
   if t.ycor() < y_min:
       t.sety(y_min)
   if t.ycor() > y_max:
       t.sety(y_max)




# ============================================
#  SPRITE FACING HELPERS
# ============================================
def update_player_sprite(player, direction):
   """
   Applies the correct sprite based on movement direction.
   """
   if direction == "up":
       player.shape(player.back)
   elif direction == "down":
       player.shape(player.front)
   elif direction == "left":
       player.shape(player.left_img)
   elif direction == "right":
       player.shape(player.right_img)




# ============================================
#  HITBOX HELPERS
# ============================================
def is_near(player, target, distance=50):
   return player.distance(target) < distance




def is_in_rectangle(player, x_min, x_max, y_min, y_max):
   return (x_min <= player.xcor() <= x_max) and (y_min <= player.ycor() <= y_max)




# ============================================
#  HEALTH BAR CREATION
# ============================================
def create_healthbars():
   p1 = turtle.Turtle()
   p1.hideturtle()
   p1.penup()
   p1.goto(410, 255)
   p1.shape(healthbar_images[100])


   p2 = turtle.Turtle()
   p2.hideturtle()
   p2.penup()
   p2.goto(-410, 255)
   p2.shape(healthbar_images[100])


   return p1, p2




# ============================================
#  HEALTH BAR UPDATER
# ============================================
def _closest_health_bar(value):
   levels = sorted(healthbar_images.keys(), reverse=True)
   for h in levels:
       if value >= h:
           return healthbar_images[h]
   return healthbar_images[0]




def update_healthbars(game_state, p1_healthbar, p2_healthbar):
   p1_healthbar.shape(_closest_health_bar(game_state["p1_health"]))
   p2_healthbar.shape(_closest_health_bar(game_state["p2_health"]))


# ============================================
#  UNIVERSAL PLAYER SPAWNER FOR ALL STAGES
# ============================================
def create_default_players(p1_start, p2_start):
   """
   Creates P1 and P2 using the standard sprite set used across all stages.
   """
   player1 = create_player(
       "stage_1/P1_front.gif",
       "stage_1/P1_back.gif",
       "stage_1/P1_left.gif",
       "stage_1/P1_right.gif",
       p1_start[0], p1_start[1]
   )

   player2 = create_player(
       "stage_1/P2_front.gif",
       "stage_1/P2_back.gif",
       "stage_1/P2_left.gif",
       "stage_1/P2_right.gif",
       p2_start[0], p2_start[1]
   )


   return player1, player2
"""
Unified movement for ALL stages.
Handles boundaries, sprite facing, and keybindings.
Stages only call: bind_player_controls(screen, p1, p2, game_state, extra_callback=None)
"""


import sys
sys.path.append('/usercode')


from collision import is_blocked
import notes
import invisibility # Import the invisibility module


# ===== WORLD BOUNDS =====
HALF_W = 480
HALF_H = 270
MARGIN = 32


MIN_X = -HALF_W + MARGIN
MAX_X = HALF_W - MARGIN
MIN_Y = -HALF_H + MARGIN
MAX_Y = HALF_H - MARGIN




# ===== MOVEMENT =====


def update_sprite_direction(t, direction):
   """
   Updates the player's sprite and facing direction.
   Checks for invisibility status if the attribute exists.
   """
   t.facing = direction
  
   # If the player has the 'is_invisible' attribute, use the invisibility logic
   if hasattr(t, 'is_invisible'):
       # Pass the direction to the invisibility handler
       invisibility.update_player_direction(t, direction)
   else:
       # Otherwise, use the standard sprite logic for other stages
       # Note: 'up' direction uses the 'back' image, 'down' uses the 'front' image
       if direction == "back":
           t.shape(t.back)
       elif direction == "front":
           t.shape(t.front)
       elif direction == "left":
           t.shape(t.left_img)
       elif direction == "right":
           t.shape(t.right_img)




def move_up(t, speed):
   # Changed "up" to "back"
   update_sprite_direction(t, "back")
   new_x = t.xcor()
   new_y = t.ycor() + speed
   if new_y <= MAX_Y and not is_blocked(new_x, new_y) and notes.can_move(new_x, new_y):
       t.sety(new_y)
  




def move_down(t, speed):
   # Changed "down" to "front"
   update_sprite_direction(t, "front")
   new_x = t.xcor()
   new_y = t.ycor() - speed
   if new_y >= MIN_Y and not is_blocked(new_x, new_y) and notes.can_move(new_x, new_y):
       t.sety(new_y)
  




def move_left(t, speed):
   update_sprite_direction(t, "left")
   new_x = t.xcor() - speed
   new_y = t.ycor()
   if new_x >= MIN_X and not is_blocked(new_x, new_y) and notes.can_move(new_x, new_y):
       t.setx(new_x)




def move_right(t, speed):
   update_sprite_direction(t, "right")
   new_x = t.xcor() + speed
   new_y = t.ycor()
   if new_x <= MAX_X and not is_blocked(new_x, new_y) and notes.can_move(new_x, new_y):
       t.setx(new_x)
  




# ===================================================
#   MAIN FUNCTION STAGES WILL CALL
# ===================================================
def bind_player_controls(screen, player1, player2, game_state, extra_callback=None):
   """
   Binds WASD for P1 and Arrow Keys for P2.
   extra_callback() is optional, but no longer necessary for invisibility logic.
   """
   # We ignore extra_callback here, as movement.py now handles the logic internally
   speed = game_state["player_speed"]


   # P1
   screen.onkey(lambda: move_up(player1, speed), "w")
   screen.onkey(lambda: move_down(player1, speed), "s")
   screen.onkey(lambda: move_left(player1, speed), "a")
   screen.onkey(lambda: move_right(player1, speed), "d")


   # P2
   screen.onkey(lambda: move_up(player2, speed), "Up")
   screen.onkey(lambda: move_down(player2, speed), "Down")
   screen.onkey(lambda: move_left(player2, speed), "Left")
   screen.onkey(lambda: move_right(player2, speed), "Right")


   screen.listen()