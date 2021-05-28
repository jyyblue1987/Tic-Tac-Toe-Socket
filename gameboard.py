
class BoardClass():
    def __init__(self):
        # keeps track of all the moves
        self.grid = []

        # Usernames of both players
        self.player1 = ''
        self.player2 = ''

        # Username of the last player to have a turn
        self.last_player = ''

        # Total Number of games played
        self.total_playing_count = 0

        # Total Number of wins
        self.total_wins = 0

        # Total Number of ties
        self.total_ties = 0

        # Total Number of losses
        self.total_losses = 0

        # init Game board
        self.resetGameBoard()

    # Updates how many total games have been played
    def recordGamePlayed(self):
        self.total_playing_count += 1

    # Clear all the moves from game board
    def resetGameBoard(self):
        self.grid = [['O', 'X', ''],
                    ['', '', ''],
                    ['', '', '']]

    # Updates the game board with the player's move
    def playMoveOnBoard(self, row, col):
        if self.grid[row][col] != '':
            return False

        c = 'O' if self.last_player == self.player1 else 'X'
        self.grid[row][col] = c

    # Checks if the board is full (I.e. no more moves to make)
    def isBoardFull(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == '':
                    return False

        return True

    # Checks if the latest move resulted in a win, loss or tie
    def isGameFinished(self):
        c = ''
        # check horizontal
        for i in range(len(self.grid)):
            if self.grid[i][0] != '' and self.grid[i][0] == self.grid[i][1] and self.grid[i][0] == self.grid[i][2]:
                c = self.grid[i][0]

        # check vertical
        for j in range(len(self.grid[0])):
            if self.grid[0][j] != '' and self.grid[0][j] == self.grid[1][j] and self.grid[0][j] == self.grid[2][j]:
                c = self.grid[0][j]

        # check diaogonal
        if self.grid[0][0] != '' and self.grid[0][0] == self.grid[1][1] and self.grid[0][0] == self.grid[2][2]:
            c = self.grid[0][0]

        if self.grid[2][0] != '' and self.grid[2][0] == self.grid[1][1] and self.grid[2][0] == self.grid[0][2]:
            c = self.grid[0][0]


        if c != '':
            if c == 'O':    # player 1 win
                self.total_wins += 1
            if c == 'X':    # player 2 win
                self.total_losses += 1

            return True        

        if self.isBoardFull():
            self.total_ties += 1
            return True

        return False

    # Gathers and returns the following information:
    def computeStats(self):
        return self.player1, self.player2, self.last_player, self.total_playing_count, self.total_wins, self.total_losses, self.total_ties