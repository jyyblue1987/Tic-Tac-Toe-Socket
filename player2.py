from tkinter import Tk, X, Y, TOP, BOTTOM, LEFT, RIGHT, BOTH, END, NO, W
from tkinter import Frame, Canvas, Button, Label, Entry, Checkbutton, IntVar
from tkinter import simpledialog, messagebox

import socket
import threading
import json
import time

from gameboard import BoardClass
from drawing import *

class Player2Thread(threading.Thread):
    def __init__(self, main, game, canvas, host, port):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        
        self.conn = None
        self.main = main
        self.game = game
        self.canvas = canvas
        self.host = host
        self.port = port

    def stop(self):
        self._stop_event.set()
        self.conn.close()

    def stopped(self):
        return self._stop_event.is_set()

    def sendMove(self, row, col):
        if self.conn == None:
            print("Player1 is not connected!")
            return False

        send = {
                    'type': 'Move',
                    'row': row,
                    'col': col,
                }

        send_data = json.dumps(send)
        self.conn.send(send_data.encode('ascii'))

        return True


    def run(self):        
        # 2. Using that information they will attempt to connect to Player 1
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            self.conn = s
            
            with self.conn:
                print('Connected To Server')

                # 2.1 Upon successful connection they will send Player 1 their username (just alphanumeric username with no special characters)
                print('send Player 1 their username')

                send = {
                        'type': 'Player',
                        'message': self.game.player2
                    }

                send_data = json.dumps(send)
                self.conn.send(send_data.encode('ascii'))

                self.game.last_player = self.game.player2

                while True:
                    try: 
                        recv = self.conn.recv(1024)
                        if not recv:
                            time.sleep(0.01)
                            continue
                    except:
                        print("Network broken")
                        break

                    print("Player2 Receive", recv)

                    data = json.loads(recv.decode('ascii'))

                    data_type = data['type']

                    if data_type == "Player":   # 4. Once Player 1 receives Player 2's user name
                        # then Player 1 will send "player1" as their username to Player 2 and wait for Player 2 to send their move
                        self.game.player1 = data['message']

                        self.game.last_player = self.game.player2

                    elif data_type == "Move":
                        # update game status
                        self.game.playMoveOnBoard(data['row'], data['col'])

                        # draw game status
                        draw_game_status(self.game, self.canvas)

                        # switch player
                        self.game.last_player = self.game.player2

                        
                    self.main.showGameStatus()

root = Tk()
root.geometry("500x500+300+100")

class MainWindow(Frame):
    def __init__(self):
        super().__init__()
        
        self.game = BoardClass()
        self.initUI()

        # 1. The user will be asked to provide the host information so that it can establish a socket connection as the server
        self.setPlayerName()

        # start server thread
        self.startThread()


        
    def initUI(self):
        self.master.title("Player2")

        self.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        frmBoard = Frame(self, background="red")
        frmBoard.pack(fill=BOTH, expand=True)
        
        self.cnsBoard = Canvas(frmBoard, highlightthickness=1, highlightbackground="grey")
        self.cnsBoard.pack(fill=BOTH, expand=True, side=LEFT)

        self.cnsBoard.bind('<Button-1>', self.mouse_click)

        draw_board_line(self.cnsBoard)
        draw_game_status(self.game, self.cnsBoard)
    
        
    def setPlayerName(self):
        # the input dialog
        # player1 = simpledialog.askstring(title="Player1",
        #                                 prompt="What's your name?:")

        # self.game.player1 = player1
        self.game.player2 = 'player2'
        # self.host = simpledialog.askstring(title="Player2", prompt="What's Server Address?:")
        # self.port = simpledialog.askstring(title="Player2", prompt="What's Server Port?:")

        self.host = '127.0.0.1'
        self.port = 65432

    def startThread(self):
        self.thread = Player2Thread(self, self.game, self.cnsBoard, self.host, self.port)
        self.thread.start()

    def stopThread(self):
        self.thread.stop()

    def mouse_click(self, event):
        print("Mouse position: (%s %s)" % (event.x, event.y))

        row, col = get_position(event.x, event.y)
        print("Cell position: (%s %s)" % (row, col))

        if self.game.last_player != self.game.player2:
            print("Player1 turn")
            return

        if self.thread.sendMove(row, col) == False:
            return

        self.game.playMoveOnBoard(row, col)
        
        self.game.last_player = self.game.player1

        self.showGameStatus()
        
    def showGameStatus(self):
        draw_game_status(self.game, self.cnsBoard)
        if self.game.isGameFinished() == True:
            print("Game is finished")

        

app = MainWindow()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.stopThread()
        root.destroy()        

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

