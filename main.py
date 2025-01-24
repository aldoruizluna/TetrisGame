import pygame
import random
import enum
import json
import os
from datetime import datetime

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_OFFSET_X = (SCREEN_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
GRID_OFFSET_Y = (SCREEN_HEIGHT - GRID_HEIGHT * BLOCK_SIZE) // 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Game States
class GameState(enum.Enum):
    MAIN_MENU = 1
    MODE_SELECTION = 2
    CLASSIC_GAME = 3
    SPEED_GAME = 4
    BATTLE_GAME = 5
    SETTINGS = 6
    HIGH_SCORES = 7
    PAUSE = 8

# Game settings
class Settings:
    def __init__(self):
        self.music_volume = 0.7
        self.sfx_volume = 1.0
        self.difficulty = "Normal"
        self.controls = {
            "MOVE_LEFT": pygame.K_LEFT,
            "MOVE_RIGHT": pygame.K_RIGHT,
            "ROTATE": pygame.K_UP,
            "SOFT_DROP": pygame.K_DOWN,
            "HARD_DROP": pygame.K_SPACE
        }
        self.load_settings()

    def save_settings(self):
        settings_dict = {
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "difficulty": self.difficulty,
            "controls": {k: v for k, v in self.controls.items()}
        }
        with open("settings.json", "w") as f:
            json.dump(settings_dict, f)

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                settings_dict = json.load(f)
                self.music_volume = settings_dict.get("music_volume", self.music_volume)
                self.sfx_volume = settings_dict.get("sfx_volume", self.sfx_volume)
                self.difficulty = settings_dict.get("difficulty", self.difficulty)
                self.controls.update(settings_dict.get("controls", {}))
        except FileNotFoundError:
            self.save_settings()

class HighScores:
    def __init__(self):
        self.scores = []
        self.max_scores = 10
        self.load_scores()

    def add_score(self, score, mode):
        date = datetime.now().strftime("%Y-%m-%d")
        self.scores.append({"score": score, "date": date, "mode": mode})
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:self.max_scores]
        self.save_scores()

    def save_scores(self):
        with open("highscores.json", "w") as f:
            json.dump(self.scores, f)

    def load_scores(self):
        try:
            with open("highscores.json", "r") as f:
                self.scores = json.load(f)
        except FileNotFoundError:
            self.save_scores()

class Button:
    def __init__(self, x, y, width, height, text, color=WHITE, hover_color=BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        text_surface = self.font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class Menu:
    def __init__(self, screen, settings, high_scores):
        self.screen = screen
        self.settings = settings
        self.high_scores = high_scores
        self.state = GameState.MAIN_MENU
        self.selected_setting = None
        self.create_buttons()

    def create_buttons(self):
        button_width = 200
        button_height = 50
        start_y = SCREEN_HEIGHT // 3
        spacing = 70
        center_x = SCREEN_WIDTH // 2 - button_width // 2

        # Main Menu Buttons
        self.main_menu_buttons = [
            Button(center_x, start_y, button_width, button_height, "Play Game"),
            Button(center_x, start_y + spacing, button_width, button_height, "High Scores"),
            Button(center_x, start_y + spacing * 2, button_width, button_height, "Settings"),
            Button(center_x, start_y + spacing * 3, button_width, button_height, "Quit")
        ]

        # Game Mode Buttons
        self.mode_buttons = [
            Button(center_x, start_y, button_width, button_height, "Classic Mode"),
            Button(center_x, start_y + spacing, button_width, button_height, "Speed Mode"),
            Button(center_x, start_y + spacing * 2, button_width, button_height, "Battle Mode"),
            Button(center_x, start_y + spacing * 3, button_width, button_height, "Back")
        ]

        # Settings Buttons
        self.settings_buttons = [
            Button(center_x, start_y, button_width, button_height, f"Music: {int(self.settings.music_volume * 100)}%"),
            Button(center_x, start_y + spacing, button_width, button_height, f"SFX: {int(self.settings.sfx_volume * 100)}%"),
            Button(center_x, start_y + spacing * 2, button_width, button_height, f"Difficulty: {self.settings.difficulty}"),
            Button(center_x, start_y + spacing * 3, button_width, button_height, "Controls"),
            Button(center_x, start_y + spacing * 4, button_width, button_height, "Back")
        ]

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw title
        font = pygame.font.Font(None, 74)
        title = font.render("TETRIS", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)

        # Draw buttons based on current state
        if self.state == GameState.MAIN_MENU:
            for button in self.main_menu_buttons:
                button.draw(self.screen)
        elif self.state == GameState.MODE_SELECTION:
            for button in self.mode_buttons:
                button.draw(self.screen)
        elif self.state == GameState.SETTINGS:
            for button in self.settings_buttons:
                button.draw(self.screen)
        elif self.state == GameState.HIGH_SCORES:
            self.draw_high_scores()

        pygame.display.flip()

    def draw_high_scores(self):
        font = pygame.font.Font(None, 36)
        y = SCREEN_HEIGHT // 4
        
        # Draw header
        header = font.render("HIGH SCORES", True, WHITE)
        header_rect = header.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(header, header_rect)
        
        y += 50
        for score in self.high_scores.scores:
            score_text = f"{score['score']:,} - {score['mode']} - {score['date']}"
            text = font.render(score_text, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 40

        # Back button
        back_btn = Button(SCREEN_WIDTH // 2 - 100, y + 40, 200, 50, "Back")
        back_btn.draw(self.screen)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return GameState.QUIT

            if self.state == GameState.MAIN_MENU:
                for i, button in enumerate(self.main_menu_buttons):
                    if button.handle_event(event):
                        if i == 0:  # Play Game
                            self.state = GameState.MODE_SELECTION
                        elif i == 1:  # High Scores
                            self.state = GameState.HIGH_SCORES
                        elif i == 2:  # Settings
                            self.state = GameState.SETTINGS
                        elif i == 3:  # Quit
                            return GameState.QUIT

            elif self.state == GameState.MODE_SELECTION:
                for i, button in enumerate(self.mode_buttons):
                    if button.handle_event(event):
                        if i == 0:  # Classic Mode
                            return GameState.CLASSIC_GAME
                        elif i == 1:  # Speed Mode
                            return GameState.SPEED_GAME
                        elif i == 2:  # Battle Mode
                            return GameState.BATTLE_GAME
                        elif i == 3:  # Back
                            self.state = GameState.MAIN_MENU

            elif self.state == GameState.SETTINGS:
                for i, button in enumerate(self.settings_buttons):
                    if button.handle_event(event):
                        if i == 0:  # Music Volume
                            self.settings.music_volume = (self.settings.music_volume + 0.1) % 1.1
                            self.settings_buttons[0].text = f"Music: {int(self.settings.music_volume * 100)}%"
                            self.settings.save_settings()
                        elif i == 1:  # SFX Volume
                            self.settings.sfx_volume = (self.settings.sfx_volume + 0.1) % 1.1
                            self.settings_buttons[1].text = f"SFX: {int(self.settings.sfx_volume * 100)}%"
                            self.settings.save_settings()
                        elif i == 2:  # Difficulty
                            difficulties = ["Easy", "Normal", "Hard"]
                            current_idx = difficulties.index(self.settings.difficulty)
                            self.settings.difficulty = difficulties[(current_idx + 1) % len(difficulties)]
                            self.settings_buttons[2].text = f"Difficulty: {self.settings.difficulty}"
                            self.settings.save_settings()
                        elif i == 4:  # Back
                            self.state = GameState.MAIN_MENU

            elif self.state == GameState.HIGH_SCORES:
                back_btn = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Back")
                if back_btn.handle_event(event):
                    self.state = GameState.MAIN_MENU

        return None

class Tetrimino:
    def __init__(self, x, y, shape_data):
        self.x = x
        self.y = y
        self.shape = shape_data['shape']
        self.color = shape_data['color']

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))
        self.shape = [list(row) for row in self.shape]

SHAPES = [
    {'shape': [[1, 1, 1, 1]], 'color': CYAN},    # I
    {'shape': [[1, 1], [1, 1]], 'color': YELLOW},  # O
    {'shape': [[0, 1, 1], [1, 1, 0]], 'color': GREEN},  # S
    {'shape': [[1, 1, 0], [0, 1, 1]], 'color': RED},    # Z
    {'shape': [[1, 1, 1], [0, 0, 1]], 'color': BLUE},   # L
    {'shape': [[1, 1, 1], [1, 0, 0]], 'color': ORANGE}, # J
    {'shape': [[1, 1, 1], [0, 1, 0]], 'color': PURPLE}  # T
]

class Tetris:
    def __init__(self, screen, settings, high_scores):
        self.screen = screen
        self.settings = settings
        self.high_scores = high_scores
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.screen, settings, high_scores)
        self.current_state = GameState.MAIN_MENU
        self.running = True
        self.reset_game()

    def reset_game(self):
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.fall_time = 0
        self.fall_speed = 500
        if self.settings.difficulty == "Easy":
            self.fall_speed = 600
        elif self.settings.difficulty == "Hard":
            self.fall_speed = 400
        self.game_over = False
        self.score = 0
        self.spawn_new_piece()

    def spawn_new_piece(self):
        start_x = GRID_WIDTH // 2 - 1
        start_y = 0
        self.current_piece = Tetrimino(start_x, start_y, random.choice(SHAPES))

    def check_collision(self, x_offset=0, y_offset=0, shape=None):
        if shape is None:
            shape = self.current_piece.shape

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    abs_x = self.current_piece.x + x + x_offset
                    abs_y = self.current_piece.y + y + y_offset

                    if (abs_x < 0 or abs_x >= GRID_WIDTH or 
                        abs_y >= GRID_HEIGHT or 
                        (abs_y >= 0 and self.grid[abs_y][abs_x] is not None)):
                        return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    abs_y = self.current_piece.y + y
                    if abs_y >= 0:
                        self.grid[abs_y][self.current_piece.x + x] = self.current_piece.color

        self.clear_lines()
        self.spawn_new_piece()
        if self.check_collision():
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(cell is not None for cell in self.grid[y]):
                lines_cleared += 1
                for move_y in range(y, 0, -1):
                    self.grid[move_y] = self.grid[move_y - 1][:]
                self.grid[0] = [None] * GRID_WIDTH
            else:
                y -= 1

        if lines_cleared > 0:
            self.score += (100 * lines_cleared) * lines_cleared
        return lines_cleared

    def handle_game_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and not self.game_over:
                if event.key == pygame.K_LEFT:
                    if not self.check_collision(x_offset=-1):
                        self.current_piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not self.check_collision(x_offset=1):
                        self.current_piece.x += 1
                elif event.key == pygame.K_DOWN:
                    if not self.check_collision(y_offset=1):
                        self.current_piece.y += 1
                elif event.key == pygame.K_UP:
                    original_shape = [row[:] for row in self.current_piece.shape]
                    self.current_piece.rotate()
                    if self.check_collision():
                        self.current_piece.shape = original_shape
                elif event.key == pygame.K_SPACE:
                    while not self.check_collision(y_offset=1):
                        self.current_piece.y += 1
                    self.lock_piece()
                elif event.key == pygame.K_ESCAPE:
                    self.current_state = GameState.PAUSE

    def update_game(self):
        if self.game_over:
            return

        self.fall_time += self.clock.get_rawtime()
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            if not self.check_collision(y_offset=1):
                self.current_piece.y += 1
            else:
                self.lock_piece()

    def draw_game(self):
        self.screen.fill(BLACK)

        # Draw grid
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, GRAY,
                           (GRID_OFFSET_X + x * BLOCK_SIZE, GRID_OFFSET_Y),
                           (GRID_OFFSET_X + x * BLOCK_SIZE, GRID_OFFSET_Y + GRID_HEIGHT * BLOCK_SIZE))
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, GRAY,
                           (GRID_OFFSET_X, GRID_OFFSET_Y + y * BLOCK_SIZE),
                           (GRID_OFFSET_X + GRID_WIDTH * BLOCK_SIZE, GRID_OFFSET_Y + y * BLOCK_SIZE))

        # Draw locked pieces
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                if color:
                    pygame.draw.rect(self.screen, color,
                                   (GRID_OFFSET_X + x * BLOCK_SIZE,
                                    GRID_OFFSET_Y + y * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw current piece
        if self.current_piece:
            for y, row in enumerate(self.current_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, self.current_piece.color,
                                       (GRID_OFFSET_X + (self.current_piece.x + x) * BLOCK_SIZE,
                                        GRID_OFFSET_Y + (self.current_piece.y + y) * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (20, 20))

        if self.game_over:
            game_over_text = font.render('GAME OVER - Press ESC', True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if self.current_state in [GameState.MAIN_MENU, GameState.MODE_SELECTION, 
                                    GameState.SETTINGS, GameState.HIGH_SCORES]:
                new_state = self.menu.handle_events(events)
                if new_state:
                    if new_state == GameState.QUIT:
                        self.running = False
                    else:
                        self.current_state = new_state
                        if new_state in [GameState.CLASSIC_GAME, GameState.SPEED_GAME, 
                                       GameState.BATTLE_GAME]:
                            self.reset_game()
                self.menu.draw()

            elif self.current_state == GameState.CLASSIC_GAME:
                self.handle_game_events(events)
                self.update_game()
                self.draw_game()
                if self.game_over:
                    self.high_scores.add_score(self.score, "Classic")

            elif self.current_state == GameState.SPEED_GAME:
                self.handle_game_events(events)
                self.update_game()
                self.draw_game()
                if self.game_over:
                    self.high_scores.add_score(self.score, "Speed")

            elif self.current_state == GameState.BATTLE_GAME:
                self.handle_game_events(events)
                self.update_game()
                self.draw_game()
                if self.game_over:
                    self.high_scores.add_score(self.score, "Battle")

            elif self.current_state == GameState.PAUSE:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.current_state = GameState.MAIN_MENU

class SpeedGame(Tetris):
    def __init__(self, screen, settings, high_scores):
        super().__init__(screen, settings, high_scores)
        self.initial_fall_speed = 500
        self.min_fall_speed = 100
        self.speed_increase_rate = 0.95
        self.lines_for_speed_up = 5
        self.lines_cleared_count = 0

    def clear_lines(self):
        lines_cleared = super().clear_lines()
        if lines_cleared:
            self.lines_cleared_count += lines_cleared
            if self.lines_cleared_count >= self.lines_for_speed_up:
                self.lines_cleared_count = 0
                self.fall_speed = max(self.min_fall_speed, 
                                    self.fall_speed * self.speed_increase_rate)

class BattleGame(Tetris):
    def __init__(self, screen, settings, high_scores):
        super().__init__(screen, settings, high_scores)
        self.player2_grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.player2_piece = None
        self.player2_score = 0
        self.ai_move_timer = 0
        self.ai_move_delay = 200

    def update(self):
        super().update()
        self.update_ai()

    def update_ai(self):
        self.ai_move_timer += self.clock.get_rawtime()
        if self.ai_move_timer >= self.ai_move_delay:
            self.ai_move_timer = 0
            # Simple AI: randomly move and rotate pieces
            if random.random() < 0.3:
                if random.random() < 0.5:
                    self.move_piece_left()
                else:
                    self.move_piece_right()
            if random.random() < 0.2:
                self.rotate_piece()

    def draw(self):
        super().draw()
        # Draw player 2's grid on the right side
        for y, row in enumerate(self.player2_grid):
            for x, color in enumerate(row):
                if color:
                    pygame.draw.rect(self.screen, color,
                                   (GRID_OFFSET_X + GRID_WIDTH * BLOCK_SIZE + 100 + x * BLOCK_SIZE,
                                    GRID_OFFSET_Y + y * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))

if __name__ == '__main__':
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    settings = Settings()
    high_scores = HighScores()
    game = Tetris(screen, settings, high_scores)
    game.run()
    pygame.quit()
