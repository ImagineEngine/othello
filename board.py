class Board:
    def __init__(self):
        #  0 -> empty
        #  1 -> white
        # -1 -> black
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1,-1, 0, 0, 0],
                      [0, 0, 0,-1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]

    #update text and sbtext + sbtext visibility

    def get(self, x, y):
        return self.board[x][y] if 0 <= x <= 7 and 0 <= y <= 7 else 0

    def set(self, x, y, col):
        self.board[x][y] = col