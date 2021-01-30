

import arcade

BLACK = 1
WHITE = -1

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

TILE_WIDTH = 80

class Tile(arcade.SpriteSolidColor):

    def __init__(self, color, position_x, position_y, size):
        self.type = type
        self.pos_x = position_x
        self.pos_y = position_y

        self.START_X = (SCREEN_WIDTH - TILE_WIDTH * (size-1)) / 2
        self.START_Y = (SCREEN_HEIGHT - TILE_WIDTH * (size-1) ) / 2
        
        super().__init__(TILE_WIDTH, TILE_WIDTH, color)
        super().set_position( self.START_X + TILE_WIDTH * position_x, self.START_Y + TILE_WIDTH * position_y)
    


