class GameState:

    file_path = 'data/othello_save.txt'
    file = None

    @classmethod
    def load_board(cls):
        moves = []
        with open(cls.file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                moves.append([int(x) for x in line.replace('\n', '').split(' ')])
        return moves

    @classmethod
    def init(cls):
        cls.file = open(cls.file_path, 'w')

    @classmethod
    def add_move(cls, x, y):
        cls.file.write(f'{x} {y}\n')

    @classmethod
    def reset(cls):
        cls.file.close()
        with open(cls.file_path, 'w') as f:
            pass
