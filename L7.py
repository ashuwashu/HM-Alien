import pygame
from pygame.locals import*
import random

pygame.init()
clock=pygame.time.Clock()
fps=60

screen_width=864
screen_height=936

screen= pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("flappy bird")

#game variables

font=pygame.font.Sysfont("Times new roman", 60)
white=(255,255,255)
ground_scroll=0
scroll_speed=4
flying=False
game_over=False
PipeGap=150
PipeFrenquency=1500  #milliseconds
Last_Pipe=pygame.time.get_ticks()
score=0
Pass_Pipe=False

#load images

bg=pygame.image.load("BG.png")
ground_img=pygame.image.load("Ground.png")
re_button=pygame.image.load("Restart.png")

#function for placing text ont he screen

def draw_text(text, font, text_col, x, y):
    img=font.render(text, True, text_col)
    screen.blit(img,( x, y))
    

def reset():
    pipe_group.empty()
    flappy.rect.X = 100
    flappy.rect.y = int(screen_height/2)
    score = 0
    return score
    
    


class Bird(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite. __init__ (self)
        self.images=[]
        self.index=0
        self.counter=0
        
        for i in range(1,3):
            image=pygame.image.load(f"bird{i}.png")
            self.images.append(image)

        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=0
        self.clicked=False()

    def update(self):
        if flying == True:
            # appling gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y = self.rect.y + int(self.vel)

        if game_over == False:
            # Jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked==False:
                self.clicked = True
                self.vel = -10

            if pygame.mouse.get.pressed()[0] == 0: 
                self.clicked=False

            flap_cooldown=5
            self.counter+=1

            if self.counter > flap_cooldown:
                self.counter=0 
                self.index=self.index+1   
                if self.index >= len(self.images):
                    self.index=0

                self.image=self.images[self.index]
            self.image=pygame.transform.rotate(self.images[self.index], self.vel * -2)
            
        else:
            self.image=pygame.transform.rotate(self.images[self.index], -90)

class Pipe (pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("Pipe.png")
        self.rect=self.image.get_rect()

        # position variable determines if the pip is coming form the bottom or top
        #poition 1 is from the top,  -1 is from the bottom
        if position==1:
            self.image=pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft=[x,y - int(PipeGap/2)]
        
        if position == -1:
            self.rect.topleft=[x,y + int(PipeGap/2)]

    def update(self):
        self.rect.x  -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)

    def draw(self):
        action=False
        pos=pygame.mouse.get_pos()
        if self.rect.collidePoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                action=True

        screen.blit(self.image, (self.rect.x, self.rect.y))

pipe_group=pygame.sprite.Group()
bird_group=pygame.sprite.Group()

flappy=Bird(100, 468)
bird_group.add(flappy)
button=Button(432, 350, re_button)



while True:
    clock.tick(60)
    screen.blit(bg, (0,0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()
    screen.blit(ground_img,(ground_scroll, 768))  
    if len(pipe_group )>0:
        if (bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left 
            and bird_group.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right and 
            Pass_Pipe==False):
            Pass_Pipe = True

        if Pass_Pipe==True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score = score + 1
                Pass_Pipe=False

    draw_text(str(score), font, white, 850, 100)
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True:
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if flying == True and game_over == False:
        TimeNow=pygame.time.get_ticks()
        if TimeNow - Last_Pipe > PipeFrenquency:
            pipe_height = random.randint(-100,100)
            btm_pipe= Pipe (screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe (screen_width, int (screen_height / 2) +pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)

        pipe_group.update()
        ground_scroll -= 5
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        if game_over == True:
            if button.draw():
                game_over - False
                score= reset()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and flying==False and game_over==False:
            flying = True

pygame.display.update()
pygame.quit()