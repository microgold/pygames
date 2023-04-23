import sys
import pygame
import pygame.mixer

# Initialize the game

pygame.init()


# Initialize the mixer
# to play sound
pygame.mixer.init()
pygame.mixer.music.load("resources/shortbeep.mp3")

# Create the screen
screen = pygame.display.set_mode((320, 240))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

HelloWorldColors = [BLACK, RED]

# create the font object
font = pygame.font.Font(None, 32)
mouse_pos = None
time = pygame.time

count = 0
oneSecondMarkReached = False
lastTime = 0

while True:
    if oneSecondMarkReached:
        count = count + 1

    screen.fill(WHITE)  # fill the background

    # check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

    # create the text surface
    text = font.render("Hello World", True, HelloWorldColors[count % 2])

    # surround text with black rectangular border
    pygame.draw.rect(screen, BLACK, ((screen.get_width() - text.get_width())/2 - 10,
                                     (screen.get_height() -
                                      text.get_height()) / 2 - 10,
                                     text.get_width() + 20,
                                     text.get_height() + 20), 1)

    # draw an image of a smiley above the border with a size of 32x32
    if mouse_pos != None:
        screen.blit(pygame.image.load("resources/smiley.png"),
                    (mouse_pos[0] - 16, mouse_pos[1] - 16))
    else:
        screen.blit(pygame.image.load("resources/smiley.png"),
                    (screen.get_width()/2 - 16,
                     (screen.get_height() - text.get_height()) / 2 - 60))

    # blit the text surface to the screen
    screen.blit(text, ((screen.get_width() - text.get_width()) /
                2, (screen.get_height() - text.get_height()) / 2))

    if oneSecondMarkReached:
        pygame.mixer.music.play()

    # update the screen
    pygame.display.flip()

    # reset the oneSecondMarkReached flag
    oneSecondMarkReached = False

    # inform the program every time the 1 second mark is reached

    currentTime = time.get_ticks()
    if currentTime - lastTime > 1000:
        lastTime = currentTime
        oneSecondMarkReached = True
        
    
