# File: main.py
# Name: Evan Bai, Sami Ahmed
# Date: Jan 08th 2024
# Class: ICS4UI
# Asteroid Game culminating assignment


# Imports
import pygame
import math
import random
import draw



# import module
import draw

## Constant Variables

spriteclass = pygame.sprite.Sprite
Display = pygame.display
PLAYERSIZE = 50
FPS = 30

# Width & Height
WIDTH = 1200
HEIGHT = 800

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

  # Initialization
  def __init__(self, x, y, img):
    
    # Initial (x, y) coordinates
    self.x = x
    self.y = y

    # Image & Initial Angle (forward)
    self.img = img
    self.rect = self.img.get_rect()
    self.angle = 0

    # Size and initial speed
    self.size = PLAYERSIZE
    self.speed = 50


  # Function to move left
  def moveLeft(self):
    self.x -= self.speed
    self.angle = 90
    self.img = pygame.transform.rotate(self.img, self.angle)


  # Function to move right
  def moveRight(self):
    self.x += self.speed
    self.angle = 270


  # Function to move forward
  def moveForward(self):
    self.y -= self.speed
    self.angle = 0


  # Function to move backward
  def moveBack(self):
    self.y += self.speed
    self.angle = 180
  

# Asteroid Class
class Asteroids(spriteclass):

  # Table for all asteroids created
  AsteroidTable = []
  lasttick = pygame.time.get_ticks()
  
  # Initialization
  def __init__(self):

    # All attributes of asteroids created are randomized
    self.speed = random.randint(1,10)
    self.size = random.randint(1,10)
    x = random.choice([True, False])

    # Chooses if the asteroid will be placed along the x axis or the y axis randomly
    if x:
      self.posx = random.randint(0, WIDTH - self.size)
      self.posy = random.choice([self.size, HEIGHT])
    else:
      self.posy = random.randint(self.size, HEIGHT)
      self.posx = random.choice([0, WIDTH - self.size])

      
  def draw(self):
    draw.DrawImage(display, )


# Bullets Class
class Bullets(spriteclass):
  # List of all bullets on screen
  BulletTable = []

  # Initialization
  def __init__(self):
    pass


# Powerups Class
class Powerups(spriteclass):
  PowerupTable = []

  # Initialization
  def __init__(self):
    pass
    


# Updates Display
while True:

  draw


  for event in pygame.event.get():
    if event.type == pygame.QUIT:
          pygame.quit()


  # Player 1 and 2 movement
  key = pygame.key.get_pressed()

  if key[pygame.K_w]:
    pass


  # Asteroid Spawn
  
  # spawns an asteroid every 0.5 seconds
  if pygame.time.get_ticks() - Asteroids.lasttick > 500:
    Asteroids()
          
  # Powerup spawn
  
  
  # Updates Screen
  pygame.time.Clock().tick(FPS)
  pygame.display.update()
  print("penispenis")