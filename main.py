# File: main.py
# Name: Evan Bai, Sami Ahmed
# Date: Jan 08th 2024
# Class: ICS4UI
# Asteroid Game culminating assignment


# Imports
import pygame
import math
import random

# import module
import drawings

## Constant Variables

spriteclass = pygame.sprite.Sprite
Display = pygame.display
PLAYERSIZE = 30
FPS = 30

# Width & Height
WIDTH = 1200
HEIGHT = 700

# Colors
BLACK = (0, 0, 0)
WHITE = (255,255,255)

# Lists


# Screen Setups
screen = pygame.display.set_mode([WIDTH, HEIGHT])

pygame.display.set_caption("Asteroid") # Caption


# Classes
# Player Class
class Players(spriteclass):
  PlayerGroup = pygame.sprite.Group()

  # Initialization
  def __init__(self, x, y, img):
    spriteclass.__init__(self)
    self.PlayerGroup.add(self)

    # Image & Initial Angle (forward)
    self.rootimg = drawings.Resize(img, PLAYERSIZE, PLAYERSIZE)
    self.image = self.rootimg
    self.rect = self.rootimg.get_rect()
    self.angle = 0

    # Initial (x, y) coordinates
    self.rect.topleft = (x, y)

    # Size and initial speed
    self.size = PLAYERSIZE
    self.speed = 20


  # Function to move left
  def moveLeft(self):
    self.angle += math.pi / 20
    self.image = drawings.rot_center(self.rootimg, math.degrees(self.angle))


  # Function to move right
  def moveRight(self):
    self.angle -= math.pi / 20
    self.image = drawings.rot_center(self.rootimg, math.degrees(self.angle))
    

  # Function to move forward
  def moveForward(self):
    self.rect.move_ip(-(self.speed * math.sin(self.angle)),-(self.speed * math.cos(self.angle)))
    self.image = drawings.rot_center(self.rootimg, math.degrees(self.angle))

  # Function to move backward
  def moveBack(self):
    self.rect.move_ip(-(self.speed * math.sin(self.angle)),(self.speed * math.cos(self.angle)))
    self.image = drawings.rot_center(self.rootimg, math.degrees(self.angle))


# Asteroid Class
class Asteroids(spriteclass):
  sourceimage = drawings.LoadImage("woman.png")

  AsteroidGroup = pygame.sprite.Group()
  lasttick = pygame.time.get_ticks()
  
  # Initialization
  def __init__(self):
    spriteclass.__init__(self)

    self.AsteroidGroup.add(self)

    # All attributes of asteroids created are randomized
    self.size = random.randint(20,50)
    self.speed = random.randint(1,2)
    self.angle = random.randint(-2,2)
    self.image = drawings.Resize(self.sourceimage, self.size, self.size)
    self.rect = self.image.get_rect()

    x = random.choice([True, False])
    # Chooses if the asteroid will be placed along the x axis or the y axis randomly
    if x:
      self.x = random.randint(0, WIDTH - self.size)
      self.y = random.choice([0, HEIGHT - self.size])
      self.speedx = self.angle

      if self.y == 0:
        self.speedy = self.speed
      else:
        self.speedy = -self.speed

    else:
      self.speedy = self.angle
      self.y = random.randint(self.size, HEIGHT)
      self.x = random.choice([0, WIDTH - self.size])

      if self.x == 0:
        self.speedx = self.speed
      else:
        self.speedx = -self.speed


    self.rect.topleft = (self.x,self.y)


  def update(self):
    self.rect.move_ip(self.speedx,self.speedy)


# Bullets Class
class Bullets(spriteclass):

  # Initialization
  def __init__(self):
    spriteclass.__init__()
    pass


# Powerups Class
class Powerups(spriteclass):

  # Initialization
  def __init__(self):
    spriteclass.__init__()
    pass
    

background = drawings.Resize(drawings.bgimg1, WIDTH, HEIGHT)


player1img = pygame.transform.rotate(drawings.shipimg1, 180)

player1 = Players(200, 200, player1img) 
player2 = Players(WIDTH - 200, HEIGHT - 200, drawings.shipimg2)

# Updates Display
while True:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
          pygame.quit()

  drawings.DrawImage(screen, background , 0,0)


  # Player 1 and 2 movement
  key = pygame.key.get_pressed()

  if key[pygame.K_w] and player1.rect.y - player1.speed > 0:
    player1.moveForward()

  if key[pygame.K_a] and player1.rect.x - player1.speed > 0:
    player1.moveLeft()

  if key[pygame.K_s] and player1.rect.y + player1.speed < HEIGHT - PLAYERSIZE:
    player1.moveBack()
  
  # THESE MAKE NO SENSE SAMI

  if key[pygame.K_d] and player1.rect.x + player1.speed < WIDTH - PLAYERSIZE:
    player1.moveRight()

  if key[pygame.K_UP] and player2.y - player2.speed > 0:
    player2.moveForward()

  if key[pygame.K_DOWN]:
    player2.moveBack()

  if key[pygame.K_LEFT]:
    player2.moveLeft()

  if key[pygame.K_RIGHT]:
    player2.moveRight()

  # Draw Players 1 and 2
  
  Players.PlayerGroup.draw(screen)



  # Asteroid Spawn

  Asteroids.AsteroidGroup.update()
  Asteroids.AsteroidGroup.draw(screen)
  
  
  # spawns an asteroid every 0.5 seconds
  if pygame.time.get_ticks() - Asteroids.lasttick > 500:
    Asteroids.lasttick = pygame.time.get_ticks()
    print("cock")
    Asteroids()
          
  # Powerup spawn
  
  
  # Updates Screen
  pygame.time.Clock().tick(FPS)
  Display.update()
