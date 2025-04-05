'''Background Scrolling'''
# I changed my mind on how I wanted the ground to scroll I also wanted to add a scrolling background. 
# So I decided to create a function called scroll_image to handle both background & ground scrolling.
# If you want to understand the concept of how it works check the original code in scroll_concept.py.
# I also increased the size of the game window and moved the bird 100px on x axis.
import pygame
import os 

# initialize pygame
pygame.init()
   
# window width and height
screen_width = 600
screen_height = 600

# screen & title
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# load images
background = pygame.image.load(os.path.join('img','bg.png')) 
ground = pygame.image.load(os.path.join('img','ground.png')) 

# scrolling variables
#ground
ground_scroll = 0 
ground_speed = 4 
ground_width = ground.get_width()  # Get the width of the ground image for scrolling
#backgroung
bg_scroll = 0 # this is for the background scrolling, we will use this to move the background image to create a scrolling effect.
background_speed = 0.5  # speed at which the background scrolls
background_width = background.get_width()  # Get the width of the background image for scrolling

# transform the images 
background = pygame.transform.scale(background, (background_width, 500)) 
ground = pygame.transform.scale(ground, (ground_width, 100)) 
# Note: the backgound image width is 864 px we got this number from background.get_width() which returns the width of the image.
# background.get_height() would give you image height.

# frame per second (FPS) and clock
FPS = 60 
clock = pygame.time.Clock() 

# Bird class child of pygame sprite
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y): 
        #pygame.sprite.Sprite.__init__(self) # initialize the sprite class (it has in-built update & draw methods making it easy to manage)
        super().__init__() # use this instead of line above.
        # Bird Animation
        self.animation_list = [] # list to hold bird images for animation
        self.index = 0 # index for animation list
        self.counter = 0 # counter for animation speed

        # load images for animation
        for i in range(1, 4): 
            # load each bird images and append to the animation list
            img = pygame.image.load(os.path.join('img', f'bird{i}.png')) # load the image from the img folder, f-string to get the number of the image
            img = pygame.transform.scale(img, (34, 24)) # scale the image to the desired size (width, height)
            self.animation_list.append(img)

        self.image = self.animation_list[self.index]
        self.rect = self.image.get_rect() 
        self.rect.center = (x, y) 

    # overide the update method from pygame.sprite.Sprite to create our own update method for animation
    def update(self):
        # update the bird animation
        self.counter += 1
        flap_speed = 5 # flap speed (lower number = faster animation)
        
        # check if counter has reached the flap speed (to control animation speed)
        if self.counter >= flap_speed: # if counter reaches flap speed, change the image
            self.counter = 0 # reset the counter to start the next animation frame
            self.index += 1 # move to the next image in the animation list
            # if index exceeds the length of the animation list, reset it to 0
            if self.index >= len(self.animation_list): 
                self.index = 0 # reset index
            # set the image to the current index in the animation list
            self.image = self.animation_list[self.index]

# bird group instance to manage all bird sprites
bird_group = pygame.sprite.Group() 

'''Change in Bird x position'''
flappy = Bird(100, (screen_height // 2)) #instance of the Bird class
bird_group.add(flappy) 

'''Function to scroll both background and ground'''
def scroll_image(image, scroll, speed, y_position, width):
    # Draws and updates the scrolling position of an image.
    screen.blit(image, (scroll, y_position))  
    screen.blit(image, (scroll + width, y_position))  # Draw the second instance to create a seamless effect
    
    # Move image left
    scroll -= speed  # Decrease the scroll value to move the image left

    # Reset scroll when the entire image moves off-screen
    if abs(scroll) >= width:
        scroll = 0  

    return scroll  # Return the updated scroll value

is_running = True
while is_running:

    # control the frame rate
    clock.tick(FPS) 

    '''Scroll background and ground'''
    bg_scroll = scroll_image(background, bg_scroll, background_speed, 0, background_width)
    ground_scroll = scroll_image(ground, ground_scroll, ground_speed, 500, ground_width)
    
    # draw the bird using the sprite group
    bird_group.draw(screen) 

    # update the bird animation
    bird_group.update() # this will call the update method of all sprites in the group (in this case, just the flappy bird instance)
    
    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # update the display
    pygame.display.update()

pygame.quit()
