import math, random, time, tqdm
from data import colors

class TicTacToe():
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    def make_board():
        return ['-' for _ in range(9)]

    def print_board(self):
        for row in [self.board[i*3:(i+1) * 3] for i in range(3)]:
            print(' | '.join(row))

    @staticmethod
    def print_board_nums():
        number_board = [[str(i+1) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print(' | '.join(row))

    def make_move(self, square, letter):
        if self.board[square] == '-':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check the row
        row_ind = math.floor(square / 3)
        row = self.board[row_ind*3:(row_ind+1)*3]
        # print('row', row)
        if all([s == letter for s in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        # print('col', column)
        if all([s == letter for s in column]):
            return True
        if square % 2 == 0:
            diagonal_1 = [self.board[i] for i in [0, 4, 8]]
            # print('diag1', diagonal1)
            if all([s == letter for s in diagonal_1]): return True
            diagonal_2 = [self.board[i] for i in [2, 4, 6]]
            # print('diag2', diagonal2)
            if all([s == letter for s in diagonal_2]): return True
        return False

    def empty_squares(self):
        return '-' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == "-"]


class Player():
    def __init__(self, letter, name):
        self.letter = letter
        self.name = name

    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, letter, name):
        super().__init__(letter, name)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(colors['cian']+self.name + '\'s turn. Input move (0-9): '+colors['end'])
            try:
                val = int(square)
                val -= 1
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print(colors['red']+'Invalid square. Try again.'+colors['end'])
        return val


class SmartComputerPlayer(Player):
    def __init__(self, letter, name):
        super().__init__(letter, name)

    def get_move(self, game):
        print(colors['cian']+'Machine is working...'+colors['end'])
        for i in tqdm.trange(10):
            time.sleep(0.1)
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # yourself
        other_player = 'O' if player == 'X' else 'X'

        # first we want to check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}
        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # each score should maximize
        else: best = {'position': None, 'score': math.inf}  # each score should minimize
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)  # simulate a game after making that move

            # undo move
            state.board[possible_move] = '-'
            state.current_winner = None
            sim_score['position'] = possible_move  # this represents the move optimal next move

            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best
    

def play(game, name, x_player, o_player, print_game=True):

    print(colors['cian']+f'Welcome {name}, this is te Tic Tac Toe game.'+colors['end'])
    time.sleep(1)
    print(colors['cian']+f'To play, just select the number os the square that you want, following the schematic below.'+colors['end'])
    time.sleep(1)

    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        if game.make_move(square, letter):

            if print_game:
                print(colors['cian']+letter+f' makes a move to square {square}'+colors['end'])
                game.print_board()
            
            if game.current_winner:
                if print_game:
                    print(colors['green']+letter+' wins!'+colors['end'])
                return letter  # ends the loop and exits the game
            letter = 'O' if letter == 'X' else 'X'  # switches player

        time.sleep(1)

    if print_game:
        print(colors['yellow']+'It\'s a tie!'+colors['end'])


if __name__ == '__main__':
    x_player = SmartComputerPlayer('X', 'Machine')
    name = input(colors['cian']+'What\'s your name ? '+colors['end']).strip().capitalize()
    o_player = HumanPlayer('O', name)
    t = TicTacToe()
    play(t, name, x_player, o_player, print_game=True)
    