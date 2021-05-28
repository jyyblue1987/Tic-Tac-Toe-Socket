from tkinter import Tk, X, Y, TOP, BOTTOM, LEFT, RIGHT, BOTH, END, NO, W
from tkinter import Frame, Canvas, Button, Label, Entry, Checkbutton, IntVar
from tkinter import simpledialog, messagebox

import socket
import threading
import json
from gameboard import BoardClass
from drawing import *

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


class Player1Thread(threading.Thread):
    def __init__(self, main, game, canvas):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        
        self.conn = None
        self.server = None
        self.main = main
        self.game = game
        self.canvas = canvas

    def stop(self):
        self._stop_event.set()
        self.server.close()

    def stopped(self):
        return self._stop_event.is_set()

    def sendMove(self, row, col):
        if self.conn == None:
            print("Player2 is not connected!")
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
        # 2. Player 1 will accept incoming requests to start a new game
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.server = s            
            s.bind((HOST, PORT))
            s.listen()

            conn, addr = s.accept()
            self.conn = conn
            with conn:
                print('Connected by', addr)

                # 3. When a connection request is received and accepted, Player 1 will wait for Player 2 to send their username
                print('Player 1 will wait for Player 2 to send their username')
                while True:
                    recv = conn.recv(1024)
                    if not recv:
                        break

                    # conn.sendall(data)
                    print("Player1 Receive", recv)

                    data = json.loads(recv.decode('ascii'))

                    data_type = data['type']

                    if data_type == "Player":   # 4. Once Player 1 receives Player 2's user name
                        # then Player 1 will send "player1" as their username to Player 2 and wait for Player 2 to send their move
                        self.game.player2 = data['message'];

                        send = {
                            'type': 'Player',
                            'message': self.game.player1
                        }
                        self.game.last_player = self.game.player2

                        send_data = json.dumps(send)
                        conn.send(send_data.encode('ascii'))

                    elif data_type == "Move":
                        # update game status
                        self.game.playMoveOnBoard(data['row'], data['col'])

                        # draw game status
                        draw_game_status(self.game, self.canvas)

                        # switch player
                        self.game.last_player = self.game.player1

                    elif data_type == 'Restart':
                        print('Restart')
                        self.game.resetGameBoard()
                        self.canvas.delete('all')
                        self.game.last_player = self.game.player2

                    elif data_type == 'Exit':
                        self.main.exitApp()
                        break

                    self.main.showGameStatus()

            s.close()

root = Tk()
root.geometry("500x500+300+100")

class MainWindow(Frame):
    def __init__(self):
        super().__init__()
        
        self.game = BoardClass()
        self.initUI()

        # start server thread
        self.startThread()

        # 1. The user will be asked to provide the host information so that it can establish a socket connection as the server
        self.setPlayerName()

        
    def initUI(self):
        self.master.title("Player1")

        self.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        frmBoard = Frame(self, background="red")
        frmBoard.pack(fill=BOTH, expand=True)
        
        self.cnsBoard = Canvas(frmBoard, highlightthickness=1, highlightbackground="grey")
        self.cnsBoard.pack(fill=BOTH, expand=True, side=LEFT)

        self.cnsBoard.bind('<Button-1>', self.mouse_click)

        draw_game_status(self.game, self.cnsBoard)

        
    def setPlayerName(self):
        # the input dialog
        # player1 = simpledialog.askstring(title="Player1",
        #                                 prompt="What's your name?:")

        # self.game.player1 = player1
        self.game.player1 = 'player1'

    def startThread(self):
        self.thread = Player1Thread(self, self.game, self.cnsBoard)
        self.thread.start()

    def stopThread(self):
        self.thread.stop()

    def mouse_click(self, event):
        print("Mouse position: (%s %s)" % (event.x, event.y))

        row, col = get_position(event.x, event.y)
        print("Cell position: (%s %s)" % (row, col))

        if self.game.last_player != self.game.player1:
            print("Player2 turn")
            return

        if self.thread.sendMove(row, col) == False:
            return

        self.game.playMoveOnBoard(row, col)
        
        self.game.last_player = self.game.player2

        self.showGameStatus()
        
    def showGameStatus(self):
        draw_game_status(self.game, self.cnsBoard)
        if self.game.isGameFinished() == True:
            print("Game is finished")

    def exitApp(self):
        self.stopThread()
        root.destroy()
        

app = MainWindow()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.exitApp()
        
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()





