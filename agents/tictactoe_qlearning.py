import sys
import os
import random
import pickle
import numpy as np
from copy import deepcopy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from games.tictactoe import TicTacToe

class TicTacToeQLearningAgent:
    def __init__(self, player_symbol, epsilon=1.0, alpha=0.5, gamma=0.999):
        self.player_symbol = player_symbol
        self.epsilon = epsilon  # exploration rate
        self.alpha = alpha      # learning rate
        self.gamma = gamma      # discount factor
        self.q_table = {}       # Q-table: state -> {action -> value}
        self.last_state = None
        self.last_action = None
        self.training = True
        
    def get_state_key(self, game):
        """Convert game state to a string key for the Q-table."""
        # Flatten the board and convert to string
        return ''.join(''.join(row) for row in game.board) + game.current_player
    
    def get_move(self, game):
        """Choose an action using epsilon-greedy policy."""
        state = self.get_state_key(game)
        valid_moves = game.get_valid_moves()
        
        if not valid_moves:
            return None
        
        # Initialize Q-values for new state
        if state not in self.q_table:
            self.q_table[state] = {move: 0.0 for move in valid_moves}
        
        # Choose action based on epsilon-greedy policy
        if self.training and random.random() < self.epsilon:
            # Exploration: choose random action
            action = random.choice(valid_moves)
        else:
            # Exploitation: choose best action (with random tie-breaking)
            q_values = self.q_table[state]
            max_value = max(q_values[a] for a in valid_moves)
            best_actions = [a for a in valid_moves if q_values[a] == max_value]
            action = random.choice(best_actions)
        
        # Remember state and action for learning
        self.last_state = state
        self.last_action = action
        
        return action
    
    def learn(self, game, reward):
        """Update Q-value based on reward and new state."""
        if not self.training or self.last_state is None:
            return
        
        # Get new state
        new_state = self.get_state_key(game)
        
        # Calculate max Q for next state
        if new_state in self.q_table and game.get_valid_moves():
            max_q_next = max(self.q_table[new_state].get(a, 0) for a in game.get_valid_moves())
        else:
            max_q_next = 0
        
        # Update Q-value using the Q-learning formula
        old_q = self.q_table[self.last_state][self.last_action]
        self.q_table[self.last_state][self.last_action] = old_q + self.alpha * (
            reward + self.gamma * max_q_next - old_q
        )
    
    def save_qtable(self, filename):
        """Save Q-table to a file."""
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f"Q-table saved to {filename}")
    
    def load_qtable(self, filename):
        """Load Q-table from a file."""
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
            print(f"Q-table loaded from {filename}")
            return True
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with empty Q-table.")
            return False

def train_tictactoe_agent(episodes=10000, save_path="tictactoe_qtable.pkl"):
    """Train a Q-learning agent for Tic Tac Toe."""
    agent_x = TicTacToeQLearningAgent('X', epsilon=0.9)
    agent_o = TicTacToeQLearningAgent('O', epsilon=0.9)
    
    agents = {'X': agent_x, 'O': agent_o}
    
    # Statistics tracking
    stats = {
        'X': {'wins': 0, 'draws': 0, 'games': 0},
        'O': {'wins': 0, 'draws': 0, 'games': 0}
    }
    
    # Define the decay rate for epsilon
    epsilon_decay = 0.99999
    min_epsilon = 0.05
    log_interval = 1000
    
    # Training loop
    for episode in range(episodes):
        game = TicTacToe()
        
        while not game.game_over:
            current_agent = agents[game.current_player]
            move = current_agent.get_move(game)
            
            if move:
                row, col = move
                prev_state = deepcopy(game)
                game.make_move(row, col)
                
                # Determine reward
                reward = 0
                if game.winner == current_agent.player_symbol:
                    reward = 1  # Win
                    stats[current_agent.player_symbol]['wins'] += 1
                elif game.game_over and not game.winner:
                    reward = 0.5  # Draw
                    stats['X']['draws'] += 1
                    stats['O']['draws'] += 1
                
                current_agent.learn(game, reward)
                
                # Other agent also learns from this move
                other_agent = agents['O' if game.current_player == 'X' else 'X']
                if game.winner and game.winner != other_agent.player_symbol:
                    other_agent.learn(game, -1)  # Negative reward for losing
                elif game.game_over and not game.winner:
                    other_agent.learn(game, 0.5)  # Draw
        
        # Update game statistics
        stats['X']['games'] += 1
        stats['O']['games'] += 1
        
        # Decay epsilon (reduce exploration over time)
        agent_x.epsilon = max(min_epsilon, agent_x.epsilon * epsilon_decay)
        agent_o.epsilon = max(min_epsilon, agent_o.epsilon * epsilon_decay)
        
        # Progress reporting
        if (episode + 1) % log_interval == 0 or episode == 0:
            x_win_rate = stats['X']['wins'] / stats['X']['games'] * 100 if stats['X']['games'] > 0 else 0
            o_win_rate = stats['O']['wins'] / stats['O']['games'] * 100 if stats['O']['games'] > 0 else 0
            draw_rate = stats['X']['draws'] / stats['X']['games'] * 100 if stats['X']['games'] > 0 else 0
            
            print(f"Episode {episode + 1}/{episodes} | Epsilon: {agent_x.epsilon:.4f} | X wins: {x_win_rate:.2f}% | O wins: {o_win_rate:.2f}% | Draws: {draw_rate:.2f}%")
            
            # Reset statistics for the next interval
            if episode != 0:  # Don't reset after the first episode
                stats = {
                    'X': {'wins': 0, 'draws': 0, 'games': 0},
                    'O': {'wins': 0, 'draws': 0, 'games': 0}
                }
    
    # Save the trained agent
    agent_x.save_qtable(save_path)
    
    # Return the trained agent
    agent_x.training = False
    agent_x.epsilon = 0.05  # Reduce exploration for actual play
    return agent_x

if __name__ == "__main__":
    from games.tictactoe import play_game
    
    # Train agent if needed
    train_new = input("Train new agent? (y/n): ").lower() == 'y'
    if train_new:
        episodes = int(input("Number of episodes (default: 10000): ") or 10000)
        agent = train_tictactoe_agent(episodes)
    else:
        # Load pre-trained agent
        agent = TicTacToeQLearningAgent('X', epsilon=0.05)
        agent.training = False
        if not agent.load_qtable("tictactoe_qtable.pkl"):
            print("No pre-trained agent found. Training new agent...")
            agent = train_tictactoe_agent()
    
    # Play against the trained agent
    class HumanPlayer:
        def get_move(self, game):
            game.print_board()
            while True:
                try:
                    row = int(input(f"Player {game.current_player}, enter row (0-2): "))
                    col = int(input(f"Player {game.current_player}, enter col (0-2): "))
                    if 0 <= row < 3 and 0 <= col < 3 and game.board[row][col] == ' ':
                        return row, col
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter valid integers.")
    
    print("\nPlaying against trained Q-learning agent...")
    play_game(HumanPlayer(), agent) 