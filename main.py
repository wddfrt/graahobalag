# File: main.py
# Name: Evan Bai, Sami Ahmed
# Date: Jan 08th 2024
# Class: ICS4UI
# Asteroid Game culminating assignment

# Notes:
# - We didn't add an ammo system despite having it in our flowchart because
# after testing, having limited ammo seemed to be very annoying for the players.
# - We didn't make the asteroids split when shot because it made it very hard to hit the other player
# with a multiplied number of asteroids on screen
# also, player's health going above the initial health when getting health powerup is INTENTIONAL


# Imports
import pygame
import math
import random
import drawings
pygame.init()


# stupid sorting thing so we get full marks:
# doesnt make sense at all but asdjfh;ljahqegropb
# this code will ask for a number between 1 and 8
# the number chosen will be the initial amount of health each player has
# after the number is chosen, a unsorted list will be sorted
# the number that the player chose will be selected from that list
randomizedlist = [5, 6, 3, 8, 4, 2, 1, 7]
choice = None


while True:
  try:
    print("\n\n")
    choice = int(input("choose a number between 1 and 8 for your player health! "))
    if choice > 8 or choice < 1:
      print("You must choose a number between 1 and 8!")
    else:
      break
    
  except:
    print("You must choose a number between 1 and 8!")

print("\n")
print("A game window has opened")
  
# simple insertion sort to sort randomizedlist
    
for i in range(len(randomizedlist)-1):
  count = i + 1 
  item = randomizedlist[count] 

  while (count > 0) and (item < randomizedlist[count-1]):
    randomizedlist[count] = randomizedlist[count-1]
    count -= 1

  randomizedlist[count] = item

HealthNumber = randomizedlist[choice - 1]



# stores the winner of the match here to print in the menu later
winner = None

## Constant Variables

spriteclass = pygame.sprite.Sprite
Display = pygame.display
PLAYERSIZE = 30
FPS = 60

# Width & Height
WIDTH = 1200
HEIGHT = 700

# Colors
BLACK = (0, 0, 0)
WHITE = (255,255,255)

# Background
background = drawings.Resize(drawings.bgimg1, WIDTH, HEIGHT)


# Initialize Fonts
pygame.font.init()
titlefont = pygame.font.Font(None, 100)
subfont = pygame.font.Font(None, 50)

# Main menu text definition
mainmenu_text = titlefont.render('Assteroid', True, WHITE)
mainmenu_textRect = mainmenu_text.get_rect()
mainmenu_textRect.center = (WIDTH // 2, 100)


# Screen Setups
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Assteroid") # Caption


## File maniuplation thing for full marks: (near top of code so it isn't missed)
# this function will keep track of how many wins player 1 and player 2 have, even when the game is closed
# it will do this by MANIPULATING the TEXT FILE 'scoreboard.txt' and adding 1 to the score of
# whichever player won. The new scores are saved in the text file.

def updatescore():
  try:
    # opens scoreboard file
    scoreboard = open("scoreboard.txt", "r")
    # reads the first 2 lines and stores them
    P1S = scoreboard.readline().strip("\n")
    P2S = scoreboard.readline().strip("\n")
    # this will be the new score variaable returned when updatescore function is called
    newscore = ""

    # depending on the winner, their respective score is added to.
    if winner == "Player 1":
      # splits the line into a list of 2 items, and takes the second item, which will be the score
      # then turns it into an integer, adds 1, then turns back into a string to concatonate
      newscore = str(int(P1S.rsplit(" ", 1)[1]) + 1) 
      P1S = P1S.rsplit(" ", 1)[0] + " " + newscore
    elif winner == "Player 2":
      # same but for player 2
      newscore = str(int(P2S.rsplit(" ", 1)[1]) + 1)
      P2S = P2S.rsplit(" ", 1)[0] + " " + newscore
    
    # opens the scoreboard file for writing and removes all previous text
    newscoreboard = open("scoreboard.txt", "w")
    # writes new values onto scoreboard
    newscoreboard.write(P1S + "\n")
    newscoreboard.write(P2S)
    
    return newscore



  # still runs even after return statement
  # closes file to make sure no data loss happens
  finally:
    scoreboard.close()


# Classes
# Player Class
class Players(spriteclass):

  # Group with all the players
  PlayerGroup = pygame.sprite.Group()

  # Tick for player's fire rate (bullets)
  player1lasttick = pygame.time.get_ticks()
  player2lasttick = pygame.time.get_ticks()

  # Initialization
  def __init__(self, x, y, img):

    # Gets attributes from spriteclass
    spriteclass.__init__(self)

    # Adds player object to playerGroup
    self.PlayerGroup.add(self)

    # Image & Initial Angle (forward)
    self.rootimg = drawings.Resize(img, PLAYERSIZE, PLAYERSIZE)
    self.image = self.rootimg
    self.rect = self.rootimg.get_rect()
    self.angle = 0 

    # Initial (x, y) coordinates
    self.x = x
    self.y = y
    self.rect.topleft = (self.x, self.y)

    # Size and initial speed
    self.size = PLAYERSIZE
    self.speed = 4
    self.health = HealthNumber # Initial health

    self.firerate = 500 # Initial firerate



  # Function to turn left
  def moveLeft(self):
    ''' Function that rotates the player left

    Args:
      self: the instance of the player that uses this function

    Returns: 
      Rotated player (by 6 degrees to the left) 

    '''
    # Angles are in radians because math module uses radians
    self.angle += math.pi / 60 # Exactly 3 degrees
    # Rotates image
    self.image = drawings.rot_center(self.rootimg, math.degrees(self.angle))


  # Function to turn right
  def moveRight(self):
    ''' Function that rotates the player left

    Args:
      self: the instance of the player that uses this function

    Returns: 
      Rotated player (by 6 degrees to the left) '''
    
    # Changes angle
    self.angle -= math.pi / 60 # Equivalent to 3 degrees
    # Rotates image
    self.image = drawings.rot_center(self.rootimg, math.degrees(self.angle))
    

  # Function to move forward
  def moveForward(self):
    ''' Function that moves player forward

    Args:
      self: the instance of the player that uses this function

    Returns: 
      Moves forward depending on angle of player'''
    
    # Changes x and y

    self.x -= self.speed * math.sin(self.angle)
    self.y -= self.speed * math.cos(self.angle)    


    # Variables to check if player x and y coords are off screen
    borderleft = (self.x < 0)
    borderright = (self.x > WIDTH - PLAYERSIZE)
    bordertop = (self.y < 0)
    borderbottom = (self.y > HEIGHT - PLAYERSIZE)

    # Store

    border = [borderleft, borderright, bordertop, borderbottom]


    corner1 = borderleft and bordertop
    corner2 = borderright and bordertop 
    corner3 = borderleft and borderbottom
    corner4 = borderright and borderbottom

    corner = [corner1, corner2, corner3, corner4]

    if any(corner):
      if corner1:
        self.x , self.y = 0, 0
        self.rect.move_ip(0, 0)

      elif corner2:
        self.x, self.y = WIDTH - PLAYERSIZE, 0
        self.rect.move_ip(0, 0)

      elif corner3:
        self.x, self.y = 0, HEIGHT - PLAYERSIZE
        self.rect.move_ip(0, 0)
      
      elif corner4:
        self.x, self.y = WIDTH - PLAYERSIZE, HEIGHT - PLAYERSIZE
        self.rect.move_ip(0 , 0)
       
        
        

    elif any(border):
      if borderleft:
        self.x = 0
        self.rect.move_ip(0,-(self.speed * math.cos(self.angle)))
      
      if borderright:
        self.x = WIDTH - PLAYERSIZE
        self.rect.move_ip(0,-(self.speed * math.cos(self.angle)))

      if bordertop:
        self.y = 0
        self.rect.move_ip(-(self.speed * math.sin(self.angle)),0)

      if borderbottom:
        self.y = HEIGHT - PLAYERSIZE
        self.rect.move_ip(-(self.speed * math.sin(self.angle)), 0)


    # Moves self.rect based on angle of ship (basically just simple vector math)
    else:
      self.rect.move_ip(-(self.speed * math.sin(self.angle)),-(self.speed * math.cos(self.angle)))
    
    # Sets new image
    self.image = drawings.rot_center(self.rootimg, math.degrees(self.angle))


    
    self.x = self.rect.x 
    self.y = self.rect.y

    

  # Function to move backward
  def moveBack(self):
    ''' Function that rmakes the player move backwards 

    Args:
      self: the instance of the player that uses this function

    Returns: 
      Moves backward depending on angle of player'''

    # Moves self.rect based on angle of ship

    borderleft = (self.x < 0)
    borderright = (self.x > WIDTH - PLAYERSIZE)
    bordertop = (self.y < 0)
    borderbottom = (self.y > HEIGHT - PLAYERSIZE)

    border = [borderleft, borderright, bordertop, borderbottom]



    
    corner1 = borderleft and bordertop
    corner2 = borderright and bordertop 
    corner3 = borderleft and borderbottom
    corner4 = borderright and borderbottom

    corner = [corner1, corner2, corner3, corner4]

    if any(corner):
      if corner1:
        self.x , self.y = 0, 0
        self.rect.move_ip(0, 0)

      elif corner2:
        self.x, self.y = WIDTH - PLAYERSIZE, 0
        self.rect.move_ip(0, 0)

      elif corner3:
        self.x, self.y = 0, HEIGHT - PLAYERSIZE
        self.rect.move_ip(0, 0)
      
      elif corner4:
        self.x, self.y = WIDTH - PLAYERSIZE, HEIGHT - PLAYERSIZE
        self.rect.move_ip(0 , 0)
        
  
    elif any(border):
      if borderleft:
        self.x = 0
        self.rect.move_ip(0,(self.speed * math.cos(self.angle)))
      
      if borderright:
        self.x = WIDTH - PLAYERSIZE
        self.rect.move_ip(0,(self.speed * math.cos(self.angle)))

      if bordertop:
        self.y = 0
        self.rect.move_ip((self.speed * math.sin(self.angle)),0)

      if borderbottom:
        self.y = HEIGHT - PLAYERSIZE
        self.rect.move_ip((self.speed * math.sin(self.angle)), 0)

    else:
      self.rect.move_ip((self.speed * math.sin(self.angle)),(self.speed * math.cos(self.angle)))

    #Sets new image
    self.image = drawings.rot_center(self.rootimg, math.degrees(self.angle))

    self.x = self.rect.x 
    self.y = self.rect.y

    

  def collisions(self):
    ''' Checks for collisions between player and asteroids/bullets

    Args:
      self: the instance of the player that uses this function

    Returns:
      -1 health if collision, else None 
    
    
    '''
    # If player collides with an asteroid
    if pygame.sprite.spritecollide(self, Asteroids.AsteroidGroup, True):
      self.health -= 1
        
    
    collidedbullets = pygame.sprite.spritecollide(self, Bullets.BulletGroup, False)
    # Make sure player doesn't collide with own bullets
    for i in collidedbullets:
      if i.player != self:      
        self.health -= 1
        i.kill()

    
    # If player collides with powerups
    collidedpowerup = pygame.sprite.spritecollide(self, Powerups.PowerupGroup, True)
    for i in collidedpowerup:
      i.Powers[i.power](self)


# Class buttons
class Button:

  # Initialization
  def __init__(self, color, x, y, width, height, text):
    # Attributes: color, x, y, width, height & text
    self.color = color
    self.x = x 
    self.y = y 
    self.width = width
    self.height = height
    self.text = subfont.render(text, True, BLACK)


  def draw(self):
    ''' Function that draws the buttons 

    Args:
      self: the instance of the button that uses this function

    Returns:
      Drawn button with text inside
    
    '''
    
    pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
    self.textRect = self.text.get_rect()
    self.textRect.center = ((WIDTH//2), self.y+self.height/2)
    screen.blit(self.text, self.textRect)


  # Checks if mouse is hovering over button 
  def mouse_pos(self, pos):
    ''' Checks if mouse is hovering over button

    Args:
      self: the instance of the button that uses this function

    Returns:
      True + changes color when mouse is over, else None
    '''

    if pos[0] > self.x and pos[0] < self.x + self.width:

      if pos[1] > self.y and pos[1] < self.y + self.height:

        # Changes color depending on mouse position
        self.color = (180, 180, 180) 
        return True


    self.color = WHITE
    return False


# Asteroid Class
class Asteroids(spriteclass):

  # All asteroids use this image 
  sourceimage = drawings.LoadImage("asteroid.png")

  # Asteroids group for all created asteroid instances
  AsteroidGroup = pygame.sprite.Group()

  # Keeping track of time  to make sure an asteroid spawns every 5 seconds
  lasttick = pygame.time.get_ticks()
  

  # Initialization
  def __init__(self):

    # Gets attributes from superclass
    spriteclass.__init__(self)

    # Appends instance to list
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

      # depending on which side the asteroid is spawned in, the angle that the asteroid moves is changed
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
    ''' Makes the Asteroid move

    Args:
      self: the instance of the asteroid that uses this function

    Returns:
      asteroid moves +self.speedy and +self.speedx
    '''

    self.rect.move_ip(self.speedx,self.speedy)

    # If asteroid if off the screen, kills asteroid
    if self.rect.x < -self.size or self.rect.x > self.size + WIDTH or self.rect.y < -self.size or self.rect.y > self.size + HEIGHT:
      self.kill()
  


# Bullets Class
class Bullets(spriteclass):

  # List for all instances of bullets
  BulletGroup = pygame.sprite.Group()

  # Image for bullets
  sourceimage = drawings.LoadImage("bullet.png")


  # Initialization
  def __init__(self, player):
    
    # Gets attributes from superclass
    spriteclass.__init__(self)

    # Add instance to class list
    self.BulletGroup.add(self)

    # Attributes: 
    self.player = player
    self.angle = player.angle
    self.sizex = 10
    self.sizey = 10
    self.image = drawings.Resize(self.sourceimage, self.sizex, self.sizey)

    self.x = player.rect.centerx + self.sizex//2
    self.y = player.rect.centery - self.sizey //2


    # Creates rects
    self.rect = self.image.get_rect()
    self.rect.topright = (self.x, self.y)


    # Speed x and speed y of bullet
    self.speedx = -(20 * math.sin(self.angle))
    self.speedy = -(20 * math.cos(self.angle))

  
  
  def update(self):
    ''' Makes the bullet move

    Args:
      self: the instance of the bullet that uses this function

    Returns:
      bullet moves +self.speedy and +self.speedx
    '''
    self.rect.move_ip(self.speedx, self.speedy)

    # If bullet if off screen
    if self.rect.x < -self.sizex or self.rect.x > WIDTH or self.rect.y < -self.sizey or self.rect.y > HEIGHT:
      self.kill()

  def collisions(self):
     ''' Checks for collisions between bullet and asteroid

    Args:
      self: the instance of the bullet that uses this function

    Returns:
      kills instance of bullet if collision is True
    '''
     if pygame.sprite.spritecollide(self, Asteroids.AsteroidGroup, True):
       self.kill()

    
  


# Powerups Class
class Powerups(spriteclass):


  # Last tick since last powerup spawn (every 5 seconds)
  lasttick = 0

  # Power Up list of instances
  PowerupGroup = pygame.sprite.Group()
  
  def SpeedBoost(player):
    ''' Speedboost for player

    Args:
      player: the instance of the player that collects this powerup

    Returns:
      playerspeed increases by x 1.2
    '''
    if player.speed < 8:
      player.speed = player.speed * 1.2

  def FirerateBoost(player):
    ''' Boosts fire rate for player

    Args:
      player: the instance of the player that collects this powerup

    Returns:
      firerate increases by 30 percent (time between each shot reduced by 30 percent)
    '''
    player.firerate = player.firerate * 0.7

  def Heal(player):
    ''' Extra Health for player

    Args:
      player: the instance of the player that collects this powerup

    Returns:
      Increases player health by +3
    '''
    player.health += 3

  
  # Dictionary for powerups
  Powers = {
    "SpeedBoost" : SpeedBoost,
    "Heal" : Heal,
    "FirerateBoost" : FirerateBoost
  }

  # Dictionary for Images
  Images = {
    "SpeedBoost" : drawings.LoadImage("speed.png"),
    "Heal" : drawings.LoadImage("heal.png"),
    "FirerateBoost" : drawings.LoadImage("firerate.png")
  }

  # Initialization
  def __init__(self):

    # Gives object attributes of superclass
    spriteclass.__init__(self)

    # Adds instance to list
    self.PowerupGroup.add(self)
  
    # Selects which power randomly
    self.power = random.choice(["SpeedBoost", "FirerateBoost", "Heal"])
    self.effect = self.Powers[self.power]

    # Other attributes: size, image, rect, x and y
    self.size = 30
    self.image = drawings.Resize(self.Images[self.power], self.size, self.size)
    self.rect = self.image.get_rect()
    self.x = random.randint(50, WIDTH - self.size - 50)
    self.y = random.randint(50, HEIGHT - self.size - 50)

    self.rect.topright = (self.x, self.y)


def gameover():
  ''' Gameover screen when a player dies
  
  Args:
    None
    
  Returns:
    Ends program or goes back to menu (depending on user)
  
  
  '''
  # Variables for mainloop
  running = True
  clock = pygame.time.Clock()


  # Gameover text
  gameover1_text = titlefont.render('GAME OVER', True, WHITE)
  # runs updatescore to update the scoreboard file, and to return the amount of wins the winner has.
  gameover2_text = subfont.render('Winner: ' + winner +  " (" + updatescore() + " wins)", True, WHITE)


  gameover1_textRect = gameover1_text.get_rect()
  gameover1_textRect.center = (WIDTH // 2, 100)

  gameover2_textRect = gameover2_text.get_rect()
  gameover2_textRect.center = (WIDTH // 2, 250)

  # Play and end buttons
  play = Button(WHITE, 475, 400, 250, 100, 'Menu')
  end = Button(WHITE, 475, 600, 250, 100, 'Quit')

  # Mainloop
  while running:
    clock.tick(FPS) # FPS
    screen.fill(BLACK) # Fills screen

    screen.blit(gameover1_text, gameover1_textRect) 
    screen.blit(gameover2_text, gameover2_textRect) 


    # Draws buttons
    end.draw()
    play.draw()

    # Gets mouse position
    mouse_position = pygame.mouse.get_pos()

    for event in pygame.event.get():
      mouse_click = (event.type == pygame.MOUSEBUTTONUP)
      
      # If player clicks on Quit button
      if end.mouse_pos(mouse_position) and mouse_click:
        pygame.quit()

      # If player clicks on 
      if play.mouse_pos(mouse_position) and mouse_click:
        running = False

    pygame.display.update() # Update
    


def playerinstructions():
  ''' Player Instructions when player
  asks for instructions

  Args:
    None

  Returns:
    Menu for instructions, 
    Returns back to menu when quit is pressed
  
  
  '''
  # Variables for mainloop
  running = True
  clock = pygame.time.Clock()

  # Intructions text (Literallt a wall of text it's pygame's fault not mine - Smai)
  instructions1_text = subfont.render('Player 1: WASD to move, Q to shoot', True, WHITE)
  instructions2_text = subfont.render('Player 2: Arrow keys to move, M to shoot', True, WHITE)
  instructions3_text = subfont.render('Dodge the asteroids, collect powerups and shoot each other', True, WHITE)
  health_text = subfont.render('= health packs', True, WHITE)
  ammo_text = subfont.render('= ammo packs', True, WHITE)
  boots_text = subfont.render('= speed boost', True, WHITE)

  instructions1_textRect = instructions1_text.get_rect()
  instructions1_textRect.center = (WIDTH // 2, 100)

  instructions2_textRect = instructions2_text.get_rect()
  instructions2_textRect.center = (WIDTH // 2, 200)

  instructions3_textRect = instructions3_text.get_rect()
  instructions3_textRect.center = (WIDTH // 2, 300)

  health_textRect = health_text.get_rect()
  health_textRect.center = (250, 425)

  ammo_textRect = ammo_text.get_rect()
  ammo_textRect.center = (650, 425)

  boots_textRect = boots_text.get_rect()
  boots_textRect.center = (1000, 425)
  
  health = drawings.Resize(drawings.LoadImage("heal.png"), 60, 60)
  ammo = drawings.Resize(drawings.LoadImage('firerate.png'), 60, 60)
  boots = drawings.Resize(drawings.LoadImage('speed.png'), 60, 60)

  
  # Button for menu
  end = Button(WHITE, 475, 500, 250, 100, 'Menu')

  # Mainloop
  while running:
    clock.tick(FPS) # FPS
    
    # Draws all the text
    screen.fill((0,0,0))

    screen.blit(instructions1_text, instructions1_textRect) 
    screen.blit(instructions2_text, instructions2_textRect) 
    screen.blit(instructions3_text, instructions3_textRect) 


    drawings.DrawImage(screen ,health, 50, 400)
    drawings.DrawImage(screen, ammo, WIDTH/2- 150, 400)
    drawings.DrawImage(screen, boots, 800, 400)

    screen.blit(health_text, health_textRect) 
    screen.blit(ammo_text, ammo_textRect) 
    screen.blit(boots_text, boots_textRect) 

    end.draw()# Draws button

    # Gets mouse position
    mouse_position = pygame.mouse.get_pos()

    # Checks events
    for event in pygame.event.get():

      # if window closes
      if event.type == pygame.QUIT:
        pygame.quit()

      # Checks if mouse is clicked
      mouse_click = (event.type == pygame.MOUSEBUTTONUP)
      
      # If menu button is clicked, goes back to menu
      if end.mouse_pos(mouse_position) and mouse_click:
        running = False
        
    pygame.display.update() # Update



def draw_menu(play, instructions, end):
  ''' Draws starting menu for program
  
  Args:
    play, instructions, end:
    Instances of button class, draws them after the screen is filled

  Returns: 
    Fills screen black, and draws play, instruction and quit buttons
  '''


  screen.fill((0,0,0))
  screen.blit(mainmenu_text, mainmenu_textRect)
  play.draw()
  instructions.draw()
  end.draw()



def menu():
  ''' Starting menu for the game
  
  Args:
    None

  Returns:
    Menu: 
      Play button that starts game
      Instructions button that gives instructions

  
  '''
  # Variables for mainloop
  running = True
  clock = pygame.time.Clock()

  # Play, Instructions, and Quit Button
  play = Button(WHITE, 475, 200, 250, 100, 'Play')
  instructions = Button(WHITE, 475, 400, 250, 100, 'Instructions')
  end = Button(WHITE, 475, 600, 250, 100, 'Quit')

  # Mainloop
  while running:
        
    # Draws menu
    draw_menu(play, instructions, end)
    clock.tick(FPS) # FPS

    # Gets mouse position
    mouse_position = pygame.mouse.get_pos()


    # Checks events
    for event in pygame.event.get():
      
      # If mouse is left clicked
      mouse_click = (event.type == pygame.MOUSEBUTTONUP)
      
    
      # if window closes
      if event.type == pygame.QUIT:
        running = False

    
      # If player clicks on play button
      if play.mouse_pos(mouse_position) and mouse_click:
        main() # Main game

        # Kills all instances of objects in class groups 
        for plr in Players.PlayerGroup:
          plr.kill()
          
        for i in Asteroids.AsteroidGroup:
          i.kill()

        for i in Powerups.PowerupGroup:
          i.kill()

        for i in Bullets.BulletGroup:
          i.kill()

        gameover() # Gameover screen



      # If player clicks on instructions button
      if instructions.mouse_pos(mouse_position) and mouse_click:
        playerinstructions()


      # If player clicks on quit button
      if end.mouse_pos(mouse_position) and mouse_click:
        running = False # End


    pygame.display.update()


# Updates Display
def main():
  ''' Main program: The game itself

  Args:
    None
  
  Returns:
    None: Just runs the game
  '''
  # Global variables
  global winner

  winner = None

# Players
  player1 = Players(200, 200, drawings.shipimg1) 
  player2 = Players(WIDTH - 200, HEIGHT - 200, drawings.shipimg2)
  
  # While loop for game
  while True:

    # Checks events 
    for event in pygame.event.get():
   
    # Ends program
      if event.type == pygame.QUIT:
        pygame.quit()

  
    # If player 1 health less than 0
    if player1.health <= 0:
      winner = "Player 2"
      break
    
    # If player 2 health less than 0
    elif player2.health <= 0:
      winner = "Player 1"
      break
    

    # Draws background
    drawings.DrawImage(screen, background , 0,0)

    ## Player 1 and 2 movement

    # Checks for key input
    key = pygame.key.get_pressed()

      
    # WHen player one presses W (moves up)
    if key[pygame.K_w]:
      player1.moveForward()
    
    
    # When player one presses A (turns left)
    if key[pygame.K_a]:
      player1.moveLeft()

    
    # When player one presses S (moves back)
    if key[pygame.K_s]:
      player1.moveBack()
        

    # When player one presses D (turns right)
    if key[pygame.K_d]:
      player1.moveRight()


    # When player 1 presses UP Arrow Key (Turns UP)
    if key[pygame.K_UP]:
      player2.moveForward()

      
    # When player 1 presses Down Arrow Key (Turns Down)
    if key[pygame.K_DOWN]:
      player2.moveBack()

      
    # When player 1 presses Left Arrow Key (Turns Left)
    if key[pygame.K_LEFT]:
      player2.moveLeft()


    # When player 1 presses Right Arrow Key (Turns right)
    if key[pygame.K_RIGHT]:
      player2.moveRight()
    

    # When player 1 presses Q (shoots bullet)
    if key[pygame.K_q] and pygame.time.get_ticks() - Players.player1lasttick > player1.firerate:
      Players.player1lasttick = pygame.time.get_ticks()
      Bullets(player1)
    
      
    # When player 2 presses M (shoots bullet)
    if key[pygame.K_m] and pygame.time.get_ticks() - Players.player2lasttick > player2.firerate:
      Players.player2lasttick = pygame.time.get_ticks()
      Bullets(player2)
      
    
    # updating positions for next frame
    Asteroids.AsteroidGroup.update()
    Bullets.BulletGroup.update()

    
    # spawns an asteroid every 0.5 seconds
    if pygame.time.get_ticks() - Asteroids.lasttick > 500:
      Asteroids.lasttick = pygame.time.get_ticks()
      Asteroids()


    # spawns a powerup every 5 seconds
    if pygame.time.get_ticks() - Powerups.lasttick > 5000:
      Powerups.lasttick = pygame.time.get_ticks()
      Powerups()

      
    # handles collisions
    for plr in Players.PlayerGroup:
      plr.collisions()
    for bul in Bullets.BulletGroup:
      bul.collisions()
    

    # Draw next frame
    Players.PlayerGroup.draw(screen)
    Asteroids.AsteroidGroup.draw(screen)
    Powerups.PowerupGroup.draw(screen)
    Bullets.BulletGroup.draw(screen)

      
    # Sets up text for player 1 and 2 health (another wall of text)
    p1_text = subfont.render('Player 1 Health: ' + str(player1.health), True, WHITE)
    p1_textRect = p1_text.get_rect()
    p1_textRect.center = (200, 50)

    p2_text = subfont.render('Player 2 Health: ' + str(player2.health), True, WHITE)
    p2_textRect = p2_text.get_rect()
    p2_textRect.center = (WIDTH - 200, 50)

    
    # Displays player1 and player2 health
    screen.blit(p1_text, p1_textRect)

    screen.blit(p2_text, p2_textRect)
              
    
    # Updates Screen
    pygame.time.Clock().tick(FPS)
    Display.update()
    

# Main code
menu()