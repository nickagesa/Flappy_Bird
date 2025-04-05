'''Adding score & Restart Button'''
# We need away to monitor where the bird is in relation to the pipe. (check image for reference)
# this is done by a trigger variable that will be set to True when the bird passes the orange line
# when the bird passes the green line, we will add 1 to the score and trigger will be set to False again
# Print score on the screen (pygame doesn't have a built-in way to display text, you have to convert text to image then blit it on the screen 
# so we will use the font module to create a font object and render the text to the screen)
# 1st We will need to create a function to display the score on the screen
# Restart button - we will create a restart button that will reset the game when clicked. 
   # Begin by loading the restart button image and scaling it to the desired size (width, height)
   

import pygame
import os 
import random # import random to generate random positions for the pipes
import sys 
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
restart_button = pygame.image.load(os.path.join('img','restart.png')) # load the restart button image


# variable declaration
ground_scroll = 0 
ground_speed = 4 
ground_width = ground.get_width()  # Get the width of the ground image for scrolling
bg_scroll = 0 # this is for the background scrolling, we will use this to move the background image to create a scrolling effect.
background_speed = 0.5  # speed at which the background scrolls
background_width = background.get_width()  # Get the width of the background image for scrolling
flying = False # Used to check if the game has started and also gravity is applied to the bird. When `flying` is `False`, the bird will not fall due to gravity and will remain in its initial position. This allows us to control when the bird starts to fall and when it can jump.
game_over = False # Used to check if the game is over or not. We can use this to reset the game or end it when the bird collides with an obstacle or goes off-screen.
pipe_gap = 100 # gap between the top and bottom pipes (in pixels) - this will determine how much space the bird has to fly through between the pipes. You can adjust this value to make it easier or harder for the player to navigate through the pipes.
pipe_frequency = 1500 # time in milliseconds (ms) to wait before spawning a new pipe (1500 ms = 1.5 seconds) - this will control how often new pipes are spawned and how quickly they scroll across the screen. You can adjust this value to make the game more challenging or easier for the player.
last_pipe = pygame.time.get_ticks() # get the current time in milliseconds since pygame was initialized. This will be used to track when the last pipe was spawned so we can spawn a new one after the specified frequency.

'''1. new variables'''
trigger = False # this will be used to check if the bird has passed the pipe (to add score)
score = 0 # this will be used to keep track of the score (number of pipes passed)
font = pygame.font.SysFont('Bauhaus 93', 40) # create a font object with the specified font name and size (font size = 30)
white = (255, 255, 255) # color of the text (white)

# transform the images 
background = pygame.transform.scale(background, (background_width, 500)) 
ground = pygame.transform.scale(ground, (ground_width, 100)) 
restart_button = pygame.transform.scale(restart_button, (100, 50)) # scale the restart button image to the desired size (width, height)

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
        if flying == True: # only apply gravity when the game has started (when flying is True)
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

#Pipe Class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y,position): 
        super().__init__() # initialize the sprite class
        # Load pipe image 
        self.image = pygame.image.load(os.path.join('img', 'pipe.png'))
        self.image = pygame.transform.scale(self.image, (52, 400)) # scale the pipe image to the desired size (width, height) # 52 is the width and 320 is the height of the pipe image (you can adjust these values based on your pipe image size)
        # create a rect around pipe image
        self.rect = self.image.get_rect() # get the rectangle of the image for collision detection 
        # Set the pipe position
        if position == "top": # (flip pipe upside down)
            self.image = pygame.transform.flip(self.image, False, True) # false = no flip on x-axis, True = flip on y-axis (this will flip the pipe image upside down)
            self.rect.bottomleft = (x, y - (pipe_gap // 2)) # set the bottom left corner of the pipe to the x and y coordinates passed to the constructor (this will position the pipe at the top of the screen)
        elif position == "bottom": # (bottom pipe)
            self.rect.topleft = (x, y + (pipe_gap // 2)) # set the position of the pipe (top left corner) based on the x and y coordinates passed to the constructor
    
    # Scrolling the pipe
    def update(self):
        if game_over == False: # only update the pipe position if the game is not over (to avoid updating the position when the game is over)
            self.rect.x -= ground_speed # Move the pipe left to create a scrolling effect
        
        #Remove the pipe when it goes off-screen to avoid memory leaks
        if self.rect.right < 0: # 0 is x position change to 300 to see kill effect
            self.kill() # remove the pipe from the group (this will remove the pipe from the screen and free up memory)
"""########################### STEP 4 - RESTART BUTTON ####################################"""
class RestartButton():
    def __init__(self, x, y):
        self.image = restart_button # load the restart button image
        self.rect = self.image.get_rect() # create a rect around the image for collision detection
        self.rect.topleft = (x, y) # set the position of the button (top left corner)

    def draw(self):
        '''4.1 Get mouse position, check if the button is clicked & draw the button'''
        mouse_is_clicked = False # variable to check if the mouse is clicked
        mouse_pos = pygame.mouse.get_pos() # get the current mouse position (x, y) on the screen
        # check if the mouse is clicked and if the mouse position is within the button rect
        if pygame.mouse.get_pressed()[0] == 1 and self.rect.collidepoint(mouse_pos):
            mouse_is_clicked = True
            # Restart the game if the button is clicked

        # draw the button on the screen  
        screen.blit(self.image, (self.rect.x, self.rect.y)) # draw the button on the screen at the specified position (x, y)
        
        return mouse_is_clicked # return the mouse_is_clicked variable to check if the button is clicked

'''4.2 Create an instance of the RestartButton class'''
restart = RestartButton((screen_width // 2) - 50, (screen_height // 2) - 25) # create an instance of the RestartButton class and set its position to the center of the screen (you can adjust these values to position the button on the screen)

"""#######################################################################################"""
# Pipe Group 
bird_group = pygame.sprite.Group() 
pipe_group = pygame.sprite.Group() # create a group for pipes to manage multiple pipe instances

# Instance of the Bird class
flappy = Bird(100, (screen_height // 2)) 
bird_group.add(flappy) 
     
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

"""########################### STEP 3 - DRAW SCORE ####################################"""

'''Anti-aliasing is a technique used to smooth out jagged edges in images, text, and graphics.'''
def draw_score(text,font,white,x,y):
    score_image = font.render(text, True, white) # render the text to an image (True = anti-aliasing, color = color of the text)
    screen.blit(score_image, (x, y)) # draw the image on the screen at the specified position (x, y)

"""#######################################################################################"""

"""########################### STEP 5 - RESET GAME ####################################"""
def reset_game():
    pipe_group.empty() # remove all pipes from the group (this will remove all pipes from the screen and free up memory)
    flappy.rect.center = (100, (screen_height // 2)) # reset the bird position to the initial position (x, y) (you can adjust these values to position the bird on the screen)  
    score = 0 # reset the score to 0 (you can adjust this value to set the initial score)
    return score # return the score to be used in the main game loop
"""#######################################################################################"""
# Main game loop
is_running = True
while is_running:

    # control the frame rate
    clock.tick(FPS) 
    
    # game over conditions
    if game_over == False and flying == True: # Only scroll the background and ground if the game is not over and the game has started (flying is True)
        
        # ***Generate new pipes at intervals***
        current_time = pygame.time.get_ticks() # Check time to spawn a new pipe based on the last_pipe time and pipe_frequency
        if current_time - last_pipe > pipe_frequency: # if this is true spawn a new pipe
            
            pipe_height = random.randint(-30, 100) # Random height variation (btwn -30 to 30 px) for pipes based on pipe_gap 
            
            # move the pipe instance & group here**
            # Pipe instance & group
            bottom_pipe = Pipe(screen_width, (screen_height // 2) + pipe_height,"bottom") # add pipe_height to the y position of the bottom pipe to create a gap between the pipes (this will create a random height for the bottom pipe based on the pipe_gap value)
            top_pipe = Pipe(screen_width, (screen_height // 2) + pipe_height, "top") 
            pipe_group.add(bottom_pipe) 
            pipe_group.add(top_pipe) 

            # Update the last_pipe time to the current time**
            last_pipe = current_time  # Update the last_pipe time to the current time to track when the last pipe was spawned. This will ensure that we can spawn a new pipe after the specified frequency.
        
        # background scrolling
        bg_scroll = scroll_image(background, bg_scroll, background_speed, 0, background_width)
        
        # Draw Pipes btwn BG and Ground
        pipe_group.draw(screen) 
        pipe_group.update()

        # ground scrolling 
        ground_scroll = scroll_image(ground, ground_scroll, ground_speed, 500, ground_width)
        
    # If the game is over, stop scrolling the background and ground   
    else: 
        # draw background, pipe and ground
        screen.blit(background, (0, 0))  
        pipe_group.draw(screen) 
        screen.blit(ground, (0, 500))
    
    """########################### STEP 2 - SCORE ####################################""" 
    # Check if the bird has passed the pipe (trigger) to add score 
    if len(pipe_group) > 0: # check if any pipes that have been created
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and trigger == False: # check if the bird has passed orange but not passed green line (pipe)
            trigger = True # set trigger to True to indicate that the bird has passed trigger line (orange line)
        
        if trigger == True: # check if the trigger is True (bird has passed orange line)   
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right: # check if the bird has passed the green line (pipe)  
                score += 1 # add 1 to the score when the bird passes the pipe (this will increase the score by 1 each time the bird passes a pipe)
                trigger = False # set trigger to False to indicate that the bird has not passed the pipe yet (this will reset the trigger so that we can check for the next pipe)
                #print(score) # print the score to the console (you can remove this line if you don't want to print the score)
    
    '''Display score on the screen'''
    score_text = str(score) # convert the score to a string to display it on the screen
    draw_score(score_text, font, white, (screen_width // 2), 20) # call the draw_score function to display the score on the screen (x = 10, y = 10) (you can adjust these values to position the score on the screen)
    '''#########################################################################''' 
   
    # draw the bird & update animation
    bird_group.draw(screen) 
    bird_group.update() # this will call the update method of all sprites in the group (in this case, just the flappy bird instance)
    
    # Collision detection #
    # Check for collision between the bird and pipes or if the bird goes off-screen
    if pygame.sprite.spritecollide(flappy, pipe_group, False) or flappy.rect.top < 0: 
        game_over = True
        
    # check if the bird has hit the ground
    if flappy.rect.bottom >= screen_height - 100: # (100 px from the bottom of the screen)
        game_over = True # set game_over to True 
        flying = False # stop flying

    '''##### 4.3 Draw Restart Button & RESET GAME #######'''
    if game_over == True: # check if the game is over
            if restart.draw() == True: # check if the restart button is clicked
                game_over = False
                score = reset_game() # reset the game and score when the restart button is clicked (this will reset the game to its initial state)
    '''################################################'''       

    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Handle mouse click event to start the game
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over: # check if the mouse is clicked and the game has not started yet (flying is False) and game is not over (game_over is False)
            flying = True # set flying to True when the mouse is clicked to start the game (this can be used to control game state)

    # update the display
    pygame.display.update()

pygame.quit()
sys.exit() 
