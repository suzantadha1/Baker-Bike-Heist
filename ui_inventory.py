



import turtle
from sprites import inventory_images

def create_inventory_ui():
   inv = turtle.Turtle()
   inv.hideturtle()
   inv.penup()
   inv.goto(-380, -200)  # bottom-left-ish
   inv.shape(inventory_images["empty"])
   inv.speed(0)
   inv.setundobuffer(None)
   return inv

def _player_has_key(inventory_list):
   return ("Exit Key" in inventory_list) or ("Bike Key" in inventory_list)


def update_inventory_ui(game_state, inventory_ui):
   """
   Uses game_state["inventory_p1"] and ["inventory_p2"] to select correct icon.
   """
   p1_has = _player_has_key(game_state["inventory_p1"])
   p2_has = _player_has_key(game_state["inventory_p2"])

   if p1_has and p2_has:
       inventory_ui.shape(inventory_images["both"])
   elif p1_has:
       inventory_ui.shape(inventory_images["p1key"])
   elif p2_has:
       inventory_ui.shape(inventory_images["p2key"])
   else:
       inventory_ui.shape(inventory_images["empty"])