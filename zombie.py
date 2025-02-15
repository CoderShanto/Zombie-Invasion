import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load assets
player_img = pygame.Surface((50, 50))
player_img.fill(BLUE)

zombie_img = pygame.Surface((50, 50))
zombie_img.fill(RED)

bullet_img = pygame.Surface((10, 20))
bullet_img.fill(GREEN)

# FPS clock
clock = pygame.time.Clock()
FPS = 60

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 60)
        self.speed = 5
        self.health = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Zombie class
class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = zombie_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(2, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, WIDTH - self.rect.width)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Groups
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
zombies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)
players.add(player)

# Create zombies
for _ in range(5):
    zombie = Zombie()
    all_sprites.add(zombie)
    zombies.add(zombie)

# Score and font
score = 0
font = pygame.font.SysFont("Arial", 20)

# Game loop
running = True
while running:
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.groupcollide(zombies, bullets, True, True)
    for hit in hits:
        score += 10
        zombie = Zombie()
        all_sprites.add(zombie)
        zombies.add(zombie)

    # Check if zombies reach the player
    hits = pygame.sprite.spritecollide(player, zombies, False)
    for hit in hits:
        player.health -= 10
        zombies.remove(hit)
        zombie = Zombie()
        all_sprites.add(zombie)
        zombies.add(zombie)
        if player.health <= 0:
            running = False

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Display score and health
    score_text = font.render(f"Score: {score}", True, WHITE)
    health_text = font.render(f"Health: {player.health}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 40))

    pygame.display.flip()

pygame.quit()
