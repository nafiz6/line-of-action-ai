import java.util.List;


public class Minimax {

    static int INF = Integer.MAX_VALUE;
    static int NEG_INF = Integer.MIN_VALUE;
    static int maxDepth = 6;
    static int bestScore = NEG_INF;

    public static int[] bestMove = new int[4];

    public static int minimaxWithPruning(Board board, int depth, int alpha, int beta, boolean maximizingPlayer) {
        int checkWinner = board.checkEndState();
        if (checkWinner == AI_Handler.color)return INF;
        if (checkWinner == AI_Handler.color * -1) return NEG_INF;

        if (depth == 0){
            
            int pieceSquare = Evaluate.pieceSquareTableEvaluation(board, AI_Handler.color);
            int connectedness = Evaluate.connectednessEvaluation(board, AI_Handler.color);
            int area = Evaluate.area(board, AI_Handler.color);
            int quadCount = Evaluate.quadCount(board, AI_Handler.color);
            int density = Evaluate.density(board, AI_Handler.color);
            int pieceDifference = Evaluate.pieceDifference(board, AI_Handler.color);

            int opponentConnectedness = Evaluate.connectednessEvaluation(board,-1* AI_Handler.color);
            int opponentArea = Evaluate.area(board, AI_Handler.color * -1);
            int opponentQuadCount = Evaluate.quadCount(board, AI_Handler.color * -1);
        

            
            
            return pieceSquare * 4
             + 7 * connectedness
             - 17 * area
             + quadCount * 6
             - density * 12
             - 5 * opponentConnectedness
             + 17 * opponentArea
             - opponentQuadCount * 6;

            
        }


        if (maximizingPlayer){
            //AI PLAYER
            int maxPossible = NEG_INF;

            //GENERATE NEXT DEPTH
            for (int i=0; i<Board.boardSize; i++){
                for (int j=0; j<Board.boardSize; j++){
                    if (board.getPiece(i, j) == AI_Handler.color){
                        List<int[] > validMoves = board.getValidMoves(i, j);

                        for (int[] move: validMoves){
                            //store piece for reverting later
                            if (isTimeOver())return maxPossible;
                            int pieceAtTarget = board.getPiece(move[0], move[1]);
                            board.movePiece(i, j, move[0], move[1]);

                            int score = minimaxWithPruning(board, depth - 1, alpha, beta, false);

                            // undo last move
                            board.movePiece(move[0], move[1], i, j);
                            board.boardState[move[0]][move[1]] = pieceAtTarget;

                            maxPossible = Math.max(maxPossible, score);
                            alpha = Math.max(alpha, score);

                            //store best move
                            if (depth == maxDepth){
                                bestScore = Math.max(bestScore, maxPossible);
                                if (score == bestScore){
                                    bestMove[0] = i;
                                    bestMove[1] = j;
                                    bestMove[2] = move[0];
                                    bestMove[3] = move[1];
                                }
                            }


                            if (beta <= alpha){
                                return maxPossible;
                            }

                        }

                    }
                }
            }
            return maxPossible;
        }
        else{
            //OPPONENT
            int minPossible = INF;

            //GENERATE NEXT DEPTH
            for (int i=0; i<Board.boardSize; i++){
                for (int j=0; j<Board.boardSize; j++){
                    if (board.getPiece(i, j) == AI_Handler.color * -1){
                        List<int[] > validMoves = board.getValidMoves(i, j);

                        for (int[] move: validMoves){
                            if (isTimeOver())return minPossible;
                            int pieceAtTarget = board.getPiece(move[0], move[1]);
                            board.movePiece(i, j, move[0], move[1]);

                            int score = minimaxWithPruning(board, depth - 1, alpha, beta, true);


                            //undo last move
                            board.movePiece(move[0], move[1], i, j);
                            board.boardState[move[0]][move[1]] = pieceAtTarget;
                            minPossible = Math.min(minPossible, score);
                            beta = Math.min(beta, score);
                            if (beta <= alpha){
                                return minPossible;
                            }

                        }

                    }
                }
            }
            return minPossible;

        }

    }

    static boolean isTimeOver(){
        long diff = System.currentTimeMillis() - AI_Handler.time;
        if (Board.boardSize == 8){
            if (diff >= 1900)return true;
            return false;
        }
        else{
            if (diff >= 900) return true;
            return false;

        }

    }
    
}
