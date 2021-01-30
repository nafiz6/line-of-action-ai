import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class Board {
    int[][] boardState;

    static int BLACK = 1;
    static int WHITE = -1;
    static int NONE = 0;
    static int OUTSIDE = -2;

    static int boardSize;

    int lastColor = NONE;


    public Board(int size){
        boardSize = size;
                
        boardState = new int[boardSize][boardSize];
        for (int i=1;i<=boardSize - 2;i++){
            // 1 is black
            boardState[i][boardSize - 1] = BLACK;  // top
            boardState[i][0] = BLACK;  // bottom

            // -1 is white
            boardState[0][i] = WHITE; // left
            boardState[boardSize - 1][i] = WHITE; // right

        }
    }

    public List<int[]> getValidMoves(int x, int y){
        List<int[] > validMoves = new ArrayList<>();

        int pieceColor = getPiece(x, y);
        if (pieceColor == NONE || pieceColor == OUTSIDE)return validMoves;

        int opponentColor = pieceColor * -1;

        //moves count
        int horizontalCount = 0;
        int verticalCount = 0;
        int topLeftToBottomRight = 0;
        int topRightToBottomLeft = 0;
        for (int i=0; i<boardSize; i++){
            if (getPiece(x, i) != NONE) verticalCount++;
            if (getPiece(i, y) != NONE) horizontalCount++;
            if (getPiece(i, y + x - i) != NONE && getPiece(x, y + x-i) != OUTSIDE){
                topLeftToBottomRight++;
            }
            if (getPiece(i, y - x + i) != NONE && getPiece(x, y - (x-i)) != OUTSIDE){
                topRightToBottomLeft++;
            }
        }


        //going left
        //not same color or outside
        if (getPiece(x - horizontalCount, y) != OUTSIDE && getPiece(x - horizontalCount, y) != getPiece(x, y)){
            boolean valid = true;

            for (int i = 1; i < horizontalCount; i++) {
                if (getPiece(x - i, y) == opponentColor){
                    valid = false;
                    break;
                }
            }
            if (valid){
                int[] move = {x - horizontalCount, y};
                validMoves.add(move);
            }
        }
        
        //going right
        if (getPiece(x + horizontalCount, y) != OUTSIDE && getPiece(x + horizontalCount, y) != getPiece(x, y)){
            boolean valid = true;

            for (int i = 1; i < horizontalCount; i++) {
                if (getPiece(x + i, y) == opponentColor){
                    valid = false;
                    break;
                }
            }
            if (valid){
                int[] move = {x + horizontalCount, y};
                validMoves.add(move);
            }
        }

        //going up
        if (getPiece(x, y + verticalCount) != OUTSIDE && getPiece(x, y + verticalCount) != getPiece(x, y)){
            boolean valid = true;

            for (int i = 1; i < verticalCount; i++) {
                if (getPiece(x, y + i) == opponentColor){
                    valid = false;
                    break;
                }
            }
            if (valid){
                int[] move = {x, y + verticalCount};
                validMoves.add(move);
            }
        }

        //going down
        if (getPiece(x, y - verticalCount) != OUTSIDE && getPiece(x, y - verticalCount) != getPiece(x, y)){
            boolean valid = true;

            for (int i = 1; i < verticalCount; i++) {
                if (getPiece(x, y - i) == opponentColor){
                    valid = false;
                    break;
                }
            }
            if (valid){
                int[] move = {x, y - verticalCount};
                validMoves.add(move);
            }
        }


        //going topleft
        if (getPiece(x - topLeftToBottomRight, y + topLeftToBottomRight) != OUTSIDE 
                    && getPiece(x - topLeftToBottomRight, y + topLeftToBottomRight) != getPiece(x, y)){
            boolean valid = true;

            for (int i = 1; i < topLeftToBottomRight; i++) {
                if (getPiece(x - i, y + i) == opponentColor){
                    valid = false;
                    break;
                }
            }
            if (valid){
                int[] move = {x - topLeftToBottomRight, y + topLeftToBottomRight};
                validMoves.add(move);
            }
        }


        //going bottomright
        if (getPiece(x + topLeftToBottomRight, y - topLeftToBottomRight) != OUTSIDE 
                    && getPiece(x + topLeftToBottomRight, y - topLeftToBottomRight) != getPiece(x, y)){
            boolean valid = true;

            for (int i = 1; i < topLeftToBottomRight; i++) {
                if (getPiece(x + i, y - i) == opponentColor){
                    valid = false;
                    break;
                }
            }
            if (valid){
                int[] move = {x + topLeftToBottomRight, y - topLeftToBottomRight};
                validMoves.add(move);
            }
        }


        //going topRight
        if (getPiece(x + topRightToBottomLeft, y + topRightToBottomLeft) != OUTSIDE 
                    && getPiece(x + topRightToBottomLeft, y + topRightToBottomLeft) != getPiece(x, y)){
            boolean valid = true;

            for (int i = 1; i < topRightToBottomLeft; i++) {
                if (getPiece(x + i, y + i) == opponentColor){
                    valid = false;
                    break;
                }
            }
            if (valid){
                int[] move = {x + topRightToBottomLeft, y + topRightToBottomLeft};
                validMoves.add(move);
            }
        }

        //going bottomleft
        if (getPiece(x - topRightToBottomLeft, y - topRightToBottomLeft) != OUTSIDE 
                    && getPiece(x - topRightToBottomLeft, y - topRightToBottomLeft) != getPiece(x, y)){
            boolean valid = true;

            for (int i = 1; i < topRightToBottomLeft; i++) {
                if (getPiece(x - i, y - i) == opponentColor){
                    valid = false;
                    break;
                }
            }
            if (valid){
                int[] move = {x - topRightToBottomLeft, y - topRightToBottomLeft};
                validMoves.add(move);
            }
        }

        return validMoves;
    }

    public void movePiece(int x1, int y1, int x2, int y2){
        lastColor = boardState[x1][y1];
        boardState[x2][y2] = boardState[x1][y1];
        boardState[x1][y1] = NONE;

    }

    public int getPiece(int x, int y){
        if (x<0 || y<0 || x>=boardSize || y>=boardSize)return OUTSIDE;
        return boardState[x][y];
    }

    public int checkEndState(){
        int blackCount = connectedComponents(BLACK);
        int whiteCount = connectedComponents(WHITE);
        if (blackCount == 1 && whiteCount == 1)return lastColor;
        if (blackCount == 1) return BLACK;
        if (whiteCount == 1) return WHITE;
        return NONE;
        
    }

    public int connectedComponents(int color){
        int[][] vis = new int[boardSize][boardSize];
        
        int count = 0;

        for (int i=0;i<boardSize;i++){
            for (int j=0;j<boardSize;j++){
                //found unvisited piece
                if (boardState[i][j] == color && vis[i][j]==0){
                    count++;
                    vis[i][j] = 1;
                    Queue<int[] > q = new LinkedList<>();
                    int [] curr = {i, j};
                    q.add(curr);
                    //bfs
                    while (!q.isEmpty()){
                        int[] current = q.poll();
                        int[] dir = { -1, 0, 1 };
                        for (int x : dir) {
                            for (int y : dir) {
                                //ignore if self
                                if (x == y && x==0)
                                    continue;
                                //matching colored neighbor
                                if (getPiece(current[0] + x, current[1] + y) == color && vis[current[0] + x][current[1] + y] == 0) {
                                    int[] next = { current[0] + x, current[1] + y };
                                    q.add(next);
                                    vis[next[0]][next[1]] = 1;
                                }
                            }
                        }

                    }
                }
            }
        }
        return count;
    }
}
