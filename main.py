# Flappy Bird Game using Pygame
import pygame
import os 
import random # import random to generate random positions for the pipes
import sys 
pygame.init()
   
# window width and height
screen_width, screen_height = 600, 600

# screen & title
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# load images
background = pygame.image.load(os.path.join('img','bg.png')) 
ground = pygame.image.load(os.path.join('img','ground.png')) 
restart_button = pygame.image.load(os.path.join('img','restart.png')) 

# variable declaration
ground_scroll = 0 # ground scrolling (x set to 0) , we will use this to move the ground image to the left to create a scrolling effect.
ground_speed = 4 # speed at which the ground scrolls (pixels per frame)
ground_width = ground.get_width()  # Get the width of the ground image for scrolling
bg_scroll = 0 # background scrolling(x set to 0) , we will use this to move the background image to the left to create a scrolling effect.
background_speed = 0.5  # speed at which the background scrolls
background_width = background.get_width()  # Get the width of the background image for scrolling
flying = False # Used to check if bird is flying or not. (gravity is applied when flying is True)
game_over = False # Used to check if the game is over or not. 
pipe_gap = 100 # gap between top & bottom pipes (in pixels) 
pipe_frequency = 1500 # time (ms) to wait before spawning new pipe (1500 ms = 1.5 seconds)
last_pipe = pygame.time.get_ticks() # get the current time(ms) since pygame was initialized. Used to track when last pipe was spawned so we can spawn a new one after the specified frequency.
trigger = False # used to check if the bird has passed the pipe (to add score)
score = 0 # used to keep track of the score (number of pipes passed)
font = pygame.font.SysFont('Bauhaus 93', 40) # font object with the specified font name and size (font size = 30)
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
            self.animation_list.append(img) # append the image to the animation list

        self.image = self.animation_list[self.index]
        self.rect = self.image.get_rect() 
        self.rect.center = (x, y) # rectangle that wraps around the image, used for collision detection, positioning and movement of the sprite (bird).
        self.gravity = 0 # initial gravity for the bird (this will control the falling speed of the bird)
        self.clicked = False # this will be used to only ensure one jump per click (to avoid multiple jumps when the mouse is clicked multiple times ie. holding down the mouse button)

    # overide the update method from pygame.sprite.Sprite to create our own update method for animation
    def update(self):
        # Apply gravity to the bird
        if flying == True: # only apply gravity when the game has started (when flying is True)
            self.gravity += 0.5 # increase gravity to simulate falling (higher number = faster fall)
            if self.gravity >= 6: # limit the gravity to a max value (to avoid the value of y to keep increasing indefinitely)
                self.gravity = 6 # cap the gravity at 6 to avoid too fast falling
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
            self.image = pygame.transform.rotate(self.animation_list[self.index], (-self.gravity * 3)) # -self.gravity * 3 to rotate the bird based on the gravity (higher gravity = more rotation) 
            # negative rotation to make the bird look like it is falling down when it is falling and going up when it is jumping 
        else:
            # If the game is over, keep the bird static and do not update the animation or position, rotate the bird
            self.image = pygame.transform.rotate(self.animation_list[self.index], -90) # Rotate the bird to a fixed angle (e.g., -90 degrees) to indicate game over.

# PIPE CLASS #
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y,position): 
        super().__init__() # initialize sprite class
        # Load pipe image 
        self.image = pygame.image.load(os.path.join('img', 'pipe.png'))
        self.image = pygame.transform.scale(self.image, (52, 400)) # scale the pipe image to the desired size (width, height) 
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
# RESTART BUTTON #
class RestartButton():
    def __init__(self, x, y):
        self.image = restart_button # load the restart button image
        self.rect = self.image.get_rect() # create a rect around the image for collision detection
        self.rect.topleft = (x, y) # set the position of the button (top left corner)

    def draw(self):
        # Get mouse position, check if the button is clicked & draw the button
        mouse_is_clicked = False # variable to check if the mouse is clicked
        mouse_pos = pygame.mouse.get_pos() # get the current mouse position (x, y) on the screen
        # check if mouse is clicked and if the mouse position is within the button rect
        if pygame.mouse.get_pressed()[0] == 1 and self.rect.collidepoint(mouse_pos):
            mouse_is_clicked = True # set mouse_is_clicked to True             

        # draw the button on the screen  
        screen.blit(self.image, (self.rect.x, self.rect.y)) # draw the button on the screen at the specified position (x, y)
        
        return mouse_is_clicked # return the mouse_is_clicked variable (used later in main game loop 2 restart game)

# Create Bird & Pipe Group (manage multiple Bird & pipe instances/sprites/Objects)
bird_group = pygame.sprite.Group() 
pipe_group = pygame.sprite.Group() 

# Instances/Objects Bird & RestartButton
flappy = Bird(100, (screen_height // 2)) #(x,y)
bird_group.add(flappy) # append bird
restart = RestartButton((screen_width // 2) - 50, (screen_height // 2) - 25) 
     
# BACKGROUND & GROUND SCROLLING #
def scroll_image(image, scroll, speed, y_position, width):
    # Draw & update the scrolling position of image.
    screen.blit(image, (scroll, y_position))  
    screen.blit(image, (scroll + width, y_position))  # Draw the second instance to create a seamless effect
    
    # Move image left
    scroll -= speed  # Decrease the scroll value to move the image left

    # Reset scroll when the entire image moves off-screen
    if abs(scroll) >= width: 
        scroll = 0  

    return scroll  # Return the updated scroll value

# DRAW SCORE #
'''Anti-aliasing is a technique used to smooth out jagged edges in images, text, and graphics.'''
def draw_score(text,font,white,x,y):
    score_image = font.render(text, True, white) # render the text to an image (True = anti-aliasing)
    screen.blit(score_image, (x, y)) # draw score_image screen at the specified position (x, y)

# RESET GAME #
def reset_game():
    pipe_group.empty() # remove all pipes from the group 
    flappy.rect.center = (100, (screen_height // 2)) # reset bird position to initial position (x, y) 
    score = 0 # reset the score to 0 
    return score # return the score to be used in the main game loop

# Main game loop
is_running = True
while is_running:

    # control the frame rate
    clock.tick(FPS) 

     # Event Handling
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            is_running = False

        # Mouse click, start game
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over: # check if the mouse is clicked and the game has not started yet (flying is False) and game is not over (game_over is False)
            flying = True # set flying to True when the mouse is clicked to start the game
    
    # Start & End Game
    if game_over == False and flying == True: # start game 
        
        # GENERATE PIPES AT INTERVALS #
        current_time = pygame.time.get_ticks() # Check time to spawn a new pipe based on the last_pipe time and pipe_frequency
        if current_time - last_pipe > pipe_frequency: # if this is true spawn a new pipe
            # Random pipe height variation
            pipe_height = random.randint(-30, 100) # (btwn -30 to 100 px)
            
            # Pipe instance & group
            bottom_pipe = Pipe(screen_width, (screen_height // 2) + pipe_height,"bottom") # pipe_height is random
            top_pipe = Pipe(screen_width, (screen_height // 2) + pipe_height, "top") # pipe_height is random
            pipe_group.add(bottom_pipe) # append bottom pipe 
            pipe_group.add(top_pipe) # append top pipe

            # Update the last_pipe time to the current time**
            last_pipe = current_time  # Update the last_pipe time to the current time to track when the last pipe was spawned. This will ensure that we can spawn a new pipe after the specified frequency.
        
        # background scrolling
        bg_scroll = scroll_image(background, bg_scroll, background_speed, 0, background_width) # call scroll_image()
        
        # Draw Pipes btwn BG and Ground
        pipe_group.draw(screen) 
        pipe_group.update()

        # ground scrolling 
        ground_scroll = scroll_image(ground, ground_scroll, ground_speed, 500, ground_width) # call scroll_image()
        
    # If the game is over, stop scrolling the background and ground   
    else: 
        # draw background, pipe and ground
        screen.blit(background, (0, 0))  
        pipe_group.draw(screen) 
        screen.blit(ground, (0, 500))
    
    # SCORE CALCULATION # 
    if len(pipe_group) > 0: # check if any pipes have been created
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and trigger == False: # bird has passed orange but not passed green line 
            trigger = True # set trigger to True (bird has passed trigger line (orange line))
        
        if trigger == True: # check if the trigger is True (bird passed orange line)   
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right: # check bird passed green line (pipe)  
                score += 1 # increase score
                trigger = False # reset trigger
        #print(score) # print score to console 
    
    #Display score on screen
    draw_score(str(score), font, white, (screen_width // 2), 20) # call draw_score()
    
    # draw bird & update animation
    bird_group.draw(screen) 
    bird_group.update() 
    
    # COLLISION DETECTION #
    # 1. bird & pipes or going off-top-screen
    if pygame.sprite.spritecollide(flappy, pipe_group, False) or flappy.rect.top < 0: 
        game_over = True
        
    # 2. bird & ground
    if flappy.rect.bottom >= screen_height - 100: # (100 px from the bottom of the screen)
        game_over = True # game_over  
        flying = False # stop flying

    # Restart game 
    if game_over == True: # game is over
            if restart.draw() == True: # restart clicked
                game_over = False
                score = reset_game() # reset game & score 
   

    # update the display
    pygame.display.update()

pygame.quit()
sys.exit() 
