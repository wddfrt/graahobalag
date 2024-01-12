# File: draw.py
# Name: Evan Bai, Sami Ahmed
# Date: Jan 08th 2024
# Class: ICS4UI
# Asteroid Game culminating assignment

import pygame
import main

# Uploading Images 
# Ship for Player 1
shipimg1 = pygame.image.load('mcqueen.png')
shipimg1 = pygame.transform.scale(shipimg1, (main.PLAYERSIZE, main.PLAYERSIZE))

## Ship for Player 2
shipimg2 = pygame.image.load('download.png')
shipimg2 = pygame.transform.scale(shipimg2, (main.PLAYERSIZE, main.PLAYERSIZE))

# Asteroid Image
asteroidimg = pygame.image.load('woman.png')

# Background image
bgimg = pygame.image.load('bg.jpg')
bgimg = pygame.transform.scale(bgimg, (main.WIDTH, main.HEIGHT))

Images = {
    "Player1" : shipimg1,
    "Player2" : shipimg2,
    "Asteroid" : asteroidimg,
    "BG1" : bgimg,
}


def DrawImage(display, image, x, y):
    display.blit(Images[image], (x,y))




def DrawShape():
    pass

if __name__ == '__main__':
    pass