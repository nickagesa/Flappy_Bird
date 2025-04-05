'''Flappy Bird Game using Pygame'''
# This is lesson 1, we will focus on: 
# 1. Setting up the game window
# 2. Implementing a basic game loop and handling QUIT event
# 3. Loading and displaying the background and ground images
# 4. FPS (Frames Per Second) to control the speed of the game loop
# 5. Scrolling the ground to create an effect of movement (I will change this in a later lesson to make it more efficient)

'''Import necessary libraries'''
import pygame
import os # os is used to join the path of the images, so that it can be loaded properly on any operating system

# initialize pygame
pygame.init()

# set the width and height of the window
screen_width = 400
screen_height = 600

'''Game window and caption '''
screen = pygame.display.set_mode((screen_width, screen_height)) # screen object is created with the width and height of the window, this will create a window of 400x600 pixels for the game.
pygame.display.set_caption('Flappy Bird')

'''Load the images'''
background = pygame.image.load(os.path.join('img','bg.png')) # background image
ground = pygame.image.load(os.path.join('img','ground.png')) # ground image

'''transform the images to fit the screen'''
background = pygame.transform.scale(background, (400, 500)) # background image
ground = pygame.transform.scale(ground, (415, 100)) # ground image

# Note: background image height is 500 px meaning it leaves 100 px of space for the ground to be drawn below it, thus the ground image height is 100 pixels.
# The ground image is width 415 pixels while game window is 400.
# This means that the ground image will overflow by 15 pixels on the right side, this is done to create a seamless scrolling effect.
# The ground image will scroll to the left and when it reaches -15 pixels it will reset to 0, this creates the effect of infinite scrolling of the ground.

# define game variables
scroll = 0 # ground scroll speed
ground_speed = 4 # ground speed

'''set the frames per second (FPS) for the game loop'''
FPS = 60 # frames per second
clock = pygame.time.Clock() # clock object to control the frame rate of the game loop
# The clock object will be used to control the frame rate of the game loop, this will ensure that the game runs at a consistent speed across different hardware.

is_running = True # this variable will be used to control the game loop, it will be set to False when the user closes the window, thus ending the game loop.
while is_running:

    '''frame rate control'''
    clock.tick(FPS) # pass the FPS value to the clock.tick() method to control the frame rate of the game loop, this will ensure that the game runs at 60 frames per second.

    '''draw background'''
    screen.blit(background, (0, 0)) # blit() method is used to draw the image on the screen
    
    '''draw and scroll the ground'''
    screen.blit(ground, (scroll, 500)) # blit() is used to draw the image on the screen
    scroll -= ground_speed # scroll the ground to the left (0-4 = -4)
    if abs(scroll) > 15: # abs() is used to get the absolute value of the ground scroll,(ie. drops the negative(-) from the value 4) 
        scroll = 0 # reset the scroll
        # 15 is the overflow width value for the ground image, when it reaches 15 it will reset to 0, so that it can scroll again, this is used to create the effect of infinite scrolling of the ground
        # instead of abs() you can also use if scroll < -15: # this will also work.
    
    '''Handle quit event'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    '''update the display'''
    pygame.display.update() # update the display to show the changes made in the game loop, this will refresh the screen and show the new position of the images, this is important to keep the game loop running and showing the updated images on the screen.
# Note: this should be called at the end of the game loop to ensure that all the changes made in the loop are displayed on the screen.
pygame.quit()