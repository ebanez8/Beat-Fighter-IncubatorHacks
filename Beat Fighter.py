import pygame
import random
import sys
from pygame import mixer


# Initialize Pygame
pygame.init()
mixer.init()


# Constants
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000
NOTE_WIDTH = 50
NOTE_HEIGHT = 20
NOTE_SPEED = 5
TRACK_COUNT = 4
TRACK_WIDTH = NOTE_WIDTH + 20
SCORE_HEIGHT = 50
HIT_ZONE_Y = WINDOW_HEIGHT - 100
TRACK_START_Y = WINDOW_HEIGHT // 2
ANIMATION_FRAME_DURATION = 10


# Health bar constants
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_POSITION = (170, WINDOW_HEIGHT // 2 + 30)
ENEMY_HEALTH_BAR_WIDTH = 200
ENEMY_HEALTH_BAR_HEIGHT = 20
ENEMY_HEALTH_BAR_POSITION = (WINDOW_WIDTH - 370, WINDOW_HEIGHT // 2 + 30)


# Enemy attack animation constants
ENEMY_ATTACK_DURATION = 15
ENEMY_ATTACK_DISTANCE = 500


# Character positions
CHARACTER_BASE_X = WINDOW_WIDTH // 2 - 300
ENEMY_BASE_X = WINDOW_WIDTH // 2 + 200
CHARACTER_Y = WINDOW_HEIGHT // 2 - 175


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Beat Fighter")


# Load and scale images
background_image = pygame.image.load("bg.png")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT // 2))


character_idle = pygame.image.load("character.png")
character_idle = pygame.transform.scale(character_idle, (100, 100))


enemy_sprite = pygame.image.load("enemy.png")
enemy_sprite = pygame.transform.scale(enemy_sprite, (200, 200))


def load_animation_frames(base_path, count, size=(100, 100)):
    return [pygame.transform.scale(pygame.image.load(f"{base_path}{i}.png"), size)
            for i in range(1, count + 1)]


# Load all animation frames
left_punch_frames = load_animation_frames("characterp1.", 3)
right_punch_frames = load_animation_frames("characterp1.", 3)
up_punch_frames = load_animation_frames("characterp2.", 4)
down_punch_frames = load_animation_frames("characterp2.", 4)
enemy_attack_frames = load_animation_frames("enemyp1.", 3, size=(200, 200))


class Note:
    def __init__(self, track):
        self.track = track
        total_track_width = TRACK_COUNT * TRACK_WIDTH
        start_x = (WINDOW_WIDTH - total_track_width) // 2
        self.x = start_x + track * TRACK_WIDTH + (TRACK_WIDTH - NOTE_WIDTH) // 2
        self.y = TRACK_START_Y - NOTE_HEIGHT
        self.color = [RED, BLUE, GREEN, YELLOW][track]
        self.active = True
        self.arrow_size = 30


    def move(self):
        self.y += NOTE_SPEED


    def draw(self, surface):
        if self.active:
            center_x = self.x + NOTE_WIDTH // 2
            center_y = self.y + NOTE_HEIGHT // 2
            points = []


            if self.track == 0:  # Left arrow
                points = [
                    (center_x + self.arrow_size // 2, center_y - self.arrow_size // 2),
                    (center_x - self.arrow_size // 2, center_y),
                    (center_x + self.arrow_size // 2, center_y + self.arrow_size // 2),
                ]
            elif self.track == 1:  # Down arrow
                points = [
                    (center_x - self.arrow_size // 2, center_y - self.arrow_size // 2),
                    (center_x + self.arrow_size // 2, center_y - self.arrow_size // 2),
                    (center_x, center_y + self.arrow_size // 2),
                ]
            elif self.track == 2:  # Up arrow
                points = [
                    (center_x - self.arrow_size // 2, center_y + self.arrow_size // 2),
                    (center_x + self.arrow_size // 2, center_y + self.arrow_size // 2),
                    (center_x, center_y - self.arrow_size // 2),
                ]
            elif self.track == 3:  # Right arrow
                points = [
                    (center_x - self.arrow_size // 2, center_y - self.arrow_size // 2),
                    (center_x + self.arrow_size // 2, center_y),
                    (center_x - self.arrow_size // 2, center_y + self.arrow_size // 2),
                ]


            pygame.draw.polygon(surface, self.color, points)
            pygame.draw.polygon(surface, WHITE, points, 2)


class Game:
    def __init__(self):
        self.notes = []
        self.score = 0
        self.health = 100
        self.max_health = 100
        self.enemy_health = 350  # New enemy health attribute
        self.enemy_max_health = 350  # New enemy max health attribute
        self.spawn_timer = 0
        self.spawn_delay = 60
        self.font = pygame.font.Font(None, 36)
        self.keys = [pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT]
       
        # Player animation attributes
        self.animation_frame_index = 0
        self.is_animating = False
        self.animation_timer = 0
        self.current_punch_frames = left_punch_frames
        self.character_x = CHARACTER_BASE_X
        self.is_attacking = False
       
        # Enemy animation attributes
        self.enemy_x = ENEMY_BASE_X
        self.enemy_is_attacking = False
        self.enemy_animation_frame_index = 0
        self.enemy_animation_timer = 0
        self.enemy_current_frames = enemy_attack_frames


    def spawn_note(self):
        track = random.randint(0, TRACK_COUNT - 1)
        self.notes.append(Note(track))


    def draw_health_bar(self, surface):
        pygame.draw.rect(surface, RED, (*HEALTH_BAR_POSITION, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        current_health_width = (self.health / self.max_health) * HEALTH_BAR_WIDTH
        pygame.draw.rect(surface, GREEN,
                        (HEALTH_BAR_POSITION[0], HEALTH_BAR_POSITION[1],
                         current_health_width, HEALTH_BAR_HEIGHT))
        health_text = self.font.render(f"Health: {self.health}", True, WHITE)
        surface.blit(health_text, (HEALTH_BAR_POSITION[0], HEALTH_BAR_POSITION[1] - 25))


    def draw_enemy_health_bar(self, surface):
        pygame.draw.rect(surface, RED, (*ENEMY_HEALTH_BAR_POSITION, ENEMY_HEALTH_BAR_WIDTH, ENEMY_HEALTH_BAR_HEIGHT))
        current_health_width = (self.enemy_health / self.enemy_max_health) * ENEMY_HEALTH_BAR_WIDTH
        pygame.draw.rect(surface, GREEN,
                        (ENEMY_HEALTH_BAR_POSITION[0], ENEMY_HEALTH_BAR_POSITION[1],
                         current_health_width, ENEMY_HEALTH_BAR_HEIGHT))
        health_text = self.font.render(f"Enemy Health: {self.enemy_health}", True, WHITE)
        surface.blit(health_text, (ENEMY_HEALTH_BAR_POSITION[0], ENEMY_HEALTH_BAR_POSITION[1] - 25))


    def draw_tracks(self, surface):
        total_track_width = TRACK_COUNT * TRACK_WIDTH
        start_x = (WINDOW_WIDTH - total_track_width) // 2
        for i in range(TRACK_COUNT + 1):
            x = start_x + (i * TRACK_WIDTH)
            pygame.draw.line(surface, GRAY, (x, TRACK_START_Y), (x, WINDOW_HEIGHT), 2)
            if i < TRACK_COUNT:
                center_x = x + TRACK_WIDTH // 2
                center_y = HIT_ZONE_Y
                self.draw_track_arrow(surface, i, center_x, center_y)


    def draw_track_arrow(self, surface, track, center_x, center_y):
        arrow_size = 30
        points = []
       
        if track == 0:  # Left
            points = [(center_x + arrow_size//2, center_y - arrow_size//2),
                     (center_x - arrow_size//2, center_y),
                     (center_x + arrow_size//2, center_y + arrow_size//2)]
        elif track == 1:  # Down
            points = [(center_x - arrow_size//2, center_y - arrow_size//2),
                     (center_x + arrow_size//2, center_y - arrow_size//2),
                     (center_x, center_y + arrow_size//2)]
        elif track == 2:  # Up
            points = [(center_x - arrow_size//2, center_y + arrow_size//2),
                     (center_x + arrow_size//2, center_y + arrow_size//2),
                     (center_x, center_y - arrow_size//2)]
        elif track == 3:  # Right
            points = [(center_x - arrow_size//2, center_y - arrow_size//2),
                     (center_x + arrow_size//2, center_y),
                     (center_x - arrow_size//2, center_y + arrow_size//2)]


        pygame.draw.polygon(surface, WHITE, points)
        pygame.draw.polygon(surface, WHITE, points, 2)


    def check_note_hit(self, track):
        hit_y = HIT_ZONE_Y
        hit_range = 30


        for note in self.notes:
            if note.track == track and note.active and abs(note.y - hit_y) < hit_range:
                note.active = False
                self.score += 100
                # Reduce enemy health by 2%
                self.enemy_health = max(0, self.enemy_health - 2)
                # Check if enemy is defeated
                if self.enemy_health <= 0:
                    pygame.quit()
                    sys.exit()
               
                self.current_punch_frames = [left_punch_frames, down_punch_frames,
                                          up_punch_frames, right_punch_frames][track]
                self.is_animating = True
                self.is_attacking = True
                self.animation_frame_index = 0
                self.animation_timer = 0
                self.character_x = ENEMY_BASE_X - 100
                return True
        return False


    def update(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_note()
            self.spawn_timer = 0


        for note in self.notes:
            note.move()
            if note.active and note.y > HIT_ZONE_Y + 30:
                note.active = False
                self.health = max(0, self.health - 7.5)
                self.enemy_is_attacking = True
                self.enemy_animation_frame_index = 0
                self.enemy_animation_timer = 0
                if self.health <= 0:
                    pygame.quit()
                    sys.exit()


        self.notes = [note for note in self.notes if note.y < WINDOW_HEIGHT]


        # Update player animation
        if self.is_animating:
            self.animation_timer += 1
            if self.animation_timer >= ANIMATION_FRAME_DURATION:
                self.animation_frame_index += 1
                self.animation_timer = 0
                if self.animation_frame_index >= len(self.current_punch_frames):
                    self.is_animating = False
                    self.is_attacking = False
                    self.character_x = CHARACTER_BASE_X


        # Update enemy animation
        if self.enemy_is_attacking:
            self.enemy_animation_timer += 1
            if self.enemy_animation_timer >= ANIMATION_FRAME_DURATION:
                self.enemy_animation_frame_index += 1
                self.enemy_animation_timer = 0
                if self.enemy_animation_frame_index >= len(enemy_attack_frames):
                    self.enemy_is_attacking = False
                    self.enemy_x = ENEMY_BASE_X


    def draw(self, surface):
        surface.fill(BLACK)
        surface.blit(background_image, (0, 0))
        self.draw_tracks(surface)
        self.draw_score(surface)
        self.draw_health_bar(surface)
        self.draw_enemy_health_bar(surface)  # Add enemy health bar


        for note in self.notes:
            note.draw(surface)


        # Draw player
        if self.is_animating:
            surface.blit(self.current_punch_frames[self.animation_frame_index],
                        (self.character_x, CHARACTER_Y))
        else:
            surface.blit(character_idle, (self.character_x, CHARACTER_Y))


        # Draw enemy
        if self.enemy_is_attacking:
            attack_x = self.enemy_x - ENEMY_ATTACK_DISTANCE
            surface.blit(enemy_attack_frames[self.enemy_animation_frame_index],
                        (attack_x, CHARACTER_Y - 75))
        else:
            surface.blit(enemy_sprite, (self.enemy_x, CHARACTER_Y - 75))


    def draw_score(self, surface):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 10))


    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.keys:
                        track = self.keys.index(event.key)
                        self.check_note_hit(track)


            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()



