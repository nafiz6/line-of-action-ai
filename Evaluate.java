public class Evaluate {
    

    //sum of positional scores
    public static int pieceSquareTableEvaluation(Board board, int color){
        int[][] pieceSquareTable8 = {
            {-100, -80, -80, -80, -80, -80, -80, -100},
            {-80,  5,  10,  10,  10,  10,  5,  -80},
            {-80,  10,  25,  25,  25,  25,  10,  -80},
            {-80,  10,  25,  50,  50,  25,  10,  -80},
            {-80,  10,  25,  50,  50,  25,  10,  -80},
            {-80,  10,  25,  25,  25,  25,  10,  -80},
            {-80,  5,  10,  10,  10,  10,  5,  -80},
            {-100, -80, -80, -80, -80, -80, -80, -100}
        };

        int[][] pieceSquareTable6 = {
            
            {  -100,  -80,  -80,  -80,  -80,  -100},
            {  -80,  10,  25,  25,  10,  -80},
            {  -80,  25,  50,  50,  25,  -80},
            {  -80,  25,  50,  50,  25,  -80},
            {  -80,  10,  25,  25,  10,  -80},
            {  -100,  -80,  -80,  -80,  -80,  -100},
        };

        int[][] tableToUse = pieceSquareTable8;
        if (Board.boardSize == 6)tableToUse = pieceSquareTable6;

        int score = 0;
        for (int i=0; i<Board.boardSize; i++){
            for (int j=0;j<Board.boardSize; j++){
                if (board.getPiece(i, j) == color){
                    score += tableToUse[i][j];
                }

            }
        }
        return score;

    }


    // returns sum of connections for all pieces
    public static int connectednessEvaluation(Board board, int color){
        int score = 0;
        for (int i=0; i<Board.boardSize; i++){
            for (int j=0; j<Board.boardSize; j++){
                if (board.getPiece(i, j) == color){
                    //check 8 position
                    int[] dir = {-1, 0, 1};
                    for (int x: dir){
                        for (int y: dir){
                            if (x==0 && y==0)continue;
                            // increment if there is a connected piece
                            if (board.getPiece(i + x, j + y) == color)
                                score++;
                        }
                    }

                }
            }

        }
        return score;

    }

    //calculates (area taken by pieces) less is better 
    public static int area(Board board, int color){
        int minX=Board.boardSize-1, minY = Board.boardSize - 1, maxX = 0, maxY = 0;
        for (int i=0;i<Board.boardSize; i++){
            for (int j=0; j<Board.boardSize; j++){
                if (board.boardState[i][j] == color){
                    minX = Math.min(minX, i);
                    minY = Math.min(minY, j);
                    maxX = Math.max(maxX, i);
                    maxY = Math.max(maxY, j);
                }
            }
        }
        int areaOfPieces = Math.abs(maxX - minX + 1) * Math.abs(maxY - minY + 1);

        return areaOfPieces;
    }

    public static int possibleMovesCount(Board board, int color){
        int count = 0;
        for (int i=0;i<Board.boardSize; i++){
            for (int j=0; j<Board.boardSize; j++){
                if (board.getPiece(i, j) == color){
                    //get valid moves returns a list and we increment the size of that list
                    count += board.getValidMoves(i, j).size();
                }
            }
        
        }
        return count;
    }

    //q3 + q4
    public static int quadCount(Board board, int color){
        int q3 =0, q4 = 0;
        int[] center = centerOfMass(board, color);
        int centerX = center[0];
        int centerY = center[1];
        for (int i=centerX-2; i<=centerX + 2; i++){
            for (int j=centerY - 2 ;j<=centerY + 2; j++){
                int pieceCount = 0;
                if (board.getPiece(i, j) == color)pieceCount++;
                if (board.getPiece(i + 1, j) == color)pieceCount++;
                if (board.getPiece(i, j + 1) == color)pieceCount++;
                if (board.getPiece(i + 1, j + 1) == color)pieceCount++;
                if (pieceCount == 3)q3++;
                if (pieceCount == 4)q4++;
            }
        }
        return q3 * 1 + q4 * 2;
    }


    //density returns the sum of distance from center of mass
    public static int density(Board board, int color){
        int center[] = centerOfMass(board, color);
        int centerX = center[0];
        int centerY = center[1];
        int dist = 0;
        for (int i=0; i<Board.boardSize; i++){
            for (int j=0; j<Board.boardSize; j++){
                if (board.getPiece(i, j) == color){
                    dist += Math.abs(centerX - i);
                    dist += Math.abs(centerY - j);
                }
            }
        }
        return dist;

        
    }

    public static int[] centerOfMass(Board board, int color){
        int xSum =0, ySum = 0;
        for (int i=0; i<Board.boardSize; i++){
            for (int j=0; j<Board.boardSize; j++){
                if (board.getPiece(i, j) == color){
                    xSum+=i;
                    ySum+=j;
                }
            }
        }
        int centerX = xSum/Board.boardSize;
        int centerY = ySum/Board.boardSize;
        int[] center = {centerX, centerY};
        return center;
        
    }

    public static int pieceDifference(Board board, int color){
        int playerCount = 0;
        int opponentCount = 0;
        for (int i=0;i<Board.boardSize; i++){
            for (int j=0;j<Board.boardSize;j++){
                if (board.getPiece(i, j) == color) playerCount++;
                else if (board.getPiece(i, j) == color*-1) opponentCount++;
            }
        }
        return opponentCount - playerCount;
    }

}
