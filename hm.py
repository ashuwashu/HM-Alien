import pygame
from pygame.locals import *
import random

pygame.init()


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invasion")

clock = pygame.time.Clock()
fps = 60


font = pygame.font.SysFont("Times New Roman", 60)
small_font = pygame.font.SysFont("Times New Roman", 30)
white = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

    
        self.image = pygame.image.load("Image20260704110922.png")
        self.image = pygame.transform.scale(self.image, (60, 60))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.speed = 10

    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= self.speed

    def move_right(self):
        if self.rect.right < screen_width:
            self.rect.x += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)



class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Image20260704110917.png")
        self.image = pygame.transform.scale(self.image, (10, 30))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    def draw(self):
        screen.blit(self.image, self.rect)



class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        
        self.image = pygame.image.load("Image20260704110847.png")
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def draw(self):
        screen.blit(self.image, self.rect)



class Button():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 120, 50)

    def draw(self):
        pygame.draw.rect(screen, (200, 0, 0), self.rect)
        text = small_font.render("RESET", True, white)
        screen.blit(text, (self.rect.x + 20, self.rect.y + 10))

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
        return False



def create_aliens():
    aliens = []
    rows = 5
    cols = 10
    for row in range(rows):
        for col in range(cols):
            alien = Alien(60 + col * 60, 50 + row * 50)
            aliens.append(alien)
    return aliens


player = Player(screen_width // 2, screen_height - 80)
lasers = pygame.sprite.Group()
aliens = create_aliens()

alien_speed = 2
direction = 1

game_over = False
you_win = False
you_lose = False
score = 0

reset_button = Button(screen_width//2 - 60, screen_height//2 + 80)



running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if not game_over:
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    laser = Laser(player.rect.centerx, player.rect.top)
                    lasers.add(laser)

    if not game_over:

        
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            player.move_left()
        if keys[K_RIGHT]:
            player.move_right()

        
        edge_reached = False
        for alien in aliens:
            alien.rect.x += alien_speed * direction
            if alien.rect.right >= screen_width or alien.rect.left <= 0:
                edge_reached = True

        if edge_reached:
            direction *= -1
            for alien in aliens:
                alien.rect.y += 20

lasers.update()

for laser in lasers:
    for alien in aliens:
        if laser.rect.colliderect(alien.rect):
            lasers.remove(laser)
            aliens.remove(alien)
            score += 1
            break

        
        if len(aliens) == 0:
            you_win = True
            game_over = True

        
        for alien in aliens:
            if alien.rect.bottom >= player.rect.top:
                you_lose = True
                game_over = True

    
    screen.fill((0, 0, 0))


    score_text = small_font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    player.draw()

    for alien in aliens:
        alien.draw()

    for laser in lasers:
        laser.draw()


    if you_win:
        text=font.render("YOU WIN!", True,white)
        screen.blit(text, (screen_width//2 - 150, screen_height//2))

    if you_lose:
        text=font.render("YOU LOSE!", True,  white)
        screen.blit(text,   (screen_width//2 - 150, screen_height//2))

    
    if game_over:
        if reset_button.draw():
        
            player = Player(screen_width // 2, screen_height - 80)
            lasers = pygame.sprite.Group()
            aliens = create_aliens()
            alien_speed = 2
            direction = 1
            game_over = False
            you_win = False
            you_lose = False
            score = 0

    pygame.display.update()

pygame.quit()
