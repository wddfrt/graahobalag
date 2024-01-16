# File: draw.py
# Name: Evan Bai, Sami Ahmed
# Date: Jan 08th 2024
# Class: ICS4UI
# Asteroid Game culminating assignment

import pygame

def bruh():
    print("ok")

def Resize(img, x, y):
    pygame.transform.scale(img, (x, y))


def DrawImage(screen, image, x, y):
    screen.blit(image, (x,y))


def DrawShape():
    pass
