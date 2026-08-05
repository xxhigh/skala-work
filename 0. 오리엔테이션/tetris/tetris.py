import random
import sys
from array import array
from math import pi, sin

try:
    import pygame
except ModuleNotFoundError as error:
    if error.name != "pygame":
        raise
    print(
        "pygame 모듈을 찾을 수 없습니다.\n"
        "아래 명령으로 프로젝트 가상환경을 활성화한 뒤 다시 실행하세요.\n\n"
        "  source .venv/bin/activate\n"
        "  python tetris/tetris.py\n\n"
        "또는 가상환경 Python을 직접 실행하세요.\n\n"
        "  .venv/bin/python tetris/tetris.py",
        file=sys.stderr,
    )
    sys.exit(1)


CELL_SIZE = 30
COLUMNS = 10
ROWS = 20
SIDEBAR_WIDTH = 180
WINDOW_WIDTH = COLUMNS * CELL_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = ROWS * CELL_SIZE
FPS = 60
SAMPLE_RATE = 22050
BGM_VOLUME = 0.18

BOARD_BG = (18, 20, 26)
GRID_COLOR = (35, 39, 49)
TEXT_COLOR = (232, 236, 243)
MUTED_TEXT = (151, 160, 175)
LOCKED_BORDER = (10, 12, 16)

SHAPES = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "T": [[0, 1, 0], [1, 1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "Z": [[1, 1, 0], [0, 1, 1]],
    "J": [[1, 0, 0], [1, 1, 1]],
    "L": [[0, 0, 1], [1, 1, 1]],
}

COLORS = {
    "I": (52, 211, 235),
    "O": (250, 204, 21),
    "T": (168, 85, 247),
    "S": (34, 197, 94),
    "Z": (239, 68, 68),
    "J": (59, 130, 246),
    "L": (249, 115, 22),
}

BGM_MELODY = [
    ("E5", 0.25),
    ("B4", 0.125),
    ("C5", 0.125),
    ("D5", 0.25),
    ("C5", 0.125),
    ("B4", 0.125),
    ("A4", 0.25),
    ("A4", 0.125),
    ("C5", 0.125),
    ("E5", 0.25),
    ("D5", 0.125),
    ("C5", 0.125),
    ("B4", 0.375),
    ("C5", 0.125),
    ("D5", 0.25),
    ("E5", 0.25),
    ("C5", 0.25),
    ("A4", 0.25),
    ("A4", 0.25),
    ("REST", 0.25),
]

NOTE_FREQUENCIES = {
    "A4": 440.00,
    "B4": 493.88,
    "C5": 523.25,
    "D5": 587.33,
    "E5": 659.25,
}


class Piece:
    def __init__(self, shape_name):
        self.shape_name = shape_name
        self.matrix = [row[:] for row in SHAPES[shape_name]]
        self.color = COLORS[shape_name]
        self.x = COLUMNS // 2 - len(self.matrix[0]) // 2
        self.y = 0

    def rotated(self):
        return [list(row) for row in zip(*self.matrix[::-1])]


class BgmPlayer:
    def __init__(self):
        self.enabled = False
        self.playing = False
        self.sound = None

        try:
            pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1)
            self.sound = pygame.mixer.Sound(buffer=create_bgm_buffer())
            self.sound.set_volume(BGM_VOLUME)
            self.enabled = True
        except pygame.error as error:
            print(f"배경 음악을 초기화할 수 없습니다: {error}", file=sys.stderr)

    def play(self):
        if self.enabled and not self.playing:
            self.sound.play(loops=-1)
            self.playing = True

    def stop(self):
        if self.enabled and self.playing:
            self.sound.stop()
            self.playing = False


def create_bgm_buffer():
    samples = array("h")

    for note, beat in BGM_MELODY:
        duration = beat * 60 / 132
        sample_count = int(SAMPLE_RATE * duration)

        for index in range(sample_count):
            if note == "REST":
                sample = 0
            else:
                frequency = NOTE_FREQUENCIES[note]
                time = index / SAMPLE_RATE
                envelope = min(1.0, index / 120) * min(1.0, (sample_count - index) / 400)
                wave = sin(2 * pi * frequency * time)
                harmonic = 0.35 * sin(2 * pi * frequency * 2 * time)
                sample = int((wave + harmonic) * envelope * 9000)
            samples.append(sample)

    return samples.tobytes()


def create_board():
    return [[None for _ in range(COLUMNS)] for _ in range(ROWS)]


def create_piece():
    return Piece(random.choice(list(SHAPES)))


def is_valid_position(board, piece, matrix=None, offset_x=0, offset_y=0):
    matrix = matrix or piece.matrix

    for row_index, row in enumerate(matrix):
        for col_index, cell in enumerate(row):
            if not cell:
                continue

            x = piece.x + col_index + offset_x
            y = piece.y + row_index + offset_y

            if x < 0 or x >= COLUMNS or y >= ROWS:
                return False
            if y >= 0 and board[y][x]:
                return False

    return True


def lock_piece(board, piece):
    for row_index, row in enumerate(piece.matrix):
        for col_index, cell in enumerate(row):
            if cell:
                x = piece.x + col_index
                y = piece.y + row_index
                if 0 <= y < ROWS:
                    board[y][x] = piece.color


def clear_lines(board):
    remaining_rows = [row for row in board if any(cell is None for cell in row)]
    cleared = ROWS - len(remaining_rows)
    new_rows = [[None for _ in range(COLUMNS)] for _ in range(cleared)]
    board[:] = new_rows + remaining_rows
    return cleared


def draw_cell(screen, x, y, color):
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect.inflate(-2, -2), border_radius=4)
    pygame.draw.rect(screen, LOCKED_BORDER, rect.inflate(-2, -2), 1, border_radius=4)


def draw_board(screen, board):
    board_rect = pygame.Rect(0, 0, COLUMNS * CELL_SIZE, WINDOW_HEIGHT)
    pygame.draw.rect(screen, BOARD_BG, board_rect)

    for x in range(COLUMNS + 1):
        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x * CELL_SIZE, 0),
            (x * CELL_SIZE, WINDOW_HEIGHT),
        )
    for y in range(ROWS + 1):
        pygame.draw.line(
            screen,
            GRID_COLOR,
            (0, y * CELL_SIZE),
            (COLUMNS * CELL_SIZE, y * CELL_SIZE),
        )

    for y, row in enumerate(board):
        for x, color in enumerate(row):
            if color:
                draw_cell(screen, x, y, color)


def draw_piece(screen, piece):
    for row_index, row in enumerate(piece.matrix):
        for col_index, cell in enumerate(row):
            if cell:
                draw_cell(screen, piece.x + col_index, piece.y + row_index, piece.color)


def draw_preview(screen, small_font, next_piece):
    panel = pygame.Rect(8, 8, 122, 102)
    preview_cell = 20
    panel_surface = pygame.Surface(panel.size, pygame.SRCALPHA)
    panel_surface.fill((27, 31, 39, 220))
    screen.blit(panel_surface, panel.topleft)
    pygame.draw.rect(screen, GRID_COLOR, panel, 1, border_radius=6)

    title = small_font.render("Next", True, TEXT_COLOR)
    screen.blit(title, (panel.x + 10, panel.y + 8))

    matrix = next_piece.matrix
    shape_width = len(matrix[0]) * preview_cell
    shape_height = len(matrix) * preview_cell
    start_x = panel.x + (panel.width - shape_width) // 2
    start_y = panel.y + 46 + (42 - shape_height) // 2

    for row_index, row in enumerate(matrix):
        for col_index, cell in enumerate(row):
            if not cell:
                continue
            rect = pygame.Rect(
                start_x + col_index * preview_cell,
                start_y + row_index * preview_cell,
                preview_cell,
                preview_cell,
            )
            pygame.draw.rect(
                screen,
                next_piece.color,
                rect.inflate(-2, -2),
                border_radius=3,
            )
            pygame.draw.rect(
                screen,
                LOCKED_BORDER,
                rect.inflate(-2, -2),
                1,
                border_radius=3,
            )


def draw_sidebar(screen, font, small_font, score, lines, level, game_over):
    sidebar_x = COLUMNS * CELL_SIZE
    sidebar = pygame.Rect(sidebar_x, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, (27, 31, 39), sidebar)

    title = font.render("TETRIS", True, TEXT_COLOR)
    screen.blit(title, (sidebar_x + 28, 34))

    entries = [("Score", score), ("Lines", lines), ("Level", level)]
    for index, (label, value) in enumerate(entries):
        y = 105 + index * 62
        screen.blit(small_font.render(label, True, MUTED_TEXT), (sidebar_x + 24, y))
        screen.blit(font.render(str(value), True, TEXT_COLOR), (sidebar_x + 24, y + 22))

    controls = [
        "Left/Right: Move",
        "Up: Rotate",
        "Down: Soft drop",
        "Space: Hard drop",
        "R: Restart",
        "Esc: Quit",
    ]
    for index, text in enumerate(controls):
        screen.blit(
            small_font.render(text, True, MUTED_TEXT),
            (sidebar_x + 20, 330 + index * 24),
        )

    if game_over:
        overlay = pygame.Surface((COLUMNS * CELL_SIZE, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        screen.blit(overlay, (0, 0))

        message = font.render("GAME OVER", True, TEXT_COLOR)
        prompt = small_font.render("Press R to restart", True, TEXT_COLOR)
        screen.blit(message, message.get_rect(center=(COLUMNS * CELL_SIZE // 2, 270)))
        screen.blit(prompt, prompt.get_rect(center=(COLUMNS * CELL_SIZE // 2, 310)))


def score_for_lines(cleared, level):
    points = {1: 100, 2: 300, 3: 500, 4: 800}
    return points.get(cleared, 0) * level


def restart_game():
    board = create_board()
    piece = create_piece()
    next_piece = create_piece()
    return board, piece, next_piece, 0, 0, 1, False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 30, bold=True)
    small_font = pygame.font.SysFont("arial", 16)

    board, current_piece, next_piece, score, lines, level, game_over = restart_game()
    fall_time = 0
    fall_speed = 650
    bgm = BgmPlayer()
    bgm.play()

    while True:
        delta_time = clock.tick(FPS)
        fall_time += delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bgm.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    bgm.stop()
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    (
                        board,
                        current_piece,
                        next_piece,
                        score,
                        lines,
                        level,
                        game_over,
                    ) = restart_game()
                    fall_time = 0
                    fall_speed = 650
                    bgm.play()
                    continue
                if game_over:
                    continue

                if event.key == pygame.K_LEFT and is_valid_position(
                    board, current_piece, offset_x=-1
                ):
                    current_piece.x -= 1
                elif event.key == pygame.K_RIGHT and is_valid_position(
                    board, current_piece, offset_x=1
                ):
                    current_piece.x += 1
                elif event.key == pygame.K_DOWN and is_valid_position(
                    board, current_piece, offset_y=1
                ):
                    current_piece.y += 1
                    score += 1
                elif event.key == pygame.K_UP:
                    rotated = current_piece.rotated()
                    if is_valid_position(board, current_piece, matrix=rotated):
                        current_piece.matrix = rotated
                elif event.key == pygame.K_SPACE:
                    while is_valid_position(board, current_piece, offset_y=1):
                        current_piece.y += 1
                        score += 2
                    fall_time = fall_speed

        if not game_over and fall_time >= fall_speed:
            fall_time = 0
            if is_valid_position(board, current_piece, offset_y=1):
                current_piece.y += 1
            else:
                lock_piece(board, current_piece)
                cleared = clear_lines(board)
                if cleared:
                    lines += cleared
                    level = lines // 10 + 1
                    score += score_for_lines(cleared, level)
                    fall_speed = max(120, 650 - (level - 1) * 55)

                current_piece = next_piece
                next_piece = create_piece()
                if not is_valid_position(board, current_piece):
                    game_over = True
                    bgm.stop()

        screen.fill((12, 14, 18))
        draw_board(screen, board)
        if not game_over:
            draw_piece(screen, current_piece)
        draw_preview(screen, small_font, next_piece)
        draw_sidebar(screen, font, small_font, score, lines, level, game_over)
        pygame.display.flip()


if __name__ == "__main__":
    main()
