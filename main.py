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
lorepoint_counter = 0

# Variables d'estat
facing_x: number = 1
facing_y: number = 0
last_anim_state = ""

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
    my_player = sprites.create(assets.animation("cyberdruida_sprite_site1_animation")[0], SpriteKind.player)

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
    global facing_x, facing_y, my_player, score_start_level_2, level2_doors_opened

    if not level2_doors_opened and current_level_num == 2 and info.score() - score_start_level_2 >= 600:
        level2_doors_opened = True
        scene.camera_shake(3, 2000)
        music.spooky.play(200)
        my_player.say_text("Les portes s'obren!", 1500)
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

        # Si enemic i player estan a menys de x pixels, l'enemic s'activa
        if distance < 72:
            # Si l'enemic no s'esta movent (primera vegada que detecta el player)
            if enemy.vx == 0 and enemy.vy == 0:
                music.beam_up.play(100)
                enemy.say_text("!", 1000)
                effects.clear_particles(enemy)

            if not level2_doors_opened:
                enemy.follow(my_player, 70)
            else:
                enemy.follow(my_player, 30)

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
    
    update_player_animation()
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
        projectile = sprites.create_projectile_from_sprite(assets.animation("shoot_player_sprite_animation")[0], my_player, 0, 0)
        animation.run_image_animation(projectile, assets.animation("shoot_player_sprite_animation"), 50, True)

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
def spawn_enemies(location: tiles.Location, type_of_enemy: number):
    """
    Genera un enemic en posicions escollides segons tiles
    """
    if type_of_enemy == 1:
        enemy = sprites.create(assets.animation("inse-glitch_sprite_animation")[0], SpriteKind.enemy)
        animation.run_image_animation(enemy, assets.animation("inse-glitch_sprite_animation"), 200, True)
    else:
        enemy = sprites.create(assets.animation("tank_virus_sprite_animation")[0], SpriteKind.enemy)
        animation.run_image_animation(enemy, assets.animation("tank_virus_sprite_animation"), 200, True)
        statusbar = statusbars.create(20, 4, StatusBarKind.EnemyHealth)
        statusbar.attach_to_sprite(enemy)
        statusbar.max = 2
        statusbar.value = 2
        statusbar.set_flag(SpriteFlag.INVISIBLE, True)

    # El mostrem al tile corresponent
    tiles.place_on_tile(enemy, location)

    # Comencen dormits
    enemy.start_effect(effects.bubbles)


# GESTIÓ DE COL·LISIONS
def on_projectile_hit_enemy(projectile, enemy):
    """
    Gestiona quan un projectil xoca contra un enemic
    """
    global level2_doors_opened
    # Destruïm el projectil
    projectile.destroy()

    # Destruïm l'enemic
    if not level2_doors_opened:
        enemy.destroy(effects.fire, 500)
    else:
        bar = statusbars.get_status_bar_attached_to(StatusBarKind.EnemyHealth, enemy)
        if bar:
            bar.value -= 1
            enemy.start_effect(effects.fire)

        if bar.value <=0:
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

    boss_sprite = sprites.create(assets.animation("kernel_corrupt_sprite_animation")[0], Boss)
    animation.run_image_animation(boss_sprite, assets.animation("kernel_corrupt_sprite_animation"), 200, True)

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
        boss_projectile = sprites.create(assets.animation("shoot_finalboss_sprite_animation")[0], EnemyProjectile)
        
        boss_projectile.x = boss_sprite.x
        boss_projectile.y = boss_sprite.y
        
        animation.run_image_animation(boss_projectile, assets.animation("shoot_finalboss_sprite_animation"), 50, True)

        # Apunta el projectil cap el jugador
        boss_projectile.follow(my_player, 80)
        music.zapped.play(100)

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
    projectile.destroy(effects.fire)

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
            "- Targetes: " + str(keys_count) + "/2",
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
        game.splash("NIVELL 2", "Zona Corrupte")
    elif level == 3:
        tiles.set_tilemap(assets.tilemap("level5"))
        game.splash("NIVELL 3", "Kernel Corrupte")
        spawn_boss(175, 200)

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
            game.show_long_text("Has trobat l'arma CYBER GUN!\nAra prem A per disparar.", DialogLayout.BOTTOM)
    elif tiles.tile_at_location_equals(location, assets.tile("spawn_npc_base_floor")):
        music.magic_wand.play(100)
        if current_level_num == 1:
            game.show_long_text(
                "Cyber Druida! Has respost a la crida.", DialogLayout.BOTTOM
            )
            game.show_long_text(
                "GAIA-PRIME, el servidor viu, està sent devorat per una plaga de codi corrupte.", DialogLayout.BOTTOM
            )
            game.show_long_text(
                "Els sistemes convencionals han fallat.", DialogLayout.BOTTOM
            )
            game.show_long_text(
                "Només tu, un antivirus antic i oblidat, pots restaurar l'equilibri.", DialogLayout.BOTTOM
            )
            game.show_long_text(
                "Dins d'aquest cofre hi reposa la CYBER GUN.", DialogLayout.BOTTOM
            )
            game.show_long_text(
                "Agafa-la. Les teves runes de dades no destrueixen, purifiquen.", DialogLayout.BOTTOM
            )
        elif current_level_num == 2:
            game.show_long_text(
                "Benvingut a la Zona Corrupte.", DialogLayout.BOTTOM
            )
            game.show_long_text(
                "Abans era una zona de processament estable, on GAIA-PRIME regulava la vida.", DialogLayout.BOTTOM
            )
            game.show_long_text(
                "Però el Kernel Corrupte hi va arrelar, reescrivint el codi com una infecció.", DialogLayout.BOTTOM
            )
            game.show_long_text(
                "Les dades van començar a fallar, els camins es van trencar,i el sector va ser aïllat.", DialogLayout.BOTTOM
            )
            game.show_long_text(
                "Ara és un guantlet de supervivència.", DialogLayout.BOTTOM
            )
            game.show_long_text(
                "Si vols avançar, hauràs d'afrontar la corrupció de front.", DialogLayout.BOTTOM
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
    global lorepoint_counter
    lorepoint_counter += 1
    music.magic_wand.play(100)
    if lorepoint_counter == 1:
        game.show_long_text("ALERTA: Entitats Inse-Glitch detectades.", DialogLayout.BOTTOM)
        game.show_long_text("Són fragments de malware primitiu.", DialogLayout.BOTTOM)
        game.show_long_text("Ràpids. Inestables. Es mouen com un eixam de dades trencades", DialogLayout.BOTTOM)
        game.show_long_text("No pensen. Només infecten.", DialogLayout.BOTTOM)
        game.show_long_text("La sala romandrà segellada fins que totes les anomalies siguin purificades.", DialogLayout.BOTTOM)
        game.show_long_text("Elimina cada Inse-Glitch per desbloquejar l'accés a la següent zona.", DialogLayout.BOTTOM)
    elif lorepoint_counter == 2:
        game.show_long_text("Entitat detectada: EL TROYÀ.", DialogLayout.BOTTOM)
        game.show_long_text("Creat per ocultar corrupció dins d'estructures aparentment sòlides.", DialogLayout.BOTTOM)
        game.show_long_text("Funciona com una barrera viva, bloquejant camins i protegint el nucli del malware", DialogLayout.BOTTOM)
        game.show_long_text("No el subestimis.", DialogLayout.BOTTOM)
        game.show_long_text("La paciència i la precisió seran claus per reescriure'l.", DialogLayout.BOTTOM)
    elif lorepoint_counter == 3:
        game.show_long_text("Has arribat al Nucli.", DialogLayout.BOTTOM)
        game.show_long_text("Davant teu es troba el Kernel Corrupte.", DialogLayout.BOTTOM)
        game.show_long_text("El cor de GAIA-PRIME, ara dominat per ell.", DialogLayout.BOTTOM)
        game.show_long_text("Cada pulsació del seu ull és una ordre de destrucció.", DialogLayout.BOTTOM)
        game.show_long_text("Si cau el Kernel, el sistema serà restaurat.", DialogLayout.BOTTOM)
        game.show_long_text("Si caus tu, GAIA-PRIME serà esborrada per sempre.", DialogLayout.BOTTOM)
    if lorepoint_counter % 2 != 0:
        all_lore_locations = tiles.get_tiles_by_type(assets.tile("lore_point_base_floor"))    
        for loc in all_lore_locations:
            tiles.set_tile_at(loc, assets.tile("base_floor"))
    else:
        all_lore_locations2 = tiles.get_tiles_by_type(assets.tile("lore_point_base_floor2"))
        for loc2 in all_lore_locations2:
            tiles.set_tile_at(loc2, assets.tile("base_floor"))

# Crida de la funció
scene.on_overlap_tile(SpriteKind.player, assets.tile("lore_point_base_floor"), on_player_step_on_lore)
scene.on_overlap_tile(SpriteKind.player, assets.tile("lore_point_base_floor2"), on_player_step_on_lore)


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
    
    enemy_spawns = tiles.get_tiles_by_type(assets.tile("spawn_enemy_base_floor2"))
    for loc3_enemy in enemy_spawns:
        spawn_enemies(loc3_enemy, 2)
        tiles.set_tile_at(loc3_enemy, assets.tile("base_floor"))

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
    lorepoint_spawn = tiles.get_tiles_by_type(assets.tile("lore_point_base_floor2"))

# ANIMACIÓ DE PLAYER
def update_player_animation():
    global last_anim_state, my_player, facing_x, facing_y

    # Si no s'ha creat el player, no executem res, retornem
    if not my_player:
        return
    # Determinem si el jugador està en moviment
    is_moving = controller.dx() != 0 or controller.dy() != 0

    # Determinem l'estat actual
    current_state = ""

    # Canviem l'estat segons si té arma
    if has_weapon:
        current_state += "gun_"
    
    # Direcció
    # Si no s'està movent, agafem l'última direcció que apuntava
    if facing_y == -1:
        current_state += "back"
    if facing_y == 1:
        current_state += "front"
    if facing_x == -1:
        current_state += "left"
    if facing_x == 1:
        current_state += "right"
    
    # Executem l'animació només si el player es mou
    if current_state != last_anim_state:
        # Sense arma
        last_anim_state = current_state # actualitzem l'estat
        if current_state == "front":
            animation.run_image_animation(my_player, assets.animation("cyberdruida_sprite_front_animation"), 200, True)
        elif current_state == "back":
            animation.run_image_animation(my_player, assets.animation("cyberdruida_sprite_back_animation"), 200, True)
        elif current_state == "left":
            animation.run_image_animation(my_player, assets.animation("cyberdruida_sprite_site2_animation"), 200, True)
        elif current_state == "right":
            animation.run_image_animation(my_player, assets.animation("cyberdruida_sprite_site1_animation"), 200, True)
        
        # Amb arma
        elif current_state == "gun_front":
            animation.run_image_animation(my_player, assets.animation("gun_cyberdruida_sprite_front_animation"), 200, True)
        elif current_state == "gun_back":
            animation.run_image_animation(my_player, assets.animation("gun_cyberdruida_sprite_back_animation"), 200, True)
        elif current_state == "gun_left":
            animation.run_image_animation(my_player, assets.animation("gun_cyberdruida_sprite_site2_animation"), 200, True)
        elif current_state == "gun_right":
            animation.run_image_animation(my_player, assets.animation("gun_cyberdruida_sprite_site1_animation"), 200, True)
    
    # Si no es mou, parem les animacions
    if not is_moving:
        animation.stop_animation(animation.AnimationTypes.ALL, my_player)

        # Canviem l'estat a quiet
        last_anim_state = "not_moving"
        # Agafem el primer frame de cada animacio per quedarnos mirant cap allà
        if current_state == "front":
            my_player.set_image(assets.animation("cyberdruida_sprite_front_animation")[0])
        elif current_state == "back":
            my_player.set_image(assets.animation("cyberdruida_sprite_back_animation")[0])
        elif current_state == "left":
            my_player.set_image(assets.animation("cyberdruida_sprite_site2_animation")[0])
        elif current_state == "right":
            my_player.set_image(assets.animation("cyberdruida_sprite_site1_animation")[0])
        elif current_state == "gun_front":
            my_player.set_image(assets.animation("gun_cyberdruida_sprite_front_animation")[0])
        elif current_state == "gun_back":
            my_player.set_image(assets.animation("gun_cyberdruida_sprite_back_animation")[0])
        elif current_state == "gun_left":
            my_player.set_image(assets.animation("gun_cyberdruida_sprite_site2_animation")[0])
        elif current_state == "gun_right":
            my_player.set_image(assets.animation("gun_cyberdruida_sprite_site1_animation")[0])

# TRIGGER DEL JOC
def start_game():
    """
    inicia el joc setejant el jugador i el nivell que pertoqui
    """
    scene.set_background_image(None)
    setup_player()
    load_level(current_level_num)

# PANTALLES DE LORE
def mostrar_lore():
    """
    Mostra les pantalles d'història i després torna al menú.
    """
    # Posem un fons fosc o diferent si voleu, o mantenim l'actual
    scene.set_background_image(assets.image("bg"))
    
    music.magic_wand.play()
    
    game.show_long_text(
        "ACCÉS A ARXIUS DE GAIA-PRIME...\n" +
        "El servidor viu està sent devorat per una plaga de codi corrupte.",
        DialogLayout.BOTTOM
    )
    game.show_long_text(
        "Els sistemes convencionals han fallat.\n" +
        "El Kernel Corrupte ha arrelat, reescrivint el codi com una infecció.",
        DialogLayout.BOTTOM
    )
    game.show_long_text(
        "Només tu, CYBER-DRUIDA, un antivirus antic i oblidat, pots restaurar l'equilibri.",
        DialogLayout.BOTTOM
    )
    game.show_long_text(
        "OBJECTIU:\n" +
        "- Troba les tarjetes d'accés.\n" +
        "- Elimina els virus.\n" +
        "- Destrueix el Kernel Corrupte.",
        DialogLayout.BOTTOM
    )
    
    # Tornem a cridar el menú principal
    show_menu()

# MENÚ PRINCIPAL:
def show_menu():
    """
    Pantalla d'inici del joc
    """
    # Assegurem que no hi ha sprites d'altres partides si tornem enrere
    sprites.destroy_all_sprites_of_kind(SpriteKind.player)
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)

    # Fons del menú
    scene.set_background_color(15)
    scene.set_background_image(assets.image("bg"))

    pause(1)

    seleccio = game.ask("CYBER-DRUID: El Reinici", "A: JUGAR   B: LORE")

    if seleccio:
        start_game()
    elif not seleccio:
        mostrar_lore()

# EXECUCIÓ

show_menu()

