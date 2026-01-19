import turtle
from sprites import healthbar_images
from PIL import Image

def resize_gif(input_file, output_file, scale=0.5):
    img = Image.open(input_file)
    img = img.resize((int(img.width * scale), int(img.height * scale)))
    img.save(output_file)

# shrink camera GIFs
resize_gif("camera_left.gif", "camera_left_small.gif", 0.25)
resize_gif("camera_right.gif", "camera_right_small.gif", 0.25)

def start_camera(screen, player1, player2, hp1, hp2, get_hp_image,
                 stage2_state, update_healthbars,
                 speed=5, damage_distance=100, damage_amount=10,
                 image_left="camera_left_small.gif", image_right="camera_right_small.gif"):

    screen.register_shape(image_left)
    screen.register_shape(image_right)
    
    camera = turtle.Turtle()
    camera.penup()
    camera.shape(image_right)
    camera.goto(-5, 250)

    direction = -1  # 1 = right, -1 = left
    move_interval = 1000

    # Ensure health keys exist
    if "p1_health" not in stage2_state:
        stage2_state["p1_health"] = 100
    if "p2_health" not in stage2_state:
        stage2_state["p2_health"] = 100

    def switch_direction():
        nonlocal direction
        direction *= -1
        camera.shape(image_right if direction == 1 else image_left)
        screen.ontimer(switch_direction, move_interval)

    def check_damage():
        if stage2_state["game_over"]:
            return

        # Damage players if camera close AND they are not invisible
        for player, hp_key in [(player1, "p1_health"), (player2, "p2_health")]:
            if hasattr(player, "is_invisible") and player.is_invisible:
                continue  # Skip invisible players
            if camera.distance(player) < damage_distance:
                stage2_state[hp_key] = max(0, stage2_state[hp_key] - damage_amount)

        # Update health bars
        update_healthbars(stage2_state, hp1, hp2)

        # Trigger game over if needed
        if stage2_state["p1_health"] <= 0 or stage2_state["p2_health"] <= 0:
            stage2_state["game_over"] = True
            from game_over import show_game_over
            show_game_over(screen)
            return

        screen.ontimer(check_damage, 150)

    switch_direction()
    check_damage()
