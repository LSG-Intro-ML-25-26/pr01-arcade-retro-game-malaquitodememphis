//  ===============================
//  ERIC LORENZO
//  FRANCIS MORETA
//  ===============================
//  VARIABLES GLOBALS
//  Sprites
let Boss = SpriteKind.create()
let EnemyProjectile = SpriteKind.create()
let Chest = SpriteKind.create()
let NPC = SpriteKind.create()
let my_player : Sprite = null
let boss_sprite : Sprite = null
let boss_statusbar : StatusBarSprite = null
//  Variables
let inventory_list : string[] = []
let has_weapon = false
let current_level_num = 1
let has_key = false
let loading_level = false
let score_start_level_2 = 0
let level2_doors_opened = false
let lorepoint_counter = 0
//  Variables d'estat
let facing_x = 1
let facing_y = 0
let last_anim_state = ""
//  Constants
let projectile_speed = 200
let enemy_speed = 50
game.setGameOverMessage(false, "☠️HAS PERDUT!☠️")
game.setGameOverMessage(true, "🏆SERVIDOR RESTAURAT!🏆")
//  FUNCIÓ DE CONFIGURACIÓ
function on_start() {
    music.play(music.stringPlayable("C5 B C5 A C5 G C5 C C5 B C5 A C5 G C5 C B A B G# B F B E B A B G# B F B E A G A F A E A D A G A F A E A D G# F G# E G# D G# C G# F G# E G# D G# C", 240), music.PlaybackMode.LoopingInBackground)
}

on_start()
function setup_player() {
    /** Crea el sprite del jugador, defineix les seves físiques i estableix vides. */
    
    //  Placeholder temporal per my_player
    my_player = sprites.create(assets.animation`cyberdruida_sprite_site1_animation`[0], SpriteKind.Player)
    //  Físiques de moviment
    controller.moveSprite(my_player, 100, 100)
    //  La càmara segueix el jugador
    scene.cameraFollowSprite(my_player)
    //  Sistema de vides
    info.setLife(3)
}

//  BUCLE D'ACTUALITZACIÓ
//  Vinculem la funció del bucle al joc
game.onUpdate(function on_game_update() {
    let laser_loc: tiles.Location[];
    let dx: number;
    let dy: number;
    let distance: number;
    /** Aquesta funció s'executa a cada frame del joc */
    
    if (!level2_doors_opened && current_level_num == 2 && info.score() - score_start_level_2 >= 600) {
        level2_doors_opened = true
        scene.cameraShake(3, 2000)
        music.spooky.play(200)
        my_player.sayText("Les portes s'obren!", 1500)
        //  Agafem els tiles laser
        laser_loc = tiles.getTilesByType(assets.tile`laser_block_wall`)
        for (let loc of laser_loc) {
            tiles.setTileAt(loc, assets.tile`way_floor`)
            tiles.setWallAt(loc, false)
        }
    }
    
    //  Esborrem els murs
    //  Obtenim tots els enemics del mapa
    let all_enemies = sprites.allOfKind(SpriteKind.Enemy)
    for (let enemy of all_enemies) {
        //  Calculem la distància entre jugador i enemic
        dx = enemy.x - my_player.x
        dy = enemy.y - my_player.y
        //  Fórmula hipotenusa
        distance = Math.sqrt(dx * dx + dy * dy)
        //  Si enemic i player estan a menys de x pixels, l'enemic s'activa
        if (distance < 72) {
            //  Si l'enemic no s'esta movent (primera vegada que detecta el player)
            if (enemy.vx == 0 && enemy.vy == 0) {
                music.beamUp.play(100)
                enemy.sayText("!", 1000)
                effects.clearParticles(enemy)
            }
            
            if (!level2_doors_opened) {
                enemy.follow(my_player, 70)
            } else {
                enemy.follow(my_player, 30)
            }
            
        }
        
    }
    //  Detectem si el jugador s'està movent
    if (controller.dx() != 0 || controller.dy() != 0) {
        //  Si ens movem, actualitzem la direcció on mirem.
        //  Gestió eix X
        if (controller.dx() > 0) {
            facing_x = 1
        } else if (controller.dx() < 0) {
            facing_x = -1
        } else {
            facing_x = 0
        }
        
        //  Gestió eix Y
        if (controller.dy() > 0) {
            facing_y = 1
        } else if (controller.dy() < 0) {
            facing_y = -1
        } else {
            facing_y = 0
        }
        
        //  Gestió de diagonals (excepció)
        if (facing_x != 0 && facing_y != 0) {
            
        }
        
    }
    
    update_player_animation()
})
//  SISTEMA DE COMBAT
//  Vinculem al botó A la funció shoot_projectile
controller.A.onEvent(ControllerButtonEvent.Pressed, function shoot_projectile() {
    let projectile: Sprite;
    /** Genera un projectil desde la possició del jugador */
    
    //  Només disparem si el jugador existeix
    if (my_player && has_weapon) {
        //  Creem el projectil (placeholder momentani)
        projectile = sprites.createProjectileFromSprite(assets.animation`shoot_player_sprite_animation`[0], my_player, 0, 0)
        animation.runImageAnimation(projectile, assets.animation`shoot_player_sprite_animation`, 50, true)
        //  Lògica per disparar cap on mirem
        if (facing_x == 0 && facing_y == 0) {
            projectile.vx = projectile_speed
        } else {
            //  direcció projectil per defecte: dreta
            //  Velocitat del projectil segons velocitat del jugador
            projectile.vx = facing_x * projectile_speed
            projectile.vy = facing_y * projectile_speed
        }
        
        music.pewPew.play(100)
        //  Destruïm el projectil un cop surt de la pantalla o xoca contra una paret
        projectile.setFlag(SpriteFlag.DestroyOnWall, true)
    } else if (my_player && !has_weapon) {
        music.thump.play(100)
    }
    
})
//  GENERACIÓ D'ENEMICS
function spawn_enemies(location: tiles.Location, type_of_enemy: number) {
    let enemy: Sprite;
    let statusbar: StatusBarSprite;
    /** Genera un enemic en posicions escollides segons tiles */
    if (type_of_enemy == 1) {
        enemy = sprites.create(assets.animation`inse-glitch_sprite_animation`[0], SpriteKind.Enemy)
        animation.runImageAnimation(enemy, assets.animation`inse-glitch_sprite_animation`, 200, true)
    } else {
        enemy = sprites.create(assets.animation`tank_virus_sprite_animation`[0], SpriteKind.Enemy)
        animation.runImageAnimation(enemy, assets.animation`tank_virus_sprite_animation`, 200, true)
        statusbar = statusbars.create(20, 4, StatusBarKind.EnemyHealth)
        statusbar.attachToSprite(enemy)
        statusbar.max = 2
        statusbar.value = 2
        statusbar.setFlag(SpriteFlag.Invisible, true)
    }
    
    //  El mostrem al tile corresponent
    tiles.placeOnTile(enemy, location)
    //  Comencen dormits
    enemy.startEffect(effects.bubbles)
}

//  GESTIÓ DE COL·LISIONS
//  Registrem l'esdeveniment
sprites.onOverlap(SpriteKind.Projectile, SpriteKind.Enemy, function on_projectile_hit_enemy(projectile: Sprite, enemy: Sprite) {
    let bar: StatusBarSprite;
    /** Gestiona quan un projectil xoca contra un enemic */
    
    //  Destruïm el projectil
    projectile.destroy()
    //  Destruïm l'enemic
    if (!level2_doors_opened) {
        enemy.destroy(effects.fire, 500)
    } else {
        bar = statusbars.getStatusBarAttachedTo(StatusBarKind.EnemyHealth, enemy)
        if (bar) {
            bar.value -= 1
            enemy.startEffect(effects.fire)
        }
        
        if (bar.value <= 0) {
            enemy.destroy(effects.fire, 500)
        }
        
    }
    
    music.smallCrash.play(100)
    //  Sumem punts
    info.changeScoreBy(100)
})
//  Registrem l'esdeveniment
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function on_enemy_hit_player(player: Sprite, enemy: Sprite) {
    /** Gestiona quan un enemic xoca contra el jugador */
    //  Restem una vida
    info.changeLifeBy(-1)
    music.zapped.play(100)
    info.changeScoreBy(100)
    //  Destruïm l'enemic
    enemy.destroy(effects.fire, 500)
    //  Feedback visual (sacsejar càmera)
    scene.cameraShake(4, 500)
})
//  FUNCIONS DEL "FINAL BOSS"
function spawn_boss(x_pos: number, y_pos: number) {
    /** Invoca el "Kernel Corrupte" */
    
    boss_sprite = sprites.create(assets.animation`kernel_corrupt_sprite_animation`[0], Boss)
    animation.runImageAnimation(boss_sprite, assets.animation`kernel_corrupt_sprite_animation`, 200, true)
    //  El col·loquem
    boss_sprite.x = x_pos
    boss_sprite.y = y_pos
    //  Li donem vida (extensió de "status-bar")
    boss_statusbar = statusbars.create(20, 4, StatusBarKind.EnemyHealth)
    boss_statusbar.max = 20
    boss_statusbar.value = 20
    boss_statusbar.setColor(7, 2)
    boss_statusbar.attachToSprite(boss_sprite)
    //  "IA" del "boss"
    game.onUpdateInterval(2000, function boss_shooting_pattern() {
        let boss_projectile: Sprite;
        /** Funció executada periòdicament perquè el "boss" dispari */
        
        //  Només disparem si ambdós sprites existeixen
        if (boss_sprite && my_player) {
            //  Creem el projectil enemic
            boss_projectile = sprites.create(assets.animation`shoot_finalboss_sprite_animation`[0], EnemyProjectile)
            boss_projectile.x = boss_sprite.x
            boss_projectile.y = boss_sprite.y
            animation.runImageAnimation(boss_projectile, assets.animation`shoot_finalboss_sprite_animation`, 50, true)
            //  Apunta el projectil cap el jugador
            boss_projectile.follow(my_player, 80)
            music.zapped.play(100)
            //  Destruïm el projectil un cop surt de la pantalla o xoca contra una paret
            boss_projectile.setFlag(SpriteFlag.DestroyOnWall, true)
        }
        
    })
}

//  COL·LISIONS DEL "FINAL BOSS"
//  Registrem l'esdeveniment
sprites.onOverlap(SpriteKind.Projectile, Boss, function on_projectile_hit_boss(projectile: Sprite, boss_sprite: Sprite) {
    /** Gestiona quan un projectil de player xoca contra el final boss */
    projectile.destroy()
    //  Si hi ha statusbar, li restem 1
    if (boss_statusbar) {
        boss_statusbar.value -= 1
        music.smallCrash.play(100)
    }
    
    //  FX
    boss_sprite.startEffect(effects.ashes, 200)
})
//  Registrem l'esdeveniment
sprites.onOverlap(SpriteKind.Player, Boss, function on_boss_hit_player(player: Sprite, boss: Sprite) {
    /** Si el player xoca contra el boss */
    info.changeLifeBy(-1)
    music.zapped.play(100)
    scene.cameraShake(4, 500)
})
//  Registrem l'esdeveniment
statusbars.onZero(StatusBarKind.EnemyHealth, function on_boss_death(status: StatusBarSprite) {
    /** Quan el boss mori (statusbar = 0) */
    if (boss_sprite) {
        boss_sprite.destroy(effects.fire, 1000)
        music.stopAllSounds()
        music.powerUp.play(100)
        game.over(true)
    }
    
})
info.onLifeZero(function on_life_zero() {
    /** Quan ens quedem sense vides */
    music.stopAllSounds()
    music.wawawawaa.play()
    game.gameOver(false)
})
//  Registrem l'esdeveniment
sprites.onOverlap(SpriteKind.Player, EnemyProjectile, function on_enemy_projectile_hit_player(player: Sprite, projectile: Sprite) {
    /** Quan els projectils del bos xocan contra el player */
    //  Restem vida al jugador
    info.changeLifeBy(-1)
    //  Destruïm el projectil
    projectile.destroy(effects.fire)
    //  Efecte visual
    scene.cameraShake(4, 200)
})
//  SISTEMA D'INVENTARI
function spawn_key(location: tiles.Location) {
    /** Mostra les claus a les localitzacions assignades segons tiles */
    let key_sprite = sprites.create(assets.tile`access_card_base_floor`, SpriteKind.Food)
    tiles.placeOnTile(key_sprite, location)
    //  FX
    key_sprite.startEffect(effects.halo)
}

//  Funcion para recoger la llave
sprites.onOverlap(SpriteKind.Player, SpriteKind.Food, function on_collect_key(player: Sprite, item: Sprite) {
    /** Funció per recollir la clau */
    
    has_key = true
    //  Añade la llave al inventario
    
    inventory_list.push("Key Card")
    item.destroy()
    music.baDing.play(100)
    player.sayText("Tinc la clau!", 1000)
})
//  Registrem l'esdeveniment al botó "B"
controller.B.onEvent(ControllerButtonEvent.Pressed, function show_inventory() {
    /** Mostra una finestra amb l'inventari */
    
    //  Variables amb valors per defecte
    let weapon = "No"
    let keys_count = 0
    if (has_weapon) {
        weapon = "Cyber Gun"
    }
    
    //  Comptem les claus de l'inventari
    for (let item of inventory_list) {
        if (item == "Key Card") {
            keys_count += 1
        }
        
    }
    game.showLongText("==============\n" + "INVENTARI:\n" + "==============\n" + "- Arma: " + weapon + "\n" + "- Targetes: " + ("" + keys_count) + "/2", DialogLayout.Center)
})
//  FUNCIÓ D'OBJECTE: COFRE
function spawn_chest(location: any) {
    /** Crea un cofre en una Posició */
    let chest = sprites.create(img`
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
    `, Chest)
    tiles.placeOnTile(chest, location)
}

//  FUNCIONS MONITOR NPC
function spawn_lore_monitor(location: any) {
    let monitor = sprites.create(img`
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
    `, NPC)
    tiles.placeOnTile(monitor, location)
}

//  GESTIÓ DE NIVELLS
function load_level(level: number) {
    /** Gestiona el canvi de nivells */
    
    //  Reiniciar el nivell
    has_key = false
    sprites.destroyAllSpritesOfKind(SpriteKind.Enemy)
    sprites.destroyAllSpritesOfKind(SpriteKind.Food)
    sprites.destroyAllSpritesOfKind(NPC)
    //  Selecciona el mapa
    if (level == 1) {
        tiles.setTilemap(assets.tilemap`level1`)
        game.splash("NIVELL 1", "Entrenament")
    } else if (level == 2) {
        score_start_level_2 = info.score()
        tiles.setTilemap(assets.tilemap`level6`)
        game.splash("NIVELL 2", "Zona Corrupte")
    } else if (level == 3) {
        tiles.setTilemap(assets.tilemap`level5`)
        game.splash("NIVELL 3", "Kernel Corrupte")
        spawn_boss(175, 200)
    }
    
    //  Spawn del jugador
    let player_spawns = tiles.getTilesByType(assets.tile`spawn_player_base_floor`)
    //  Retorna el tile a la normalitat (borra el spawn)
    if (player_spawns.length > 0) {
        tiles.placeOnTile(my_player, player_spawns[0])
        tiles.setTileAt(player_spawns[0], assets.tile`base_floor`)
    }
    
    // Crida de funció
    spawn_objects_from_tiles()
}

//  GESTIÓ DE COL·LISIONS
//  Trigger que activa la funció
scene.onHitWall(SpriteKind.Player, function on_hit_door_wall(player: Sprite, location: tiles.Location) {
    let loading_level: boolean;
    /** Gestiona si s'ha de fer alguna cosa en xocar amb tiles concrets */
    
    if (tiles.tileAtLocationEquals(location, assets.tile`acces_doors`)) {
        // Passa de nivell si té la clau
        if (has_key && !loading_level) {
            loading_level = true
            music.spooky.play(200)
            pause(500)
            current_level_num += 1
            load_level(current_level_num)
            loading_level = false
        } else {
            // Sense la clau, xoca amb la porta i rebota
            player.sayText("Tancat!", 500)
            music.thump.play(200)
            scene.cameraShake(2, 200)
            // Rebot del jugador
            if (player.vx > 0) {
                player.x -= 5
            }
            
            if (player.vx < 0) {
                player.x += 5
            }
            
            if (player.vy > 0) {
                player.y -= 5
            }
            
            if (player.vy < 0) {
                player.y += 5
            }
            
        }
        
    } else if (tiles.tileAtLocationEquals(location, assets.tile`close_chest`)) {
        
        if (!has_weapon) {
            has_weapon = true
            inventory_list.push("Cyber Gun")
            music.baDing.play(100)
            tiles.setTileAt(location, assets.tile`open_chest`)
            game.showLongText(`Has trobat l'arma CYBER GUN!
Ara prem A per disparar.`, DialogLayout.Bottom)
        }
        
    } else if (tiles.tileAtLocationEquals(location, assets.tile`spawn_npc_base_floor`)) {
        music.magicWand.play(100)
        if (current_level_num == 1) {
            game.showLongText("Cyber Druida! Has respost a la crida.", DialogLayout.Bottom)
            game.showLongText("GAIA-PRIME, el servidor viu, està sent devorat per una plaga de codi corrupte.", DialogLayout.Bottom)
            game.showLongText("Els sistemes convencionals han fallat.", DialogLayout.Bottom)
            game.showLongText("Només tu, un antivirus antic i oblidat, pots restaurar l'equilibri.", DialogLayout.Bottom)
            game.showLongText("Dins d'aquest cofre hi reposa la CYBER GUN.", DialogLayout.Bottom)
            game.showLongText("Agafa-la. Les teves runes de dades no destrueixen, purifiquen.", DialogLayout.Bottom)
        } else if (current_level_num == 2) {
            game.showLongText("Benvingut a la Zona Corrupte.", DialogLayout.Bottom)
            game.showLongText("Abans era una zona de processament estable, on GAIA-PRIME regulava la vida.", DialogLayout.Bottom)
            game.showLongText("Però el Kernel Corrupte hi va arrelar, reescrivint el codi com una infecció.", DialogLayout.Bottom)
            game.showLongText("Les dades van començar a fallar, els camins es van trencar,i el sector va ser aïllat.", DialogLayout.Bottom)
            game.showLongText("Ara és un guantlet de supervivència.", DialogLayout.Bottom)
            game.showLongText("Si vols avançar, hauràs d'afrontar la corrupció de front.", DialogLayout.Bottom)
        }
        
    } else if (tiles.tileAtLocationEquals(location, assets.tile`laser_block_wall`)) {
        player.sayText("Tancat! Mata a tots els virus!", 500)
        music.thump.play(200)
        scene.cameraShake(1, 100)
        player.x -= 5
    }
    
})
function on_player_step_on_lore(player: Sprite, location: tiles.Location) {
    let all_lore_locations: tiles.Location[];
    let all_lore_locations2: tiles.Location[];
    /** Gestiona els missatges de lore en trepitjar punts concrets */
    
    lorepoint_counter += 1
    music.magicWand.play(100)
    if (lorepoint_counter == 1) {
        game.showLongText("ALERTA: Entitats Inse-Glitch detectades.", DialogLayout.Bottom)
        game.showLongText("Són fragments de malware primitiu.", DialogLayout.Bottom)
        game.showLongText("Ràpids. Inestables. Es mouen com un eixam de dades trencades", DialogLayout.Bottom)
        game.showLongText("No pensen. Només infecten.", DialogLayout.Bottom)
        game.showLongText("La sala romandrà segellada fins que totes les anomalies siguin purificades.", DialogLayout.Bottom)
        game.showLongText("Elimina cada Inse-Glitch per desbloquejar l'accés a la següent zona.", DialogLayout.Bottom)
    } else if (lorepoint_counter == 2) {
        game.showLongText("Entitat detectada: EL TROYÀ.", DialogLayout.Bottom)
        game.showLongText("Creat per ocultar corrupció dins d'estructures aparentment sòlides.", DialogLayout.Bottom)
        game.showLongText("Funciona com una barrera viva, bloquejant camins i protegint el nucli del malware", DialogLayout.Bottom)
        game.showLongText("No el subestimis.", DialogLayout.Bottom)
        game.showLongText("La paciència i la precisió seran claus per reescriure'l.", DialogLayout.Bottom)
    } else if (lorepoint_counter == 3) {
        game.showLongText("Has arribat al Nucli.", DialogLayout.Bottom)
        game.showLongText("Davant teu es troba el Kernel Corrupte.", DialogLayout.Bottom)
        game.showLongText("El cor de GAIA-PRIME, ara dominat per ell.", DialogLayout.Bottom)
        game.showLongText("Cada pulsació del seu ull és una ordre de destrucció.", DialogLayout.Bottom)
        game.showLongText("Si cau el Kernel, el sistema serà restaurat.", DialogLayout.Bottom)
        game.showLongText("Si caus tu, GAIA-PRIME serà esborrada per sempre.", DialogLayout.Bottom)
    }
    
    if (lorepoint_counter % 2 != 0) {
        all_lore_locations = tiles.getTilesByType(assets.tile`lore_point_base_floor`)
        for (let loc of all_lore_locations) {
            tiles.setTileAt(loc, assets.tile`base_floor`)
        }
    } else {
        all_lore_locations2 = tiles.getTilesByType(assets.tile`lore_point_base_floor2`)
        for (let loc2 of all_lore_locations2) {
            tiles.setTileAt(loc2, assets.tile`base_floor`)
        }
    }
    
}

//  Crida de la funció
scene.onOverlapTile(SpriteKind.Player, assets.tile`lore_point_base_floor`, on_player_step_on_lore)
scene.onOverlapTile(SpriteKind.Player, assets.tile`lore_point_base_floor2`, on_player_step_on_lore)
//  GENERACIÓ DE SPRITES
function spawn_objects_from_tiles() {
    /** Crea enemics i objectes segons les tiles del mapa actual */
    //  Genera enemics al spawn
    let enemy_spawns = tiles.getTilesByType(assets.tile`spawn_enemy_way_floor`)
    for (let loc_enemy of enemy_spawns) {
        spawn_enemies(loc_enemy, 1)
        tiles.setTileAt(loc_enemy, assets.tile`way_floor`)
    }
    enemy_spawns = tiles.getTilesByType(assets.tile`spawn_enemy_base_floor`)
    for (let loc2_enemy of enemy_spawns) {
        spawn_enemies(loc2_enemy, 1)
        tiles.setTileAt(loc2_enemy, assets.tile`base_floor`)
    }
    enemy_spawns = tiles.getTilesByType(assets.tile`spawn_enemy_base_floor2`)
    for (let loc3_enemy of enemy_spawns) {
        spawn_enemies(loc3_enemy, 2)
        tiles.setTileAt(loc3_enemy, assets.tile`base_floor`)
    }
    //  Genera la clau al spawn
    let key_spawns = tiles.getTilesByType(assets.tile`access_card_base_floor`)
    for (let loc_key of key_spawns) {
        spawn_key(loc_key)
        tiles.setTileAt(loc_key, assets.tile`base_floor`)
    }
    //  Genera el chest al spawn
    let chest_spawn = tiles.getTilesByType(assets.tile`close_chest`)
    for (let loc_chest of chest_spawn) {
        spawn_chest(loc_chest)
    }
    //  Genera el NPC al spawn
    let monitor_spawn = tiles.getTilesByType(assets.tile`spawn_npc_base_floor`)
    for (let loc_monitor of monitor_spawn) {
        spawn_lore_monitor(loc_monitor)
    }
    //  Genera el lorepoint al spawn
    let lorepoint_spawn = tiles.getTilesByType(assets.tile`lore_point_base_floor`)
    lorepoint_spawn = tiles.getTilesByType(assets.tile`lore_point_base_floor2`)
}

//  ANIMACIÓ DE PLAYER
function update_player_animation() {
    
    //  Si no s'ha creat el player, no executem res, retornem
    if (!my_player) {
        return
    }
    
    //  Determinem si el jugador està en moviment
    let is_moving = controller.dx() != 0 || controller.dy() != 0
    //  Determinem l'estat actual
    let current_state = ""
    //  Canviem l'estat segons si té arma
    if (has_weapon) {
        current_state += "gun_"
    }
    
    //  Direcció
    //  Si no s'està movent, agafem l'última direcció que apuntava
    if (facing_y == -1) {
        current_state += "back"
    }
    
    if (facing_y == 1) {
        current_state += "front"
    }
    
    if (facing_x == -1) {
        current_state += "left"
    }
    
    if (facing_x == 1) {
        current_state += "right"
    }
    
    //  Executem l'animació només si el player es mou
    if (current_state != last_anim_state) {
        //  Sense arma
        last_anim_state = current_state
        //  actualitzem l'estat
        if (current_state == "front") {
            animation.runImageAnimation(my_player, assets.animation`cyberdruida_sprite_front_animation`, 200, true)
        } else if (current_state == "back") {
            animation.runImageAnimation(my_player, assets.animation`cyberdruida_sprite_back_animation`, 200, true)
        } else if (current_state == "left") {
            animation.runImageAnimation(my_player, assets.animation`cyberdruida_sprite_site2_animation`, 200, true)
        } else if (current_state == "right") {
            animation.runImageAnimation(my_player, assets.animation`cyberdruida_sprite_site1_animation`, 200, true)
        } else if (current_state == "gun_front") {
            //  Amb arma
            animation.runImageAnimation(my_player, assets.animation`gun_cyberdruida_sprite_front_animation`, 200, true)
        } else if (current_state == "gun_back") {
            animation.runImageAnimation(my_player, assets.animation`gun_cyberdruida_sprite_back_animation`, 200, true)
        } else if (current_state == "gun_left") {
            animation.runImageAnimation(my_player, assets.animation`gun_cyberdruida_sprite_site2_animation`, 200, true)
        } else if (current_state == "gun_right") {
            animation.runImageAnimation(my_player, assets.animation`gun_cyberdruida_sprite_site1_animation`, 200, true)
        }
        
    }
    
    //  Si no es mou, parem les animacions
    if (!is_moving) {
        animation.stopAnimation(animation.AnimationTypes.All, my_player)
        //  Canviem l'estat a quiet
        last_anim_state = "not_moving"
        //  Agafem el primer frame de cada animacio per quedarnos mirant cap allà
        if (current_state == "front") {
            my_player.setImage(assets.animation`cyberdruida_sprite_front_animation`[0])
        } else if (current_state == "back") {
            my_player.setImage(assets.animation`cyberdruida_sprite_back_animation`[0])
        } else if (current_state == "left") {
            my_player.setImage(assets.animation`cyberdruida_sprite_site2_animation`[0])
        } else if (current_state == "right") {
            my_player.setImage(assets.animation`cyberdruida_sprite_site1_animation`[0])
        } else if (current_state == "gun_front") {
            my_player.setImage(assets.animation`gun_cyberdruida_sprite_front_animation`[0])
        } else if (current_state == "gun_back") {
            my_player.setImage(assets.animation`gun_cyberdruida_sprite_back_animation`[0])
        } else if (current_state == "gun_left") {
            my_player.setImage(assets.animation`gun_cyberdruida_sprite_site2_animation`[0])
        } else if (current_state == "gun_right") {
            my_player.setImage(assets.animation`gun_cyberdruida_sprite_site1_animation`[0])
        }
        
    }
    
}

//  TRIGGER DEL JOC
function start_game() {
    /** inicia el joc setejant el jugador i el nivell que pertoqui */
    scene.setBackgroundImage(null)
    setup_player()
    load_level(current_level_num)
}

//  PANTALLES DE LORE
function mostrar_lore() {
    /** Mostra les pantalles d'història i després torna al menú. */
    //  Posem un fons fosc o diferent si voleu, o mantenim l'actual
    scene.setBackgroundImage(assets.image`bg`)
    music.magicWand.play()
    game.showLongText(`ACCÉS A ARXIUS DE GAIA-PRIME...
` + "El servidor viu està sent devorat per una plaga de codi corrupte.", DialogLayout.Bottom)
    game.showLongText(`Els sistemes convencionals han fallat.
` + "El Kernel Corrupte ha arrelat, reescrivint el codi com una infecció.", DialogLayout.Bottom)
    game.showLongText("Només tu, CYBER-DRUIDA, un antivirus antic i oblidat, pots restaurar l'equilibri.", DialogLayout.Bottom)
    game.showLongText("OBJECTIU:\n" + `- Troba les tarjetes d'accés.
` + `- Elimina els virus.
` + "- Destrueix el Kernel Corrupte.", DialogLayout.Bottom)
    //  Tornem a cridar el menú principal
    show_menu()
}

//  MENÚ PRINCIPAL:
function show_menu() {
    /** Pantalla d'inici del joc */
    //  Assegurem que no hi ha sprites d'altres partides si tornem enrere
    sprites.destroyAllSpritesOfKind(SpriteKind.Player)
    sprites.destroyAllSpritesOfKind(SpriteKind.Enemy)
    //  Fons del menú
    scene.setBackgroundColor(15)
    scene.setBackgroundImage(assets.image`bg`)
    pause(1)
    let seleccio = game.ask("CYBER-DRUID: El Reinici", "A: JUGAR   B: LORE")
    if (seleccio) {
        start_game()
    } else if (!seleccio) {
        mostrar_lore()
    }
    
}

//  EXECUCIÓ
show_menu()
