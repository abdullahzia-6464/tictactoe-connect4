#!/usr/bin/env python3
import sys
import os
import argparse

from games.tictactoe import TicTacToe, play_game as play_tictactoe
from games.connect4 import Connect4, play_game as play_connect4
from agents.tictactoe_agents import TicTacToeDefaultAgent, TicTacToeMinimaxAgent
from agents.connect4_agents import Connect4DefaultAgent, Connect4MinimaxAgent, run_connect4_experiment
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
    parser.add_argument('--player1', choices=['human', 'default', 'minimax'], default='human', help='First player type')
    parser.add_argument('--player2', choices=['human', 'default', 'minimax'], default='default', help='Second player type')
    parser.add_argument('--depth', type=int, default=5, help='Depth limit for minimax (Connect 4 only)')
    parser.add_argument('--experiment', action='store_true', help='Run Connect 4 minimax experiment')
    parser.add_argument('--tournament', action='store_true', help='Run a tournament between agents')
    parser.add_argument('--games', type=int, default=10, help='Number of games for tournament')
    
    args = parser.parse_args()
    
    if args.experiment and args.game == 'connect4':
        run_connect4_experiment()
        return
        
    if args.tournament:
        if args.game == 'tictactoe':
            run_tictactoe_tournament(num_games=args.games)
        else:
            run_connect4_tournament(num_games=args.games)
        return
    
    # Set up players
    if args.game == 'tictactoe':
        player_types = {
            'human': lambda symbol: HumanTicTacToePlayer(),
            'default': lambda symbol: TicTacToeDefaultAgent(symbol),
            'minimax': lambda symbol: TicTacToeMinimaxAgent(symbol, use_alpha_beta=True)
        }
        
        player1 = player_types[args.player1]('X')
        player2 = player_types[args.player2]('O')
        
        print("Starting Tic Tac Toe game...")
        play_tictactoe(player1, player2)
    else:  # Connect 4
        player_types = {
            'human': lambda symbol: HumanConnect4Player(),
            'default': lambda symbol: Connect4DefaultAgent(symbol),
            'minimax': lambda symbol: Connect4MinimaxAgent(symbol, use_alpha_beta=True, max_depth=args.depth)
        }
        
        player1 = player_types[args.player1]('X')
        player2 = player_types[args.player2]('O')
        
        print("Starting Connect 4 game...")
        play_connect4(player1, player2)

if __name__ == "__main__":
    main() 