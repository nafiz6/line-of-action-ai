
import arcade

BLACK = 1
WHITE = -1

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

TILE_WIDTH = 80
START_X = (SCREEN_WIDTH - TILE_WIDTH * 7) / 2
START_Y = (SCREEN_HEIGHT - TILE_WIDTH * 7 ) / 2

class Piece(arcade.SpriteCircle):

    def __init__(self, type, position_x, position_y, size):
        self.type = type

        global START_X
        global START_Y
        START_X = (SCREEN_WIDTH - TILE_WIDTH * (size-1)) / 2
        START_Y = (SCREEN_HEIGHT - TILE_WIDTH * (size-1) ) / 2
        
        if type == BLACK: 
            super().__init__(30, "BLACK")
        else:
            super().__init__(30, "WHITE")
        self.move(position_x, position_y)
    
    def move(self, position_x, position_y):
        self.pos_x = position_x
        self.pos_y = position_y
        super().set_position( START_X + TILE_WIDTH * position_x, START_Y + TILE_WIDTH * position_y)



