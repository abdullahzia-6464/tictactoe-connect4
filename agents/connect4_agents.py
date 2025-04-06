import sys
import os
import random
import time
from copy import deepcopy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from games.connect4 import Connect4
from agents.default_agent import DefaultAgent

class Connect4DefaultAgent(DefaultAgent):
    pass  # Uses the default implementation

class Connect4MinimaxAgent:
    def __init__(self, player_symbol, use_alpha_beta=True, max_depth=None):
        self.player_symbol = player_symbol
        self.opponent_symbol = 'O' if player_symbol == 'X' else 'X'
        self.use_alpha_beta = use_alpha_beta
        self.max_depth = max_depth  # None for full search, or a number for depth-limited search
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
                game_copy.drop_piece(move)
                
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
                game_copy.drop_piece(move)
                
                score = self.minimax_no_pruning(game_copy, 0, False)
                
                if score > best_score:
                    best_score = score
                    best_move = move
        
        end_time = time.time()
        print(f"Minimax agent evaluated {self.nodes_evaluated} nodes in {end_time - start_time:.2f} seconds")
        
        # If no best move was found (possible in depth-limited search), choose random
        if best_move is None and game.get_valid_moves():
            best_move = random.choice(game.get_valid_moves())
            
        return best_move
    
    def minimax(self, game, depth, is_maximizing, alpha, beta):
        self.nodes_evaluated += 1
        
        # Terminal states
        if game.winner == self.player_symbol:
            return 100 - depth  # Prefer winning sooner
        elif game.winner == self.opponent_symbol:
            return depth - 100  # Prefer losing later
        elif game.game_over:  # Draw
            return 0
            
        # Depth limit check
        if self.max_depth is not None and depth >= self.max_depth:
            return self.evaluate_board(game)
            
        if is_maximizing:
            max_eval = float('-inf')
            for move in game.get_valid_moves():
                game_copy = deepcopy(game)
                game_copy.drop_piece(move)
                
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
                game_copy.drop_piece(move)
                
                eval = self.minimax(game_copy, depth + 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                
                beta = min(beta, eval)
                if beta <= alpha:
                    break
                    
            return min_eval
    
    def minimax_no_pruning(self, game, depth, is_maximizing):
        self.nodes_evaluated += 1
        
        # Terminal states
        if game.winner == self.player_symbol:
            return 100 - depth
        elif game.winner == self.opponent_symbol:
            return depth - 100
        elif game.game_over:  # Draw
            return 0
            
        # Depth limit check
        if self.max_depth is not None and depth >= self.max_depth:
            return self.evaluate_board(game)
            
        if is_maximizing:
            max_eval = float('-inf')
            for move in game.get_valid_moves():
                game_copy = deepcopy(game)
                game_copy.drop_piece(move)
                
                eval = self.minimax_no_pruning(game_copy, depth + 1, False)
                max_eval = max(max_eval, eval)
                    
            return max_eval
        else:
            min_eval = float('inf')
            for move in game.get_valid_moves():
                game_copy = deepcopy(game)
                game_copy.drop_piece(move)
                
                eval = self.minimax_no_pruning(game_copy, depth + 1, True)
                min_eval = min(min_eval, eval)
                    
            return min_eval
            
    def evaluate_board(self, game):
        """Heuristic evaluation function for Connect4."""
        score = 0
        
        # Check horizontal windows
        for row in range(game.rows):
            for col in range(game.cols - 3):
                window = [game.board[row][col+i] for i in range(4)]
                score += self.evaluate_window(window)
                
        # Check vertical windows
        for row in range(game.rows - 3):
            for col in range(game.cols):
                window = [game.board[row+i][col] for i in range(4)]
                score += self.evaluate_window(window)
                
        # Check diagonal windows (positive slope)
        for row in range(game.rows - 3):
            for col in range(game.cols - 3):
                window = [game.board[row+i][col+i] for i in range(4)]
                score += self.evaluate_window(window)
                
        # Check diagonal windows (negative slope)
        for row in range(3, game.rows):
            for col in range(game.cols - 3):
                window = [game.board[row-i][col+i] for i in range(4)]
                score += self.evaluate_window(window)
                
        # Center column preference (control of center is good in Connect4)
        center_col = game.cols // 2
        center_count = sum(1 for row in range(game.rows) if game.board[row][center_col] == self.player_symbol)
        score += center_count * 3
        
        return score
        
    def evaluate_window(self, window):
        """Evaluate a window of 4 positions."""
        player_count = window.count(self.player_symbol)
        opponent_count = window.count(self.opponent_symbol)
        empty_count = window.count(' ')
        
        # Scoring for different combinations
        if player_count == 4:
            return 100  # Winning window
        elif player_count == 3 and empty_count == 1:
            return 5  # Potential win
        elif player_count == 2 and empty_count == 2:
            return 2  # Building up
        elif opponent_count == 3 and empty_count == 1:
            return -4  # Block opponent's potential win
            
        return 0


def run_connect4_experiment(time_limit_seconds=1800):  # 30 minutes
    """Run experiment to compare full minimax vs depth-limited minimax for Connect4."""
    print("Connect4 Minimax Performance Experiment")
    print("=======================================")
    
    # Track maximum depth reached and nodes evaluated
    results = {}
    
    # Test with alpha-beta pruning
    for test_name, use_pruning, max_depth in [
        ("Full Minimax with Alpha-Beta Pruning", True, None),
        ("Full Minimax without Pruning", False, None),
        ("Depth-Limited (5) with Alpha-Beta Pruning", True, 5),
        ("Depth-Limited (5) without Pruning", False, 5)
    ]:
        print(f"\nRunning {test_name}...")
        print(f"{'=' * len(test_name)}")
        
        game = Connect4()
        agent = Connect4MinimaxAgent('X', use_alpha_beta=use_pruning, max_depth=max_depth)
        
        start_time = time.time()
        elapsed_time = 0
        moves_made = 0
        total_nodes = 0
        
        try:
            while not game.game_over and elapsed_time < time_limit_seconds:
                move = agent.get_move(game)
                game.drop_piece(move)
                
                if not game.game_over:
                    # Other player makes a random move
                    opponent_move = random.choice(game.get_valid_moves())
                    game.drop_piece(opponent_move)
                
                moves_made += 1
                total_nodes += agent.nodes_evaluated
                elapsed_time = time.time() - start_time
                
                print(f"Move {moves_made}: Evaluated {agent.nodes_evaluated} nodes")
                print(f"Total time: {elapsed_time:.2f} seconds, Total nodes: {total_nodes}")
                print()
        
        except KeyboardInterrupt:
            print("Experiment stopped by user")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"Experiment finished after {total_time:.2f} seconds")
        print(f"Moves made: {moves_made} (max possible: 42)")
        print(f"Total nodes evaluated: {total_nodes}")
        print(f"Nodes per second: {total_nodes / total_time:.2f}")
        
        results[test_name] = {
            "moves_made": moves_made,
            "total_nodes": total_nodes,
            "total_time": total_time,
            "nodes_per_second": total_nodes / total_time
        }
    
    # Print comparative results
    print("\nComparative Results")
    print("===================")
    for test_name, data in results.items():
        print(f"{test_name}:")
        print(f"  Moves made: {data['moves_made']}")
        print(f"  Total nodes: {data['total_nodes']}")
        print(f"  Total time: {data['total_time']:.2f} seconds")
        print(f"  Nodes per second: {data['nodes_per_second']:.2f}")
    
    # Print conclusions
    print("\nConclusions:")
    if "Full Minimax with Alpha-Beta Pruning" in results and "Full Minimax without Pruning" in results:
        pruning_speedup = results["Full Minimax with Alpha-Beta Pruning"]["nodes_per_second"] / \
                          results["Full Minimax without Pruning"]["nodes_per_second"]
        print(f"Alpha-Beta pruning speedup factor: {pruning_speedup:.2f}x")
    
    if "Full Minimax with Alpha-Beta Pruning" in results and "Depth-Limited (5) with Alpha-Beta Pruning" in results:
        depth_limited_moves = results["Depth-Limited (5) with Alpha-Beta Pruning"]["moves_made"]
        full_minimax_moves = results["Full Minimax with Alpha-Beta Pruning"]["moves_made"]
        print(f"Full minimax completed {full_minimax_moves} moves vs {depth_limited_moves} for depth-limited")
        
    print("\nRecommendation: Use depth-limited minimax with alpha-beta pruning for Connect4")


if __name__ == "__main__":
    from games.connect4 import play_game
    
    # Uncomment to run the full experiment (takes 30 minutes)
    # run_connect4_experiment()
    
    # Play a sample game with depth-limited search
    print("Playing Connect4 with Depth-Limited Minimax (depth=5) vs Default Agent")
    play_game(Connect4MinimaxAgent('X', use_alpha_beta=True, max_depth=5), Connect4DefaultAgent('O')) 