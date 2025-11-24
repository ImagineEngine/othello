from file_manager import GameState

class Game:

    #list of directions
    vs = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
    GameState.init()

    @classmethod
    def state(cls, board, color):
        moves = []
        c1 = 0
        c2 = 0
        for i in range(0, 8):
            for j in range(0, 8):
                if board.get(i, j)==color:
                    c1 += 1
                    for v in Game.vs:
                        if board.get(i + v[0], j + v[1]) != color * -1:
                            continue
                        d = 2
                        while True:
                            nxt_d = board.get(i + d * v[0], j + d * v[1])
                            if nxt_d == color * -1:
                                d += 1
                            else:
                                if nxt_d == 0:
                                    moves.append([i + d * v[0], j + d * v[1]])
                                #if it reaches the same color after its opposite colors, it ignores that as a possible move
                                break
                elif board.get(i, j)==color*-1:
                    c2 += 1

        final_moves = []
        for move in moves:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                if move not in final_moves:
                    final_moves.append(move)
        count = [c1, c2] if color == -1 else [c2, c1]
        return [final_moves] + count
        # remove all invalid moves ie outside the board


    @classmethod
    def play_move(cls, board, move, col):
        board.set(move[0], move[1], col)
        for v in Game.vs:
            d = 1
            flips = []
            while True:
                nxt_d = [move[0] + d * v[0], move[1] + d * v[1]]
                if board.get(nxt_d[0], nxt_d[1]) == col * -1:
                    flips.append(nxt_d)
                    d += 1
                else:
                    if board.get(nxt_d[0], nxt_d[1]) == col:
                        for flip in flips:
                            board.set(flip[0], flip[1], col)
                    break
        GameState.add_move(move[0], move[1])
