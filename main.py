# VARIABLES GLOBALS
# Sprites
Boss = SpriteKind.create()
EnemyProjectile = SpriteKind.create()
Chest = SpriteKind.create()
NPC = SpriteKind.create()
my_player: Sprite = None
boss_sprite: Sprite = None
boss_statusbar: StatusBarSprite = None

# Variables
inventory_list: List[str] = []
has_weapon: bool = False

# Variables d'estat de d'apuntament (dreta per defecte)
facing_x: number = 1
facing_y: number = 0

# Constants
projectile_speed = 200
enemy_speed = 50

# FUNCIÓ DE CONFIGURACIÓ
def setup_player():
    """
    Crea el sprite del jugador, defineix les seves físiques i estableix vides.
    """
    global my_player

    # Placeholder temporal per my_player
    my_player = sprites.create(img("""
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . 8 8 8 8 . . . . . .
            . . . . . . 8 8 8 8 . . . . . .
            . . . . . . 8 8 8 8 . . . . . .
            . . . . . . 8 8 8 8 . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
        """), SpriteKind.player)
    
    # Físiques de moviment
    controller.move_sprite(my_player, 100, 100)

    # La càmara segueix el jugador
    scene.camera_follow_sprite(my_player)

    # Sistema de vides
    info.set_life(3)

# BUCLE D'ACTUALITZACIÓ
def on_game_update():
    """
    Aquesta funció s'executa a cada frame del joc
    """
    global facing_x, facing_y

    # Detectem si el jugador s'està movent
    if controller.dx() != 0 or controller.dy() != 0:
        # Si ens movem, actualitzem la direcció on mirem.

        # Gestió eix X
        if controller.dx() > 0: facing_x = 1
        elif controller.dx() < 0: facing_x = -1
        else: facing_x = 0

        # Gestió eix Y
        if controller.dy() > 0: facing_y = 1
        elif controller.dy() <0: facing_y = -1
        else: facing_y = 0

        # Gestió de diagonals (excepció)
        if facing_x !=0 and facing_y !=0:
            pass

# Vinculem la funció del bucle al joc
game.on_update(on_game_update)

# SISTEMA DE COMBAT
def shoot_projectile():
    """
    Genera un projectil desde la possició del jugador
    """
    global my_player, facing_x, facing_y, has_weapon

    # Només disparem si el jugador existeix
    if my_player and has_weapon:
        # Creem el projectil (placeholder momentani)
        projectile = sprites.create_projectile_from_sprite(img("""
        . . . . .
        . . 5 . .
        . 5 5 5 .
        . . 5 . .
        . . . . .
        """), my_player, 0, 0) # Velocitat inicial: 0

        # Lògica per disparar cap on mirem
        if facing_x == 0 and facing_y == 0:
            projectile.vx = projectile_speed # direcció projectil per defecte: dreta
        else:
            # Velocitat del projectil segons velocitat del jugador
            projectile.vx = facing_x * projectile_speed
            projectile.vy = facing_y * projectile_speed
        
        # Destruïm el projectil un cop surt de la pantalla
        projectile.set_flag(SpriteFlag.DESTROY_ON_WALL, True)
    elif my_player and not has_weapon:
        music.thump.play()

controller.A.on_event(ControllerButtonEvent.PRESSED, shoot_projectile)


# GENERACIÓ D'ENEMICS
def spawn_enemies(number_of_enemies, x_pos, y_pos):
    """
    Genera una llista d'enemics en posicions aleatòries
    """
    # Bucle per generar 'n' enemics
    for i in range(number_of_enemies):
        # Creem l'enemic
        enemy = sprites.create(img("""
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . 2 2 2 2 . . . . . .
        . . . . . 2 2 2 2 2 2 . . . . .
        . . . . . 2 2 2 2 2 2 . . . . .
        . . . . . 2 2 2 2 2 2 . . . . .
        . . . . . . 2 2 2 2 . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        """), SpriteKind.enemy)

        #Posició aleatòria dins de la pantalla
        # Pendent d'actualitzar quan sapiguem tamany real total del mapa
        enemy.x = x_pos
        enemy.y = y_pos

        # "IA" per perseguir al jugador
        enemy.follow(my_player, enemy_speed)

        pause(200)

# GESTIÓ DE COL·LISIONS (projectil-enemic//enemic-jugador)
def on_projectile_hit_enemy(projectile, enemy):
    """
    Gestiona quan un projectil xoca contra un enemic
    """
    # Destruïm el projectil
    projectile.destroy()

    # Destruïm l'enemic (amb FX)
    enemy.destroy(effects.disintegrate, 500)

    # Sumar punts ? (a veure si es desenvolupa en el futur)
    info.change_score_by(100)

# Registrem l'esdeveniment
sprites.on_overlap(SpriteKind.projectile, SpriteKind.enemy, on_projectile_hit_enemy)

def on_enemy_hit_player(player, enemy):
    """
    Gestiona quan un enemic xoca contra el jugador
    """
    # Restem una vida
    info.change_life_by(-1)

    # Destruïm l'enemic
    enemy.destroy(effects.fire, 500)

    # Feedback visual (sacsejar càmera)
    scene.camera_shake(4, 500)

# Registrem l'esdeveniment
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_enemy_hit_player)

# FUNCIONS DEL "FINAL BOSS"
def spawn_boss(x_pos, y_pos):
    """
    Invoca el "Kernel Corrupte"
    """
    global boss_sprite, boss_statusbar

    boss_sprite = sprites.create(img("""
    . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . .
    . . . . f f f f f f f f . . . .
    . . . f f 2 2 2 2 2 2 f f . . .
    . . . f 2 2 7 7 7 7 2 2 f . . .
    . . . f 2 7 f f f f 7 2 f . . .
    . . . f 2 7 f 2 2 f 7 2 f . . .
    . . . f 2 7 f 2 2 f 7 2 f . . .
    . . . f 2 7 f f f f 7 2 f . . .
    . . . f 2 2 7 7 7 7 2 2 f . . .
    . . . f f 2 2 2 2 2 2 f f . . .
    . . . . f f f f f f f f . . . .
    . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . .
    """), Boss)

    # El col·loquem al centre
    boss_sprite.x = x_pos
    boss_sprite.y = y_pos

    # Li donem vida (extensió de "status-bar")
    boss_statusbar = statusbars.create(20, 4, StatusBarKind.enemy_health)
    boss_statusbar.max = 20
    boss_statusbar.value = 20
    boss_statusbar.set_color(7, 2)
    boss_statusbar.attach_to_sprite(boss_sprite)

    # "IA" del "boss"
    game.on_update_interval(2000, boss_shooting_pattern)

def boss_shooting_pattern():
    """
    Funció executada periòdicament perquè el "boss" dispari
    """
    global boss_sprite, my_player

    # Només disparem si ambdós sprites existeixen
    if boss_sprite and my_player:
        # Creem el projectil enemic
        boss_projectile = sprites.create_projectile_from_sprite(img("""
        . . . 2 . . .
        . . 2 2 2 . .
        . 2 2 2 2 2 .
        . . 2 2 2 . .
        . . . 2 . . .
        """), boss_sprite, 0, 0)

        boss_projectile.set_kind(EnemyProjectile)

        # Apunta el projectil cap el jugador
        boss_projectile.follow(my_player, 80)

# COL·LISIONS DEL "FINAL BOSS"
def on_projectile_hit_boss(projectile, boss_sprite):
    projectile.destroy()
    
    # Si hi ha statusbar, li restem 1
    if boss_statusbar:
        boss_statusbar.value -= 1

    # FX
    boss_sprite.start_effect(effects.ashes, 200)

# Registrem l'esdeveniment
sprites.on_overlap(SpriteKind.projectile, Boss, on_projectile_hit_boss)

def on_boss_hit_player(player, boss):
    info.change_life_by(-1)
    scene.camera_shake(4, 500)
    # Empenyem el jugador cap enrere
    player.y += 10

# Registrem l'esdeveniment
sprites.on_overlap(SpriteKind.player, Boss, on_boss_hit_player)

def on_boss_death(status):
    if boss_sprite:
        boss_sprite.destroy(effects.disintegrate, 1000)
        game.show_long_text("SERVIDOR RESTAURAT! HAS GUANYAT!", DialogLayout.BOTTOM)
        game.over(True)

# Registrem l'esdeveniment
statusbars.on_zero(StatusBarKind.enemy_health, on_boss_death)

def on_enemy_projectile_hit_player(player, projectile):
    # Restem vida al jugador
    info.change_life_by(-1)

    # Destruïm el projectil
    projectile.destroy()

    # Efecte visual
    scene.camera_shake(4, 200)

# Registrem l'esdeveniment
sprites.on_overlap(SpriteKind.player, EnemyProjectile, on_enemy_projectile_hit_player)

# SISTEMA D'INVENTARI
def spawn_key(x_pos, y_pos):
    """
    Crea un objecte recol·lectable (Clau Mestre)
    """
    key_sprite = sprites.create(img("""
    . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . .
    . . . . . 5 5 5 5 5 . . . . . .
    . . . . 5 5 . . . 5 5 . . . . .
    . . . . 5 . . . . . 5 . . . . .
    . . . . 5 . . . . . 5 . . . . .
    . . . . . 5 5 5 5 5 . . . . . .
    . . . . . . . 5 . . . . . . . .
    . . . . . . . 5 . . . . . . . .
    . . . . . . . 5 . . . . . . . .
    . . . . . . 5 5 5 . . . . . . .
    . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . .
    """), SpriteKind.food) # Usem "food" per objectes recol·lectables

    key_sprite.x = x_pos
    key_sprite.y = y_pos

    # FX
    key_sprite.start_effect(effects.halo, 2000)

def on_player_collect_key(player, key_sprite):
    """
    Gestió de l'inventari
    """
    global inventory_list

    # Afegim l'element a la llista
    inventory_list.append("Master Key")

    # Feedback visual
    key_sprite.destroy(effects.confetti, 500)
    music.ba_ding.play()

    # Mostrem l'inventari per pantalla
    my_player.say_text(("Tinc: " + str(len(inventory_list)) + " ítems"), 3000)

# Registrem l'esdeveniment
sprites.on_overlap(SpriteKind.player, SpriteKind.food, on_player_collect_key)

def show_inventory():
    """
    Mostra una finestra amb l'inventari
    """
    global inventory_list, has_weapon

    # Variables amb valors per defecte
    weapon = "No"
    keys_count = 0

    if has_weapon:
        weapon = "Cyber Gun"
    
    # Comptem les claus de l'inventari
    for item in inventory_list:
        if item == "Key Card":
            keys_count += 1
    
    game.show_long_text(
            "INVENTARI:\n" +
            "- Arma: " + weapon + "\n" +
            "- Targetes d'Accés: " + str(keys_count) + "/3",
            DialogLayout.CENTER
        )

# Registrem l'esdeveniment al botó "B"
controller.B.on_event(ControllerButtonEvent.PRESSED, show_inventory)
    
# FUNCIÓ D'OBJECTE: COFRE
def spawn_chest(x_pos, y_pos):
    """
    Crea un cofre en una Posició
    """
    chest = sprites.create(img("""
        . . b b b b b b b b b b . . . .
        . b e 4 4 4 4 4 4 4 4 e b . . .
        b e 4 4 4 4 4 4 4 4 4 4 e b . .
        b e 4 4 4 4 4 4 4 4 4 4 e b . .
        b e 4 4 4 4 4 4 4 4 4 4 e b . .
        b e e 4 4 4 4 4 4 4 4 e e b . .
        b e e e e e e e e e e e e b . .
        . b b b b b b b b b b b b . . .
        . . . . . . . . . . . . . . . .
    """), Chest)
    chest.x = x_pos
    chest.y = y_pos

def on_open_chest(player, chest):
    global has_weapon, inventory_list

    if not has_weapon:
        has_weapon = True
        inventory_list.append("Cyber Gun")

        game.show_long_text("Has trobat l'ARMA DE PLASMA!\nAra prem A per disparar.", DialogLayout.BOTTOM)

        chest.destroy(effects.confetti, 500)
        music.power_up.play()

sprites.on_overlap(SpriteKind.player, Chest, on_open_chest)

# FUNCIONS MONITOR NPC
def spawn_lore_monitor(x_pos, y_pos):
    monitor = sprites.create(img("""
        . . . . . . . . . . . . . . . .
        . . 5 5 5 5 5 5 5 5 5 5 5 5 . .
        . . 5 b b b b b b b b b b 5 . .
        . . 5 b 1 1 1 1 1 1 1 1 b 5 . .
        . . 5 b 1 1 1 1 1 1 1 1 b 5 . .
        . . 5 b 1 1 1 1 1 1 1 1 b 5 . .
        . . 5 b b b b b b b b b b 5 . .
        . . 5 5 5 5 5 5 5 5 5 5 5 5 . .
        . . . . . . 5 5 . . . . . . . .
        . . . . . 5 5 5 5 . . . . . . .
    """), NPC)
    monitor.x = x_pos
    monitor.y = y_pos

def on_talk_npc(player, monitor):
    game.show_long_text(
        "LORE", DialogLayout.BOTTOM
    )
    player.y += 10

sprites.on_overlap(SpriteKind.player, NPC, on_talk_npc)

# EXECUCIÓ
# Mostrem el jugador
setup_player()

# Mostrem cofre(x,y)
# spawn_chest(120, 60)

# Mostrem monitor(x,y)
# spawn_lore_monitor(40, 60)

# Generem 5 enemics per començar(num_of_enemies,x,y)
# spawn_enemies(5, 100, 50)

# Generació del "final boss"(x,y)
# spawn_boss(100, 50)

# Generació de la clau(x,y)
# spawn_key(100, 50)