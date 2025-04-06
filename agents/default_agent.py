import random

class DefaultAgent:
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol
        
    def get_move(self, game):
        # Try to find a winning move
        winning_move = self.find_winning_move(game)
        if winning_move is not None:
            return winning_move
            
        # Try to find a blocking move
        blocking_move = self.find_blocking_move(game)
        if blocking_move is not None:
            return blocking_move
            
        # Make a random move
        valid_moves = game.get_valid_moves()
        return random.choice(valid_moves)
        
    def find_winning_move(self, game):
        return self._find_critical_move(game, self.player_symbol)
        
    def find_blocking_move(self, game):
        opponent = 'O' if self.player_symbol == 'X' else 'X'
        return self._find_critical_move(game, opponent)
        
    def _find_critical_move(self, game, player_symbol):
        """Find a move that would result in a win for the given player symbol."""
        valid_moves = game.get_valid_moves()
        original_state = game.get_state()
        
        for move in valid_moves:
            # Save current game state
            current_player = game.current_player
            
            # Temporarily set current player to the player we're checking for
            game.current_player = player_symbol
            
            # Try the move
            if hasattr(game, 'make_move'):  # For TicTacToe
                row, col = move
                game.make_move(row, col)
            else:  # For Connect4
                game.drop_piece(move)
            
            # Check if this move would result in a win
            if game.winner == player_symbol:
                # Restore game state
                game.set_state(original_state)
                return move
            
            # Restore game state for next iteration
            game.set_state(original_state)
        
        return None 