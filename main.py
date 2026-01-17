# VARIABLES GLOBALS
my_player: Sprite = None

# FUNCIONS DE CONFIGURACIÓ
def config_player():
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

def shoot():
    """
    Genera un projectil desde la possició del jugador
    """
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
        if controller.dx() == 0 and controller.dy() == 0:
            projectile.vx = 100 # direcció projectil per defecte: dreta
        else:
            # Velocitat del projectil segons velocitat del jugador
            projectile.vx = controller.dx() * 2
            projectile.vy = controller.dy() * 2
        
        # Destruïm el projectil un cop surt de la pantalla
        projectile.set_flag(SpriteFlag.DESTROY_ON_WALL, True)
    
    # Vinculem al botó A la funció
    controller.A.on_event(ControllerButtonEvent.PRESSED, shoot)

# CRIDA INICIAL
config_player()
