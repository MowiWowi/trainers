import gym
from gym import spaces
import numpy as np
import random
import pygame

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ShooterEnv(gym.Env):
    def __init__(self):
        super(ShooterEnv, self).__init__()
        self.action_space = spaces.Discrete(3)  # Actions: left, shoot, right
        self.observation_space = spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)
        self.reset()

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Shooter Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        # Define player, bullet, and enemy visuals
        self.player_img = pygame.Surface((50, 50))
        self.player_img.fill((0, 255, 0))  # Green player
        self.bullet_img = pygame.Surface((5, 10))
        self.bullet_img.fill((255, 0, 0))  # Red bullet
        self.enemy_img = pygame.Surface((50, 50))
        self.enemy_img.fill((255, 0, 255))  # Purple enemy

        self.shoot_cooldown = 20  # Number of frames to wait before shooting again
        self.shoot_timer = 0  # Timer for the shooting cooldown

    def reset(self):
        self.player_x = 400  # Starting X position of the player
        self.player_y = 550  # Starting Y position of the player
        self.bullets = []  # List of Bullet objects
        self.enemies = []   # List of enemies represented as [x, y]
        self.score = 0      # Score
        self.shoot_timer = 0  # Reset shoot timer
        return self.state()

    def step(self, action):
        # Initialize reward
        reward = 0

        if action == 0:  # Move left
            self.player_x = max(0, self.player_x - 5)
        elif action == 2:  # Move right
            self.player_x = min(800 - 50, self.player_x + 5)
        elif action == 1:  # Shoot
            if self.shoot_timer == 0:  # Check if cooldown is over
                # Fire a bullet aimed at the current enemy positions
                bullet_x = self.player_x + 22  # Center bullet on player
                bullet_y = self.player_y - 10   # Bullet starts above player
                self.bullets.append(Bullet(bullet_x, bullet_y))  # Create bullet
                self.shoot_timer = self.shoot_cooldown  # Reset cooldown timer

        # Update bullets
        for bullet in list(self.bullets):
            bullet.y -= 10  # Move bullet up
            if bullet.y < 0:  # Remove bullet if it goes off screen
                self.bullets.remove(bullet)

        # Spawn enemies randomly
        if random.random() < 0.02:
            self.enemies.append([random.randint(0, 750), 0])  # Random X position

        # Update shoot timer
        if self.shoot_timer > 0:
            self.shoot_timer -= 1

        # Update enemies and check for collisions
        for enemy in list(self.enemies):
            enemy[1] += 3  # Move enemy down
            if enemy[1] > 600:  # Remove enemy if it goes off screen
                self.enemies.remove(enemy)
                reward -= 20  # Penalize for letting enemies pass

            # Check for collision with bullets
            bullet_hit = False
            for bullet in list(self.bullets):
                if (bullet.x in range(enemy[0], enemy[0] + 50) and
                        bullet.y in range(enemy[1], enemy[1] + 50)):
                    bullet_hit = True
                    reward += 50  # Reward for hitting an enemy
                    self.bullets.remove(bullet)  # Remove bullet on hit
                    self.enemies.remove(enemy)     # Remove enemy on hit
                    break  # Stop checking this enemy

            if bullet_hit:
                break  # Stop checking bullets once one hits

        # Check if player is hit by any enemy
        for enemy in self.enemies:
            if enemy[1] > 550:  # If enemy reaches player's Y position
                return self.state(), -100, True, {}  # Game over with a heavy penalty

        # Reward for survival
        survival_bonus = 0.1  # Small reward for staying alive each step
        reward += survival_bonus

        return self.state(), reward, False, {}  # Return the state and reward

    def state(self):
        # Return normalized state
        return np.array([self.player_x / 800, self.player_y / 600, self.score / 100, len(self.enemies) / 10])

    def render(self, mode='human'):
        # Handle Pygame events to keep the window responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                raise KeyboardInterrupt("Pygame window closed.")

        # Clear the screen
        self.screen.fill((0, 0, 0))  # Black background

        # Draw the player
        self.screen.blit(self.player_img, (self.player_x, self.player_y))

        # Draw the bullets
        for bullet in self.bullets:
            self.screen.blit(self.bullet_img, (bullet.x, bullet.y))

        # Draw the enemies
        for enemy in self.enemies:
            self.screen.blit(self.enemy_img, (enemy[0], enemy[1]))

        # Display score and FPS
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(fps_text, (10, 40))

        # Update the display
        pygame.display.flip()
        self.clock.tick(60)  # Limit to 120 frames per second

    def close(self):
        pygame.quit()

# Uncomment the lines below to run the environment for testing
#if __name__ == "__main__":
#    env = ShooterEnv()
#    obs = env.reset()
#    try:
#        for _ in range(10000):
#            action = env.action_space.sample()  # Random action
#            obs, reward, done, info = env.step(action)
#            env.render()
#            if done:
#                obs = env.reset()
#    except KeyboardInterrupt:
#        env.close()
#        print("Game closed.")
#    env.close()
#