

# inventory.py
"""
Inventory management for Player 1 and Player 2.
Contains helper functions for adding/removing/checking items
and debugging inventory state.
"""




# ==============================
#  CREATE EMPTY INVENTORIES
# ==============================
def create_inventories():
   """Returns (inventory_p1, inventory_p2)."""
   return [], []




# ==============================
#  BASIC CHECKS
# ==============================
def has_exit_key(inventory):
   return "Exit Key" in inventory




def has_bike_key(inventory):
   return "Bike Key" in inventory




def has_any_key(inventory):
   """True if player has any key (exit or bike)."""
   return has_exit_key(inventory) or has_bike_key(inventory)




def has_all_keys(inventory):
   """True if player has both keys."""
   return has_exit_key(inventory) and has_bike_key(inventory)




# ==============================
#  MUTATION HELPERS
# ==============================
def add_item(inventory, item_name):
   """
   Adds an item to a player's inventory list.
   """
   if item_name not in inventory:
       inventory.append(item_name)




def remove_item(inventory, item_name):
   """
   Removes an item if it exists.
   """
   if item_name in inventory:
       inventory.remove(item_name)




# ==============================
#  TEAM-WIDE CHECKS
# ==============================
def team_has_exit_key(inv1, inv2):
   return has_exit_key(inv1) or has_exit_key(inv2)




def team_has_bike_key(inv1, inv2):
   return has_bike_key(inv1) or has_bike_key(inv2)




def team_has_all_keys(inv1, inv2):
   return (team_has_exit_key(inv1, inv2)
           and team_has_bike_key(inv1, inv2))




# ==============================
#  DEBUGGING
# ==============================
def debug_print_inventories(inventory_p1, inventory_p2):
   print(f"P1 Inventory: {inventory_p1}")
   print(f"P2 Inventory: {inventory_p2}")