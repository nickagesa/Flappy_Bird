'''Lesson 6 continuation: Adding Pipes to the Flappy Bird Game'''
# we made the pipes and managed to scroll once across the screen. Now we will add logic to reset the pipes once they go off-screen to create an endless scrolling effect. 
# **Scrolling Pipes**: The pipes will scroll across the screen, and you can add logic to reset their position once they go off-screen to create an endless scrolling effect.
# let's create a timer to spawn pipes at regular intervals. This will make the game more challenging and fun to play. We will also add a gap between the pipes for the bird to fly through.
# **Remove Pipes**: Once the pipes go off-screen, we will remove them from the game to free up memory and improve performance. 
# **Collision Detection**: btwn bird and the pipes, Prevent the bird from flying off the screen
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

'''1. New timer variables '''
pipe_frequency = 1500 # time in milliseconds (ms) to wait before spawning a new pipe (1500 ms = 1.5 seconds) - this will control how often new pipes are spawned and how quickly they scroll across the screen. You can adjust this value to make the game more challenging or easier for the player.
last_pipe = pygame.time.get_ticks() # get the current time in milliseconds since pygame was initialized. This will be used to track when the last pipe was spawned so we can spawn a new one after the specified frequency.

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
        
        '''3. Remove the pipe when it goes off-screen to avoid memory leaks'''
        if self.rect.right < 0: # 0 is x position change to 300 to see kill effect
            self.kill() # remove the pipe from the group (this will remove the pipe from the screen and free up memory)

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

# Main game loop
is_running = True
while is_running:

    # control the frame rate
    clock.tick(FPS) 
    
    # game over conditions
    if game_over == False and flying == True: # Only scroll the background and ground if the game is not over and the game has started (flying is True)
        
        """########################### STEP 2 ####################################"""
        
        '''2. Generate new pipes at intervals'''
        current_time = pygame.time.get_ticks() # Check time to spawn a new pipe based on the last_pipe time and pipe_frequency
        if current_time - last_pipe > pipe_frequency: # if this is true spawn a new pipe
            
            pipe_height = random.randint(-30, 100) # Random height variation (btwn -30 to 30 px) for pipes based on pipe_gap 
            
            # **2.1 move the pipe instance & group here**
            # Pipe instance & group
            bottom_pipe = Pipe(screen_width, (screen_height // 2) + pipe_height,"bottom") # add pipe_height to the y position of the bottom pipe to create a gap between the pipes (this will create a random height for the bottom pipe based on the pipe_gap value)
            top_pipe = Pipe(screen_width, (screen_height // 2) + pipe_height, "top") 
            pipe_group.add(bottom_pipe) 
            pipe_group.add(top_pipe) 

            #**2.2 Update the last_pipe time to the current time**
            last_pipe = current_time  # Update the last_pipe time to the current time to track when the last pipe was spawned. This will ensure that we can spawn a new pipe after the specified frequency.
        
        # background scrolling
        bg_scroll = scroll_image(background, bg_scroll, background_speed, 0, background_width)
        
        # Draw Pipes btwn BG and Ground
        pipe_group.draw(screen) 
        pipe_group.update()

        # ground scrolling 
        ground_scroll = scroll_image(ground, ground_scroll, ground_speed, 500, ground_width)
        
    # 2.3 If the game is over, stop scrolling the background and ground   
    else: 
        # draw background, pipe and ground
        screen.blit(background, (0, 0))  
        pipe_group.draw(screen) 
        screen.blit(ground, (0, 500))
    '''#########################################################################'''
       
   
    # draw the bird & update animation
    bird_group.draw(screen) 
    bird_group.update() # this will call the update method of all sprites in the group (in this case, just the flappy bird instance)
    
    '''4. Collision detection'''
    # Check for collision between the bird and pipes or if the bird goes off-screen
    if pygame.sprite.spritecollide(flappy, pipe_group, False) or flappy.rect.top < 0: 
        game_over = True
        
    # check if the bird has hit the ground
    if flappy.rect.bottom >= screen_height - 100: # (100 px from the bottom of the screen)
        game_over = True # set game_over to True 
        flying = False # stop flying

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
