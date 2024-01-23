# File: draw.py
# Name: Evan Bai, Sami Ahmed
# Date: Jan 08th 2024
# Class: ICS4UI
# Asteroid Game culminating assignment

import pygame


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def bruh():
    print("ok")

def LoadImage(path):
    return pygame.image.load(path)

def Resize(img, x, y):
    return pygame.transform.scale(img, (x, y))


def DrawImage(screen, image, x, y):
    screen.blit(image, (x,y))


def DrawShape():
    pass

# Images 


# Ship for Player 1
shipimg1 = LoadImage("ship1.png")
## Ship for Player 2
shipimg2 = LoadImage("ship2.png")
# Background image
bgimg1 = pygame.image.load('bg.png')