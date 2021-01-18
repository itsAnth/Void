#  import and initialize pygame library
import pygame
from pygame.math import Vector2
import random

pygame.init()

# import key values
from pygame.locals import(
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

# set score
score = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("../Assets/dragon_flames.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (int(100*self.surf.get_width()/self.surf.get_height()), 100))
        self.rect = self.surf.get_rect(
            center = (
                int(screen_width/2),
                screen_height - int(self.surf.get_height()/2) - 15
            )
        )

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-15, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(15, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load("../Assets/asteroid_circle_shape.png").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.image = pygame.transform.scale(self.image, (int(30*self.image.get_width()/self.image.get_height()), 30))
        self.original_img = self.image
        pos = (
                random.randint(0, screen_width),
                random.randint(-15, 0)
            )
        self.rect = self.image.get_rect(center = pos)
        self.position = Vector2(pos)
        self.direction = Vector2(random.randint(-2, 2), random.randint(5, 10)).normalize()
        self.speed = random.randint(1,10)
        self.angle_speed = random.randint(-10, 10)
        self.angle = 0
        self.ignore_collision = 0

    def update(self):


        for enemy in enemies:
            if enemy != self and not self.ignore_collision and pygame.sprite.collide_circle(self, enemy):
                
                print("Collision")
                if self.direction[0]*enemy.direction[0] < 0 and self.direction[1]*enemy.direction[1] < 0:
                    # bounce
                    print("Bounce")
                    # find line between centers
                    dx = self.rect.centerx - enemy.rect.centerx
                    dy = self.rect.centery - enemy.rect.centery

                    # get normal vector
                    n = pygame.math.Vector2(dx, dy)

                    # reflect with normal
                    self.direction.reflect_ip(n)
                    enemy.direction.reflect_ip(n)
                    
                    # swap the speeds
                    self.speed, enemy.speed = enemy.speed, self.speed

                    # ignore collisions until they move away from each other
                    self.ignore_collision = 10
                    enemy.ignore_collision = 10
            
        if self.ignore_collision:
            self.ignore_collision -= 1
        self.angle += self.angle_speed
        self.image = pygame.transform.rotate(self.original_img, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.position += self.direction*self.speed
        self.rect.center = self.position

        # kill enemy when it is off the screen
        # increment score if player avoided enemy
        if self.rect.right < 0 or self.rect.left > screen_width or self.rect.top > screen_height:
            if self.rect.top > player.rect.top:
                global score
                score += 1
            self.kill()

# set game clock speed
FPS = 25
fpsclock = pygame.time.Clock()

# set drawing window size
SCREEN_HEIGHT_IPHONE = 2778
SCREEN_WIDTH_IPHONE = 1284
screen_height = 600
screen_width = int(600*SCREEN_WIDTH_IPHONE/SCREEN_HEIGHT_IPHONE)
screen = pygame.display.set_mode([screen_width, screen_height])

background = pygame.image.load("../Assets/background.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# set font
font = pygame.font.SysFont("sfchaerilidae", 18)

# create an event for adding enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 700)

# instantiate player
player = Player()

# create group to hold all enemies and all sprites
# enemies group will be used for collision detection and for updates
# all sprites will be used to render all sprites
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# variable to control the game state
running = True

#  main game loop
while running:
    # iterate through the event queue
    for event in pygame.event.get():
        # exit the main loop if escape key pressed or quit is clicked
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        # create a new enemy and add it to the enemy and all sprite groups
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # get all pressed keys
    pressed_keys = pygame.key.get_pressed()

    # update player and enemy positions
    player.update(pressed_keys)
    enemies.update()

    # set background image
    screen.blit(background, (0, 0))

    # draw all sprites
    for entity in all_sprites:
        try:
            screen.blit(entity.surf, entity.rect)
        except:
            screen.blit(entity.image, entity.rect)

    score_img = font.render(f"SCORE: {score}", True, (255, 28, 0)) 
    screen.blit(score_img, (5, 5))

    # check if player collided with any enemies
    # if pygame.sprite.spritecollideany(player, enemies):
    #     player.kill()
    #     running = False

    pygame.display.flip()
    fpsclock.tick(FPS)

pygame.quit()