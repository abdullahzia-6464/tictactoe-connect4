# Tic Tac Toe and Connect 4 AI

This project implements console-based versions of Tic Tac Toe and Connect 4 games with various AI agents.

## Project Structure

```
/
├── games/
│   ├── tictactoe.py         # Tic Tac Toe game implementation
│   └── connect4.py          # Connect 4 game implementation
├── agents/
│   ├── default_agent.py     # Basic agent (win, block, random)
│   ├── tictactoe_agents.py  # Tic Tac Toe specific agents
│   ├── connect4_agents.py   # Connect 4 specific agents
│   ├── tictactoe_qlearning.py # Q-learning agent for Tic Tac Toe
│   └── connect4_qlearning.py  # Q-learning agent for Connect 4
├── experiments/
│   └── run_experiments.py   # Tournament and experiment code
└── main.py                  # Main entry point
```

## Agents

The project includes three types of agents:

1. **Default Agent**: Uses a simple strategy
   - Makes a winning move if possible
   - Makes a blocking move if opponent is about to win
   - Makes a random move otherwise

2. **Minimax Agent**: Uses the minimax algorithm
   - For Tic Tac Toe: Full minimax with optional alpha-beta pruning
   - For Connect 4: Depth-limited minimax with evaluation function

3. **Q-learning Agent**: Uses reinforcement learning
   - Learns from experience through self-play
   - Uses an epsilon-greedy policy for exploration/exploitation
   - Can save and load learned Q-tables

## Usage

### Playing Games

```bash
# Play Tic Tac Toe as human vs default agent
python main.py tictactoe

# Play Connect 4 as human vs minimax agent with depth 5
python main.py connect4 --player2 minimax --depth 5

# Play Tic Tac Toe with default agent vs minimax agent
python main.py tictactoe --player1 default --player2 minimax

# Play against a Q-learning agent
python main.py tictactoe --player2 qlearning

# Play against a Q-learning agent with a specific Q-table file
python main.py connect4 --player2 qlearning --load my_qtable.pkl
```

### Training Q-learning Agents

```bash
# Train a Tic Tac Toe Q-learning agent (default: 10000 episodes)
python main.py tictactoe --train

# Train a Connect 4 Q-learning agent with custom episodes and save path
python main.py connect4 --train --episodes 2000 --save my_connect4_agent.pkl
```

### Running Experiments

```bash
# Run Connect 4 minimax experiment (30 minutes)
python main.py connect4 --experiment

# Run Tic Tac Toe tournament (100 games)
python main.py tictactoe --tournament --games 100

# Run Connect 4 tournament (10 games)
python main.py connect4 --tournament --games 10
```

## Connect 4 Minimax Analysis

The Connect 4 game has a much larger state space than Tic Tac Toe:
- Tic Tac Toe: Maximum of 9 moves
- Connect 4: Maximum of 42 moves (6 rows × 7 columns)

Full minimax search is infeasible for Connect 4 due to its branching factor. The project includes a depth-limited minimax implementation with an evaluation function that looks ahead a fixed number of moves.

The evaluation function scores board positions based on:
- Number of connected pieces
- Control of the center column
- Potential winning windows

Alpha-beta pruning is used to optimize the search process and explore more nodes in the same time.

## Q-learning Implementation

The Q-learning agents learn through self-play and experience. Key components:

1. **State Representation**: Board state is represented as a string
2. **Action Selection**: Uses epsilon-greedy strategy (balances exploration/exploitation)
3. **Reward System**: 
   - +1 for winning
   - +0.5 for drawing
   - -1 for losing
4. **Learning Rate (alpha)**: Controls how quickly new information overrides old
5. **Discount Factor (gamma)**: Values future rewards

The Q-table stores state-action values that are updated based on the Q-learning formula:
```
Q(s,a) = Q(s,a) + α * (reward + γ * max Q(s',a') - Q(s,a))
```

For Connect 4, a smaller number of training episodes is used due to the larger state space, with more emphasis on using the learned information.

## Running Experiments

The project includes code to compare the effectiveness of different agents and parameters. The experiment module measures:
- Win rates of different agents
- Number of nodes evaluated
- Time taken per move
- Effectiveness of alpha-beta pruning 