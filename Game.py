"""
LOA
"""
import arcade
from piece import Piece
from tile import Tile
from board import Board
from ai_handler import AI_Handler
import json
import subprocess
import string

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "LOA"

TILE_WIDTH = 80

BLACK = 1
WHITE = -1
NONE = 0


SELECTED = True

SELECT_SIZE = 0
SELECT_TYPE = 1
GAME_STARTED = 2

HUMAN_V_HUMAN = 0
HUMAN_V_AI = 1


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        # TILES
        self.tile_list = None

        self.board = None

        self.turn = None
        self.state = None
        self.winner = None

        self.select_size = None
        self.display_state = None
        self.game_type = None

        self.ai_process = None
        self.error_message = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.select_size = arcade.SpriteList()
        self.display_state = SELECT_TYPE
        size6 = arcade.SpriteSolidColor( (int)(2 * SCREEN_WIDTH / 3), (int)(0.2 * SCREEN_HEIGHT), arcade.color.ALLOY_ORANGE)
        size8 = arcade.SpriteSolidColor( int(2 * SCREEN_WIDTH / 3), (int)(0.2 * SCREEN_HEIGHT), arcade.color.ALLOY_ORANGE)
        size6.set_position(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.75)
        size8.set_position(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.25)
        self.select_size.append(size6)
        self.select_size.append(size8)
        self.error_message = ""

        
    
    def start_game(self, size):
        self.tile_list: arcade.SpriteList = arcade.SpriteList()
        self.board = Board(size)
        self.winner = NONE
        self.display_state = GAME_STARTED

        self.state = not SELECTED

        for i in range(size):
            for j in range(size):
                color = arcade.color.CERULEAN
                if (i+j)%2 == 1:
                    color = arcade.color.CERULEAN_BLUE
                tile = Tile(color, i, j, size)
                self.tile_list.append(tile)        

        
        self.turn = BLACK

        if self.game_type == HUMAN_V_AI:
            msg = str(size) + "\n"
            self.ai_process = AI_Handler(msg)

        

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        arcade.start_render()

        if self.display_state == GAME_STARTED:
            self.tile_list.draw()
            for i in range(self.board.size):
                arcade.draw_text(string.ascii_uppercase[i], self.tile_list[0].START_X + i * TILE_WIDTH, self.tile_list[0].START_Y - TILE_WIDTH, arcade.color.WHITE, 20)
            for i in range(self.board.size):
                arcade.draw_text(str(i), self.tile_list[0].START_X - TILE_WIDTH, self.tile_list[0].START_Y + i * TILE_WIDTH, arcade.color.WHITE, 20)
            self.board.draw()

            if (self.winner == WHITE):
                arcade.draw_text("WHITE WINS", SCREEN_WIDTH/3, SCREEN_HEIGHT - 75, arcade.color.WHITE, 50)
            elif self.winner == BLACK:
                arcade.draw_text("BLACK WINS", SCREEN_WIDTH/3, SCREEN_HEIGHT - 75, arcade.color.WHITE, 50)
            elif (self.turn == WHITE):
                arcade.draw_text("WHITE'S TURN", SCREEN_WIDTH / 3, SCREEN_HEIGHT - 75, arcade.color.WHITE, 50)
            else:
                arcade.draw_text("BLACK'S TURN", SCREEN_WIDTH / 3, SCREEN_HEIGHT - 75, arcade.color.WHITE, 50)

        elif self.display_state == SELECT_SIZE:
            self.select_size.draw()
            arcade.draw_text("6x6", SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT * 0.75 - 25, arcade.color.WHITE, 50)
            arcade.draw_text("8x8", SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT * 0.25 - 25, arcade.color.WHITE, 50)
        elif self.display_state == SELECT_TYPE:
            self.select_size.draw()
            arcade.draw_text("HUMAN vs. HUMAN", SCREEN_WIDTH / 4, SCREEN_HEIGHT * 0.75 - 25, arcade.color.WHITE, 50)
            arcade.draw_text("HUMAN vs. AI", SCREEN_WIDTH / 3, SCREEN_HEIGHT * 0.25 - 25, arcade.color.WHITE, 50)
        
        arcade.draw_text(self.error_message, SCREEN_WIDTH / 2 - 50, 25, arcade.color.RED, 50)
        






    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        if self.display_state == GAME_STARTED:

            pieces = arcade.get_sprites_at_point((x,y), self.board.pieces)
            if len(pieces) > 0 and pieces[0].type == self.turn:
                #draws lines
                self.board.get_valid_moves(pieces[0])
                self.state = SELECTED
                return
                
            if self.state == SELECTED:
                #piece selected by user
                tiles = arcade.get_sprites_at_point((x,y), self.tile_list)
                if len(tiles) > 0:
                    #returns a boolean
                    init_x = self.board.selected_piece.pos_x
                    init_y = self.board.selected_piece.pos_y
                    valid_move = self.board.move_piece(init_x, init_y, tiles[0].pos_x, tiles[0].pos_y, self.turn)
                    if valid_move:
                        self.state = not SELECTED
                        self.winner = self.board.check_end_state(self.turn)
                        self.turn *= -1

                        #disable controls
                        if self.winner != NONE:
                            self.turn = NONE
                        elif self.game_type == HUMAN_V_AI and self.turn == WHITE:
                            self.handle_ai_move(init_x, init_y, tiles[0].pos_x, tiles[0].pos_y, self.turn)
                    else:
                        self.error_message = "INVALID MOVE"
                    
                return
        elif self.display_state == SELECT_SIZE:
            click = arcade.get_sprites_at_point((x,y), self.select_size)
            if len(click) > 0:
                if click[0].center_y == SCREEN_HEIGHT * 0.75:
                    self.start_game(6)
                else:
                    self.start_game(8)
        elif self.display_state == SELECT_TYPE:
            click = arcade.get_sprites_at_point((x,y), self.select_size)
            if len(click) > 0:
                if click[0].center_y == SCREEN_HEIGHT * 0.75:
                    self.game_type = HUMAN_V_HUMAN
                else:
                    self.game_type = HUMAN_V_AI
                self.display_state = SELECT_SIZE



    def handle_ai_move(self, x1, y1, x2, y2, turn):
        msg = str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2) + "\n"
        print("SENT MOVE", msg)
        self.ai_process.write(msg)
        moves = self.ai_process.read()
        print("Received move: ", moves)

        move_list = moves.split(",")
        valid_move = self.board.move_piece(int(move_list[0]), int(move_list[1]), int(move_list[2]), int(move_list[3]), turn)

        if valid_move:
            self.state = not SELECTED
            self.winner = self.board.check_end_state(self.turn)
            self.turn *= -1
            self.error_message = ""

            #disable controls
            if self.winner != NONE:
                self.turn = NONE

        else:
            self.error_message = "INVALID MOVE BY AI"
        



def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()