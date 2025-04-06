import sys
import os
import random
import time
from copy import deepcopy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from games.tictactoe import TicTacToe
from agents.default_agent import DefaultAgent

class TicTacToeDefaultAgent(DefaultAgent):
    pass  # Uses the default implementation

class TicTacToeMinimaxAgent:
    def __init__(self, player_symbol, use_alpha_beta=True):
        self.player_symbol = player_symbol
        self.opponent_symbol = 'O' if player_symbol == 'X' else 'X'
        self.use_alpha_beta = use_alpha_beta
        self.nodes_evaluated = 0
        
    def get_move(self, game):
        self.nodes_evaluated = 0
        start_time = time.time()
        
        if self.use_alpha_beta:
            best_score = float('-inf')
            best_move = None
            
            for move in game.get_valid_moves():
                # Create a deep copy to avoid modifying the original game
                game_copy = deepcopy(game)
                row, col = move
                game_copy.make_move(row, col)
                
                score = self.minimax(game_copy, 0, False, float('-inf'), float('inf'))
                
                if score > best_score:
                    best_score = score
                    best_move = move
        else:
            best_score = float('-inf')
            best_move = None
            
            for move in game.get_valid_moves():
                # Create a deep copy to avoid modifying the original game
                game_copy = deepcopy(game)
                row, col = move
                game_copy.make_move(row, col)
                
                score = self.minimax_no_pruning(game_copy, 0, False)
                
                if score > best_score:
                    best_score = score
                    best_move = move
        
        end_time = time.time()
        print(f"Minimax agent evaluated {self.nodes_evaluated} nodes in {end_time - start_time:.2f} seconds")
        return best_move
    
    def minimax(self, game, depth, is_maximizing, alpha, beta):
        self.nodes_evaluated += 1
        
        if game.winner == self.player_symbol:
            return 10 - depth
        elif game.winner == self.opponent_symbol:
            return depth - 10
        elif game.game_over:  # Draw
            return 0
            
        if is_maximizing:
            max_eval = float('-inf')
            for move in game.get_valid_moves():
                game_copy = deepcopy(game)
                row, col = move
                game_copy.make_move(row, col)
                
                eval = self.minimax(game_copy, depth + 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
                    
            return max_eval
        else:
            min_eval = float('inf')
            for move in game.get_valid_moves():
                game_copy = deepcopy(game)
                row, col = move
                game_copy.make_move(row, col)
                
                eval = self.minimax(game_copy, depth + 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                
                beta = min(beta, eval)
                if beta <= alpha:
                    break
                    
            return min_eval
    
    def minimax_no_pruning(self, game, depth, is_maximizing):
        self.nodes_evaluated += 1
        
        if game.winner == self.player_symbol:
            return 10 - depth
        elif game.winner == self.opponent_symbol:
            return depth - 10
        elif game.game_over:  # Draw
            return 0
            
        if is_maximizing:
            max_eval = float('-inf')
            for move in game.get_valid_moves():
                game_copy = deepcopy(game)
                row, col = move
                game_copy.make_move(row, col)
                
                eval = self.minimax_no_pruning(game_copy, depth + 1, False)
                max_eval = max(max_eval, eval)
                    
            return max_eval
        else:
            min_eval = float('inf')
            for move in game.get_valid_moves():
                game_copy = deepcopy(game)
                row, col = move
                game_copy.make_move(row, col)
                
                eval = self.minimax_no_pruning(game_copy, depth + 1, True)
                min_eval = min(min_eval, eval)
                    
            return min_eval


if __name__ == "__main__":
    from games.tictactoe import play_game
    
    # Test agents
    print("Testing Default Agent vs Minimax Agent (with Alpha-Beta pruning)")
    play_game(TicTacToeDefaultAgent('X'), TicTacToeMinimaxAgent('O', use_alpha_beta=True))
    
    print("\nTesting Minimax Agent (no pruning) vs Default Agent")
    play_game(TicTacToeMinimaxAgent('X', use_alpha_beta=False), TicTacToeDefaultAgent('O')) 