## Battleship AI Benchmarking (Quick Overview)

This project is based on the popular game, [Battleship](https://en.wikipedia.org/wiki/Battleship_(game)). Players call out coordinates to hit or miss a part of a ship. The first player to sink all their opponent’s ships wins. 

A mid-game position for Battleship is displayed below. (Please note that the opponent’s board is at the top, where their ships are not visible, and the player’s board is at the bottom, where their ships are shown. You can check your Hits (H) or Misses (M) on the opponent’s board.)

![battleship_board](https://github.com/user-attachments/assets/b0b626bd-2f63-4e1e-840c-4a424a3be032)

This script allows you to play the game against an AI opponent or simulate any number of games (AI vs AI). The AI algorithms implemented are as follows:
1. Greedy algorithm
2. Minimax algorithm with alpha-beta pruning
3. Custom Probability (custom made heuristic-based algorithm for Battleship)

For an AI algorithm to demonstrate any signs of intelligence while playing, it must consistently outperform random guessing. Consequently, all benchmarking results are based on comparing the AI opponent against random guessing. The table below presents the results:

![battleship_ai_benchmark_results](https://github.com/user-attachments/assets/17206f78-8d7c-4bc2-ae4e-18387f7a0c06)

### For a full, in-depth understanding of this project, AI algorithms, and benchmarking results, please refer to the [REPORT](https://github.com/aagarwal32/Battleship-AI-Benchmarking/blob/16d0db70efad83427f54d17d8241a4635dd44129/Battleship_Benchmark_Report.pdf).

## The Team

### Arjun Agarwal, Patrick Shugerts, Anxhelo Kambo, Alan Morcus

## How to Play/Simulate:
1. Install Python (If you don't already have it) then download the battleship.py file.
2. Comment or Uncomment "play_games()" or "simulate_multiple_games()" functions to switch between play or simulate, respectively. These functions are found at the end of the file.
3. Type and enter ```python battleship.py``` to run the script!

########################################################
