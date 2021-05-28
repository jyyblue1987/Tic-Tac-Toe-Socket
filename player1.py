from tkinter import Tk, X, Y, TOP, BOTTOM, LEFT, RIGHT, BOTH, END, NO, W
from tkinter import Frame, Canvas, Button, Label, Entry, Checkbutton, IntVar

import socket
import threading
from gameboard import BoardClass
from drawing import *


root = Tk()
root.geometry("1200x800+300+100")


class MainWindow(Frame):
    def __init__(self):
        super().__init__()
        
        self.game = BoardClass()
        self.initUI()
        
    def initUI(self):
        self.master.title("Player1")

        self.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        frmBoard = Frame(self, background="red")
        frmBoard.pack(fill=BOTH, expand=True)
        
        self.cnsBoard = Canvas(frmBoard, highlightthickness=1, highlightbackground="grey")
        self.cnsBoard.pack(fill=BOTH, expand=True, side=LEFT)

        draw_board_line(self.cnsBoard)
        draw_game_status(self.game, self.cnsBoard)
    
        


app = MainWindow()

root.mainloop()



# draw_board_line(screen)

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


# thread = Player1Thread()
# thread.start()
