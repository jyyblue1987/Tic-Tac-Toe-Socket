import pygame
import socket
import threading
from gameboard import BoardClass
from drawing import *

pygame.init()
w = 800;
h = 800
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Player1')

game = BoardClass()

draw_board_line(screen)

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

class Player1Thread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(Player1Thread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.conn = None

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            self.conn = conn
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    # conn.sendall(data)


    


clock = pygame.time.Clock()  
running = True

thread = Player1Thread()
thread.start()

while (running): # loop listening for end of game
    clock.tick(10)  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            thread.stop()

    # This function must write after all the other drawing commands.  
    draw_game_status(game, screen)
    pygame.display.flip()  

# loop over, quite pygame
pygame.quit()