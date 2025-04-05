'''Creating bird animation'''
# We will create a bird animation by loading multiple images of the bird and cycling through them to create a flapping effect. 
# This will be done by creating a list of images and updating the image of the bird sprite in each frame based on a counter. 

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

# Bird class child of pygame sprite
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y): 
        #pygame.sprite.Sprite.__init__(self) # initialize the sprite class (it has in-built update & draw methods making it easy to manage)
        super().__init__() # use this instead of line above.
        # instance attributes #
        '''Bird Animation'''
        self.animation_list = [] # list to hold bird images for animation
        self.index = 0 # index for animation list
        self.counter = 0 # counter for counting frames for animation speed

        # load images for animation
        for i in range(1, 4): # start at 1 and end at 4 (exclude 4) to load bird1.png, bird2.png, bird3.png
            # load each image in the img folder and append to the animation list
            img = pygame.image.load(os.path.join('img', f'bird{i}.png')) # load the image from the img folder, f-string to get the number of the image
            img = pygame.transform.scale(img, (34, 24)) # scale the image to the desired size (width, height)
            self.animation_list.append(img)

        # set the initial image for the bird sprite
        self.image = self.animation_list[self.index] # set the initial image to the first image in the animation list
        self.rect = self.image.get_rect() # for collision detection and positioning
        self.rect.center = (x, y) # initial position of the bird (x, y) coordinates
        # Note on self.rect: this creates a rectangle around the image which is used for collision detection and positioning of the sprite (bird) on the screen.

    '''Overide the update method from pygame.sprite.Sprite to create our own update method for animation'''
    def update(self):
        # update the bird animation
        self.counter += 1 # increment the counter by 1 on each update call to track the number of frames passed
        flap_speed = 5 # flap speed (lower number = faster animation)
        '''Note: The counter increases every frame, and we only change the animation frame when it reaches flap_speed.(i.e 5 frames in this case)'''
        # check if counter has reached the flap speed (to control animation speed)
        if self.counter >= flap_speed: # if counter reaches flap speed, change the image
            self.counter = 0 # reset the counter to start the next animation frame
            self.index += 1 # move to the next image in the animation list
            # if index exceeds the length of the animation list, reset it to 0
            if self.index >= len(self.animation_list): # if index is >= 2 (ie, length of the animation list) 
                self.index = 0 # reset the index to 0 to loop back to the first image in the animation list
            # set the image to the current index in the animation list
            self.image = self.animation_list[self.index]
        

# bird group instance to manage all bird sprites
bird_group = pygame.sprite.Group() 

# instance of the Bird class
flappy = Bird(50, (screen_height // 2)) 
bird_group.add(flappy) 

is_running = True
while is_running:

    # control the frame rate
    clock.tick(FPS) 

    # draw background
    screen.blit(background, (0, 0)) 

    # draw the bird using the sprite group
    bird_group.draw(screen) 

    '''Update the bird animation'''
    bird_group.update() # this will call the update method of all sprites in the group (in this case, just the flappy bird instance)
   
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