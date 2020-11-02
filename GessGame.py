# Author: Douglas Bonilla
# Date: 6/03/2020
# Description: This program contains a class named GessGame that represents a board game called Gess. It consists of a
# squares in a 18x18 grid. There are two players, black and white, each having 43 stones of his or her own color. Each
# player takes turns to move, with black starting. The way the game works is that a player chooses a location which
# only contains the player's pieces and the 3x3 area including the location chosen as a center point works as a piece.
# This 3x3 footprint is moved according to the direction the stones are located in the 3x3 footprint. Player moves the
# 3x3 footprint and tries to overlap the other player's 3x3 footprint. Any overlapping stones are eliminated and a
# a player may even eliminate their own stones. If part of the footprint lies outside the 18x18 grid, player will lose
# any stones outside those boundaries. The game is over when the a player's last ring (3x3 footprint consisting of
# pieces surrounding an empty space) is broken or if player resigns.


class GessGame:
    """Represents a Gess board game."""

    def __init__(self):
        """Initializes Gess board state."""
        self._game_state = "UNFINISHED"  # initializing game state
        self._player = "b"  # black player always starts
        # initializing the board for play
        self._board = []
        for i in range(20):
            self._board.append([])
            for j in range(21):
                if j == 20:
                    self._board[i].append(i + 1)  # y axis labeled using numbers
                else:
                    self._board[i].append(' ')
        # setting up the initial location of pieces on board
        row_2_pieces = [2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17]
        row_3_pieces = [1, 2, 3, 5, 7, 8, 9, 10, 12, 14, 16, 17, 18]
        row_4_pieces = [2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17]
        row_7_pieces = [2, 5, 8, 11, 14, 17]

        for i in range(20):
            if i in row_2_pieces:
                self._board[1][i] = 'b'  # row 2
                self._board[18][i] = 'w'  # row 19
            if i in row_3_pieces:
                self._board[2][i] = 'b'  # row 3
                self._board[17][i] = 'w'  # row 18
            if i in row_4_pieces:
                self._board[3][i] = 'b'  # row 4
                self._board[16][i] = 'w'  # row 17
            if i in row_7_pieces:
                self._board[6][i] = 'b'  # row 7
                self._board[13][i] = 'w'  # row 14
        # x axis labeled using letters
        self._board.append(
            ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"])

    def get_game_state(self):
        """Get method of game state."""
        return self._game_state

    def get_board(self):
        """Get method for board."""
        for line in self._board:
            print(line)

    def resign_game(self):
        """Resigns game and changes game state according to whom resigned."""
        if self._player == "b":
            self._game_state = "WHITE_WON"
        elif self._player == "w":
            self._game_state = "BLACK_WON"

    def update_player(self):
        """Change turns after move is made."""
        if self._player == "b":
            self._player = "w"
        elif self._player == "w":
            self._player = "b"

    def legal_footprint(self, pos):
        """Returns true if footprint is legal. All pieces in a 3x3 footprint must be from self."""
        for i in [-1, 0, 1]:  # represent row :center at 0,0 so 1,1 = SE 1,0 = E
            for j in [-1, 0, 1]:  # represent column : 0,0 = center etc.
                if self._board[pos[0] + i][pos[1] + j] != self._player and self._board[pos[0] + i][pos[1] + j] != ' ':
                    print("All pieces do not belong to current player")
                    return False
        return True

    def string_to_index(self, string):
        """Takes as parameters string consisting of a letter and number and returns corresponding index on board. """
        letters = "abcdefghijklmnopqrstuvwxyz"
        return [int(string[1:]) - 1, letters.index(string[0])]  # take into account the position of letter & number

    def get_direction(self, row, col, next_row, next_col):
        """Determines direction in relation of original row and column with next row and column. """
        if next_row > row and next_col > col:  # SE
            return [1, 1]
        elif next_row == row and next_col > col:  # Center E
            return [0, 1]
        elif next_row < row and next_col > col:  # NE
            return [-1, 1]
        elif next_row > row and next_col == col:  # Center S
            return [1, 0]
        elif next_row < row and next_col == col:  # Center N
            return [-1, 0]
        elif next_row < row and next_col < col:  # NW
            return [-1, -1]
        elif next_row > row and next_col < col:  # SW
            return [1, -1]
        elif next_row == row and next_col < col:  # Center W
            return [0, -1]

    def check_obstruction(self, direction, spaces_moved, board, pos1):
        """Determines if there is an obstruction in the pathway."""
        val = 1
        while val < spaces_moved:
            center = [pos1[0] + val * direction[0], pos1[1] + val * direction[1]]  # multiply direction by the spaces
            for i in [-1, 0, 1]:                                                   # moved to get new center from old
                for j in [-1, 0, 1]:                                               # center
                    if board[center[0] + i][center[1] + j] != " ":
                        print("Path obstructed by piece(s).")
                        return False
                    else:
                        continue
            val += 1
        return True

    def make_move(self, curr_str, final_str):
        """Takes as parameters curr_str, final str as current pos to desired pos"""
        curr_pos = self.string_to_index(curr_str)  # convert strings to indexes on board
        # print(curr_pos[0],curr_pos[1])
        final_pos = self.string_to_index(final_str)  # convert strings to indexes on board
        if self._game_state != 'UNFINISHED' or self.legal_footprint(
                curr_pos) is False:  # check if game state not unfinished and if footprint is legal
            return False
        for index in [0, 1]:  # all rows and columns: 0 = rows, 1 = columns
            if curr_pos[index] > 18 or curr_pos[index] < 1:  # check if center of current & final footprint on board
                print("Current center located out of bounds")
                return False
            elif final_pos[index] > 18 or final_pos[index] < 1:
                print("Captured center located out of bounds")
                return False
        count_ring = 0  # initialize ring count
        ring_indexes = []
        for row in range(1, 19):  # check whole board for current player rings
            for col in range(1, 19):
                count = 0
                indexes = []  # gather index coordinated square rings
                if self._board[row][col] == ' ':
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if i == 0 and j == 0:  # if center is empty continue
                                continue
                            if self._board[row + i][col + j] == self._player:  # if empty space surrounded by stones
                                count += 1
                                indexes.append([row + i, col + j])
                    if count == 8:  # 8 pieces surround center
                        indexes.append([row, col])
                        ring_indexes.append(indexes)  # store index coordinated rings
                        count_ring += 1
        count = 0
        if count_ring < 2:  # check if number of rings is less than 2, then check if curr. footprint breaking last ring
            current_indexes = []  # store indices of current footprint
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    current_indexes.append([curr_pos[0] + i, curr_pos[1] + j])
            #             print(current_indexes)
            #             print(ring_indexes[0])
            if sorted(current_indexes) != sorted(ring_indexes[0]):
                for index_coord in ring_indexes[0]:
                    if index_coord in current_indexes:  # check if index coordinate of ring is in current indexes list
                        print("Breaking of player's own last ring is not allowed.")
                        return False

        spaces_moved = max(abs(curr_pos[0] - final_pos[0]), abs(curr_pos[1] - final_pos[1]))  # calculate spaces moved
        if self._board[curr_pos[0]][
            curr_pos[1]] == " " and spaces_moved > 3:  # if center is empty then spaces moved <= 3
            print("Center empty footprint can only move up to 3 spaces")
            return False
        temp_board = [x[:] for x in
                      self._board]  # set up temp board to check obstruction path with removed current and final
        for i in [-1, 0, 1]:  # footprint values to check the path
            for j in [-1, 0, 1]:
                temp_board[curr_pos[0] + i][curr_pos[1] + j] = " "  # remove current footprint values

        # new code below
        direction = self.get_direction(curr_pos[0], curr_pos[1], final_pos[0],
                                       final_pos[1])  # determine direction of move
        #         print(curr_pos[0]+direction[0])
        #         print(self._board[curr_pos[0]+direction[0]][curr_pos[1]+direction[1]])
        #         print(direction)
        if self._board[curr_pos[0] + direction[0]][curr_pos[1] + direction[1]] != self._player:  # check if there is a
            print("There is no piece present in direction of movement.")  # piece in dir. of move
            return False
        footprint = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        if self.check_obstruction(direction, spaces_moved, temp_board,
                                  curr_pos) is True:  # if no obstruction is present than True
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    footprint[i][j] = self._board[curr_pos[0] + i][curr_pos[1] + j]
                    self._board[curr_pos[0] + i][curr_pos[1] + j] = " "
            # copy current footprint to final pos if all conditions are good to go
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    self._board[final_pos[0] + i][final_pos[1] + j] = footprint[i][j]
                # take into account if piece is beyond the edge of the board, any stones out of bounds are removed
                for x in range(0, 20):
                    self._board[0][x] = " "
                    self._board[19][x] = " "
                    self._board[x][0] = " "
                    self._board[x][19] = " "
        else:
            return False

        # check if player breaks the last ring, if 0 then change game state appropriately
        ringB = 0
        ringW = 0
        for row in range(1, 19):
            for col in range(1, 19):
                count_black = 0
                count_white = 0
                if self._board[row][col] == ' ':
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if i == 0 and j == 0:
                                continue
                            if self._board[row + i][col + j] == "b":
                                count_black += 1
                            if self._board[row + i][col + j] == "w":
                                count_white += 1
                    if count_black == 8:
                        ringB += 1
                    if count_white == 8:
                        ringW += 1
        if ringB == 0 and self._player == "w":
            self._game_state = "WHITE_WON"
        elif ringW == 0 and self._player == "b":
            self._game_state = "BLACK_WON"

        self.update_player()
        return True


# check if break ring black turn
# game = GessGame()
# game.get_board()
# print(game.make_move("l3", "m4"))
# game.get_board()
# game.get_game_state()

# p = GessGame()
# for line in p.get_board():
# print(line)

# game = GessGame()
# game.get_board()
# move_result = game.make_move('i3', 'i6')
# game.make_move('e14', 'g14')
# game.get_board()
# state = game.get_game_state()
# game.resign_game()  # black turn and player resigns
# print(state)
# print(game.get_game_state())

# initial board                         # Empieze aqui!
game = GessGame()
game.get_board()

# black player move
print(game.make_move("o6", "o7"))
game.get_board()
game.get_game_state()

# white player move
print(game.make_move("r15", "r14"))
game.get_board()
game.get_game_state()

# black player move
print(game.make_move("o7", "o10"))
game.get_board()
game.get_game_state()

# white player move
print(game.make_move("i18", "i15"))
game.get_board()
game.get_game_state()

# black player move
print(game.make_move("l3", "l6"))
game.get_board()
game.get_game_state()

# white player move
print(game.make_move("i15", "g13"))
game.get_board()
game.get_game_state()

# black player move                        # Termine aqui
print(game.make_move("l6", "j8"))
game.get_board()
game.get_game_state()

# white player move
# print(game.make_move("g13", "j10"))
# game.get_board()
# print(game.get_game_state())             # white breaks black ring and game state = white won.

# black player move                        # return false because white already won
# print(game.make_move("n3", "n4"))
# game.get_board()
# game.get_game_state()
# print(game.get_game_state())

# white player move                         # check if goes off edge of board and loses stones
print(game.make_move("g13", "b9"))
game.get_board()
game.get_game_state()

# black player move
# print(game.make_move("i3", "f3"))
# game.get_board()
# game.get_game_state()

# white player move
# print(game.make_move("b9", "d9"))
# game.get_board()
# game.get_game_state()
