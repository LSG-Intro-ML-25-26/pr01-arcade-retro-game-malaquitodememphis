# VARIABLES GLOBALS
# Sprites
my_player: Sprite = None
Boss = SpriteKind.create() # Creem categoria
EnemyProjectile = SpriteKind.create()
boss_sprite: Sprite = None
boss_statusbar: StatusBarSprite = None

# Variables
inventory_list: List[str] = []

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
    global my_player, facing_x, facing_y

    # Només disparem si el jugador existeix
    if my_player:
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

# GENERACIÓ D'ENEMICS
def spawn_enemies(number_of_enemies: number):
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
        enemy.x = randint(10, 140)
        enemy.y = randint(10, 100)

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
def spawn_boss():
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
    boss_sprite.x = 80
    boss_sprite.y = 30

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
def spawn_key():
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

    key_sprite.x = 100
    key_sprite.y = 50

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

    # Si tenim la clau, podríem invocar al Boss (o obrir la porta)
    # if "Master Key" in inventory_list:
    #     game.show_long_text("Clau trobada! El Boss ha despertat...", DialogLayout.BOTTOM)
    #     spawn_boss()

# Registrem l'esdeveniment
sprites.on_overlap(SpriteKind.player, SpriteKind.food, on_player_collect_key)

# EXECUCIÓ
setup_player()

# Vinculem al botó A la funció shoot_projectile
controller.A.on_event(ControllerButtonEvent.PRESSED, shoot_projectile)

# Generem 5 enemics per començar
# spawn_enemies(5)

# Generació del "final boss"
# spawn_boss()

# Generació de la clau
spawn_key()