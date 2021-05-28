from tkinter import Tk, X, Y, TOP, BOTTOM, LEFT, RIGHT, BOTH, END, NO, W
from tkinter import Frame, Canvas, Button, Label, Entry, Checkbutton, IntVar
from tkinter import simpledialog, messagebox

import socket
import threading
from gameboard import BoardClass
from drawing import *

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


class Player1Thread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(Player1Thread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.conn = None
        self.sever = None

    def stop(self):
        self._stop_event.set()
        self.server.close()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.server = s
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

root = Tk()
root.geometry("500x500+300+100")


class MainWindow(Frame):
    def __init__(self):
        super().__init__()
        
        self.game = BoardClass()
        self.initUI()
        self.startThread()

        
    def initUI(self):
        self.master.title("Player1")

        self.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        frmBoard = Frame(self, background="red")
        frmBoard.pack(fill=BOTH, expand=True)
        
        self.cnsBoard = Canvas(frmBoard, highlightthickness=1, highlightbackground="grey")
        self.cnsBoard.pack(fill=BOTH, expand=True, side=LEFT)

        draw_board_line(self.cnsBoard)
        draw_game_status(self.game, self.cnsBoard)
    
        
    def setPlayerName(self):
        # the input dialog
        player1 = simpledialog.askstring(title="Player1",
                                        prompt="What's your name?:")

        self.game.player1 = player1

    def startThread(self):
        self.thread = Player1Thread()
        self.thread.start()

    def stopThread(self):
        self.thread.stop()

app = MainWindow()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.stopThread()
        root.destroy()        

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()





