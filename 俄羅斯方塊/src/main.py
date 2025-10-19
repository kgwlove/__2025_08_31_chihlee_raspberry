import pygame
import random

# 遊戲設定
SCREEN_WIDTH = 450 # 增加寬度以顯示下一個方塊
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GAME_TITLE = "俄羅斯方塊"

GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

NEXT_TETROMINO_X_OFFSET = GRID_WIDTH - 5 # 調整位置以適應新的螢幕寬度

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# 方塊形狀定義 (每個形狀由4個方塊組成，座標為相對座標)
# I, J, L, O, S, T, Z
TETROMINOES = {
    'I': {'shape': [[1, 1, 1, 1]], 'color': CYAN},
    'J': {'shape': [[1, 0, 0], [1, 1, 1]], 'color': BLUE},
    'L': {'shape': [[0, 0, 1], [1, 1, 1]], 'color': ORANGE},
    'O': {'shape': [[1, 1], [1, 1]], 'color': YELLOW},
    'S': {'shape': [[0, 1, 1], [1, 1, 0]], 'color': GREEN},
    'T': {'shape': [[0, 1, 0], [1, 1, 1]], 'color': PURPLE},
    'Z': {'shape': [[1, 1, 0], [0, 1, 1]], 'color': RED},
}

def get_random_tetromino():
    shape_name = random.choice(list(TETROMINOES.keys()))
    tetromino = TETROMINOES[shape_name]
    return tetromino['shape'], tetromino['color']

def draw_block(screen, color, x, y):
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

class Tetromino:
    def __init__(self, shape, color, x=None, y=None):
        self.shape = shape
        self.color = color
        self.x = x if x is not None else GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = y if y is not None else 0

    def draw(self, screen):
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    draw_block(screen, self.color, self.x + col_idx, self.y + row_idx)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        # 轉置矩陣 (行變列，列變行)
        rotated_shape = [[self.shape[j][i] for j in range(len(self.shape))] for i in range(len(self.shape[0]) - 1, -1, -1)]
        self.shape = rotated_shape

def check_collision(tetromino, game_board, dx=0, dy=0):
    for row_idx, row in enumerate(tetromino.shape):
        for col_idx, cell in enumerate(row):
            if cell:
                new_x = tetromino.x + col_idx + dx
                new_y = tetromino.y + row_idx + dy

                # 檢查邊界碰撞
                if not (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT):
                    return True
                # 檢查與已落下方塊的碰撞
                if game_board[new_y][new_x] is not None:
                    return True
    return False

def lock_tetromino(tetromino, game_board):
    for row_idx, row in enumerate(tetromino.shape):
        for col_idx, cell in enumerate(row):
            if cell:
                game_board[tetromino.y + row_idx][tetromino.x + col_idx] = tetromino.color

def clear_lines(game_board):
    cleared_lines = 0
    for row_idx in range(GRID_HEIGHT - 1, -1, -1):
        if all(cell is not None for cell in game_board[row_idx]):
            cleared_lines += 1
            del game_board[row_idx]
            game_board.insert(0, [None for _ in range(GRID_WIDTH)])
    return cleared_lines

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)

    # 載入字體
    font = pygame.font.Font("assets/wqy-zenhei.ttc", 24)

    clock = pygame.time.Clock()
    running = True
    game_over = False

    game_board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    score = 0
    fall_time = 0
    fall_speed = 500 # 毫秒

    current_tetromino_shape, current_tetromino_color = get_random_tetromino()
    current_tetromino = Tetromino(current_tetromino_shape, current_tetromino_color)

    next_tetromino_shape, next_tetromino_color = get_random_tetromino()
    next_tetromino = Tetromino(next_tetromino_shape, next_tetromino_color, x=NEXT_TETROMINO_X_OFFSET, y=1)

    while running:
        fall_time += clock.get_rawtime()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(current_tetromino, game_board, dx=-1, dy=0):
                        current_tetromino.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    if not check_collision(current_tetromino, game_board, dx=1, dy=0):
                        current_tetromino.move(1, 0)
                if event.key == pygame.K_DOWN:
                    if not check_collision(current_tetromino, game_board, dx=0, dy=1):
                        current_tetromino.move(0, 1)
                if event.key == pygame.K_UP:
                    # 嘗試旋轉，並檢查碰撞
                    original_shape = current_tetromino.shape
                    current_tetromino.rotate()
                    if check_collision(current_tetromino, game_board):
                        current_tetromino.shape = original_shape # 旋轉失敗，恢復原狀

        # 自動下落
        if fall_time / 1000 >= fall_speed / 1000:
            if not check_collision(current_tetromino, game_board, dx=0, dy=1):
                current_tetromino.move(0, 1)
            else:
                lock_tetromino(current_tetromino, game_board)
                cleared_lines = clear_lines(game_board)
                score += cleared_lines * 100 # 每清除一行增加100分

                current_tetromino = next_tetromino
                next_tetromino_shape, next_tetromino_color = get_random_tetromino()
                next_tetromino = Tetromino(next_tetromino_shape, next_tetromino_color, x=NEXT_TETROMINO_X_OFFSET, y=1)
                if check_collision(current_tetromino, game_board): # 遊戲結束
                    running = False
                    game_over = True
            fall_time = 0

        # 繪製背景
        screen.fill(BLACK)

        # 繪製已落下方塊
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if game_board[y][x] is not None:
                    draw_block(screen, game_board[y][x], x, y)

        # 繪製當前下落方塊
        current_tetromino.draw(screen)

        # 繪製下一個方塊
        next_tetromino.draw(screen)

        # 繪製分數
        score_text = font.render(f"分數: {score}", True, WHITE)
        screen.blit(score_text, (5, 5))

        pygame.display.flip()

    pygame.quit()

    # 遊戲結束畫面
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over = False
                if event.key == pygame.K_r:
                    # 重啟遊戲
                    main()
                    game_over = False

        screen.fill(BLACK)
        game_over_text = font.render("遊戲結束!", True, WHITE)
        score_final_text = font.render(f"最終分數: {score}", True, WHITE)
        restart_text = font.render("按 'R' 重新開始, 'Q' 離開", True, WHITE)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(score_final_text, (SCREEN_WIDTH // 2 - score_final_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
