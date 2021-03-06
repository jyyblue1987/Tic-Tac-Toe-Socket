start_x = 10
start_y = 10
step = 100
def draw_board_line(canvas):
    # draw horizonal lines
    for y in range(start_y, start_y + 4 * step, step):        
        canvas.create_line(start_x, y, start_x + 3 * step, y, fill="grey", width=5)

    # draw vertical lines
    for x in range(start_x, start_x + 4 * step, step):        
        canvas.create_line(x, start_y, x, start_y + 3 * step, fill="grey", width=5)

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

def draw_game_status(game, canvas):

    draw_board_line(canvas)
    grid = game.grid

    for i in range(len(grid)):
        y = start_y + i * step + step / 2
        for j in range(len(grid[i])):
            c = grid[i][j]

            x = start_x + j * step + step / 2

            # draw circle
            if c == 'O':                     
                r = step / 4           
                canvas.create_oval(x - r, y - r, x + r, y + r, outline="green", width=4)

            if c == 'X':                
                canvas.create_line(x - step / 4, y - step / 4, x + step / 4, y + step / 4, fill="blue", width=4)
                canvas.create_line(x - step / 4, y + step / 4, x + step / 4, y - step / 4, fill="blue", width=4)

def get_position(x, y):
    row = (y - start_y) // step
    col = (x - start_x) // step

    if row < 0:
        row = 0
    if row >= 2:
        row = 2

    if col < 0:
        col = 0
    if col >= 2:
        col = 2

    return row, col