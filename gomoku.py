import sys
import re
import copy
_nsre = re.compile('([0-9]+)')

class Node(object):

    def __init__(self, player, opponent, depth, n, game_board):
        player = player
        opponent = opponent
        self.cutoff = depth
        self.n = n
        self.game_board = game_board
        self.legal_moves = self.find_legal_moves(self.game_board)
        self.score = 0
        self.next_move = []

    def greedy(self, player, game_board):
        max_score = 0
        next_move = []
        for move in self.legal_moves:
            row = move[0]
            col = move[1]
            score = self.evaluate_score(row, col, player, game_board)
            if score > max_score:
                max_score = score
                next_move = [row, col]

        return next_move


    def minimax(self, player):
        max_score = -1e309
        word = "inf"
        rword = "Infinity"
        legal_moves = self.legal_moves
        node_name = "root"
        depth = 0
        value = 0
        line1 = "{0},{1},{2}".format("Move", "Depth", "Value")
        print line1
        line1 = "{0},{1},{2}".format(node_name, depth, max_score)
        line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
        print line1
        next_move = []
        for move in legal_moves:
            depth = 0
            value = 0
            pos_x = move[0]
            pos_y = move[1]
            value = self.min_value(pos_x, pos_y, self.game_board, depth+1, value, player)
            if value > max_score:
                max_score = value
                next_move = [pos_x, pos_y]
            line1 = "{0},{1},{2}".format(node_name, depth, max_score)
            line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
            print line1
        return next_move


    def min_value(self, pos_x, pos_y, game_board, depth, value, player):
        word = "inf"
        rword = "Infinity"
        bestvalue = 1e309
        temp_val = self.evaluate_score(pos_x,pos_y, player, game_board)

        if int(depth) == int(self.cutoff):
            value += temp_val
            line1 = "{0},{1},{2}".format(self.label([pos_x, pos_y]), depth, value)
            line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
            print line1
            return value

        if temp_val >= 50000:
            value += temp_val
            line4 = "{0},{1},{2}".format(self.label([pos_x, pos_y]), depth, value)
            line4 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line4)
            print line4
            return value

        line2 = "{0},{1},{2}".format(self.label([pos_x, pos_y]), depth, bestvalue)
        line2 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line2)
        print line2

        value += temp_val
        new_game_board = self.update_game_board(game_board, player, pos_x, pos_y)
        moves = self.find_legal_moves(new_game_board)

        for move in moves:
            row = move[0]
            col = move[1]
            bestvalue = min(bestvalue, self.max_value(row, col, new_game_board, depth + 1, value, player))
            line3 = "{0},{1},{2}".format(self.label([pos_x, pos_y]), depth, bestvalue)
            line3 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line3)
            print line3

        return bestvalue

    def max_value(self, pos_x, pos_y, game_board, depth, value, player):
        #print "max player = " +str(player)
        word = "inf"
        rword = "Infinity"
        bestvalue = -1e309
        temp_val = self.evaluate_score(pos_x, pos_y, self.find_opponent(player), game_board)

        if int(depth) == int(self.cutoff):
            value -= temp_val
            line4 = "{0},{1},{2}".format(self.label([pos_x, pos_y]), depth, value)
            line4 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line4)
            print line4
            return value

        if temp_val >= 50000:
            value -= temp_val
            line4 = "{0},{1},{2}".format(self.label([pos_x, pos_y]), depth, value)
            line4 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line4)
            print line4
            return value

        line6 = "{0},{1},{2}".format(self.label([pos_x, pos_y]), depth, bestvalue)
        line6 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line6)
        print line6

        value -= temp_val
        new_game_board = self.update_game_board(game_board, self.find_opponent(player), pos_x, pos_y)
        moves = self.find_legal_moves(new_game_board)

        for move in moves:
            row = move[0]
            col = move[1]

            bestvalue = max(bestvalue, self.min_value(row, col, new_game_board, depth + 1, value, player))
            line5 = "{0},{1},{2}".format(self.label([pos_x, pos_y]), depth, bestvalue)
            line5 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line5)
            print line5
        return bestvalue

    def alphabeta(self, player):
        max_score = -1e309
        word = "inf"
        rword = "Infinity"
        alpha = -1e309
        beta = 1e309
        depth = 0
        legal_moves = self.legal_moves
        node_name = "root"
        line1 = "{0},{1},{2},{3},{4}".format("Move", "Depth", "Value", "Alpha", "Beta")
        print line1
        line1 = "{0},{1},{2},{3},{4}".format(node_name, depth, max_score, alpha, beta)
        line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
        print line1
        for move in legal_moves:
            depth = 0
            value = 0
            pos_x = move[0]
            pos_y = move[1]
            value = self.alphabeta_min(pos_x, pos_y, self.game_board, depth + 1, value, player, alpha, beta)
            if value > max_score:
                max_score = value
                next_move = [pos_x, pos_y]
            alpha = max(alpha, max_score)
            line1 = "{0},{1},{2},{3},{4}".format(node_name, depth, max_score, alpha, beta)
            line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
            print line1
        return next_move

    def alphabeta_max(self, pos_x, pos_y, game_board, depth, value, player, alpha, beta):
        # print "max player = " +str(player)
        word = "inf"
        rword = "Infinity"
        bestvalue = -1e309
        temp_val = self.evaluate_score(pos_x, pos_y, self.find_opponent(player), game_board)

        if int(depth) == int(self.cutoff):
            value -= temp_val
            line1 = "{0},{1},{2},{3},{4}".format(self.label([pos_x, pos_y]), depth, value, alpha, beta)
            line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
            print line1
            return value

        if temp_val >= 50000:
            value -= temp_val
            line1 = "{0},{1},{2},{3},{4}".format(self.label([pos_x, pos_y]), depth, value, alpha, beta)
            line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
            print line1
            return value

        line1 = "{0},{1},{2},{3},{4}".format(self.label([pos_x, pos_y]), depth, bestvalue, alpha, beta)
        line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
        print line1

        value -= temp_val
        new_game_board = self.update_game_board(game_board, self.find_opponent(player), pos_x, pos_y)
        moves = self.find_legal_moves(new_game_board)

        for move in moves:
            row = move[0]
            col = move[1]
            bestvalue = max(bestvalue, self.alphabeta_min(row, col, new_game_board, depth + 1, value, player, alpha, beta))
            if bestvalue >= beta:
                line1 = "{0},{1},{2},{3},{4}".format(self.label([pos_x, pos_y]), depth, bestvalue, alpha, beta)
                line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
                print line1
                return bestvalue
            alpha = max(alpha, bestvalue)
            line1 = "{0},{1},{2},{3},{4}".format(self.label([pos_x, pos_y]), depth, bestvalue, alpha, beta)
            line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
            print line1
        return bestvalue

    def alphabeta_min(self, pos_x, pos_y, game_board, depth, value, player, alpha, beta):
        # print "min player = " + str(player)
        word = "inf"
        rword = "Infinity"
        bestvalue = 1e309
        temp_val = self.evaluate_score(pos_x, pos_y, player, game_board)

        if int(depth) == int(self.cutoff):
            value += temp_val
            line1 = "{0},{1},{2},{3},{4}".format(self.label([pos_x, pos_y]), depth, value, alpha, beta)
            line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
            print line1
            return value

        if temp_val >= 50000:
            value += temp_val
            line1 = "{0},{1},{2},{3},{4}".format(self.label([pos_x, pos_y]), depth, value, alpha, beta)
            line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
            print line1
            return value

        line1 = "{0},{1},{2},{3},{4}".format(self.label([pos_x, pos_y]), depth, bestvalue, alpha, beta)
        line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
        print line1

        value += temp_val
        new_game_board = self.update_game_board(game_board, player, pos_x, pos_y)
        moves = self.find_legal_moves(new_game_board)

        for move in moves:
            row = move[0]
            col = move[1]
            bestvalue = min(bestvalue, self.alphabeta_max(row, col, new_game_board, depth + 1, value, player, alpha, beta))
            if bestvalue <= alpha:
                line1 = "{0},{1},{2},{3},{4}".format(self.label([pos_x, pos_y]), depth, bestvalue, alpha, beta)
                line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
                print line1
                return bestvalue
            beta = min(beta, bestvalue)
            line1 = "{0},{1},{2},{3},{4}".format(self.label([pos_x, pos_y]), depth, bestvalue, alpha, beta)
            line1 = re.sub(r'\b{0}\b'.format(re.escape(str(word))), rword, line1)
            print line1
        return bestvalue




    def find_opponent(self,player):
        if player == 'b':
            return 'w'
        else:
            return 'b'

    def find_legal_moves(self, game_board):
        moves = []
        for i in range(0, self.n):
            for j in range(0, self.n):
                if game_board[i][j] != '.':
                    if i - 1 > -1 and j - 1 > -1 and game_board[i - 1][j - 1] == '.':
                        tmp = [i - 1, j - 1]
                        moves.append(tmp)
                    if i - 1 > -1 and game_board[i - 1][j] == '.':
                        tmp = [i - 1, j]
                        moves.append(tmp)
                    if i - 1 > -1 and j + 1 <= self.n - 1 and game_board[i - 1][j + 1] == '.':
                        tmp = [i - 1, j + 1]
                        moves.append(tmp)
                    if j - 1 > -1 and game_board[i][j - 1] == '.':
                        tmp = [i, j - 1]
                        moves.append(tmp)
                    if j + 1 <= self.n - 1 and game_board[i][j + 1] == '.':
                        tmp = [i, j + 1]
                        moves.append(tmp)
                    if i + 1 <= self.n - 1 and j - 1 > -1 and game_board[i + 1][j - 1] == '.':
                        tmp = [i + 1, j - 1]
                        moves.append(tmp)
                    if i + 1 <= self.n - 1 and game_board[i + 1][j] == '.':
                        tmp = [i + 1, j]
                        moves.append(tmp)
                    if i + 1 <= self.n - 1 and j + 1 <= self.n - 1 and game_board[i + 1][j + 1] == '.':
                        tmp = [i + 1, j + 1]
                        moves.append(tmp)
                    else:
                        continue
        moves = sorted(moves)
        moves = [moves[i] for i in range(len(moves)) if i == 0 or moves[i] != moves[i - 1]]
        legal_moves = []
        for move in moves:
            new = self.label(move)
            legal_moves.append(new)
        legal_moves.sort(key=self.natural_sort_key)
        final_legal_moves = []
        for move in legal_moves:
            old = self.de_label(move)
            final_legal_moves.append(old)
        return final_legal_moves

    def natural_sort_key(self, s):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split(_nsre, s)]

    def label(self, move):
        dict = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F', '6': 'G', '7': 'H', '8': 'I', '9': 'J','10': 'K', \
                '11': 'L', '12': 'M', '13': 'N', '14': 'O', '15': 'P', '16': 'Q', '17': 'R', '18': 'S', '19': 'T','20': 'U', '21': 'V', '22': 'W', '23': 'X', '24': 'Y', '25': 'Z'}
        row = move[0]
        col = move[1]
        row = row + 1
        col = dict[str(col)]
        name = str(col) + str(row)
        return name

    def de_label(self, move):
        dict = {'A': '0', 'B': '1', 'C': '2', 'D': '3', 'E': '4', 'F': '5', 'G': '6', 'H': '7', 'I': '8', 'J': '9','K': '10', 'L': '11', 'M': '12', 'N': '13', 'O': '14', \
                'P': '15', 'Q': '16', 'R': '17', 'S': '18', 'T': '19', 'U': '20', 'V': '21', 'W': '22', 'X': '23','Y': '24', 'Z': '25'}

        regex = re.compile(r'(\d+|\s+)')
        move = regex.split(move)
        row = move[0]
        col = move[1]
        col = int(col) - 1
        row = int(dict[row])
        return [col, row]

    def update_game_board(self, game_board, player, row, col):
        new_board = copy.deepcopy(game_board)
        new_board[row][col] = player
        return new_board


    def evaluate_score(self, row, col, player, game_board):
        score = 0
        win = self.find_win(player, row, col, game_board)
        score += 50000 * win
        blockClosed = self.find_blockClosed(player, row, col, game_board)
        score += 10000 * blockClosed[0] + 100 * blockClosed[1]
        createOpen = self.find_createOpen(player, row, col, game_board)
        score += 5000 * createOpen[0] + 50 * createOpen[1] + 5 * createOpen[2]
        createClosed = self.find_createClosed(player, row, col, game_board)
        score += 1000 * createClosed[0] + 10 * createClosed[1] + 1 * createClosed[2]
        blockOpenThree = self.find_blockOpenThree(player, row, col, game_board)
        score += 500 * blockOpenThree
        return score




    def find_win(self, player, row, col, game_board):
        count = 0
        countwin = 0
        #check left
        for i in range(1,5):
            if col-i > -1:
                if game_board[row][col-i] != player:
                    break
                else:
                    count += 1
        #check right
        for i in range(1,5):
            if col+i <= self.n-1:
                if game_board[row][col+i] != player:
                    break
                else:
                    count += 1
        if count >= 4:
            countwin += 1
        count = 0
        #check up
        for i in range(1,5):
            if row-i > -1:
                if game_board[row-i][col] != player:
                    break
                else:
                    count += 1
        #check down
        for i in range(1,5):
            if row+i <= self.n-1:
                if game_board[row+i][col] != player:
                    break
                else:
                    count += 1
        if count >= 4:
            countwin += 1
        count = 0
        #check left diagonal
        for i in range(1,5):
            if row-i > -1 and col-i > -1:
                if game_board[row-i][col-i] != player:
                    break
                else:
                    count += 1
        for i in range(1,5):
            if row+i <= self.n-1 and col+i <= self.n -1:
                if game_board[row+i][col+i] != player:
                    break
                else:
                    count += 1
        if count >=4:
            countwin += 1
        count = 0
        #check right diagonal
        for i in range(1,5):
            if row+i <= self.n-1 and col-i >-1:
                if game_board[row+i][col-i] != player:
                    break
                else:
                    count += 1
        for i in range(1,5):
            if row-i>-1 and col+i <= self.n-1:
                if game_board[row-i][col+i] != player:
                    break
                else:
                    count += 1
        if count >= 4:
            countwin += 1
        count = 0
        return countwin

    def find_blockClosed(self, player, row, col, game_board):
        count = 0
        count4 = 0
        count3 = 0
        if player == 'b':
            opponent = 'w'
        elif player == 'w':
            opponent = 'b'
        #check left
        for i in range(1,5):
            if col-i>-1:
                if game_board[row][col-i] != opponent:
                    break
                else:
                    count += 1
        if count == 4:
            if col-5 > -1 and game_board[row][col-5] == player or col-5 < 0:
                count4 += 1
        elif count == 3:
            if (col-4 > -1 and game_board[row][col-4] == player) or col-4 < 0:
                count3 += 1
        count = 0
        #check right
        for i in range(1,5):
            if col+i<=self.n-1:
                if game_board[row][col+i] != opponent:
                    break
                else:
                    count += 1
        if count == 4:
            if (col+5 <= self.n-1 and game_board[row][col+5] == player) or col+5 >= self.n-1:
                count4 += 1
        elif count == 3:
            if (col + 4 <= self.n - 1 and game_board[row][col + 4] == player) or col+4 >= self.n-1:
                count3 += 1
        count = 0
        #check up
        for i in range(1,5):
            if row-i>-1:
                if game_board[row-i][col] != opponent:
                    break
                else:
                    count += 1
        if count == 4:
            if (row-5 > -1 and game_board[row-5][col] == player) or row-5 < 0:
                count4 += 1
        elif count == 3:
            if (row - 4 > -1 and game_board[row - 4][col] == player) or row - 4 < 0:
                count3 += 1
        count = 0
        #check down
        for i in range(1,5):
            if row+i<=self.n-1:
                if game_board[row+i][col] != opponent:
                    break
                else:
                    count += 1
        if count == 4:
            if (row+5 <= self.n-1 and game_board[row+5][col] == player) or row+5 > self.n-1:
                count4 += 1
        elif count == 3:
            if (row+4 <= self.n - 1 and game_board[row+4][col] == player) or row+4 > self.n-1:
                count3 += 1
        count = 0
        #check left upper diagonal
        for i in range(1,5):
            if row-i >-1 and col-i >-1:
                if game_board[row-i][col-i] != opponent:
                    break
                else: count += 1
        if count == 4:
            if (row-5 > -1 and col-5 > -1 and game_board[row-5][col-5] == player) or row-5 < 0 or col-5 < 0:
                count4 += 1
        elif count == 3:
            if (row-4 > -1 and col-4 >-1 and game_board[row-4][col-4] == player) or row-4 < 0 or col-4 < 0:
                count3 += 1
        count = 0
        #check lower left diagonal
        for i in range(1, 5):
            if row+i <=self.n-1 and col-i>-1:
                if game_board[row+i][col - i] != opponent:
                    break
                else:
                    count += 1
        if count == 4:
            if (row+5<=self.n-1 and col-5>-1 and game_board[row+5][col-5] == player) or row+5 > self.n-1 or col-5<0:
                count4 += 1
        elif count == 3:
            if (row + 4 <= self.n - 1 and col - 4 > -1 and game_board[row + 4][col - 4] == player) or row + 4 > self.n - 1 or col - 4 < 0:
                count3 += 1
        count = 0
        #check upper right diagonal
        for i in range(1, 5):
            if row-i >-1 and col+i <=self.n-1:
                if game_board[row - i][col+i] != opponent:
                    break
                else:
                    count += 1
        if count == 4:
            if (row - 5 > -1 and col + 5 <=self.n-1 and game_board[row - 5][col + 5] == player) or row - 5 < 0 or col + 5>self.n-1:
                count4 += 1
        elif count == 3:
            if (row - 4 > -1 and col + 4 <= self.n - 1 and game_board[row - 4][col + 4] == player) or row - 4 < 0 or col + 4 > self.n - 1:
                count3 += 1
        count = 0
        #check lower right diagonal
        for i in range(1, 5):
            if row + i <= self.n - 1 and col + i <=self.n -1:
                if game_board[row + i][col + i] != opponent:
                    break
                else:
                    count += 1
        if count == 4:
            if (row + 5 <= self.n - 1 and col + 5 <=self.n -1 and game_board[row + 5][col + 5] == player) or row + 5 > self.n - 1 or col + 5 >self.n-1:
                count4 += 1
        elif count == 3:
            if (row + 4 <= self.n - 1 and col + 4 <= self.n - 1 and game_board[row + 4][col + 4] == player) or row + 4 > self.n - 1 or col + 4 > self.n - 1:
                count3 += 1
        #print "blockClosed = " + str([count4, count3])
        return [count4, count3]

    def find_createOpen(self, player, row, col, game_board):
        lcount = 0
        rcount = 0
        count4 = 0
        count3 = 0
        count2 = 0
        #left
        for i in range(1, 5):
            if col-i > -1 and game_board[row][col - i] == player:
                lcount += 1
            else: break
        #right
        for i in range(1,5):
            if col+i <= self.n-1 and game_board[row][col+i] == player:
                rcount += 1
            else: break
        if col+rcount+1 <= self.n-1 and col-lcount-1 > -1 and game_board[row][col+rcount+1] == '.' and game_board[row][col-lcount-1] == '.':
            if lcount+rcount == 3:
                count4 += 1
            elif lcount + rcount == 2:
                count3 += 1
            elif lcount+rcount == 1:
                count2 += 1
        lcount = 0
        rcount = 0
        #up
        for i in range(1,5):
            if row-i > -1 and game_board[row-i][col] == player:
                lcount += 1
            else: break
        #down
        for i in range(1,5):
            if row+i <= self.n-1 and game_board[row+i][col] == player:
                rcount += 1
            else: break
        if row-lcount-1 > -1 and row+rcount+1 <= self.n-1 and game_board[row-lcount-1][col] == '.'and game_board[row+rcount+1][col] == '.':
            if lcount + rcount == 3:
                count4 += 1
            elif lcount + rcount == 2:
                count3 += 1
            elif lcount + rcount == 1:
                count2 += 1
        lcount = 0
        rcount = 0
        #left diagonal up
        for i in range(1,5):
            if row-i > -1 and col-i > -1 and game_board[row-i][col-i] == player:
                lcount += 1
            else: break
        #left diagonal down
        for i in range(1,5):
            if row+i <= self.n-1 and col+i <= self.n-1 and game_board[row+i][col+i] == player:
                rcount += 1
            else: break
        if row-lcount-1 > -1 and col-lcount-1 > -1 and row+rcount+1 <= self.n-1 and col+rcount+1 <= self.n-1 \
                and game_board[row-lcount-1][col-lcount-1] == '.' and game_board[row+rcount+1][col+rcount+1] =='.':
            if lcount + rcount == 3:
                count4 += 1
            elif lcount + rcount == 2:
                count3 += 1
            elif lcount + rcount == 1:
                count2 += 1
        lcount = 0
        rcount = 0
        #right diagonal up
        for i in range(1,5):
            if row-i > -1 and col+i <= self.n-1 and game_board[row-i][col+i] == player:
                lcount += 1
            else: break
        #right diagonal down
        for i in range(1,5):
            if row+i <= self.n-1 and col-i > -1 and game_board[row+i][col-i] == player:
                rcount += 1
            else: break
        if row-lcount-1 > -1 and col+lcount+1 <= self.n-1 and row+rcount+1 <= self.n-1 and col-rcount-1 > -1 \
                and game_board[row-lcount-1][col+lcount+1] == '.' and game_board[row+rcount+1][col-rcount-1] == '.':
            if lcount + rcount == 3:
                count4 += 1
            elif lcount + rcount == 2:
                count3 += 1
            elif lcount + rcount == 1:
                count2 += 1
        return [count4, count3, count2]

    def find_createClosed(self, player, row, col, game_board):
        lcount = 0
        rcount = 0
        count4 = 0
        count3 = 0
        count2 = 0
        if player == 'b':
            opponent = 'w'
        elif player == 'w':
            opponent = 'b'
        # left
        for i in range(1, 5):
            if col - i > -1 and game_board[row][col - i] == player:
                lcount += 1
            else: break
        # right
        for i in range(1, 5):
            if col + i <= self.n - 1 and game_board[row][col + i] == player:
                rcount += 1
            else: break
        if col-lcount-1 <0 or col+rcount+1 > self.n-1 or game_board[row][col-lcount-1] == "." \
                and game_board[row][col+rcount+1] == opponent or game_board[row][col-lcount-1] == opponent \
                and game_board[row][col+rcount+1] == '.':
            if lcount + rcount == 3:
                count4 += 1
            elif lcount + rcount == 2:
                count3 += 1
            elif lcount + rcount == 1:
                count2 += 1
        lcount = 0
        rcount = 0
        #up
        for i in range(1,5):
            if row - i >-1 and game_board[row-i][col] == player:
                lcount += 1
            else: break
        #down
        for i in range(1,5):
            if row+i <=self.n-1 and game_board[row+i][col] == player:
                rcount += 1
            else: break
        if row-lcount-1 < 0 or row+rcount+1 >self.n-1 or game_board[row-lcount-1][col] == '.' and \
                        game_board[row+rcount+1][col] == opponent or game_board[row-lcount-1][col] == opponent \
                and game_board[row+rcount+1][col] == '.':
            if lcount + rcount == 3:
                count4 += 1
            elif lcount + rcount == 2:
                count3 += 1
            elif lcount + rcount == 1:
                count2 += 1
        lcount = 0
        rcount = 0
        #left diagonal up
        for i in range(1,5):
            if row-i >-1 and col-i > -1 and game_board[row-i][col-i] == player:
                lcount += 1
            else: break
        #left diagonal down
        for i in range(1,5):
            if row+i <=self.n-1 and col+i <=self.n-1 and game_board[row+i][col+i] == player:
                rcount += 1
            else: break
        if row-lcount-1 < 0 or col-lcount-1 <0 or row+rcount+1 >self.n-1 or col+rcount+1 >self.n-1 or \
                                game_board[row-lcount-1][col-lcount-1] == '.' and game_board[row+rcount+1][col+rcount+1] == opponent \
                or game_board[row-lcount-1][col-lcount-1] == opponent and game_board[row+rcount+1][col+rcount+1] == '.':
            if lcount + rcount == 3:
                count4 += 1
            elif lcount + rcount == 2:
                count3 += 1
            elif lcount + rcount == 1:
                count2 += 1
        lcount = 0
        rcount = 0
        #right diagonal up
        for i in range(1,5):
            if row-i > -1 and col+i <=self.n-1 and game_board[row-i][col+i] == player:
                lcount += 1
            else: break
        #right diagonal down
        for i in range(1,5):
            if row+i <= self.n-1 and col-i > -1 and game_board[row+i][col-i] == player:
                rcount += 1
            else: break
        if row-lcount-1 <0 or col+lcount+1 > self.n-1 or row+rcount+1 > self.n-1 or col-rcount-1 < 0 or game_board[row-lcount-1][col+lcount+1] == '.'\
                and game_board[row+rcount+1][col-rcount-1] == opponent or game_board[row-lcount-1][col+lcount+1] == opponent \
                and game_board[row+rcount+1][col-rcount-1] == '.':
            if lcount + rcount == 3:
                count4 += 1
            elif lcount + rcount == 2:
                count3 += 1
            elif lcount + rcount == 1:
                count2 += 1
        lcount = 0
        rcount = 0
        #print "createClosed = " +str([count4, count3, count2])
        return [count4, count3, count2]

    def find_blockOpenThree(self, player, row, col, game_board):
        count = 0
        count3 = 0
        if player == 'b':
            opponent = 'w'
        elif player == 'w':
            opponent = 'b'
        # check left
        for i in range(1, 4):
            if col - i > -1 and game_board[row][col - i] != opponent:
                break
            else:
                count += 1
        if count == 3:
            if col - 4 > -1 and game_board[row][col - 4] == '.':
                count3 += 1
        count = 0
        #check right
        for i in range(1,4):
            if col+i <= self.n-1 and game_board[row][col+i] != opponent:
                break
            else: count += 1
        if count == 3:
            if col+4 <=self.n-1 and game_board[row][col+4] == '.':
                count3 += 1
        count = 0
        #check up
        for i in range(1,4):
            if row-i> -1 and game_board[row-i][col] != opponent:
                break
            else: count += 1
        if count == 3:
            if row-4 > -1 and game_board[row-4][col] == '.':
                count3 += 1
        count =0
        #check down
        for i in range(1,4):
            if row+i <=self.n-1 and game_board[row+i][col] != opponent:
                break
            else: count += 1
        if count == 3:
            if row+4 <= self.n-1 and game_board[row+4][col] == '.':
                count3 += 1
        count = 0
        #check left diagonal up
        for i in range(1,4):
            if row-i >-1 and col-i >-1 and game_board[row-i][col-i] != opponent:
                break
            else: count += 1
        if count == 3:
            if row-4 > -1 and col-4 > -1 and game_board[row-4][col-4] == '.':
                count3 += 1
        count = 0
        #check left diagonal down
        for i in range(1,4):
            if row+i <= self.n-1 and col+i <=self.n-1 and game_board[row+i][col+i] != opponent:
                break
            else: count += 1
        if count == 3:
            if row+4 <= self.n-1 and col+4 <= self.n-1 and game_board[row+4][col+4] == '.':
                count3 += 1
        count = 0
        #check right diagonal up
        for i in range(1,4):
            if row-i > -1 and col+i <= self.n-1 and game_board[row-i][col+i] != opponent:
                break
            else: count += 1
        if count == 3:
            if row-4 > -1 and col+4 <= self.n-1 and game_board[row-4][col+4] == '.':
                count3 += 1
        count = 0
        #check right diagonal down
        for i in range(1,4):
            if row+i <= self.n-1 and col-i > -1 and game_board[row+i][col-i] != opponent:
                break
            else: count += 1
        if count == 3:
            if row+4 <= self.n-1 and col-4 > -1 and game_board[row+4][col-4] == '.':
                count3 += 1
        count = 0
        #print "blockOpenThree = " + str(count3)
        return count3

def main():
    #fname =  sys.argv[1]
    #ip_file = open(fname, "r")
    ip_file = open("input_37.txt", "r")
    line = ip_file.read().splitlines()
    isEmpty = False
    task = line[0]
    player = line[1]
    opponent = " "
    if player == '1':
        player = 'b'
        opponent = 'w'
    elif player == '2':
        player = 'w'
        opponent = 'b'
    depth = int(line[2])
    n = int(line[3])

    game_board = []

    for i in range(3 + n, 3, -1):
        game_board.append(list(line[i]))

    count = 0
    for i in range(3+n,3, -1):
        tmp = set(line[i])
        if tmp & set('b') == set([]) and tmp & set('w') == set([]):
            count += 1
    if count == n:
        isEmpty = True
        f_op1 = open("next_state.txt", "w+")
        sys.stdout = f_op1
        game_board[n/2][n/2] = player
        for line in reversed(game_board):
            print "".join(map(str, line))


    if isEmpty == False:
        node = Node(player,opponent,depth, n, game_board)
        if task == '1':
            f_op1 = open("next_state.txt", "w+")
            sys.stdout = f_op1
            best_move = node.greedy(player, game_board)
            game_board[best_move[0]][best_move[1]] = player
            for line in reversed(game_board):
                print "".join(map(str, line))
            f_op1.close()
        elif task == '2':
            #tmp = sys.stdout
            max_score = 0
            f_op2 = open("traverse_log.txt", "w+")
            sys.stdout = f_op2
            best_move = node.minimax(player)
            game_board[best_move[0]][best_move[1]] = player
            f_op2.close()
            f_op3 = open("next_state.txt", "w+")
            sys.stdout = f_op3
            for line in reversed(game_board):
                print "".join(map(str, line))
            f_op3.close()
            #sys.stdout = tmp
            #print node.label(best_move)
        elif task == '3':
            f_op4 = open("traverse_log.txt", "w+")
            sys.stdout = f_op4
            best_move = node.alphabeta(player)
            game_board[best_move[0]][best_move[1]] = player
            f_op4.close()
            f_op5 = open("next_state.txt", "w+")
            sys.stdout = f_op5
            for line in reversed(game_board):
                print "".join(map(str, line))
            f_op5.close()

if __name__ == '__main__':
    main()