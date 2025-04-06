#!/usr/bin/env python3
import sys
import os
import argparse

from games.tictactoe import TicTacToe, play_game as play_tictactoe
from games.connect4 import Connect4, play_game as play_connect4
from agents.tictactoe_agents import TicTacToeDefaultAgent, TicTacToeMinimaxAgent
from agents.connect4_agents import Connect4DefaultAgent, Connect4MinimaxAgent, run_connect4_experiment
from agents.tictactoe_qlearning import TicTacToeQLearningAgent, train_tictactoe_agent
from agents.connect4_qlearning import Connect4QLearningAgent, train_connect4_agent
from experiments.run_experiments import run_tictactoe_tournament, run_connect4_tournament

class HumanTicTacToePlayer:
    def get_move(self, game):
        #game.print_board()
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

class HumanConnect4Player:
    def get_move(self, game):
        #game.print_board()
        while True:
            try:
                col = int(input(f"Player {game.current_player}, choose column (0-6): "))
                if 0 <= col < 7 and not game.is_column_full(col):
                    return col
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a valid integer.")

def main():
    parser = argparse.ArgumentParser(description='Play Tic Tac Toe or Connect 4')
    parser.add_argument('game', choices=['tictactoe', 'connect4'], help='Game to play')
    parser.add_argument('--player1', choices=['human', 'default', 'minimax', 'qlearning'], default='human', help='First player type')
    parser.add_argument('--player2', choices=['human', 'default', 'minimax', 'qlearning'], default='default', help='Second player type')
    parser.add_argument('--depth', type=int, default=5, help='Depth limit for minimax (Connect 4 only)')
    parser.add_argument('--experiment', action='store_true', help='Run Connect 4 minimax experiment')
    parser.add_argument('--tournament', action='store_true', help='Run a tournament between agents')
    parser.add_argument('--games', type=int, default=10, help='Number of games for tournament')
    parser.add_argument('--train', action='store_true', help='Train a new Q-learning agent')
    parser.add_argument('--episodes', type=int, default=None, help='Number of episodes for Q-learning training')
    parser.add_argument('--save', type=str, default=None, help='Filename to save Q-table')
    parser.add_argument('--load', type=str, default=None, help='Filename to load Q-table')
    
    args = parser.parse_args()
    
    # Run minimax experiment
    if args.experiment and args.game == 'connect4':
        run_connect4_experiment()
        return
        
    # Run tournament
    if args.tournament:
        if args.game == 'tictactoe':
            run_tictactoe_tournament(num_games=args.games)
        else:
            run_connect4_tournament(num_games=args.games)
        return
    
    # Train Q-learning agent
    if args.train:
        if args.game == 'tictactoe':
            episodes = args.episodes or 10000
            save_path = args.save or "tictactoe_qtable.pkl"
            print(f"Training Tic Tac Toe Q-learning agent for {episodes} episodes...")
            agent = train_tictactoe_agent(episodes=episodes, save_path=save_path)
            print("Training complete. Let's play against the trained agent.")
            play_tictactoe(HumanTicTacToePlayer(), agent)
        else:  # Connect 4
            episodes = args.episodes or 5000
            save_path = args.save or "connect4_qtable.pkl"
            print(f"Training Connect 4 Q-learning agent for {episodes} episodes...")
            agent = train_connect4_agent(episodes=episodes, save_path=save_path)
            print("Training complete. Let's play against the trained agent.")
            play_connect4(HumanConnect4Player(), agent)
        return
    
    # Set up players
    if args.game == 'tictactoe':
        player_types = {
            'human': lambda symbol: HumanTicTacToePlayer(),
            'default': lambda symbol: TicTacToeDefaultAgent(symbol),
            'minimax': lambda symbol: TicTacToeMinimaxAgent(symbol, use_alpha_beta=True),
            'qlearning': lambda symbol: create_tictactoe_qagent(symbol, args.load)
        }
        
        player1 = player_types[args.player1]('X')
        player2 = player_types[args.player2]('O')
        
        print("Starting Tic Tac Toe game...")
        play_tictactoe(player1, player2)
    else:  # Connect 4
        player_types = {
            'human': lambda symbol: HumanConnect4Player(),
            'default': lambda symbol: Connect4DefaultAgent(symbol),
            'minimax': lambda symbol: Connect4MinimaxAgent(symbol, use_alpha_beta=True, max_depth=args.depth),
            'qlearning': lambda symbol: create_connect4_qagent(symbol, args.load)
        }
        
        player1 = player_types[args.player1]('X')
        player2 = player_types[args.player2]('O')
        
        print("Starting Connect 4 game...")
        play_connect4(player1, player2)

def create_tictactoe_qagent(symbol, load_file=None):
    """Create a Q-learning agent for Tic Tac Toe with option to load from file."""
    agent = TicTacToeQLearningAgent(symbol, epsilon=0.05)
    agent.training = False
    
    if load_file:
        if not agent.load_qtable(load_file):
            print(f"Could not load Q-table from {load_file}. Training new agent...")
            agent = train_tictactoe_agent()
    else:
        default_file = "tictactoe_qtable.pkl"
        if not agent.load_qtable(default_file):
            print(f"No Q-table found at {default_file}. Training new agent...")
            agent = train_tictactoe_agent()
    
    return agent

def create_connect4_qagent(symbol, load_file=None):
    """Create a Q-learning agent for Connect 4 with option to load from file."""
    agent = Connect4QLearningAgent(symbol, epsilon=0.05)
    agent.training = False
    
    if load_file:
        if not agent.load_qtable(load_file):
            print(f"Could not load Q-table from {load_file}. Training new agent...")
            agent = train_connect4_agent()
    else:
        default_file = "connect4_qtable.pkl"
        if not agent.load_qtable(default_file):
            print(f"No Q-table found at {default_file}. Training new agent...")
            agent = train_connect4_agent()
    
    return agent

if __name__ == "__main__":
    main() 