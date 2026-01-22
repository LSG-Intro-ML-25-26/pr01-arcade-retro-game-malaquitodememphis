//  VARIABLES GLOBALS
//  Sprites
let my_player : Sprite = null
let Boss = SpriteKind.create()
//  Creem categoria
let EnemyProjectile = SpriteKind.create()
let boss_sprite : Sprite = null
let boss_statusbar : StatusBarSprite = null
//  Variables
let inventory_list : string[] = []
let has_weapon = false
//  Variables d'estat de d'apuntament (dreta per defecte)
let facing_x = 1
let facing_y = 0
//  Constants
let projectile_speed = 200
let enemy_speed = 50
//  FUNCIÓ DE CONFIGURACIÓ
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
//  GENERACIÓ D'ENEMICS
function spawn_enemies(number_of_enemies: number) {
    let enemy: Sprite;
    /** Genera una llista d'enemics en posicions aleatòries */
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
        // Posició aleatòria dins de la pantalla
        //  Pendent d'actualitzar quan sapiguem tamany real total del mapa
        enemy.x = randint(10, 140)
        enemy.y = randint(10, 100)
        //  "IA" per perseguir al jugador
        enemy.follow(my_player, enemy_speed)
        pause(200)
    }
}

//  GESTIÓ DE COL·LISIONS (projectil-enemic//enemic-jugador)
//  Registrem l'esdeveniment
sprites.onOverlap(SpriteKind.Projectile, SpriteKind.Enemy, function on_projectile_hit_enemy(projectile: Sprite, enemy: Sprite) {
    /** Gestiona quan un projectil xoca contra un enemic */
    //  Destruïm el projectil
    projectile.destroy()
    //  Destruïm l'enemic (amb FX)
    enemy.destroy(effects.disintegrate, 500)
    //  Sumar punts ? (a veure si es desenvolupa en el futur)
    info.changeScoreBy(100)
})
//  Registrem l'esdeveniment
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function on_enemy_hit_player(player: Sprite, enemy: Sprite) {
    /** Gestiona quan un enemic xoca contra el jugador */
    //  Restem una vida
    info.changeLifeBy(-1)
    //  Destruïm l'enemic
    enemy.destroy(effects.fire, 500)
    //  Feedback visual (sacsejar càmera)
    scene.cameraShake(4, 500)
})
//  FUNCIONS DEL "FINAL BOSS"
function spawn_boss() {
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
    //  El col·loquem al centre
    boss_sprite.x = 80
    boss_sprite.y = 30
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
        }
        
    })
}

//  COL·LISIONS DEL "FINAL BOSS"
//  Registrem l'esdeveniment
sprites.onOverlap(SpriteKind.Projectile, Boss, function on_projectile_hit_boss(projectile: Sprite, boss_sprite: Sprite) {
    projectile.destroy()
    //  Si hi ha statusbar, li restem 1
    if (boss_statusbar) {
        boss_statusbar.value -= 1
    }
    
    //  FX
    boss_sprite.startEffect(effects.ashes, 200)
})
//  Registrem l'esdeveniment
sprites.onOverlap(SpriteKind.Player, Boss, function on_boss_hit_player(player: Sprite, boss: Sprite) {
    info.changeLifeBy(-1)
    scene.cameraShake(4, 500)
    //  Empenyem el jugador cap enrere
    player.y += 10
})
//  Registrem l'esdeveniment
statusbars.onZero(StatusBarKind.EnemyHealth, function on_boss_death(status: StatusBarSprite) {
    if (boss_sprite) {
        boss_sprite.destroy(effects.disintegrate, 1000)
        game.showLongText("SERVIDOR RESTAURAT! HAS GUANYAT!", DialogLayout.Bottom)
        game.over(true)
    }
    
})
//  Registrem l'esdeveniment
sprites.onOverlap(SpriteKind.Player, EnemyProjectile, function on_enemy_projectile_hit_player(player: Sprite, projectile: Sprite) {
    //  Restem vida al jugador
    info.changeLifeBy(-1)
    //  Destruïm el projectil
    projectile.destroy()
    //  Efecte visual
    scene.cameraShake(4, 200)
})
//  SISTEMA D'INVENTARI
function spawn_key() {
    /** Crea un objecte recol·lectable (Clau Mestre) */
    let key_sprite = sprites.create(img`
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
    `, SpriteKind.Food)
    //  Usem "food" per objectes recol·lectables
    key_sprite.x = 100
    key_sprite.y = 50
    //  FX
    key_sprite.startEffect(effects.halo, 2000)
}

//  Si tenim la clau, podríem invocar al Boss (o obrir la porta)
//  if "Master Key" in inventory_list:
//      game.show_long_text("Clau trobada! El Boss ha despertat...", DialogLayout.BOTTOM)
//      spawn_boss()
//  Registrem l'esdeveniment
sprites.onOverlap(SpriteKind.Player, SpriteKind.Food, function on_player_collect_key(player: Sprite, key_sprite: Sprite) {
    /** Gestió de l'inventari */
    
    //  Afegim l'element a la llista
    inventory_list.push("Master Key")
    //  Feedback visual
    key_sprite.destroy(effects.confetti, 500)
    music.baDing.play()
    //  Mostrem l'inventari per pantalla
    my_player.sayText("Tinc: " + ("" + inventory_list.length) + " ítems", 3000)
})
//  EXECUCIÓ
setup_player()
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
        
        //  Destruïm el projectil un cop surt de la pantalla
        projectile.setFlag(SpriteFlag.DestroyOnWall, true)
    } else if (my_player && !has_weapon) {
        music.thump.play()
    }
    
})
//  Generem 5 enemics per començar
//  spawn_enemies(5)
//  Generació del "final boss"
//  spawn_boss()
//  Generació de la clau
spawn_key()
