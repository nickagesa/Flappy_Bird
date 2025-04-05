'''building the bird using pygame sprite classes'''
# This code will focus on creating a Bird class using pygame sprite classes.
# This will allow us to manage the bird sprite more efficiently and add animations later on.
# The Bird class will inherit from pygame.sprite.Sprite, allowing us to utilize sprite functionalities such as draw, update, and group management.
import pygame
import os 

# initialize pygame
pygame.init()
   
# window width and height
screen_width = 400
screen_height = 600

# screen & title
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# load images
background = pygame.image.load(os.path.join('img','bg.png')) 
ground = pygame.image.load(os.path.join('img','ground.png')) 

# transform the images 
background = pygame.transform.scale(background, (400, 500)) 
ground = pygame.transform.scale(ground, (415, 100)) 

# ground scrolling variables
scroll = 0 
ground_speed = 4 

# frame per second (FPS) and clock
FPS = 60 
clock = pygame.time.Clock() 

'''Define the Bird class using pygame sprite'''
# The Bird class will inherit from pygame.sprite.Sprite to utilize sprite functionalities. (i.e Bird is a child of the Sprite class, this allows us to use built-in methods for updating and drawing the sprite)
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y): # initialize class and set initial position (x,y) of the bird
        #pygame.sprite.Sprite.__init__(self) # initialize the sprite class (it has in-built update & draw methods making it easy to manage)
        super().__init__() # use this (instead of pygame.sprite.Sprite.__init__(self)) to initialize sprite class it's a more modern way to initialize the parent class, 
        # attributes with images & rect for the bird sprite
        self.image = pygame.image.load(os.path.join('img', 'bird1.png'))
        self.image = pygame.transform.scale(self.image, (34, 24)) # scale the image to fit the bird size
        self.rect = self.image.get_rect() # get the rectangle of the image for collision detection and positioning
        self.rect.center = (x, y) # set the initial position of the bird using the x and y coordinates passed to the constructor

'''Bird group instance to manage all bird sprites'''
bird_group = pygame.sprite.Group() # create a sprite group for the bird to manage multiple birds if needed
# a group is like a list of sprites that allows us to manage and update multiple sprites at once, it provides a way to group sprites together for easier management and drawing.

# instance of the Bird class
flappy = Bird(50, (screen_height // 2)) # create an instance of the Bird class, set initial position of the bird at x=50 and y=300 (middle of the screen height)
bird_group.add(flappy) # add the bird instance to the sprite group, this allows us to manage and update the bird easily
# SIDENOTE: if bird group was a list you would say .append(flappy)

is_running = True
while is_running:

    # control the frame rate
    clock.tick(FPS) 

    # draw background
    screen.blit(background, (0, 0)) 

    '''Draw Bird'''
    # draw the bird using the sprite group, this will automatically call the draw method for each sprite in the group
    bird_group.draw(screen) 
    #SIDENOTE: if you din't use a sprite group & class you would have to manually draw the bird using `screen.blit(flappy.image, flappy.rect)` which is not efficient for multiple sprites. 
    
    # draw and scroll the ground to left
    screen.blit(ground, (scroll, 500)) 
    scroll -= ground_speed 
    if abs(scroll) > 15:
        scroll = 0 # reset the scroll

    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # update the display
    pygame.display.update()

pygame.quit()