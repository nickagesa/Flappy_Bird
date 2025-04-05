# The concept of infinite scrolling background is implemented in a way where:
# 1. Load 2 images of the background and ground side by side to create a seamless scrolling effect.
# 2. Image 1 is drawn at the current scroll position, and image 2 is drawn right after it to create a continuous loop.
# 3. The scroll position is updated by decreasing it by the speed value, which moves the image to the left.
# 4. When the scroll position exceeds the width of the image, it resets to 0, allowing the images to loop seamlessly.
# Notice that the background scrolls slower than the ground to create a parallax effect, 
# Change the value of screen width to 1200 to see the images replace each other seamlessly.
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
background = pygame.image.load(os.path.join('img', 'bg.png'))
ground = pygame.image.load(os.path.join('img','ground.png')) 

# ground scrolling variables
ground_scroll = 0 
ground_speed = 4 
ground_width = ground.get_width()  # Get the width of the ground image for scrolling

# background scrolling variables
bg_scroll = 0  
background_speed = 1  
background_width = background.get_width()  # Get the width of the background image for scrolling

background = pygame.transform.scale(background, (background_width, 500))  # Set correct width for seamless scrolling
ground = pygame.transform.scale(ground, (ground_width, 100)) 

# ground scrolling variables
ground_scroll = 0 
ground_speed = 4 
ground_width = ground.get_width()  # Get the width of the ground image for scrolling

# background scrolling variables
bg_scroll = 0  
background_speed = 1  
background_width = background.get_width()  # Get the width of the background image for scrolling

# frame per second (FPS) and clock
FPS = 60
clock = pygame.time.Clock()
'''
def background_scrolling(bg_scroll):
    #Draws the background and updates the scrolling position.
    screen.blit(background, (bg_scroll, 0)) # Draw the first instance of the background at the current scroll position
    screen.blit(background, (bg_scroll + background_width, 0)) # Draw the second instance of the background to create a seamless effect
    # Move background left
    bg_scroll -= background_speed  

    # Reset scroll when the entire image moves off-screen
    if abs(bg_scroll) >= background_width:
        bg_scroll = 0  

    return bg_scroll  # Return the updated scroll value

is_running = True
while is_running:
    clock.tick(FPS)  # Control the frame rate

    bg_scroll = background_scrolling(bg_scroll)  # Update scroll position

    # draw and scroll the ground to left
    screen.blit(ground, (ground_scroll, 500)) 
    screen.blit(ground, (ground_scroll + ground_width, 500)) # Draw the second instance of the ground to create a seamless effect
    ground_scroll -= ground_speed 
    if abs(ground_scroll) > ground_width: # if the ground has moved off-screen, reset it
        ground_scroll = 0 # reset the scroll

    # Handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    pygame.display.update()  # Update display

pygame.quit()
'''
#'''
'''Put scrolling into one function'''
# Function to scroll both background and ground
def scroll_image(image, scroll, speed, y_position, width):
    """ Draws and updates the scrolling position of an image. """
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
    clock.tick(FPS)  # Control the frame rate

    '''Scroll background and ground'''
    bg_scroll = scroll_image(background, bg_scroll, background_speed, 0, background_width)
    ground_scroll = scroll_image(ground, ground_scroll, ground_speed, 500, ground_width)

    # Handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    pygame.display.update()  # Update display

pygame.quit()
#'''