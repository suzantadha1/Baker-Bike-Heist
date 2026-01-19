# stage4_bossfight.py — FINAL CLEAN VERSION
import turtle

from movement import bind_player_controls
from player import create_default_players, create_healthbars, update_healthbars
from collision import add_block

from animation_evolve import play_evolution_animation
from boss_fireball import load_fireball_shapes, spawn_boss_fireball
from player_fireballs import load_player_fireball_shapes, spawn_player_fireball

from boss_health import create_boss_healthbar, update_boss_healthbar
from game_over import show_game_over
from end_animation import play_end_animation


# -------------------------------------------------------------
#   CLEAN HARD RESET (no ghost turtles)
# -------------------------------------------------------------
def safe_hard_reset(screen):
    # remove keybindings
    for key in ["w","a","s","d","Up","Down","Left","Right","space","Return"]:
        screen.onkey(None, key)

    # destroy ALL turtles
    for t in screen.turtles():
        try:
            t.hideturtle()
            t.clear()
            t._destroy()
        except:
            pass

    # reset collision map
    from collision import blocked_area
    blocked_area.clear()

    # reset screen state
    screen.bgpic("")
    screen.tracer(False)
    screen.listen()
    screen.setworldcoordinates(-480, -270, 480, 270)
    screen.tracer(True)


# -------------------------------------------------------------
#   MAIN BOSS FIGHT ENTRY
# -------------------------------------------------------------
def start_boss_fight(screen, p1_health, p2_health):

    safe_hard_reset(screen)

    # apply boss arena background
    screen.bgpic("uic_fight_zone.gif")

    # ARENA WALLS
    add_block(-480, 150, 480, 170)
    add_block(-250, 53, 130, -111)

    # CREATE PLAYERS
    player1, player2 = create_default_players(
        (-300, -150),
        (300, -150)
    )

    # GAME STATE
    game_state = {
        "player_speed": 25,
        "game_over": False,
        "p1_health": p1_health,
        "p2_health": p2_health,
        "boss_hp": 12,
        "last_shooter": None
    }

    # PLAYER CONTROLS
    bind_player_controls(screen, player1, player2, game_state)

    # HEALTHBARS
    p2_bar, p1_bar = create_healthbars()
    update_healthbars(game_state, p1_bar, p2_bar)
    p1_bar.showturtle()
    p2_bar.showturtle()

    # LOAD FIREBALL FRAMES (without re-registering)
    player_fb_frames = load_player_fireball_shapes(screen)

    # BOSS TURTLE (hidden until evolution finishes)
    boss = turtle.Turtle()
    boss.penup()
    boss.speed(0)
    boss.hideturtle()

    damage_handler = {"fn": None}

    # ---------------------------------------------------------
    #   PLAYER SHOOTING
    # ---------------------------------------------------------
    def p1_shoot():
        if damage_handler["fn"]:
            spawn_player_fireball(
                screen, player1, boss,
                player_fb_frames["pink"],
                on_hit=damage_handler["fn"]
            )

    def p2_shoot():
        if damage_handler["fn"]:
            spawn_player_fireball(
                screen, player2, boss,
                player_fb_frames["blue"],
                on_hit=damage_handler["fn"]
            )

    screen.onkey(p1_shoot, "space")
    screen.onkey(p2_shoot, "Return")

    # ---------------------------------------------------------
    #   EVOLUTION FINISH → BOSS SPAWN
    # ---------------------------------------------------------
    def evolution_finished(evo_turtle):

        if evo_turtle:
            evo_turtle.hideturtle()

        # Show boss
        boss.goto(-60, 90)
        boss.shape("prof_final.gif")
        boss.showturtle()

        # BOSS HEALTH BAR
        boss_bar = create_boss_healthbar()
        update_boss_healthbar(boss_bar, int(game_state["boss_hp"]))

        # boss fireball frames
        boss_frames = load_fireball_shapes(screen)

        # -----------------------------------------------------
        #   DAMAGE TO BOSS (players hit boss)
        # -----------------------------------------------------
        def damage_boss():
            hp = game_state["boss_hp"]

            if hp <= 0:
                return

            hp -= 0.5
            game_state["boss_hp"] = max(0, hp)
            update_boss_healthbar(boss_bar, int(hp))

            if hp == 0:
                game_state["game_over"] = True
                boss.hideturtle()

                screen.onkey(None, "space")
                screen.onkey(None, "Return")

                play_end_animation(screen, "end_bike.gif", "end_bg.gif")

        damage_handler["fn"] = damage_boss

        # -----------------------------------------------------
        #   BOSS ATTACK LOOP
        # -----------------------------------------------------
        attack_state = {"target": 1}

        def boss_attack():
            if game_state["game_over"] or game_state["boss_hp"] <= 0:
                return

            # alternate between player1 and player2
            target = player1 if attack_state["target"] == 1 else player2
            attack_state["target"] = 2 if attack_state["target"] == 1 else 1

            # spawn boss fireball (correct argument order!)
            spawn_boss_fireball(
                boss,
                target,
                boss_frames,
                game_state,
                player1,
                player2,
                p1_bar,
                p2_bar
            )

            # schedule next attack
            screen.ontimer(boss_attack, 2500)

        # start boss attack 1.8 seconds after evolution
        screen.ontimer(boss_attack, 1800)

    # ---------------------------------------------------------
    #   START EVOLUTION ANIMATION
    # ---------------------------------------------------------
    screen.ontimer(lambda:
        play_evolution_animation(screen, evolution_finished),
        400
    )