import pygame, time

from file_manager import GameState
lmoves = GameState.load_board()

from game_logic import Game
from board import Board

# initializing the pygame classes
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# defining screen dimensions and initializing the window
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Othello')
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

# loading the nessesary fonts and assets

font = pygame.font.Font('fonts/Realwood Regular.otf', 60)
font_l = pygame.font.Font('fonts/Realwood Regular.otf', 100)

board = pygame.image.load('assets/othello.png')
black = pygame.image.load('assets/black.png')
white = pygame.image.load('assets/white.png')

# scaling the images to fit the window

scale = board.get_width()/SCREEN_WIDTH
blk = pygame.transform.scale(black, (black.get_width()/scale, black.get_height()/scale))
wht = pygame.transform.scale(white, (white.get_width()/scale, white.get_height()/scale))

board_img = pygame.transform.scale(board, [SCREEN_WIDTH, SCREEN_WIDTH * 1.5])

# defining some constants for UI

BOARD_STRT_X = 124
BOARD_DELTA_X = 57
BOARD_STRT_Y = 122
BOARD_DELTA_Y = 59
OFFSET_X = -1
OFFSET_Y = 6
p_rad = 22

# class UI handles the rendering of the game onto the window
class UI:

    pull = 1
    grow = 1
    hover_coords = [0, 0]

    hover_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    hover_surf.set_alpha(100)

    # finds the corresponding cell over which the mouse is pointing
    @classmethod
    def get_hover(cls, pos):
        if (pos[0] >= BOARD_STRT_X and pos[0] <= BOARD_STRT_X + 8 * BOARD_DELTA_X and pos[1] >= BOARD_STRT_Y and pos[1] <= BOARD_STRT_Y + 8 * BOARD_DELTA_Y):
            hover = [(pos[0]-BOARD_STRT_X)//BOARD_DELTA_X, (pos[1]-BOARD_STRT_Y)//BOARD_DELTA_Y]
        else:
            hover = None
        return hover

    # renders the current game frame and blits it onto the screen
    @classmethod
    def render(cls, screen, board, pos, moves, col, c1, c2):
        COL = [0, 0, 0] if col == -1 else [255, 255, 255]
        screen.blit(board_img, [0, -160])
        text = font.render(f'Black : {c1} White : {c2}', True, (20, 7, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 70))
        screen.blit(text, text_rect)

        UI.hover_surf.fill((255, 255, 255, 0))

        hover = UI.get_hover(pos)

        UI.hover_coords = pos

        if (hover in moves):
            UI.pull /= 2
            UI.hover_coords = [BOARD_STRT_X + BOARD_DELTA_X * (hover[0] + 0.5),
                            BOARD_STRT_Y + BOARD_DELTA_Y * (hover[1] + 0.5)]
            UI.grow = min(UI.grow * 2, 1)
        else:
            UI.pull = min(UI.pull * 10, 1)
            UI.grow = max(UI.grow / 2, 0.6)
            # change them back
            # use min() and max()

        # makes all the ring highlights for possible moves

        for move in moves:
            pygame.draw.circle(UI.hover_surf, COL,
                               [BOARD_STRT_X + BOARD_DELTA_X * (move[0] + 0.5),
                                BOARD_STRT_Y + BOARD_DELTA_Y * (move[1] + 0.5)],
                               p_rad, 2)

        pygame.draw.circle(UI.hover_surf, COL,
                           [(1-UI.pull) * UI.hover_coords[0] + UI.pull * pos[0], (1-UI.pull) * UI.hover_coords[1] + UI.pull * pos[1]],
                           UI.grow*p_rad)


        # renders all the discs onto the board

        for i in range(len(board)):
            for j in range(len(board[i])):
                if(board[i][j]==-1):
                    screen.blit(blk, [BOARD_STRT_X + BOARD_DELTA_X * i, OFFSET_Y + BOARD_STRT_Y + BOARD_DELTA_Y * j])
                if(board[i][j]==1):
                    screen.blit(wht, [BOARD_STRT_X + BOARD_DELTA_X * i, OFFSET_Y + BOARD_STRT_Y + BOARD_DELTA_Y * j])

        screen.blit(UI.hover_surf, (0, 0))


pygame.mouse.set_visible(False)

def endgame(col, done_game_surf):

    # endgame message
    mpos = pygame.mouse.get_pos()
    GameState.reset()
    st = time.time()
    while (True):
        if time.time() - st > 3:
            return done
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return done
            if event.type == pygame.MOUSEMOTION:
                mpos = pygame.mouse.get_pos()
        screen.blit(done_game_surf, (0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))

        msg = f'{'Black' if col == -1 else 'White'} wins!'
        if col == 0:
            msg = "Draw!"
        text = font_l.render(msg, True, (255, 255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 250))
        overlay.blit(text, text_rect)

        pygame.draw.circle(overlay, (255, 255, 255, 200), mpos, p_rad * 0.6, 0)
        screen.blit(overlay, (0, 0))

        pygame.display.update()


def game_screen():

    # main game

    board = Board()
    col = -1
    moves, c1, c2 = Game.state(board, col)
    mpos = [0, 0]

    # restores the moves from the last save
    for move in lmoves:
        Game.play_move(board, move, col)
        col *= -1
        moves, c1, c2 = Game.state(board, col)

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return done

            if event.type == pygame.MOUSEMOTION:
                mpos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if UI.get_hover(mpos) in moves:
                        Game.play_move(board, UI.get_hover(mpos), col)
                        col *= -1
                        moves, c1, c2 = Game.state(board, col)
                        if moves == []:
                            col *= -1
                            moves, c1, c2 = Game.state(board, col)
                            if moves == []:
                                done_game_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                                UI.render(done_game_surf, board.board, [-100, -100], moves, col, c1, c2)
                                if c1 == c2:
                                    return lambda : endgame(0, done_game_surf)
                                return lambda : endgame(-1 if c1 > c2 else 1, done_game_surf)

        UI.render(screen, board.board, mpos, moves, col, c1, c2)
        pygame.display.update()
        clock.tick(30)

def done():

    # terminating the game safely
    GameState.file.close()
    pygame.quit()
    quit()

game_state = game_screen
while True:
    game_state = game_state()
