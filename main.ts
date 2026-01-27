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
//  Variables d'estat de d'apuntament (dreta per defecte)
let facing_x = 1
let facing_y = 0
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
    my_player = sprites.create(img`
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
        `, SpriteKind.Player)
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
    /** Aquesta funció s'executa a cada frame del joc */
    
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
    
})
//  SISTEMA DE COMBAT
//  Vinculem al botó A la funció shoot_projectile
controller.A.onEvent(ControllerButtonEvent.Pressed, function shoot_projectile() {
    let projectile: Sprite;
    /** Genera un projectil desde la possició del jugador */
    
    //  Només disparem si el jugador existeix
    if (my_player && has_weapon) {
        //  Creem el projectil (placeholder momentani)
        projectile = sprites.createProjectileFromSprite(img`
        . . . . .
        . . 5 . .
        . 5 5 5 .
        . . 5 . .
        . . . . .
        `, my_player, 0, 0)
        //  Velocitat inicial: 0
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
function spawn_enemies(location: tiles.Location, number_of_enemies: number) {
    let enemy: Sprite;
    /** Genera una llista d'enemics en posicions escollides segons tiles */
    //  Bucle per generar 'n' enemics
    for (let i = 0; i < number_of_enemies; i++) {
        //  Creem l'enemic
        enemy = sprites.create(img`
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
        `, SpriteKind.Enemy)
        //  Els mostrem als tiles corresponents
        tiles.placeOnTile(enemy, location)
        //  Perseguim el jugador
        enemy.follow(my_player, 30)
    }
}

//  GESTIÓ DE COL·LISIONS
//  Registrem l'esdeveniment
sprites.onOverlap(SpriteKind.Projectile, SpriteKind.Enemy, function on_projectile_hit_enemy(projectile: Sprite, enemy: Sprite) {
    /** Gestiona quan un projectil xoca contra un enemic */
    //  Destruïm el projectil
    projectile.destroy()
    //  Destruïm l'enemic
    enemy.destroy(effects.disintegrate, 500)
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
    //  Destruïm l'enemic
    enemy.destroy(effects.fire, 500)
    //  Feedback visual (sacsejar càmera)
    scene.cameraShake(4, 500)
})
//  FUNCIONS DEL "FINAL BOSS"
function spawn_boss(x_pos: number, y_pos: number) {
    /** Invoca el "Kernel Corrupte" */
    
    boss_sprite = sprites.create(img`
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
    `, Boss)
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
            boss_projectile = sprites.createProjectileFromSprite(img`
        . . . 2 . . .
        . . 2 2 2 . .
        . 2 2 2 2 2 .
        . . 2 2 2 . .
        . . . 2 . . .
        `, boss_sprite, 0, 0)
            boss_projectile.setKind(EnemyProjectile)
            //  Apunta el projectil cap el jugador
            boss_projectile.follow(my_player, 80)
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
        boss_sprite.destroy(effects.disintegrate, 1000)
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
    projectile.destroy()
    //  Efecte visual
    scene.cameraShake(4, 200)
})
//  SISTEMA D'INVENTARI
function spawn_key(location: tiles.Location) {
    /** Mostra les claus a les localitzacions assignades segons tiles */
    let key_sprite = sprites.create(assets.tile`access_card_base_floor`, SpriteKind.Food)
    tiles.placeOnTile(key_sprite, location)
    //  FX
    key_sprite.startEffect(effects.halo, 2000)
}

//  Funcion para recoger la llave
sprites.onOverlap(SpriteKind.Player, SpriteKind.Food, function on_collect_key(player: Sprite, item: Sprite) {
    /** Funció per recollir la clau */
    
    has_key = true
    //  Añade la llave al inventario
    
    inventory_list.push("Key Card")
    item.destroy(effects.fire, 500)
    music.baDing.play(100)
    player.sayText("¡Tengo la llave!", 1000)
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
    game.showLongText("===============" + "INVENTARI:\n" + "===============" + "- Arma: " + weapon + "\n" + "- Targetes: " + ("" + keys_count) + "/3", DialogLayout.Center)
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
        tiles.setTilemap(assets.tilemap`level4`)
        game.splash("NIVELL 2", "Zona Corrupta")
    } else if (level == 3) {
        tiles.setTilemap(assets.tilemap`level5`)
        game.splash("NIVELL 3", "Boss Final")
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
    /** Gestiona si s'ha de fer alguna cosa en xocar amb tiles concrets */
    
    if (tiles.tileAtLocationEquals(location, assets.tile`acces_doors`)) {
        // Passa de nivell si té la clau
        if (has_key) {
            music.spooky.play(100)
            player.sayText("Obrint!", 1000)
            pause(1000)
            current_level_num += 1
            load_level(current_level_num)
        } else {
            // Sense la clau, xoca amb la porta i rebota
            player.sayText("Tancat!", 500)
            scene.cameraShake(2, 200)
            // Rebote del jugador
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
            game.showLongText(`Has trobat l'ARMA DE PLASMA!
Ara prem A per disparar.`, DialogLayout.Bottom)
            tiles.setTileAt(location, assets.tile`open_chest`)
        }
        
    } else if (tiles.tileAtLocationEquals(location, assets.tile`spawn_npc_base_floor`)) {
        music.magicWand.play(100)
        game.showLongText("LORE", DialogLayout.Bottom)
    }
    
})
//  Crida de la funció
scene.onOverlapTile(SpriteKind.Player, assets.tile`lore_point_base_floor`, function on_player_step_on_lore(player: Sprite, location: tiles.Location) {
    /** Gestiona els missatges de lore en trepitjar punts concrets */
    music.magicWand.play(100)
    game.showLongText("LORE", DialogLayout.Bottom)
    let all_lore_locations = tiles.getTilesByType(assets.tile`lore_point_base_floor`)
    for (let loc of all_lore_locations) {
        tiles.setTileAt(loc, assets.tile`base_floor`)
    }
})
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
}

//  EXECUCIÓ
//  Funció per a iniciar el joc
function start_game() {
    setup_player()
    load_level(current_level_num)
}

start_game()
