import pygame

start_x = 0
start_y = 100
step = 200
def draw_board_line(sc):
    # draw lines
    sc.fill((0, 0, 0))  

    # draw horizonal lines
    for y in range(start_y, start_y + 4 * step, step):
        pygame.draw.line(sc, (0, 255, 0), [0, y], [start_x + 3 * step, y], 5)  

    # draw vertical lines
    for x in range(start_x, start_x + 4 * step, step):
        pygame.draw.line(sc, (0, 255, 0), [x, start_y], [x, start_y + 3 * step], 5)  



def draw_game_status(game, sc):
    grid = game.grid

    for i in range(len(grid)):
        y = start_y + i * step + step / 2
        for j in range(len(grid[i])):
            c = grid[i][j]

            x = start_x + j * step + step / 2

            # draw circle
            if c == 'O':                
                pygame.draw.circle(sc, (255, 0, 0), [x, y], step / 4, 4)  

            if c == 'X':                
                pygame.draw.line(sc, (0, 0, 255), [x - step / 4, y - step / 4], [x + step / 4, y + step / 4], 4)  
                pygame.draw.line(sc, (0, 0, 255), [x - step / 4, y + step / 4], [x + step / 4, y - step / 4], 4)  
