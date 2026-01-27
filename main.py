# ===============================
# ERIC LORENZO
# FRANCIS MORETA
# ===============================

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
current_level_num = 1
has_key = False
loading_level = False
score_start_level_2 = 0
level2_doors_opened = False

# Variables d'estat de d'apuntament (dreta per defecte)
facing_x: number = 1
facing_y: number = 0

# Constants
projectile_speed = 200
enemy_speed = 50
game.set_game_over_message(False, "☠️HAS PERDUT!☠️")
game.set_game_over_message(True, "🏆SERVIDOR RESTAURAT!🏆")

# FUNCIÓ DE CONFIGURACIÓ
def on_start():
    music.play(music.string_playable("C5 B C5 A C5 G C5 C C5 B C5 A C5 G C5 C B A B G# B F B E B A B G# B F B E A G A F A E A D A G A F A E A D G# F G# E G# D G# C G# F G# E G# D G# C", 240), music.PlaybackMode.LOOPING_IN_BACKGROUND)
on_start()
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
    global facing_x, facing_y, my_player, score_start_level_2

    if not level2_doors_opened and current_level_num == 2 and info.score() - score_start_level_2 >= 600:
        level2_doors_opened = True
        scene.camera_shake(3, 1000)
        music.spooky.play(200)
        my_player.say_text("Les portes s'obren!")
        # Agafem els tiles laser
        laser_loc = tiles.get_tiles_by_type(assets.tile("laser_block_wall"))
        for loc in laser_loc:
            tiles.set_tile_at(loc, assets.tile("way_floor"))
            tiles.set_wall_at(loc, False) # Esborrem els murs

    # Obtenim tots els enemics del mapa
    all_enemies = sprites.all_of_kind(SpriteKind.enemy)

    for enemy in all_enemies:
        # Calculem la distància entre jugador i enemic
        dx = enemy.x - my_player.x
        dy = enemy.y - my_player.y
        # Fórmula hipotenusa
        distance = Math.sqrt(dx * dx + dy * dy)

        # Si enemic i player estan a menys de 100 pixels, l'enemic s'activa
        if distance < 60:
            # Si l'enemic no s'esta movent (primera vegada que detecta el player)
            if enemy.vx == 0 and enemy.vy == 0:
                music.beam_up.play(100)
                enemy.say_text("!", 1000)
                effects.clear_particles(enemy)

            enemy.follow(my_player, 50)

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
        
        music.pew_pew.play(100)
        
        # Destruïm el projectil un cop surt de la pantalla o xoca contra una paret
        projectile.set_flag(SpriteFlag.DESTROY_ON_WALL, True)
    elif my_player and not has_weapon:
        music.thump.play(100)

# Vinculem al botó A la funció shoot_projectile
controller.A.on_event(ControllerButtonEvent.PRESSED, shoot_projectile)

# GENERACIÓ D'ENEMICS
def spawn_enemies(location: tiles.Location, number_of_enemies: number):
    """
    Genera una llista d'enemics en posicions escollides segons tiles
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

        # Els mostrem als tiles corresponents
        tiles.place_on_tile(enemy, location)

        # Comencen dormits
        enemy.start_effect(effects.bubbles)


# GESTIÓ DE COL·LISIONS
def on_projectile_hit_enemy(projectile, enemy):
    """
    Gestiona quan un projectil xoca contra un enemic
    """
    # Destruïm el projectil
    projectile.destroy()

    # Destruïm l'enemic
    enemy.destroy(effects.fire, 500)
    music.small_crash.play(100)

    # Sumem punts
    info.change_score_by(100)

# Registrem l'esdeveniment
sprites.on_overlap(SpriteKind.projectile, SpriteKind.enemy, on_projectile_hit_enemy)

def on_enemy_hit_player(player, enemy):
    """
    Gestiona quan un enemic xoca contra el jugador
    """
    # Restem una vida
    info.change_life_by(-1)
    music.zapped.play(100)
    info.change_score_by(100)

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

    # El col·loquem
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
    """
    Gestiona quan un projectil de player xoca contra el final boss
    """
    projectile.destroy()
    
    # Si hi ha statusbar, li restem 1
    if boss_statusbar:
        boss_statusbar.value -= 1
        music.small_crash.play(100)

    # FX
    boss_sprite.start_effect(effects.ashes, 200)

# Registrem l'esdeveniment
sprites.on_overlap(SpriteKind.projectile, Boss, on_projectile_hit_boss)

def on_boss_hit_player(player, boss):
    """
    Si el player xoca contra el boss
    """
    info.change_life_by(-1)
    music.zapped.play(100)
    scene.camera_shake(4, 500)

# Registrem l'esdeveniment
sprites.on_overlap(SpriteKind.player, Boss, on_boss_hit_player)

def on_boss_death(status):
    """
    Quan el boss mori (statusbar = 0)
    """
    if boss_sprite:
        boss_sprite.destroy(effects.fire, 1000)
        music.stop_all_sounds()
        music.power_up.play(100)
        game.over(True)

# Registrem l'esdeveniment
statusbars.on_zero(StatusBarKind.enemy_health, on_boss_death)

def on_enemy_projectile_hit_player(player, projectile):
    """
    Quan els projectils del bos xocan contra el player
    """
    # Restem vida al jugador
    info.change_life_by(-1)

    # Destruïm el projectil
    projectile.destroy()

    # Efecte visual
    scene.camera_shake(4, 200)

def on_life_zero():
    """
    Quan ens quedem sense vides
    """
    music.stop_all_sounds()
    music.wawawawaa.play()
    game.gameOver(False)
info.on_life_zero(on_life_zero)

# Registrem l'esdeveniment
sprites.on_overlap(SpriteKind.player, EnemyProjectile, on_enemy_projectile_hit_player)

# SISTEMA D'INVENTARI
def spawn_key(location: tiles.Location):
    """
    Mostra les claus a les localitzacions assignades segons tiles
    """
    key_sprite = sprites.create(assets.tile("access_card_base_floor"), SpriteKind.food)
    
    tiles.place_on_tile(key_sprite, location)

    # FX
    key_sprite.start_effect(effects.halo)

# Funcion para recoger la llave
def on_collect_key(player, item):
    """
    Funció per recollir la clau
    """
    global has_key
    has_key = True
    # Añade la llave al inventario
    global inventory_list
    inventory_list.append("Key Card")

    item.destroy()
    music.ba_ding.play(100)
    player.say_text("Tinc la clau!", 1000)

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
            "==============\n" +
            "INVENTARI:\n" +
            "==============\n" +
            "- Arma: " + weapon + "\n" +
            "- Targetes: " + str(keys_count) + "/3",
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
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
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

# GESTIÓ DE NIVELLS
def load_level(level: number):
    """
    Gestiona el canvi de nivells
    """
    global my_player, has_key, score_start_level_2
    
    # Reiniciar el nivell
    has_key = False
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    sprites.destroy_all_sprites_of_kind(SpriteKind.food)
    sprites.destroy_all_sprites_of_kind(NPC)

    # Selecciona el mapa
    if level == 1:
        tiles.set_tilemap(assets.tilemap("level1"))
        game.splash("NIVELL 1", "Entrenament")
    elif level == 2:
        score_start_level_2 = info.score()
        tiles.set_tilemap(assets.tilemap("level6"))
        game.splash("NIVELL 2", "Zona Corrupta")
    elif level == 3:
        tiles.set_tilemap(assets.tilemap("level5"))
        game.splash("NIVELL 3", "Boss Final")

    # Spawn del jugador
    player_spawns = tiles.get_tiles_by_type(assets.tile("spawn_player_base_floor"))
    # Retorna el tile a la normalitat (borra el spawn)
    if len(player_spawns) > 0:
        tiles.place_on_tile(my_player, player_spawns[0])
        tiles.set_tile_at(player_spawns[0], assets.tile("base_floor"))
    
    #Crida de funció
    spawn_objects_from_tiles()

# GESTIÓ DE COL·LISIONS
def on_hit_door_wall(player, location):
    """
    Gestiona si s'ha de fer alguna cosa en xocar amb tiles concrets
    """
    global current_level_num
    
    if tiles.tile_at_location_equals(location, assets.tile("acces_doors")):
        #Passa de nivell si té la clau
        if has_key and not loading_level:
            loading_level = True

            music.spooky.play(200)
            pause(500)

                
            current_level_num += 1
            load_level(current_level_num)
            
            loading_level = False

        #Sense la clau, xoca amb la porta i rebota
        else:
            player.say_text("Tancat!", 500)
            music.thump.play(200)
            scene.camera_shake(2, 200)
            #Rebot del jugador
            if player.vx > 0: player.x -= 5
            if player.vx < 0: player.x += 5
            if player.vy > 0: player.y -= 5
            if player.vy < 0: player.y += 5
    elif tiles.tile_at_location_equals(location, assets.tile("close_chest")):
        global has_weapon, inventory_list
        if not has_weapon:
            has_weapon = True
            inventory_list.append("Cyber Gun")
            music.ba_ding.play(100)
            tiles.set_tile_at(location, assets.tile("open_chest"))
            game.show_long_text("Has trobat l'arme CYBER GUN!\nAra prem A per disparar.", DialogLayout.BOTTOM)
    elif tiles.tile_at_location_equals(location, assets.tile("spawn_npc_base_floor")):
        music.magic_wand.play(100)
        game.show_long_text(
            "LORE", DialogLayout.BOTTOM
        )
    elif tiles.tile_at_location_equals(location, assets.tile("laser_block_wall")):
        player.say_text("Tancat! Mata a tots els virus!", 500)
        music.thump.play(200)
        scene.camera_shake(1, 100)
        player.x -= 5


# Trigger que activa la funció
scene.on_hit_wall(SpriteKind.player, on_hit_door_wall)

def on_player_step_on_lore(player, location):
    """
    Gestiona els missatges de lore en trepitjar punts concrets
    """
    music.magic_wand.play(100)
    game.show_long_text("LORE", DialogLayout.BOTTOM)
    
    all_lore_locations = tiles.get_tiles_by_type(assets.tile("lore_point_base_floor"))
    
    for loc in all_lore_locations:
        tiles.set_tile_at(loc, assets.tile("base_floor"))
# Crida de la funció
scene.on_overlap_tile(SpriteKind.player, assets.tile("lore_point_base_floor"), on_player_step_on_lore)

# GENERACIÓ DE SPRITES
def spawn_objects_from_tiles():
    """
    Crea enemics i objectes segons les tiles del mapa actual
    """
    # Genera enemics al spawn
    enemy_spawns = tiles.get_tiles_by_type(assets.tile("spawn_enemy_way_floor"))
    for loc_enemy in enemy_spawns:
        spawn_enemies(loc_enemy, 1)
        tiles.set_tile_at(loc_enemy, assets.tile("way_floor"))

    enemy_spawns = tiles.get_tiles_by_type(assets.tile("spawn_enemy_base_floor"))
    for loc2_enemy in enemy_spawns:
        spawn_enemies(loc2_enemy, 1)
        tiles.set_tile_at(loc2_enemy, assets.tile("base_floor"))

    # Genera la clau al spawn
    key_spawns = tiles.get_tiles_by_type(assets.tile("access_card_base_floor"))
    for loc_key in key_spawns:
        spawn_key(loc_key)
        tiles.set_tile_at(loc_key, assets.tile("base_floor"))

    # Genera el chest al spawn
    chest_spawn = tiles.get_tiles_by_type(assets.tile("close_chest"))
    for loc_chest in chest_spawn:
        spawn_chest(loc_chest)

    # Genera el NPC al spawn
    monitor_spawn = tiles.get_tiles_by_type(assets.tile("spawn_npc_base_floor"))
    for loc_monitor in monitor_spawn:
        spawn_lore_monitor(loc_monitor)

    # Genera el lorepoint al spawn
    lorepoint_spawn = tiles.get_tiles_by_type(assets.tile("lore_point_base_floor"))

# TRIGGER DEL JOC
def start_game():
    """
    inicia el joc setejant el jugador i el nivell que pertoqui
    """
    setup_player()
    load_level(current_level_num)

# MENÚ PRINCIPAL:
def show_menu():
    """
    Pantalla d'inici del joc
    """
    # Fons del menú
    # scene.set_background_image(assets.image("bg"))

    # Temporal
    scene.set_background_color(15)

    game.splash("CYBER-DRUID: El Reinici", "Prem A per jugar!")

    start_game()

# EXECUCIÓ

# Generació del "final boss"(x,y)
# spawn_boss(15, 10)

show_menu()

