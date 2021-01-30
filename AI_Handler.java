import java.util.*;



public class AI_Handler {

    public static int color;
    public static long time;

    public static void main(String[] args){
        //AI COLOR
        color = Board.WHITE;

        Scanner sc = new Scanner(System.in);

        String sizeStr = sc.nextLine();

        int size = Integer.parseInt(sizeStr);
        System.out.println("RECEIVED");
        if (size == 8)Minimax.maxDepth = 5;

        Board board = new Board(size);

        while (true){
            if (board.checkEndState() != Board.NONE)break;
            String opponentMove = sc.nextLine();
            time = System.currentTimeMillis();

            String[] opponentMoves = opponentMove.split(",");
            board.movePiece(Integer.parseInt(opponentMoves[0]), Integer.parseInt(opponentMoves[1]), Integer.parseInt(opponentMoves[2]), Integer.parseInt(opponentMoves[3]));

            Minimax.bestScore = Minimax.NEG_INF;
            Minimax.minimaxWithPruning(board, Minimax.maxDepth, Minimax.NEG_INF, Minimax.INF, true);


            //perform move
            board.movePiece(Minimax.bestMove[0], Minimax.bestMove[1], Minimax.bestMove[2], Minimax.bestMove[3]);

            //return to UI
            System.out.println(Minimax.bestMove[0] + "," +  Minimax.bestMove[1] + "," + Minimax.bestMove[2] + "," + Minimax.bestMove[3]);
            System.out.flush();
            
        }

    }
}
