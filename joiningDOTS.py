# Email:snshohin@gmail.com
# JOINING THE DOTS game using python
# 9 June 2020

from tkinter import *
import numpy as np

size_of_board = 600         # Change size of board
number_of_dots = 6          # Change number of dots on board
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#000000'
player1_color = '#0492CF'
player1Shade = '#67B0CF'
player2_color = '#EE4035'
player2Shade = '#EE7E77'
Green_color = '#7BC043'
dot_width = 0.15 * size_of_board / number_of_dots
edge_width = 0.1 * size_of_board / number_of_dots
distanceDots = size_of_board / number_of_dots


class joiningDots:
    player1Score = 0  # Score variables
    player2Score = 0
    print("CLass")

    def __init__(self):
        self.window = Tk()
        self.window.title('JOINING THE DOTS')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.refresh_board()
        self.play_again()

    def play_again(self):  # Resets to default setup
        self.refresh_board()
        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))

        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []
        self.score1 = []
        self.score2 = []
        self.already_marked_boxes = []
        self.playerTurn()
        self.edgeColMarked = []
        self.edgeRowMarked = []
        self.player1Score = 0
        self.player2Score = 0

    def mainloop(self):
        self.window.mainloop()

    def is_grid_occupied(self, logical_position, type):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True

        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False

        return occupied

    def shadingCoordinate(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position - distanceDots / 4) // (distanceDots / 2)
        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0] - 1) // 2)
            c = int(position[1] // 2)
            logical_position = [r, c]
            type = 'row'

        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        val = 1
        if self.player1_turn:
            val = - 1

        if c < (number_of_dots - 1) and r < (number_of_dots - 1):
            self.board_status[c][r] += val

        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c - 1][r] += val

        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r - 1] += val

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    def checkUpDown(self, start, end, z, color):
        listt1 = [z - distanceDots, z, start]
        listt2 = [z - distanceDots, z, start + distanceDots]

        if listt1 in self.edgeColMarked and listt2 in self.edgeColMarked:
            listt3 = [start, end, z - distanceDots]

            if listt3 in self.edgeRowMarked:
                up = True
            else:
                up = False
        else:
            up = False
        if up:
            c2 = start // distanceDots
            c1 = (z // distanceDots) - 1
            if self.player1_turn:
                self.player1Score += 1
            else:
                self.player2Score += 1

            self.shade_square(c1, c2, color)
            self.player1_turn = not self.player1_turn

        listt1 = [z, z + distanceDots, start]
        listt2 = [z, z + distanceDots, start + distanceDots]

        if listt1 in self.edgeColMarked and listt2 in self.edgeColMarked:
            listt3 = [start, end, z + distanceDots]

            if listt3 in self.edgeRowMarked:
                down = True
            else:
                down = False
        else:
            down = False
        if down:
            c2 = start // distanceDots
            c1 = (z // distanceDots)

            if self.player1_turn:
                self.player1Score += 1
            else:
                self.player2Score += 1

            self.shade_square(c1, c2, color)
            self.player1_turn = not self.player1_turn

        if up and down:  # if possible, conditions become exceptional
            self.player1_turn = not self.player1_turn
            if self.player1_turn:
                self.player1Score += 1
                self.player2Score -= 1
            else:
                self.player2Score += 1
                self.player1Score -= 1

    def checkSides(self, start, end, z, color):
        listt1 = [z, z + distanceDots, start]
        listt2 = [z, z + distanceDots, start + distanceDots]
        if listt1 in self.edgeRowMarked and listt2 in self.edgeRowMarked:
            listt3 = [start, end, z + distanceDots]

            if listt3 in self.edgeColMarked:
                right = True
            else:
                right = False
        else:
            right = False

        if right:
            c1 = start // distanceDots
            c2 = z // distanceDots
            if self.player1_turn:
                self.player1Score += 1
            else:
                self.player2Score += 1
            self.shade_square(c1, c2, color)
            self.player1_turn = not self.player1_turn

        listt1 = [z - distanceDots, z, start]
        listt2 = [z - distanceDots, z, end]

        if listt1 in self.edgeRowMarked and listt2 in self.edgeRowMarked:
            listt3 = [start, end, z - distanceDots]

            if listt3 in self.edgeColMarked:
                left = True
            else:
                left = False
        else:
            left = False
        if left:
            c2 = (z - distanceDots) // distanceDots
            c1 = start // distanceDots
            if self.player1_turn:
                self.player1Score += 1
            else:
                self.player2Score += 1
            self.shade_square(c1, c2, color)
            self.player1_turn = not self.player1_turn

        if right and left:  # if possible, conditions become exceptional
            self.player1_turn = not self.player1_turn
            if not self.player1_turn:
                self.player1Score += 1
                self.player2Score -= 1
            else:
                self.player2Score += 1
                self.player1Score -= 1

    def make_edge(self, type, logical_position):
        if self.player1_turn:
            playerColor = player1Shade
        else:
            playerColor = player2Shade
        if self.player1_turn:
            color = player1_color
        else:
            color = player2_color

        if type == 'row':
            start_x = distanceDots / 2 + logical_position[0] * distanceDots
            end_x = start_x + distanceDots
            start_y = distanceDots / 2 + logical_position[1] * distanceDots
            end_y = start_y
            listt = [start_x, end_x, start_y]
            # print(start_x, " ", end_x, " ", start_y, " ", end_y, " ", type)
            self.edgeRowMarked.append(listt)
            self.checkUpDown(start_x, end_x, start_y, playerColor)

        elif type == 'col':
            start_y = distanceDots / 2 + logical_position[1] * distanceDots
            end_y = start_y + distanceDots
            start_x = distanceDots / 2 + logical_position[0] * distanceDots
            end_x = start_x
            listt = [start_y, end_y, start_x]
            # print(start_x, " ", end_x, " ", start_y, " ", end_y, " ", type)
            self.edgeColMarked.append(listt)
            self.checkSides(start_y, end_y, start_x, playerColor)

        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=edge_width)

    def display_gameover(self):

        if self.player1Score > self.player2Score:
            text = 'BLUE wins!!!'
            color = player1_color
        elif self.player2Score > self.player1Score:
            text = 'RED wins!!!'
            color = player2_color
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 4, font="cmr 40 bold", fill=color, text=text)

        self.canvas.create_line(size_of_board / 2 - 200, size_of_board / 2 - 50, size_of_board / 2 + 200,
                                size_of_board / 2 - 50, fill='#000000')
        self.canvas.create_line(size_of_board / 2 - 200, size_of_board / 2 + 10, size_of_board / 2 + 200,
                                size_of_board / 2 + 10, fill='#000000')
        self.canvas.create_line(size_of_board / 2 - 200, size_of_board / 2 - 50, size_of_board / 2 - 200,
                                size_of_board / 2 + 10, fill='#000000')
        self.canvas.create_line(size_of_board / 2 + 200, size_of_board / 2 - 50, size_of_board / 2 + 200,
                                size_of_board / 2 + 10, fill='#000000')

        score_text = 'BLUE : ' + str(self.player1Score) + '\n'
        self.canvas.create_text(size_of_board / 2 - 100, size_of_board / 2, font="cmr 30 bold", fill=player1_color,
                                text=score_text)
        score_text = 'RED : ' + str(self.player2Score) + '\n'
        self.canvas.create_text(size_of_board / 2 + 100, size_of_board / 2, font="cmr 30 bold", fill=player2_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    def refresh_board(self):
        for i in range(number_of_dots):
            x = i * distanceDots + distanceDots / 2
            self.canvas.create_line(x, distanceDots / 2, x,
                                    size_of_board - distanceDots / 2,
                                    fill='gray', dash=(2, 2))
            self.canvas.create_line(distanceDots / 2, x,
                                    size_of_board - distanceDots / 2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i * distanceDots + distanceDots / 2
                end_x = j * distanceDots + distanceDots / 2
                self.canvas.create_oval(start_x - dot_width / 2, end_x - dot_width / 2, start_x + dot_width / 2,
                                        end_x + dot_width / 2, fill=dot_color,
                                        outline=dot_color)

    def playerTurn(self):
        if self.player1_turn:
            color = player1_color

        else:
            color = player2_color
        self.canvas.create_rectangle(0, size_of_board - (distanceDots // 4), size_of_board, size_of_board, fill=color)
        self.canvas.delete(self.score1)
        text = str(self.player1Score)
        self.score1 = self.canvas.create_text(size_of_board // 4, 10, fill=player1Shade, font="cmr 15 bold",
                                              text=text)
        self.canvas.delete(self.score2)
        text = str(self.player2Score)
        self.score2 = self.canvas.create_text((size_of_board // 2) + (size_of_board // 4), 10, fill=player2Shade,
                                              font="cmr 15 bold", text=text)

    def shade_square(self, c1, c2, color):
        start_x = distanceDots / 2 + c2 * distanceDots + edge_width / 2
        start_y = distanceDots / 2 + c1 * distanceDots + edge_width / 2
        end_x = start_x + distanceDots - edge_width
        end_y = start_y + distanceDots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def click(self, event):
        if not self.reset_board:
            grid_position = [event.x, event.y]
            logical_positon, valid_input = self.shadingCoordinate(grid_position)
            if valid_input and not self.is_grid_occupied(logical_positon, valid_input):
                self.update_board(valid_input, logical_positon)
                self.make_edge(valid_input, logical_positon)
                self.refresh_board()
                self.player1_turn = not self.player1_turn

                if self.is_gameover():

                    self.display_gameover()
                else:
                    self.playerTurn()
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


game_instance = joiningDots()
game_instance.mainloop()