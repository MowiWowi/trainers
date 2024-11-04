import pygame
import random
import numpy as np
from game_env import ShooterEnv

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 3

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Shooter Game")

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT - 50, 50, 50)

    def move(self, dx):
        if 0 <= self.rect.x + dx <= WIDTH - self.rect.width:
            self.rect.x += dx

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top)

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)

    def update(self):
        self.rect.y -= BULLET_SPEED

class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 50), 0, 50, 50)

    def update(self):
        self.rect.y += ENEMY_SPEED

def main():
    player = Player()
    bullets = []
    enemies = []
    clock = pygame.time.Clock()
    score = 0

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-PLAYER_SPEED)
        if keys[pygame.K_RIGHT]:
            player.move(PLAYER_SPEED)
        if keys[pygame.K_SPACE]:
            bullets.append(player.shoot())

        # Update bullets
        for bullet in bullets:
            bullet.update()
            if bullet.rect.y < 0:
                bullets.remove(bullet)

        # Spawn enemies
        if random.random() < 0.02:
            enemies.append(Enemy())

        # Update enemies
        for enemy in enemies:
            enemy.update()
            if enemy.rect.y > HEIGHT:
                enemies.remove(enemy)
            if player.rect.colliderect(enemy.rect):
                running = False  # End the game if hit by an enemy

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, GREEN, player.rect)
        for bullet in bullets:
            pygame.draw.rect(screen, RED, bullet.rect)
        for enemy in enemies:
            pygame.draw.rect(screen, (0, 0, 255), enemy.rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
