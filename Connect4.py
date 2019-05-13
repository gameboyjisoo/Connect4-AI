import numpy as np
import time
import math
import copy
from random import randint

class Board(object):
    def __init__(self, board=None):
        self.COLUMN = 7;
        self.ROW = 6;

        if board is not None:
            self.board = board
        else:
            self.board = np.zeros((self.ROW, self.COLUMN), dtype=int)

    def insertColumn(self, move, order):
        for i in range(0, ROW):
            if self.board[ROW - 1 - i][move - 1] == 0:
                self.board[ROW - 1 - i][move - 1] = order
                break

    def printBoard(self):
        print(self.board)
        print('  1 2 3 4 5 6 7')

    def checkResult(self, order):

        sameNum = 0

        # row Check
        for i in range(ROW):
            for j in range(0, 4):
                for k in range(1, 4):
                    if (self.board[i][j] == order) and (self.board[i][j] == self.board[i][j + k]):
                        sameNum += 1
                        if sameNum == 3:
                            return 1
                sameNum = 0

        # Column Check
        for i in range(COLUMN):
            for j in range(0, 4):
                for k in range(1, 4):
                    try:
                        if (self.board[j][i] == order) and (self.board[j][i] == self.board[j + k][i]):
                            sameNum += 1
                        if sameNum == 3:
                            return 1
                    except IndexError:
                        pass
                sameNum = 0

        # Diagonal Down Check
        for i in range(0, 3):
            for j in range(0, 4):
                for k in range(1, 4):
                    if (self.board[i][j] == order) and (self.board[i][j] == self.board[i + k][j + k]):
                        sameNum += 1
                        if sameNum == 3:
                            return 1
                sameNum = 0

        # Diagonal Up Check
        for i in range(0, 3):
            for j in range(3, 7):
                for k in range(1, 4):
                    if (self.board[i][j] == order) and (self.board[i][j] == self.board[i + k][j - k]):
                        sameNum += 1
                        if sameNum == 3:
                            return 1
                sameNum = 0
                
                
        count = 0

        for i in range(0, self.ROW):
            for j in range(0, self.COLUMN):
                if self.board[i][j] != 0:
                    count += 1

        if count == 42:
            return 0

        return

    def children(self, order):
        children = []
        for i in range(0, self.COLUMN):
            if self.board[0][i] == 0:
                child = Board(copy.deepcopy(self.board))
                child.insertColumn(i + 1, order)
                children.append((i, child))

        return children

    def heuristic(self, board):

        heur = 0
        state = board.board
        
        for i in range(0, board.ROW):
            for j in range(0, board.COLUMN):
                # column 확인
                try:
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == state[i + 3][j] != 0:
                        if state[i][j] == 1:
                            heur += 10000
                        else:
                            heur -= 10000
                    elif state[i][j] == state[i + 1][j] == state[i + 2][j] != 0:
                        if state[i - 1][j] == 0:
                            if state[i][j] == 1:
                                heur += 30
                            else:
                                heur -= 30
                    if state[i][j] == state[i + 1][j] != 0:
                        if state[i - 1][j] == 0:
                            if state[i][j] == 1:
                                heur += 3
                            else:
                                heur -= 3
                except IndexError:
                    pass

                # row 확인
                try:
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == state[i][j + 3] != 0:
                        if state[i][j] == 1:
                            heur += 10000
                        else:
                            heur -= 10000
                    elif state[i][j] == state[i][j + 1] == state[i][j + 2] != 0:
                        if state[i][j + 3] == 0 or state[i][j - 1] == 0:
                            if state[i][j] == 1:
                                heur += 40
                            else:
                                heur -= 40
                    elif state[i][j] == state[i][j + 1] != 0:
                        if (state[i][j + 2] == state[i][j + 3] == 0) or (state[i][j - 1] == state[i][j - 2] == 0) or (
                                state[i][j + 2] == state[i][j - 1] == 0):
                            if state[i][j] == 1:
                                heur += 4
                            else:
                                heur -= 4
                except IndexError:
                    pass

                # y=-x 대각선
                try:
                    if j < 4 and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == state[i + 3][j + 3] != 0:
                        if state[i][j] == 1:
                            return 10000
                        else:
                            return -10000
                    elif j < 4 and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] != 0:
                        if state[i + 3][j + 3] == 0 or state[i - 1][j - 1] == 0:
                            if state[i][j] == 1:
                                heur += 50
                            else:
                                heur -= 50
                    elif j < 4 and state[i][j] == state[i + 1][j + 1] != 0:
                        if (state[i + 2][j + 2] == state[i + 3][j + 3] == 0) or (
                                state[i - 1][j - 1] == state[i - 2][j - 2] == 0) or (
                                state[i - 1][j - 1] == state[i + 2][j + 2] == 0):
                            if state[i][j] == 1:
                                heur += 5
                            else:
                                heur -= 5
                except IndexError:
                    pass

                # y=x 대각선
                try:
                    if j > 2 and state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] == state[i + 3][j - 3] != 0:
                        if state[i][j] == 1:
                            return 10000
                        else:
                            return -10000
                    elif j > 2 and state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] != 0:
                        if state[i + 3][j - 3] == 0 or state[i - 1][j + 1] == 0:
                            if state[i][j] == 1:
                                heur += 50
                            else:
                                heur -= 50
                    elif j > 2 and state[i][j] == state[i + 1][j - 1] != 0:
                        if (state[i + 2][j - 2] == state[i + 3][j - 3] == 0) or (
                                state[i - 1][j + 1] == state[i - 2][j + 2] == 0) or (
                                state[i - 1][j + 1] == state[i + 2][j - 2] == 0):
                            if state[i][j] == 1:
                                heur += 5
                            else:
                                heur -= 5
                except IndexError:
                    pass
        return heur
    

class Player:
    def __init__(self, name, order, ai, ai_mode=None):

        self.order = order
        self.name = name
        self.ai = ai
        self.depth = 8

    def makeMove(self, board):

        empty = True
        for x in range(0, 7):
            if (board.board[5][x] != 0):
                empty = False

        while True:
            print("\n*** Player " + self.name + " Selects!***\n")

            if self.ai:
                print('AI\'s thinking...')

                start = time.clock()

                if aiMode == 1:
                    move = game.rule()
                else:
                    move = self.minimax(board, self.depth, self.order, -math.inf, math.inf, start)[1] + 1
                    print("move : " + str(move))

                timeout = time.clock() - start
                print('Timeout: %.6f\n' % timeout)

            else:
                move = int(input("select move : "))

            if (move < 0) or (move > COLUMN):
                print("out of range please type in again")
                continue
            elif empty and move == 4:
                print("cannot place in column 4 on first turn. please type in again")
            elif board.board[0][move - 1] != 0:
                print("column full, try again")
            else:
                break

        return move

    def minimax(self, board, depth, order, alpha, beta, start):

        now = time.clock()

        if depth == 0:
            return board.heuristic(board), -1
        elif order == 1 and board.checkResult(order) == 1:
            return 1000000, -1
        elif order == 2 and board.checkResult(order) == 1:
            return -1000000, -1

        children = board.children(order)
        bestMove = -1

        empty = True
        for x in range(0, 7):
            if (board.board[5][x] != 0):
                empty = False
        
        count = 0
        for i in range(0, board.ROW):
            for j in range(0, board.COLUMN):
                if board.board[i][j] != 0:
                    count+=1
                    
        if count == 1:
            return 100000, 3
        
        if order == 1:
            bestVal = -math.inf

            for child in children:
                childMove = child[0]
                childBoard = child[1]

                value = self.minimax(childBoard, depth - 1, order + 1, alpha, beta, start)[0]

                if depth == self.depth:
                    now = time.clock()
                    print("Move : " + str(childMove + 1) + " heur : " + str(value) + " time ; " + str(now - start))

                if bestVal<value:
                    tempVal = bestVal
                    tempMove = bestMove

                    bestVal = max(bestVal, value)
                    bestMove = childMove

                    if empty:
                        if bestMove == 3:
                            bestVal = tempVal
                            bestMove = tempMove

                alpha = max(alpha, bestVal)
                
                if now - start > 118:
                    break
                
                if alpha >= beta:
                    break

            return bestVal, bestMove

        else:
            bestVal = math.inf
            for child in children:
                childMove = child[0]
                childBoard = child[1]

                value = self.minimax(childBoard, depth - 1, order - 1, alpha, beta, start)[0]

                if depth == self.depth:
                    print("Move : " + str(childMove + 1) + " heur : " + str(value))

                if bestVal>value:
                    tempVal = bestVal
                    tempMove = bestMove

                    bestVal = min(bestVal, value)
                    bestMove = childMove

                    if empty:
                        if bestMove == 3:
                            bestVal = tempVal
                            bestMove = tempMove

                beta = min(beta, bestVal)
                
                if now - start > 118:
                    break

                if alpha >= beta:
                    break

            return bestVal, bestMove


class Game:
    def __init__(self, board, gameMode, player1, player2):
        self.gameMode = gameMode
        self.COLUMN = 7;
        self.ROW = 6;
        self.board = board
        self.first = firstturn
        self.player1 = player1
        self.player2 = player2

    def beginGame(self):

        print('**** Game Begin! ****')
        self.board.printBoard()

        while (True):
            move = self.player1.makeMove(self.board)
            self.board.insertColumn(move, self.player1.order)
            self.board.printBoard()

            if self.board.checkResult(self.player1.order) == 0:
                print("draw")
                break

            elif self.board.checkResult(self.player1.order) == 1:
                print(self.player1.name + " Wins!!\n")
                break

            move = self.player2.makeMove(self.board)
            self.board.insertColumn(move, self.player2.order)
            self.board.printBoard()

            if self.board.checkResult(self.player2.order) == 0:
                print("draw")
                break

            elif self.board.checkResult(self.player2.order) == 1:
                print(self.player2.name + " Wins!!\n")
                break

    def rule(self):
        if self.first:
            for x in range(0, 7):
                if (self.board.board[5][x] == player2_AI.order):
                    self.first = False
        if self.first:
            if player2_AI.order == 2:
                self.first = False
                return 4
            else:
                self.first = False
                return 3
        else:
            # 내꺼 4개 이어지는 가능성 확인
            for i in range(0, self.ROW):
                for j in range(0, self.COLUMN):
                    try:
                        # 같은 column에 3개 있을 때
                        if self.board.board[i][j] == self.board.board[i + 1][j] == self.board.board[i + 2][j] == player2_AI.order:
                            print(j, "column potential 4inarow")
                            if (self.board.board[i - 1][j] == 0):
                                print("executed")
                                return j + 1
                    except IndexError:
                        pass

                    try:
                        # 같은 row에 3개 있을 떄
                        if self.board.board[i][j] == self.board.board[i][j + 1] == self.board.board[i][j + 2] == player2_AI.order:
                            if j < 4:
                                if self.board.board[i][j - 1] == 0:
                                    print(j, "row potential 4inarow, condition 1")
                                    if i == 5:
                                        print("executed")
                                        return j
                                    elif i < 5 and (self.board.board[i + 1][j - 1] != 0):
                                        print("executed")
                                        return j
                            if i == 5:
                                print(j, "row potential 4inarow, condition 2")
                                if (self.board.board[i][j + 3] == 0):
                                    print("executed")
                                    return j + 4
                                else:
                                    print("not possible")
                            if i < 5 and self.board.board[i + 1][j + 3] != 0:
                                print(j, "row potential 4inarow, condition 3")
                                if (self.board.board[i][j + 3] == 0):
                                    print("executed")
                                    return j + 4
                        elif self.board.board[i][j] == self.board.board[i][j + 1] == self.board.board[i][j + 3] == player2_AI.order:
                            if self.board.board[i][j + 2] == 0:
                                print(j, "row potential 4inarow, condition 4")
                                if i == 5:
                                    print("executed")
                                    return j + 3
                                elif self.board.board[i + 1][j + 2] != 0:
                                    print("executed")
                                    return j + 3
                                else:
                                    print("not possible")
                        elif self.board.board[i][j] == self.board.board[i][j + 2] == self.board.board[i][j + 3] == player2_AI.order:
                            if self.board.board[i][j + 1] == 0:
                                print(j, "row potential 4inarow, condition 5")
                                if i == 5:
                                    print("executed")
                                    return j + 2
                                elif self.board.board[i + 1][j + 1] != 0:
                                    print("executed")
                                    return j + 2
                    except IndexError:
                        pass
                    # y=-x 대각선. 4개 연결되는거 확인하는거니까 j>2만 확인한다.
                    try:
                        if j > 2 and self.board.board[i][j] == self.board.board[i - 1][j - 1] == \
                                self.board.board[i - 2][j - 2] == player2_AI.order:
                            print(j, "left diagonal potential 4inarow, condition 1")
                            if self.board.board[i - 3][j - 3] == 0 and self.board.board[i - 2][j - 3] != 0:
                                print("executed")
                                return j - 2
                            elif self.board.board[i + 1][j + 1] == 0:
                                if i == 4:
                                    print("executed")
                                    return j + 2
                                elif i < 4 and self.board.board[i + 2][j + 1] != 0:
                                    print("executed")
                                    return j + 2
                        elif j > 2 and self.board.board[i][j] == self.board.board[i - 1][j - 1] == \
                                self.board.board[i - 3][j - 3] == player2_AI.order:
                            print(j, "left diagonal potential 4inarow, condition 2")
                            if self.board.board[i - 2][j - 2] == 0 and self.board.board[i - 1][j - 2] != 0:
                                print("executed")
                                return j - 1
                        elif j > 2 and self.board.board[i][j] == self.board.board[i - 2][j - 2] == \
                                self.board.board[i - 3][j - 3] == player2_AI.order:
                            print(j, "left diagonal potential 4inarow, condition 3")
                            if self.board.board[i - 1][j - 1] == 0 and self.board.board[i][j - 1] != 0:
                                print("executed")
                                return j
                    except IndexError:
                        pass
                    # y=x대각선
                    try:
                        if j < 4 and self.board.board[i][j] == self.board.board[i - 1][j + 1] == \
                                self.board.board[i - 2][j + 2] == player2_AI.order:
                            print(j, "right diagonal potential 4inarow, condition 1")
                            if self.board.board[i - 3][j + 3] == 0 and self.board.board[i - 2][j + 3] != 0:
                                print("executed")
                                return j + 4
                            elif self.board.board[i + 1][j - 1] == 0:
                                if i == 4:
                                    print("executed")
                                    return j
                                elif i < 4 and self.board.board[i + 2][j - 1] != 0:
                                    print("executed")
                                    return j
                        elif j < 4 and self.board.board[i][j] == self.board.board[i - 1][j + 1] == \
                                self.board.board[i - 3][j + 3] == player2_AI.order:
                            print(j, "right diagonal potential 4inarow, condition 1")
                            if self.board.board[i - 2][j + 2] == 0 and self.board.board[i - 1][j + 2] != 0:
                                print("executed")
                                return j + 3
                        elif j < 4 and self.board.board[i][j] == self.board.board[i - 2][j + 2] == \
                                self.board.board[i - 3][j + 3] == player2_AI.order:
                            print(j, "right diagonal potential 4inarow, condition 1")
                            if self.board.board[i - 1][j + 1] == 0 and self.board.board[i][j + 1] != 0:
                                print("executed")
                                return j + 2
                    except IndexError:
                        pass

            # 상대꺼 4개 이어지는 가능성 확인
            for i in range(0, self.ROW):
                for j in range(0, self.COLUMN):
                    try:
                        # 같은 column에 3개 있을 때
                        if self.board.board[i][j] == self.board.board[i + 1][j] == self.board.board[i + 2][
                            j] == player1.order:
                            print(j, "column potential 4inarow threat")
                            if (self.board.board[i - 1][j] == 0):
                                print("blocked")
                                return j + 1
                    except IndexError:
                        pass

                    try:
                        # 같은 row에 3개 있을 떄
                        if self.board.board[i][j] == self.board.board[i][j + 1] == self.board.board[i][
                            j + 2] == player1.order:
                            if j < 4:
                                if self.board.board[i][j - 1] == 0:
                                    print(j, "row potential 4inarow threat, condition 1")
                                    if i == 5:
                                        print("blocked")
                                        return j
                                    elif i < 5 and (self.board.board[i + 1][j - 1] != 0):
                                        print("blocked")
                                        return j

                            if i == 5:
                                print(j, "row potential 4inarow threat, condition 2")
                                if (self.board.board[i][j + 3] == 0):
                                    print("blocked")
                                    return j + 4

                            if i < 5 and self.board.board[i + 1][j + 3] != 0:
                                print(j, "row potential 4inarow threat, condition 3")
                                if (self.board.board[i][j + 3] == 0):
                                    print("blocked")
                                    return j + 4

                        elif self.board.board[i][j] == self.board.board[i][j + 1] == self.board.board[i][
                            j + 3] == player1.order:
                            if self.board.board[i][j + 2] == 0:
                                print(j, "row potential 4inarow threat, condition 4")
                                if i == 5:
                                    print("blocked")
                                    return j + 3
                                elif self.board.board[i + 1][j + 2] != 0:
                                    print("blocked")
                                    return j + 3

                        elif self.board.board[i][j] == self.board.board[i][j + 2] == self.board.board[i][
                            j + 3] == player1.order:
                            if self.board.board[i][j + 1] == 0:
                                print(j, "row potential 4inarow threat, condition 5")
                                if i == 5:
                                    print("blocked")
                                    return j + 2
                                elif self.board.board[i + 1][j + 1] != 0:
                                    print("blocked")
                                    return j + 2
                    except IndexError:
                        pass
                    # y=-x 대각선. 4개 연결되는거 확인하는거니까 j>2만 확인한다.
                    try:
                        if j > 2 and self.board.board[i][j] == self.board.board[i - 1][j - 1] == \
                                self.board.board[i - 2][j - 2] == player1.order:
                            print(j, "left diagonal potential 4inarow threat, condition 1")
                            if self.board.board[i - 3][j - 3] == 0 and self.board.board[i - 2][j - 3] != 0:
                                print("blocked")
                                return j - 2
                            elif self.board.board[i + 1][j + 1] == 0:
                                if i == 4:
                                    print("blocked")
                                    return j + 2
                                elif i < 4 and self.board.board[i + 2][j + 1] != 0:
                                    print("blocked")
                                    return j + 2
                        elif j > 2 and self.board.board[i][j] == self.board.board[i - 1][j - 1] == \
                                self.board.board[i - 3][j - 3] == player1.order:
                            print(j, "left diagonal potential 4inarow threat, condition 2")
                            if self.board.board[i - 2][j - 2] == 0 and self.board.board[i - 1][j - 2] != 0:
                                print("blocked")
                                return j - 1
                        elif j > 2 and self.board.board[i][j] == self.board.board[i - 2][j - 2] == \
                                self.board.board[i - 3][j - 3] == player1.order:
                            print(j, "left diagonal potential 4inarow threat, condition 3")
                            if self.board.board[i - 1][j - 1] == 0 and self.board.board[i][j - 1] != 0:
                                print("blocked")
                                return j
                    except IndexError:
                        pass
                    # y=x대각선
                    try:
                        if j < 4 and self.board.board[i][j] == self.board.board[i - 1][j + 1] == \
                                self.board.board[i - 2][j + 2] == player1.order:
                            print(j, "right diagonal potential 4inarow threat, condition 1")
                            if self.board.board[i - 3][j + 3] == 0 and self.board.board[i - 2][j + 3] != 0:
                                print("blocked")
                                return j + 4
                            elif self.board.board[i + 1][j - 1] == 0:
                                if i == 4:
                                    print("blocked")
                                    return j
                                elif i < 4 and self.board.board[i + 2][j - 1] != 0:
                                    print("blocked")
                                    return j
                        elif j < 4 and self.board.board[i][j] == self.board.board[i - 1][j + 1] == \
                                self.board.board[i - 3][j + 3] == player1.order:
                            print(j, "right diagonal potential 4inarow threat, condition 2")
                            if self.board.board[i - 2][j + 2] == 0 and self.board.board[i - 1][j + 2] != 0:
                                print("blocked")
                                return j + 3
                        elif j < 4 and self.board.board[i][j] == self.board.board[i - 2][j + 2] == \
                                self.board.board[i - 3][j + 3] == player1.order:
                            print(j, "right diagonal potential 4inarow threat, condition 3")
                            if self.board.board[i - 1][j + 1] == 0 and self.board.board[i][j + 1] != 0:
                                print("blocked")
                                return j + 2
                    except IndexError:
                        pass

            # 상대 3개 이어지는 가능성 확인
            for i in range(0, self.ROW):
                for j in range(0, self.COLUMN):
                    # y=-x 대각선
                    try:
                        if j > 2 and self.board.board[i][j] == self.board.board[i - 1][j - 1] == player1.order:
                            print(j, "left diagonal potential 3inarow threat, condtion 1")
                            if self.board.board[i - 2][j - 2] == 0 and self.board.board[i - 1][j - 2] != 0:
                                print("blocked")
                                return j - 1
                            elif self.board.board[i + 1][j + 1] == 0:
                                if self.board.board[i + 2][j + 1] != 0:
                                    print("blocked")
                                    return j + 2
                                elif i == 4:
                                    print("blocked")
                                    return j + 2
                        elif j > 2 and self.board.board[i][j] == self.board.board[i - 2][j - 2] == player1.order:
                            print(j, "left diagonal potential 3inarow threat, condtion 2")
                            if self.board.board[i - 1][j - 1] == 0 and self.board.board[i][j - 1] != 0:
                                print("blocked")
                                return j
                    except IndexError:
                        pass
                    # y=x대각선
                    try:
                        if j < 4 and self.board.board[i][j] == self.board.board[i - 1][j + 1] == player1.order:
                            print(j, "right diagonal potential 3inarow threat, condition 1")
                            if self.board.board[i - 2][j + 2] == 0 and self.board.board[i - 1][j + 2] != 0:
                                print("blocked")
                                return j + 3
                            elif self.board.board[i + 1][j - 1] == 0:
                                if i == 4:
                                    print("blocked")
                                    return j
                                elif i < 4 and self.board.board[i + 2][j - 1] != 0:
                                    print("blocked")
                                    return j
                        elif j < 4 and self.board.board[i][j] == self.board.board[i - 2][j + 2] == player1.order:
                            print(j, "right diagonal potential 3inarow threat, condition 1")
                            if self.board.board[i - 1][j + 1] == 0 and self.board.board[i][j + 1] != 0:
                                print("blocked")
                                return j + 2
                    except IndexError:
                        pass

                    try:
                        # 같은 row에 2개 있을 떄
                        if self.board.board[i][j] == self.board.board[i][j + 1] == player1.order:
                            print(j, "row potential 3inarow threat, condition 1")
                            if j < 5:
                                if self.board.board[i][j - 1] != self.board.board[i][j] and (
                                        i == 5 or (i < 5 and self.board.board[i + 1][j - 1] != 0)):
                                    if (self.board.board[i][j - 1] == 0):
                                        print("blocked")
                                        return j
                            if i == 5 and j < 5:
                                print(i, "row, condition 2")
                                if (self.board.board[i][j + 2] == 0):
                                    print("blocked")
                                    return j + 3
                            if i < 5 and self.board.board[i + 1][j + 2] != 0 and j < 5:
                                print(i, "row, condition 3")
                                if (self.board.board[i][j + 2] == 0):
                                    print("blocked")
                                    return j + 3
                        elif self.board.board[i][j] == self.board.board[i][j + 2] == player1.order:
                            print(j, "row potential 3inarow threat, condition 1")
                            if self.board.board[i][j + 1] == 0:
                                if i == 5:
                                    print("blocked")
                                    return j + 2
                                elif i < 4 and self.board.board[i + 1][j + 1] != 0:
                                    print("blocked")
                                    return j + 2
                    except IndexError:
                        pass

                    try:
                        # 같은 column에 2개 있을 때
                        if self.board.board[i][j] == self.board.board[i - 1][j] == player1.order:
                            print(j, "column potential 3inarow threat")
                            if (self.board.board[i - 2][j] == 0):
                                print("blocked")
                                return j + 1
                    except IndexError:
                        pass

            # 내꺼 3개 이어지는 가능성 확인
            for i in range(0, self.ROW):
                for j in range(0, self.COLUMN):
                    # y=-x 대각선
                    try:
                        if j > 2 and self.board.board[i][j] == self.board.board[i - 1][j - 1] == player2_AI.order:
                            print(j, "left diagonal potential 3inarow, condition 1")
                            if self.board.board[i - 2][j - 2] == 0 and self.board.board[i - 1][j - 2] != 0:
                                return j - 1
                            elif self.board.board[i + 1][j + 1] == 0:
                                if self.board.board[i + 2][j + 1] != 0:
                                    return j + 2
                                elif i == 4:
                                    return j + 2
                        elif j > 2 and self.board.board[i][j] == self.board.board[i - 2][j - 2] == player2_AI.order:
                            print(j, "left diagonal potential 3inarow, condition 2")
                            if self.board.board[i - 1][j - 1] == 0 and self.board.board[i][j - 1] != 0:
                                return j
                    except IndexError:
                        pass
                    # y=x대각선
                    try:
                        if j < 4 and self.board.board[i][j] == self.board.board[i - 1][j + 1] == player2_AI.order:
                            print(j, "right diagonal potential 3inarow, condtion 1")
                            if self.board.board[i - 2][j + 2] == 0 and self.board.board[i - 1][j + 2] != 0:
                                return j + 3
                            elif self.board.board[i + 1][j - 1] == 0:
                                if i == 4:
                                    return j
                                elif i < 4 and self.board.board[i + 2][j - 1] != 0:
                                    return j
                        elif j < 4 and self.board.board[i][j] == self.board.board[i - 2][j + 2] == player2_AI.order:
                            print(j, "right diagonal potential 3inarow, condtion 2")
                            if self.board.board[i - 1][j + 1] == 0 and self.board.board[i][j + 1] != 0:
                                return j + 2
                    except IndexError:
                        pass

                    try:
                        # 같은 row에 2개 있을 떄
                        if self.board.board[i][j] == self.board.board[i][j + 1] == player2_AI.order:
                            print(j, "row potential 3inarow, condition 1")
                            if j < 5:
                                if self.board.board[i][j - 1] != self.board.board[i][j] and (
                                        i == 5 or (i < 5 and self.board.board[i + 1][j - 1] != 0)):
                                    if (self.board.board[i][j - 1] == 0):
                                        return j
                            if i == 5 and j < 5:
                                print(i, "row, condition 2")
                                if (self.board.board[i][j + 2] == 0):
                                    return j + 3
                            if i < 5 and self.board.board[i + 1][j + 2] != 0 and j < 5:
                                if (self.board.board[i][j + 2] == 0):
                                    return j + 3
                        elif self.board.board[i][j] == self.board.board[i][j + 2] == player2_AI.order:
                            print(j, "row potential 3inarow, condition 1")
                            if self.board.board[i][j + 1] == 0:
                                if i == 5:
                                    return j + 2
                                elif i < 4 and self.board.board[i + 1][j + 1] != 0:
                                    return j + 2
                    except IndexError:
                        pass

            # 상대꺼 옆에 놓기
            for i in range(0, self.ROW):
                for j in range(0, self.COLUMN):
                    try:
                        if self.board.board[i][j] == player1.order:
                            if i == 5:
                                if self.board.board[i][j - 1] != 0 and self.board.board[i - 1][j - 1] == 0:
                                    return j
                                elif self.board.board[i][j + 1] != 0 and self.board.board[i - 1][j + 1] == 0:
                                    return j + 2
                                elif self.board.board[i][j - 1] == 0:
                                    return j
                                elif self.board.board[i][j + 1] == 0:
                                    return j + 2
                                elif self.board.board[i - 1][j] == 0:
                                    return j + 1
                            else:
                                if self.board.board[i][j - 1] != 0 and self.board.board[i - 1][j - 1] == 0:
                                    return j
                                elif self.board.board[i][j + 1] != 0 and self.board.board[i - 1][j + 1] == 0:
                                    return j + 2
                                elif self.board.board[i][j - 1] == 0 and self.board.board[i + 1][j - 1] != 0:
                                    return j
                                elif self.board.board[i][j + 1] == 0 and self.board.board[i + 1][j + 1]:
                                    return j + 2
                                elif self.board.board[i - 1][j] == 0:
                                    return j + 1
                    except IndexError:
                        pass

            # 내꺼 옆에 놓기
            for i in range(0, self.ROW):
                for j in range(0, self.COLUMN):
                    # y=-x 대각선
                    try:
                        if self.board.board[i][j] == player2_AI.order:
                            if i == 5:
                                if self.board.board[i][j - 1] != 0 and self.board.board[i - 1][j - 1] == 0:
                                    return j
                                elif self.board.board[i][j + 1] != 0 and self.board.board[i - 1][j + 1] == 0:
                                    return j + 2
                                elif self.board.board[i][j - 1] == 0:
                                    return j
                                elif self.board.board[i][j + 1] == 0:
                                    return j + 2
                                elif self.board.board[i - 1][j] == 0:
                                    return j + 1
                            else:
                                if self.board.board[i][j - 1] != 0 and self.board.board[i - 1][j - 1] == 0:
                                    return j
                                elif self.board.board[i][j + 1] != 0 and self.board.board[i - 1][j + 1] == 0:
                                    return j + 2
                                elif self.board.board[i][j - 1] == 0 and self.board.board[i + 1][j - 1] != 0:
                                    return j
                                elif self.board.board[i][j + 1] == 0 and self.board.board[i + 1][j + 1]:
                                    return j + 2
                                elif self.board.board[i - 1][j] == 0:
                                    return j + 1
                    except IndexError:
                        pass

            return (randint(1, 7))


COLUMN = 7
ROW = 6
firstturn = True

while True:

    print("select game mode")
    print("1 : human vs human 2 : human vs AI\n")
    gameMode = input("type in game mode : ")

    if gameMode == "1":

        player1_name = input("\nType in player1's name : ")
        player2_name = input("\nType in player2's name : ")
        player1 = Player(player1_name, 1, False)
        player2 = Player(player2_name, 2, False)
        board = Board()
        game = Game(board, gameMode, player1, player2)
        break

    elif gameMode == "2":
        player1_name = input("\nType in player1's name : ")
        order = int(input("\nif you want to go first press 1. otherwise press 2 : "))
        aiMode = int(input("\nif you want rule press 1. if you want minimax press 2 : "))
        player1 = Player(player1_name, order, False)
        board = Board()

        if order == 1:
            player2_AI = Player("AI", order + 1, True, aiMode)
            game = Game(board, gameMode, player1, player2_AI)
        else:
            player2_AI = Player("AI", order - 1, True, aiMode)
            game = Game(board, gameMode, player2_AI, player1)
        break
    
    else:
        print("\n***Please type in 1 or 2***\n")
        continue

game.beginGame()