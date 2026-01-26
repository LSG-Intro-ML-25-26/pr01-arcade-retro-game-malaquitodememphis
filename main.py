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

# Variables para niveles
current_level_num = 1
has_key = False

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
        
        # Destruïm el projectil un cop surt de la pantalla o xoca contra una paret
        projectile.set_flag(SpriteFlag.DESTROY_ON_WALL, True)
    elif my_player and not has_weapon:
        music.thump.play()

# Vinculem al botó A la funció shoot_projectile
controller.A.on_event(ControllerButtonEvent.PRESSED, shoot_projectile)

# GENERACIÓ D'ENEMICS
def spawn_enemies(location: tiles.Location, number_of_enemies: number):
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

        tiles.place_on_tile(enemy, location)

        # "IA" per perseguir al jugador
        enemy.follow(my_player, 30)
controller.A.on_event(ControllerButtonEvent.PRESSED, shoot_projectile)


# GENERACIÓ D'ENEMICS


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

        # Destruïm el projectil un cop surt de la pantalla o xoca contra una paret
        boss_projectile.set_flag(SpriteFlag.DESTROY_ON_WALL, True)

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
def spawn_key(location: tiles.Location):
    key_sprite = sprites.create(img("""
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
    """), SpriteKind.food)
    
    tiles.place_on_tile(key_sprite, location)

    # FX
    key_sprite.start_effect(effects.halo, 2000)

# Funcion para recoger la llave
def on_collect_key(player, item):
    global has_key
    has_key = True
    # Añade la llave al inventario
    global inventory_list
    inventory_list.append("Key Card")

    item.destroy(effects.fire, 500)
    music.ba_ding.play()
    player.say_text("¡Tengo la llave!", 1000)

sprites.on_overlap(SpriteKind.player, SpriteKind.food, on_collect_key)

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
def spawn_chest(location):
    """
    Crea un cofre en una Posició
    """
    chest = sprites.create(img("""
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
    """), Chest)
    tiles.place_on_tile(chest, location)

# FUNCIONS MONITOR NPC
def spawn_lore_monitor(location):
    monitor = sprites.create(img("""
        . . . . . . . . . . . . . . . .
        . . 5 5 5 5 5 5 5 5 5 5 5 5 . .
        . . 5 b b b b b b b b b b 5 . .
        . . 5 b 1 1 1 1 1 1 1 1 b 5 . .
        . . 5 b 1 1 1 1 1 1 1 1 b 5 . .
        . . 5 b 1 1 1 1 1 1 1 1 b 5 . .
        . . 5 b b b b b b b b b b 5 . .
        . . 5 5 5 5 5 5 5 5 5 5 5 5 . .
        . . . . . . . 5 5 . . . . . . .
        . . . . . . 5 5 5 5 . . . . . .
    """), NPC)
    tiles.place_on_tile(monitor, location)

# GESTIÓN DE NIVELES

# Función para gestionar niveles
def load_level(level: number):
    global my_player, has_key
    
    # Reiniciar el nivel entero
    has_key = False
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    sprites.destroy_all_sprites_of_kind(SpriteKind.food)

    # Selecciona el mapa
    if level == 1:
        tiles.set_tilemap(assets.tilemap("level1"))
        game.splash("NIVEL 1", "Entrenamiento")
    elif level == 2:
        tiles.set_tilemap(assets.tilemap("level4"))
        game.splash("NIVEL 2", "Zona Corrupta")
    elif level == 3:
        tiles.set_tilemap(assets.tilemap("level5"))
        game.splash("NIVEL 3", "Boss Final")

    # Spawn del jugador
    player_spawns = tiles.get_tiles_by_type(assets.tile("spawn_player_base_floor"))
    # Devuelve el tile a la normalidad (borra el spawn)
    if len(player_spawns) > 0:
        tiles.place_on_tile(my_player, player_spawns[0])
        tiles.set_tile_at(player_spawns[0], assets.tile("base_floor"))
    
    #Hacemos spawnear todos los objetos y enemigos
    spawn_objects_from_tiles()

# Función para pasar de nivel al tocar la puerta con la llave o chocar con ella sin llave
def on_hit_door_wall(player, location):
    global current_level_num
    
    if tiles.tile_at_location_equals(location, assets.tile("acces_doors")):
        #Pasa de nivel si tiene llave
        if has_key:
            music.power_up.play()
            player.say_text("¡Abriendo!", 1000)
            pause(1000)
            current_level_num += 1
            load_level(current_level_num)
        #Sin llave choca con la puerta y rebota
        else:
            player.say_text("¡Cerrado!", 500)
            scene.camera_shake(2, 200)
            #Rebote del jugador
            if player.vx > 0: player.x -= 5
            if player.vx < 0: player.x += 5
            if player.vy > 0: player.y -= 5
            if player.vy < 0: player.y += 5
    elif tiles.tile_at_location_equals(location, assets.tile("close_chest")):
        global has_weapon, inventory_list
        if not has_weapon:
            has_weapon = True
            inventory_list.append("Cyber Gun")
            music.power_up.play(500)
            game.show_long_text("Has trobat l'ARMA DE PLASMA!\nAra prem A per disparar.", DialogLayout.BOTTOM)
            tiles.set_tile_at(location, assets.tile("open_chest"))
    elif tiles.tile_at_location_equals(location, assets.tile("spawn_npc_base_floor")):
        game.show_long_text(
                "LORE", DialogLayout.BOTTOM
            )
        player.y += 10

scene.on_hit_wall(SpriteKind.player, on_hit_door_wall)


# GENERACIÓN DE SPRITES
# Función para generar objetos y enemigos
def spawn_objects_from_tiles():
    # Genera enemigos en el spawn
    enemy_spawns = tiles.get_tiles_by_type(assets.tile("spawn_enemy_way_floor"))
    for loc_enemy in enemy_spawns:
        spawn_enemies(loc_enemy, 1)
        tiles.set_tile_at(loc_enemy, assets.tile("way_floor"))

    # Genera la llave en su spawn
    key_spawns = tiles.get_tiles_by_type(assets.tile("access_card_base_floor"))
    for loc_key in key_spawns:
        spawn_key(loc_key)
        tiles.set_tile_at(loc_key, assets.tile("base_floor"))

    chest_spawn = tiles.get_tiles_by_type(assets.tile("close_chest"))
    for loc_chest in chest_spawn:
        spawn_chest(loc_chest)

    monitor_spawn = tiles.get_tiles_by_type(assets.tile("spawn_npc_base_floor"))
    for loc_monitor in monitor_spawn:
        spawn_lore_monitor(loc_monitor)

# EXECUCIÓ
# Función para iniciar el juego
def start_game():
    setup_player()
    load_level(current_level_num)
    
start_game()

# Mostrem cofre(x,y)
# spawn_chest(120, 60)

# Mostrem monitor(x,y)
# spawn_lore_monitor(40, 60)

# Generació del "final boss"(x,y)
# spawn_boss(100, 50)