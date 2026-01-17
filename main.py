# VARIABLES GLOBALS
my_player: Sprite = None

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
    enemy.x = randint(10, 150)
    enemy.y = randint(10, 110)

    # "IA" per perseguir al jugador
    enemy.follow(my_player, enemy_speed)

# EXECUCIÓ
setup_player()

# Vinculem al botó A la funció shoot_projectile
controller.A.on_event(ControllerButtonEvent.PRESSED, shoot_projectile)

# Generem 5 enemics per començar
spawn_enemies(5)

