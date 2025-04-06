class Connect4:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.move_count = 0
    
    def print_board(self):
        print(' ' + ' '.join(str(i) for i in range(self.cols)))
        for row in self.board:
            print('|' + '|'.join(row) + '|')
        print('-' * (self.cols * 2 + 1))
    
    def is_column_full(self, col):
        return self.board[0][col] != ' '
    
    def drop_piece(self, col):
        if self.game_over:
            return False
            
        if not (0 <= col < self.cols):
            return False
            
        if self.is_column_full(col):
            return False
            
        # Find the lowest empty cell in the column
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = self.current_player
                self.move_count += 1
                break
        
        # Check for win
        if self.check_winner():
            self.winner = self.current_player
            self.game_over = True
        # Check for draw
        elif self.move_count == self.rows * self.cols:
            self.game_over = True
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
        return True
    
    def check_winner(self):
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if (self.board[row][col] != ' ' and
                    self.board[row][col] == self.board[row][col+1] == 
                    self.board[row][col+2] == self.board[row][col+3]):
                    return True
        
        # Check vertical
        for row in range(self.rows - 3):
            for col in range(self.cols):
                if (self.board[row][col] != ' ' and
                    self.board[row][col] == self.board[row+1][col] == 
                    self.board[row+2][col] == self.board[row+3][col]):
                    return True
        
        # Check diagonal (positive slope)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if (self.board[row][col] != ' ' and
                    self.board[row][col] == self.board[row+1][col+1] == 
                    self.board[row+2][col+2] == self.board[row+3][col+3]):
                    return True
        
        # Check diagonal (negative slope)
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if (self.board[row][col] != ' ' and
                    self.board[row][col] == self.board[row-1][col+1] == 
                    self.board[row-2][col+2] == self.board[row-3][col+3]):
                    return True
                    
        return False
    
    def get_valid_moves(self):
        if self.game_over:
            return []
            
        return [col for col in range(self.cols) if not self.is_column_full(col)]
    
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
    game = Connect4()
    players = {'X': player1, 'O': player2}
    
    while not game.game_over:
        game.print_board()
        current_player = players[game.current_player]
        col = current_player.get_move(game)
        
        if not game.drop_piece(col):
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
                    col = int(input(f"Player {game.current_player}, choose column (0-6): "))
                    return col
                except ValueError:
                    print("Please enter a valid integer.") 