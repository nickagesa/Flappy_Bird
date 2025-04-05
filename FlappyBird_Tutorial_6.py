'''New Features Added:'''
# Adding pipes
# **pipe_gap**: This variable determines the gap between the top and bottom pipes. You can adjust this to make it easier or harder for the player to navigate through the pipes.
# **Pipe class**: This class handles the creation and positioning of pipes. It loads the pipe image, scales it, and positions it based on whether it's a top or bottom pipe. The pipes are added to a sprite group for easy management.
# I also added sys to exit the game when the user clicks close button. 
# (pygame.quit() will not exit the game, it will just stop the game loop and close the window.)
# This is only seen when you compile the code to exe.
import pygame
import os 
import sys # 6. import sys to exit the game when the user clicks the close button

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

# bool variables
is_flying = False # Used to check if the game has started and also gravity is applied to the bird. When `is_flying` is `False`, the bird will not fall due to gravity and will remain in its initial position. This allows us to control when the bird starts to fall and when it can jump.
game_over = False # Used to check if the game is over or not. We can use this to reset the game or end it when the bird collides with an obstacle or goes off-screen.

'''1. Add New Variable'''
pipe_gap = 100 # gap between the top and bottom pipes (in pixels) - this will determine how much space the bird has to fly through between the pipes. You can adjust this value to make it easier or harder for the player to navigate through the pipes.

# transform the images 
background = pygame.transform.scale(background, (background_width, 500)) 
ground = pygame.transform.scale(ground, (ground_width, 100)) 

# frame per second (FPS) and clock
FPS = 60 
clock = pygame.time.Clock() 

# Bird class child of pygame sprite
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y): 
        super().__init__() # initialize the sprite class
        # Bird Animation
        self.animation_list = [] # list to hold bird images for animation
        self.index = 0 # index for animation list
        self.counter = 0 # counter for counting frames for animation speed

        # load images for animation
        for i in range(1, 4): 
            # load each bird images and append to the animation list
            img = pygame.image.load(os.path.join('img', f'bird{i}.png')) # load the image from the img folder, f-string to get the number of the image
            img = pygame.transform.scale(img, (34, 24)) # scale the image to the desired size (width, height)
            self.animation_list.append(img)

        self.image = self.animation_list[self.index]
        self.rect = self.image.get_rect() 
        self.rect.center = (x, y) # rectangle that wraps around the image, used for collision detection, positioning and movement of the sprite (bird).
        self.gravity = 0 # initial gravity for the bird (this will control the falling speed of the bird)
        self.clicked = False # this will be used to only ensure one jump per click (to avoid multiple jumps when the mouse is clicked multiple times ie. holding down the mouse button)

    # overide the update method from pygame.sprite.Sprite to create our own update method for animation
    def update(self):
        #Apply gravity to the bird
        if is_flying == True: # only apply gravity when the game has started (when is_flying is True)
            self.gravity += 0.5 # increase gravity to simulate falling (higher number = faster fall)
            if self.gravity > 6: # limit the gravity to a max value (to avoid the value of y to keep increasing indefinitely)
                self.gravity = 6 # cap the gravity at 6 to avoid too fast falling, you can adjust this value to make it more realistic or challenging
            if self.rect.bottom < screen_height - 100: # check if the bird is within the screen height (100 px from the bottom to avoid going off-screen)
                self.rect.y += int(self.gravity) # update the y position of the bird based on gravity
            # if the bird is within the screen height, apply gravity to the bird's y position
            # this will make the bird fall down when it is not jumping

        if game_over == False: # only update the bird's position if the game is not over (to avoid updating the position when the game is over)
            # Applying Jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # check if left mouse button is pressed (bird jump) & clicked is False 
                self.clicked = True # set clicked to True to avoid multiple jumps (only allow one jump per click)
                self.gravity = -6 # set the gravity to a negative value to make the bird jump (higher number = higher jump)``
            if pygame.mouse.get_pressed()[0] == 0: # mouse button released (bird stop jumping)
                self.clicked = False # set clicked to False to allow for another jump when the mouse is clicked again

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

                # Rotate the Bird
            self.image = pygame.transform.rotate(self.animation_list[self.index], (-self.gravity * 3)) # rotate the bird image based on the gravity (higher gravity = more rotation) # -self.gravity * 3 to rotate the bird based on the gravity (higher gravity = more rotation) # negative value to rotate in the opposite direction of falling (to simulate a flapping motion)  
        else:
            # If the game is over, keep the bird static and do not update the animation or position, rotate the bird
            self.image = pygame.transform.rotate(self.animation_list[self.index], -90) # Rotate the bird to a fixed angle (e.g., -90 degrees) to indicate game over, you can adjust this value to make it more realistic or challenging

'''2. New Pipe class for Adding Pipes'''
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y,position): 
        super().__init__() # initialize the sprite class
        # 2.1. Load pipe image 
        self.image = pygame.image.load(os.path.join('img', 'pipe.png'))
        self.image = pygame.transform.scale(self.image, (52, 320)) # scale the pipe image to the desired size (width, height) # 52 is the width and 320 is the height of the pipe image (you can adjust these values based on your pipe image size)
        
        # 2.2. Create a rect around pipe image
        self.rect = self.image.get_rect() # get the rectangle of the image 
        
        # 2.3. Set the pipe position
        if position == "top": # (flip pipe upside down)
            self.image = pygame.transform.flip(self.image, False, True) # false = no flip on x-axis, True = flip on y-axis (this will flip the pipe image upside down)
            self.rect.bottomleft = (x, y - (pipe_gap // 2)) # set the bottom left corner of the pipe to the x and y coordinates passed to the constructor (this will position the pipe at the top of the screen)
        elif position == "bottom": # (bottom pipe)
            self.rect.topleft = (x, y + (pipe_gap // 2)) # set the position of the pipe (top left corner) based on the x and y coordinates passed to the constructor
    
    # 2.4. scrolling pipes
    def update(self):
        if game_over == False: # only update the pipe position if the game is not over (to avoid updating the position when the game is over)
            self.rect.x -= ground_speed # Move the pipe left to create a scrolling effect
        
'''3. Create a Pipe Group '''
bird_group = pygame.sprite.Group() 
pipe_group = pygame.sprite.Group() # create a group for pipes to manage multiple pipe instances

# instance of the Bird class
flappy = Bird(100, (screen_height // 2)) 
bird_group.add(flappy) 

'''4. create an instance of Pipe class'''
bottom_pipe = Pipe(screen_width, (screen_height // 2),"bottom") # create a bottom pipe instance (positioned at the bottom of the screen with some offset)
top_pipe = Pipe(screen_width, (screen_height // 2), "top") # create a top pipe instance (positioned above the screen with some offset)

# 4.1 add the pipes to the pipe group
pipe_group.add(bottom_pipe) # add the bottom pipe to the pipe group
pipe_group.add(top_pipe) # add the top pipe to the pipe group
       
# Function to scroll both background and ground
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


# Main game loop
is_running = True
while is_running:

    # control the frame rate
    clock.tick(FPS) 

    # Stop scrolling background and ground if game is over
    if game_over == False:
        bg_scroll = scroll_image(background, bg_scroll, background_speed, 0, background_width)
        '''5. Draw Pipes: place them in btwn BG and Ground'''
        pipe_group.draw(screen) 
        pipe_group.update()
        ground_scroll = scroll_image(ground, ground_scroll, ground_speed, 500, ground_width)

    # draw the bird & update animation
    bird_group.draw(screen) 
    bird_group.update() # this will call the update method of all sprites in the group (in this case, just the flappy bird instance)
    
    '''Collision detection'''
    # Check if bird flys off the screen (top)
    if flappy.rect.top <= 0: # check if the bird has gone off the top of the screen
        game_over = True # set game_over to True
        
    # check if the bird has hit the ground
    if flappy.rect.bottom >= screen_height - 100: # (100 px from the bottom of the screen)
        game_over = True # set game_over to True 
        flying = False # stop flying

    # Quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Start the game
        if event.type == pygame.MOUSEBUTTONDOWN and not is_flying and not game_over: # check if the mouse is clicked and the game has not started yet (is_flying is False) and game is not over (game_over is False)
            is_flying = True # set is_flying to True when the mouse is clicked to start the game (this can be used to control game state)

    # update the display
    pygame.display.update()

pygame.quit()
sys.exit() # 6. ensures game exits properly when the user clicks the close button.
