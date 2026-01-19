"""
Optimized Sprite Loader
- No duplicate loading
- Optional async loading without lag
- Caches loaded shapes
"""

import os

# ---------------------------------------------------------------
#   GLOBAL CACHE → prevents duplicate loading (lag fix)
# ---------------------------------------------------------------
_LOADED_SHAPES = set()

# ---------------------------------------------------------------
#   HEALTHBARS + INVENTORY
# ---------------------------------------------------------------
healthbar_images = {
    100: "stage_1/healthbars/hp100_small.gif",
    90:  "stage_1/healthbars/hp90_small.gif",
    80:  "stage_1/healthbars/hp80_small.gif",
    70:  "stage_1/healthbars/hp70_small.gif",
    60:  "stage_1/healthbars/hp60_small.gif",
    50:  "stage_1/healthbars/hp50_small.gif",
    40:  "stage_1/healthbars/hp40_small.gif",
    20:  "stage_1/healthbars/hp20_small.gif",
    0:   "stage_1/healthbars/hp00_small.gif",
}

inventory_images = {
    "empty": "stage_1/inventory/inventory_empty.gif",
    "p1key": "stage_1/inventory/inventory_p1key.gif",
    "p2key": "stage_1/inventory/inventory_p2key.gif",
    "both":  "stage_1/inventory/inventory_bothkeys.gif",
}

# ---------------------------------------------------------------
#   FIND ALL GIF PATHS
# ---------------------------------------------------------------
def collect_all_sprite_paths():
    folders = [
        "stage_1",
        "stage_1/healthbars",
        "stage_1/inventory",
        "prof_evolve",
        "fireball",
        "invisible_players",
        "boss_hp",
    ]

    paths = []

    for folder in folders:
        if not os.path.isdir(folder):
            continue
        for f in os.listdir(folder):
            if f.endswith(".gif"):
                paths.append(f"{folder}/{f}")

    # standalone files
    loose = [
        "start_button.gif", "next_button.gif",
        "start_stage_button.gif", "start_image.gif",
        "prof_final.gif",
        "uic_fight_zone.gif",
        "stage_4_outside.gif",
        "end_bike.gif", "end_bg.gif", "end_message.gif",
        "1story_screen.gif", "2story_screen.gif",
        "3story_screen.gif", "4story_screen.gif",
        "5story_screen.gif", "6story_screen.gif",
    ]

    for f in loose:
        if os.path.exists(f):
            paths.append(f)

    return paths


# ---------------------------------------------------------------
#   SAFE REGISTER (no duplicates)
# ---------------------------------------------------------------
def _safe_register(screen, path):
    if path in _LOADED_SHAPES:
        return
    try:
        screen.register_shape(path)
        _LOADED_SHAPES.add(path)
    except:
        pass


# ---------------------------------------------------------------
#   ASYNC REGISTRATION (SMOOTH, NON-LAGGY)
# ---------------------------------------------------------------
def register_all_sprites_async(screen, on_finish=None, chunk=3):
    """
    Loads sprites in small chunks.
    Smaller chunk size reduces lag spikes.
    """

    sprite_list = collect_all_sprite_paths()
    total = len(sprite_list)
    index = 0

    def load_chunk():
        nonlocal index

        screen.tracer(False)

        for _ in range(chunk):
            if index >= total:
                break
            _safe_register(screen, sprite_list[index])
            index += 1

        screen.tracer(True)

        if index >= total:
            if on_finish:
                on_finish()
            return

        screen.ontimer(load_chunk, 5)

    load_chunk()


# ---------------------------------------------------------------
#   SYNCHRONOUS LOADER (INSTANT LOAD, NO DUPLICATES)
# ---------------------------------------------------------------
def register_all_sprites(screen):
    for path in collect_all_sprite_paths():
        _safe_register(screen, path)