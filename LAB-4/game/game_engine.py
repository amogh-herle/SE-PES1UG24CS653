import pygame
from .player import Player
from .platform import Platform
from .hazard import Hazard

# Game Engine

WHITE = (255, 255, 255)
BROWN = (150, 100, 60)
RED = (220, 60, 60)
GREEN = (0, 200, 0)

DIFFICULTIES = {
    pygame.K_1: ("Easy", 0.45, -11),
    pygame.K_2: ("Medium", 0.6, -12),
    pygame.K_3: ("Hard", 0.85, -13),
}

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gravity = 0.6
        self.difficulty_name = "Medium"
        self.quit = False

        self.start_x, self.start_y = 40, height - 120
        self.player = Player(self.start_x, self.start_y)

        # A simple hand-built level: platforms with gaps between them
        # (falling into a gap means falling off the bottom of the
        # screen), one hazard, and a goal near the right edge.
        ground_y = height - 40
        self.platforms = [
            Platform(0, ground_y, 160),
            Platform(220, ground_y, 140),
            Platform(420, ground_y - 60, 120),
            Platform(600, ground_y, 180),
        ]
        self.hazards = [Hazard(260, ground_y - 14, 40)]
        self.goal_x = 740

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over = False

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if self.game_over:
            if event.key == pygame.K_ESCAPE:
                self.quit = True
            elif event.key in DIFFICULTIES:
                name, gravity, jump_strength = DIFFICULTIES[event.key]
                self.reset(name, gravity, jump_strength)
            return
        if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
            self.player.jump()

    def reset(self, difficulty_name=None, gravity=None, jump_strength=None):
        self.player = Player(self.start_x, self.start_y)
        if difficulty_name is not None:
            self.difficulty_name = difficulty_name
            self.gravity = gravity
            self.player.jump_strength = jump_strength
        self.score = 0
        self.game_over = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.vx = -self.player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.vx = self.player.speed

    def update(self):
        if self.game_over:
            return

        self.player.vy += self.gravity
        self.player.vy = min(self.player.vy, 20)  # terminal velocity cap
        self.player.x = max(0, self.player.x + self.player.vx)

        prev_bottom = self.player.y + self.player.height
        self.player.y += self.player.vy
        new_bottom = self.player.y + self.player.height
        self.player.on_ground = False
        if self.player.vy >= 0:
            for platform in self.platforms:
                p = platform.rect()
                # horizontal overlap, and feet crossed the platform's
                # top this frame (swept check, not just post-move overlap)
                horizontal_overlap = self.player.x + self.player.width > p.left and self.player.x < p.right
                crossed_top = prev_bottom <= p.top and new_bottom >= p.top
                if horizontal_overlap and crossed_top:
                    self.player.y = p.top - self.player.height
                    self.player.vy = 0
                    self.player.on_ground = True

        for hazard in self.hazards:
            if self.player.rect().colliderect(hazard.rect()):
                self.game_over = True
                return

        if self.player.y > self.height:
            self.game_over = True
            return

        if self.player.x >= self.goal_x:
            self.score += 1
            self.player.x, self.player.y = self.start_x, self.start_y
            self.player.vy = 0

    def render(self, screen):
        for platform in self.platforms:
            pygame.draw.rect(screen, BROWN, platform.rect())
        for hazard in self.hazards:
            pygame.draw.rect(screen, RED, hazard.rect())

        goal_rect = pygame.Rect(self.goal_x, 0, 6, self.height)
        pygame.draw.rect(screen, GREEN, goal_rect)

        pygame.draw.rect(screen, WHITE, self.player.rect())

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            self.render_game_over(screen)

    def render_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        big_font = pygame.font.SysFont("Arial", 48)
        title = big_font.render("Game Over", True, WHITE)
        screen.blit(title, (self.width // 2 - title.get_width() // 2, self.height // 2 - 80))

        score_line = self.font.render(f"Final Score: {self.score}", True, WHITE)
        screen.blit(score_line, (self.width // 2 - score_line.get_width() // 2, self.height // 2 - 20))

        prompt = self.font.render("1: Easy   2: Medium   3: Hard   ESC: Exit", True, WHITE)
        screen.blit(prompt, (self.width // 2 - prompt.get_width() // 2, self.height // 2 + 30))
