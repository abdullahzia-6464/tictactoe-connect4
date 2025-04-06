class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.move_count = 0
    
    def print_board(self):
        print('  0 1 2')
        for i in range(3):
            print(f'{i} {self.board[i][0]}|{self.board[i][1]}|{self.board[i][2]}')
            if i < 2:
                print('  -+-+-')
    
    def make_move(self, row, col):
        if self.game_over:
            return False
        
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
            
        if self.board[row][col] != ' ':
            return False
            
        self.board[row][col] = self.current_player
        self.move_count += 1
        
        # Check for win
        if self.check_winner():
            self.winner = self.current_player
            self.game_over = True
        # Check for draw
        elif self.move_count == 9:
            self.game_over = True
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
        return True
    
    def check_winner(self):
        # Check rows
        for i in range(3):
            if self.board[i][0] != ' ' and self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return True
        
        # Check columns
        for i in range(3):
            if self.board[0][i] != ' ' and self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return True
        
        # Check diagonals
        if self.board[0][0] != ' ' and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return True
            
        if self.board[0][2] != ' ' and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return True
            
        return False
    
    def get_valid_moves(self):
        if self.game_over:
            return []
            
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    moves.append((i, j))
        return moves
    
    def get_state(self):
        return [row[:] for row in self.board], self.current_player, self.game_over, self.winner
    
    def set_state(self, state):
        board, current_player, game_over, winner = state
        self.board = [row[:] for row in board]
        self.current_player = current_player
        self.game_over = game_over
        self.winner = winner
        self.move_count = sum(row.count('X') + row.count('O') for row in self.board)

def play_game(player1, player2):
    game = TicTacToe()
    players = {'X': player1, 'O': player2}
    
    while not game.game_over:
        game.print_board()
        current_player = players[game.current_player]
        row, col = current_player.get_move(game)
        
        if not game.make_move(row, col):
            print("Invalid move, try again.")
            continue
    
    game.print_board()
    if game.winner:
        print(f"Player {game.winner} wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    class HumanPlayer:
        def get_move(self, game):
            while True:
                try:
                    row = int(input(f"Player {game.current_player}, enter row (0-2): "))
                    col = int(input(f"Player {game.current_player}, enter col (0-2): "))
                    return row, col
                except ValueError:
                    print("Please enter valid integers.")
    
    play_game(HumanPlayer(), HumanPlayer()) 