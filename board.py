
import arcade
from piece import Piece

BLACK = 1
WHITE = -1
NONE = 0

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

TILE_WIDTH = 80
START_X = (SCREEN_WIDTH - TILE_WIDTH * 7) / 2
START_Y = (SCREEN_HEIGHT - TILE_WIDTH * 7 ) / 2

class Board():

    def __init__(self, size):
        global START_X
        global START_Y
        self.pieces: arcade.SpriteList = arcade.SpriteList()
        self.valid_moves = []
        self.selected_piece = None
        self.board_state = []
        self.size = size
        START_X = (SCREEN_WIDTH - TILE_WIDTH * (size-1)) / 2
        START_Y = (SCREEN_HEIGHT - TILE_WIDTH * (size-1) ) / 2

        for i in range(size):
            row = []
            for j in range(size):
                row.append(NONE)
            self.board_state.append(row)

        for i in range(1, size - 1):
            #black pieces
            #bottom
            piece = Piece(BLACK, i, 0, size)
            self.append(piece)
            self.board_state[i][0] = BLACK

            #top
            piece = Piece(BLACK, i, size - 1, size)
            self.append(piece)
            self.board_state[i][size - 1] = BLACK

            #white piece
            #left
            piece = Piece(WHITE, 0, i, size)
            self.append(piece)
            self.board_state[0][i] = WHITE
            #right
            piece = Piece(WHITE, size - 1, i, size)
            self.append(piece)
            self.board_state[size - 1][i] = WHITE
    
    def draw(self):
        self.pieces.draw()
        for move in self.valid_moves:
            line = arcade.create_line(self.selected_piece.center_x, self.selected_piece.center_y, 
                            self.selected_piece.center_x + move[0] * TILE_WIDTH, self.selected_piece.center_y + move[1] * TILE_WIDTH,  arcade.color.RED) 
            line.draw()

    def append(self, piece):
        self.pieces.append(piece)
    
    def get_valid_moves(self, piece):

        #relative move from piece
        self.valid_moves = []
        self.selected_piece = piece

        vertical_count = 0
        horizontal_count = 0
        topLeft_bottomRight = 0
        topRight_bottomLeft = 0
        for p in self.pieces:
            if p.pos_x == piece.pos_x:
                vertical_count += 1
            if p.pos_y == piece.pos_y:
                horizontal_count += 1
            if p.pos_x + p.pos_y == piece.pos_x + piece.pos_y:
                topLeft_bottomRight += 1
            if p.pos_x - piece.pos_x == p.pos_y - piece.pos_y:
                topRight_bottomLeft += 1
        
        x = piece.pos_x
        y = piece.pos_y
        opponent_color = piece.type * -1
        #left
        #if inside and not same color
        if x - horizontal_count >= 0 and self.board_state[x - horizontal_count][y] != piece.type:
            #inside
            valid = True

            for i in range(1, horizontal_count ):
                if self.board_state[x-i][y] == opponent_color:
                    valid =  False
                    break
                
            if valid:
                move = [-horizontal_count, 0]
                self.valid_moves.append(move)
            

        #right
        if x + horizontal_count < self.size and self.board_state[x + horizontal_count][y] != piece.type:
            #inside
            valid = True

            for i in range(1, horizontal_count ):
                if self.board_state[x+i][y] == opponent_color:
                    valid =  False
                    break
                
            if valid:
                move = [horizontal_count, 0]
                self.valid_moves.append(move)
            
        #up
        if y + vertical_count < self.size and self.board_state[x][y + vertical_count] != piece.type:
            #inside
            valid = True

            for i in range(1, vertical_count ):
                if self.board_state[x][y + i] == opponent_color:
                    valid =  False
                    break
                
            if valid:
                move = [0, vertical_count]
                self.valid_moves.append(move)
                
        #down
        if y - vertical_count >= 0 and self.board_state[x][y - vertical_count] != piece.type:
            #inside
            valid = True

            for i in range(1, vertical_count ):
                if self.board_state[x][y - i] == opponent_color:
                    valid =  False
                    break
                
            if valid:
                move = [0, -vertical_count]
                self.valid_moves.append(move)
        
        #topleft
        if x - topLeft_bottomRight >= 0 and y + topLeft_bottomRight < self.size and self.board_state[x - topLeft_bottomRight][y + topLeft_bottomRight] != piece.type:
            #inside
            valid = True

            for i in range(1, topLeft_bottomRight ):
                if self.board_state[x - i][y + i] == opponent_color:
                    valid =  False
                    break
                
            if valid:
                move = [-topLeft_bottomRight, topLeft_bottomRight]
                self.valid_moves.append(move)
        
        #bottomRight
        if x + topLeft_bottomRight < self.size and y - topLeft_bottomRight >= 0 and self.board_state[x + topLeft_bottomRight][y - topLeft_bottomRight] != piece.type:
            #inside
            valid = True

            for i in range(1, topLeft_bottomRight ):
                if self.board_state[x + i][y - i] == opponent_color:
                    valid =  False
                    break
                
            if valid:
                move = [topLeft_bottomRight, -topLeft_bottomRight]
                self.valid_moves.append(move)
        
        #topRight
        if x + topRight_bottomLeft < self.size and y + topRight_bottomLeft < self.size and self.board_state[x + topRight_bottomLeft][y + topRight_bottomLeft] != piece.type:
            #inside
            valid = True

            for i in range(1, topRight_bottomLeft ):
                if self.board_state[x + i][y + i] == opponent_color:
                    valid =  False
                    break
                
            if valid:
                move = [topRight_bottomLeft, topRight_bottomLeft]
                self.valid_moves.append(move)
        
        
        #bottomLeft
        if x - topRight_bottomLeft >= 0 and y - topRight_bottomLeft >= 0 and self.board_state[x - topRight_bottomLeft][y - topRight_bottomLeft] != piece.type:
            #inside
            valid = True

            for i in range(1, topRight_bottomLeft ):
                if self.board_state[x - i][y - i] == opponent_color:
                    valid =  False
                    break
                
            if valid:
                move = [-topRight_bottomLeft, -topRight_bottomLeft]
                self.valid_moves.append(move)



    #(x1, y1) to (x2, y2)
    def move_piece(self, x1, y1, x2, y2, turn):
        #select piece
        found = False
        for p in self.pieces:
            if p.pos_x == x1 and p.pos_y == y1 and p.type == turn:
                #sets selected piece and valid_moves variable
                self.get_valid_moves(p)
                found = True

        if not found:
            return False

        #relative position      
        x = x2 - self.selected_piece.pos_x 
        y = y2 - self.selected_piece.pos_y

        #get_valid_moves has relative pos
        for move in self.valid_moves:
            if move[0] == x and move[1] == y:
                #valid move
                target_x = self.selected_piece.pos_x + x
                target_y = self.selected_piece.pos_y + y

                self.board_state[self.selected_piece.pos_x][self.selected_piece.pos_y] = NONE
                self.board_state[target_x][target_y] = self.selected_piece.type

                collide = arcade.get_sprites_at_point( (START_X + target_x * TILE_WIDTH, START_Y + target_y * TILE_WIDTH ) , self.pieces)
                if len(collide) > 0:
                    self.pieces.remove(collide[0])
                
                self.selected_piece.move(target_x, target_y)
                self.selected_piece = None
                self.valid_moves = []
                return True
        return False
    
    #returns BLACK WHITE OR NONE
    def check_end_state(self, last_color):
        black_count = self.connected_components(BLACK)
        white_count = self.connected_components(WHITE)
        if black_count == 1 and white_count == 1:
            return last_color
        if black_count == 1:
            return BLACK
        if white_count == 1:
            return WHITE
        return NONE
        
        

    def connected_components(self, type):
        vis = []
        count = 0
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(0)
            vis.append(row)
        
        for piece in self.pieces:
            if vis[piece.pos_x][piece.pos_y] == 1 or piece.type != type:
                continue
            count += 1
            q = []
            q.append([piece.pos_x, piece.pos_y])
            vis[piece.pos_x][piece.pos_y] = 1

            while len(q) > 0:
                current_piece = q.pop(0)
                dir = [-1, 0, 1]
                for i in dir:
                    for j in dir:
                        if i==0 and j==0:
                            continue
                        new_x = current_piece[0] + i
                        new_y = current_piece[1] + j
                        if new_x < 0 or new_x >= self.size or new_y < 0 or new_y >= self.size:
                            continue
                        if vis[new_x][new_y] == 0 and self.board_state[new_x][new_y] == type:
                            q.append([new_x, new_y])
                            vis[new_x][new_y] = 1
        return count

                            

                    
        
        
    


    


