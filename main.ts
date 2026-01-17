//  VARIABLES GLOBALS
let my_player : Sprite = null
//  FUNCIONS DE CONFIGURACIÓ
function config_player() {
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

//  CRIDA INICIAL
config_player()
