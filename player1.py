import pygame
from gameboard import BoardClass
from drawing import *

pygame.init()
w = 800;
h = 800
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Player1')

game = BoardClass()

draw_board_line(screen)
draw_game_status(game, screen)


clock = pygame.time.Clock()  
running = True
while (running): # loop listening for end of game
    clock.tick(10)  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # This function must write after all the other drawing commands.  
    pygame.display.flip()  

# loop over, quite pygame
pygame.quit()