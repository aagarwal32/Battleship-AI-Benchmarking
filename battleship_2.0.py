import random
import heapq
import time

# Constants
GRID_SIZE = 10

# Function to create a player's game boards
def create_player_boards():
    hits_misses_board = [[' '] * GRID_SIZE for _ in range(GRID_SIZE)]  # Initialize hits/misses board
    placement_board = [[' '] * GRID_SIZE for _ in range(GRID_SIZE)]  # Initialize placement board
    return hits_misses_board, placement_board

# Function to create both players' game boards
def create_game_boards():
    player1_hits_misses, player1_placement = create_player_boards()
    player2_hits_misses, player2_placement = create_player_boards()
    return (player1_hits_misses, player1_placement), (player2_hits_misses, player2_placement)

def place_ships(board, ships):
    for ship in ships:
        ship_length, orientation, ship_name = ship
        placed = False
        while not placed:
            coordX, coordY = random.randint(0, 9), random.randint(0, 9)
            if orientation == 1:
                if coordY - ship_length < 0:
                    continue
                else:
                    conflict = False
                    for i in range(coordY, coordY - ship_length, -1):
                        if board[coordX][i] != ' ':
                            conflict = True
                            break
                    if not conflict:
                        for i in range(coordY, coordY - ship_length, -1):
                            board[coordX][i] = ship_name[0]
                        placed = True
            else:
                if coordX - ship_length < 0:
                    continue
                else:
                    conflict = False
                    for i in range(coordX, coordX - ship_length, -1):
                        if board[i][coordY] != ' ':
                            conflict = True
                            break
                    if not conflict:
                        for i in range(coordX, coordX - ship_length, -1):
                            board[i][coordY] = ship_name[0]
                        placed = True





def check_guess(board, guess_row, guess_col, targets):
    cell = board[1][guess_row][guess_col]
    if cell != ' ':
        targets[cell[0]] -= 1  # Decrement the target count for the ship
        return 'H'
    else:
        return 'M'
        
       
def display_board(board):
    print("  1 2 3 4 5 6 7 8 9 10")
    for i, row in enumerate(board):
        print(f"{chr(i + ord('A'))} {' '.join(str(cell) if cell is not None else ' ' for cell in row)}")


# Heuristic function for AI opponent (random guess for simplicity)
def random_guess(hits):
    # Generate random coordinates until an unhit square is found
    while True:
        guess_row = random.randint(0, GRID_SIZE - 1)
        guess_col = random.randint(0, GRID_SIZE - 1)
        if (guess_row, guess_col) not in hits:
            return guess_row, guess_col
        

def greedy(board, pq: list, visited: list):
    adj = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    heuristic = 0

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):     
            # make sure same coord is not considered again
            if (row, col) in visited:
                continue
            
            # hit found -- consider adjacencies
            elif board[row][col] == 'H':
                visited.append((row, col))

                # find all coords adjacent to hit
                for x, y in adj:
                    new_row, new_col = row + x, col + y
                    # ensure playable moves then increase heurisitc and add to pq
                    if new_row in range(GRID_SIZE) and new_col in range(GRID_SIZE) and \
                        board[new_row][new_col] == ' ':
                            
                        heuristic += 1
                        pq.append((-heuristic, new_row, new_col))
            
            elif board[row][col] == 'M':
                visited.append((row, col))
            else:
                continue

    # if a better guess was not found, return a random guess
    if len(pq) == 0:
        r, c = random_guess(visited)
    else:
        heapq.heapify(pq)
        _, r, c = heapq.heappop(pq)
        visited.append((r, c))

    return r, c 


def heuristic_probability_first(board, targets,hits):
    probabilities = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    # Calculate probabilities for each cell
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[0][i][j] == ' ':
                # Your probability calculation logic here
                probabilities[i][j] = sum(targets.values()) / 100
                if(i % 2 == 0):
                    probabilities[i][j] = sum(targets.values()) / 100 / 2


    row,column = -1,-1
    bestMove = -1            

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if row == -1:
                row,column = i,j
            elif bestMove < probabilities[i][j]:
                bestMove = probabilities[i][j]
                row,column = i,j

    return row,column

def find_rectangles(hits,misses, targets):
    rectangles = []
    largest_key = max(targets, key=targets.get)

    # Get the largest value
    largestship = targets[largest_key]

    for top_left_row in range(GRID_SIZE):
        for top_left_col in range(GRID_SIZE):
                width, height = 1, largestship
                # Check if the rectangle fits within the grid boundaries
                if top_left_row + width <= GRID_SIZE and top_left_col + height <= GRID_SIZE:
                    # Check if the rectangle overlaps with any obstacles
                    overlap = False
                    for i in range(top_left_row, top_left_row + width):
                        for j in range(top_left_col, top_left_col + height):
                            if (i, j) in hits or (i,j) in misses:
                                overlap = True
                                break
                        if overlap:
                            break
                    # If there's no overlap with obstacles, record the rectangle
                    if not overlap:
                        rectangles.append(((top_left_row, top_left_col), width, height))
    return rectangles

def find_rectangles_MM(grid, hits, misses):
    rectangles = {2: [], 3: [], 4: [], 5: []}  # Separate sublists for each size ship
    for top_left_row in range(GRID_SIZE):
        for top_left_col in range(GRID_SIZE):
            # Check if the cell is a hit, miss, or obstacle
            if (top_left_row, top_left_col) in hits or (top_left_row, top_left_col) in misses or grid[top_left_row][top_left_col] == 1:
                continue
            # Iterate over possible heights (from 5 to 2) to prioritize larger rectangles first
            for height in range(5, 1, -1):
                # Check if adding a rectangle of this size would cause overlap with existing rectangles of the same size, hits, or misses
                if any(top_left_row <= rect[0][0] < top_left_row + height and rect[0][1] == top_left_col for rect in rectangles[height]):
                    continue  # Skip if there's overlap with an existing rectangle of the same size
                # Check if the rectangle fits within the grid boundaries
                if top_left_row + height <= GRID_SIZE:
                    # Check if the rectangle overlaps with any hits, misses, or obstacles
                    overlap = any((i, top_left_col) in hits or (i, top_left_col) in misses or grid[i][top_left_col] == 1 for i in range(top_left_row, top_left_row + height))
                    # If there's no overlap with hits, misses, or obstacles, record the rectangle
                    if not overlap:
                        width = 1
                        rectangles[height].append(((top_left_row, top_left_col), width, height))
                        break  # Move to the next cell after adding the rectangle
    
    return rectangles

def common_points(rectangles):

    point_counts = {}
    for rectangle in rectangles:
        (top_left_row, top_left_col), width, height = rectangle
        for i in range(top_left_row, top_left_row + width):
            for j in range(top_left_col, top_left_col + height):
                if (i, j) in point_counts:
                    point_counts[(i, j)] += 1
                else:
                    point_counts[(i, j)] = 1
    sorted_points = sorted(point_counts.items(), key=lambda x: x[1], reverse=True)
    commons = sorted_points[:5]
    return commons

def common_points_MM(rectanglesList):
    point_counts = {}
    for rectangles in rectanglesList:
        for rectangle in rectangles:
            (top_left_row, top_left_col), width, height = rectangle
            for i in range(top_left_row, top_left_row + width):
                for j in range(top_left_col, top_left_col + height):
                    if (i, j) in point_counts:
                        point_counts[(i, j)] += 1
                    else:
                        point_counts[(i, j)] = 1
        sorted_points = sorted(point_counts.items(), key=lambda x: x[1], reverse=True)
        commons = sorted_points[:5]
        return commons

def heuristic_probability_based_Only(board, targets, hits,misses):

    GRID_SIZE = 10
    probabilities = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    rectangles = find_rectangles(hits,misses, targets)
    commons = common_points(rectangles) 
    Probability_Charge = sum(targets.values()) / (100 - len(hits))
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[0][i][j] == ' ':
                # Your probability calculation logic here
                if (i + j) % 2 == 0:
                    probabilities[i][j] += Probability_Charge 

                
    for (i, j), b in commons:
        if 3 <= b:
            probabilities[i][j] += Probability_Charge

    for (i, j)in hits:
        if board[0][i][j] == 'H':
            if i + 1 in range(GRID_SIZE):
                if board[0][i + 1][j] == ' ':
                    probabilities[i + 1][j] += Probability_Charge / 4
            if i - 1 in range(GRID_SIZE):
                if board[0][i - 1][j] == ' ':
                    probabilities[i - 1][j] += Probability_Charge / 4
            if j + 1 in range(GRID_SIZE):
                if board[0][i][j + 1] == ' ':
                    probabilities[i][j + 1] += Probability_Charge / 4
            if j - 1 in range(GRID_SIZE):
                if board[0][i][j - 1] == ' ':
                    probabilities[i][j - 1] += Probability_Charge / 4

    row, column = -1, -1
    best_move = -1

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if row == -1:
                row, column = i, j
            elif best_move < probabilities[i][j]:
                best_move = probabilities[i][j]
                row, column = i, j

    return row, column

def heuristic_probability_MM(move, targets, hits, misses, Maximizing_Player):
    GRID_SIZE = 10
    probabilities = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    Probability_Charge = sum(targets.values()) / (100 - len(hits))
    a, b = move
    ## Assume Hit or Miss
    if Maximizing_Player:
        # Adjust probabilities around past hits
        for (i, j) in hits:
            if i + 1 in range(GRID_SIZE):
                probabilities[i + 1][j] += Probability_Charge / 2
            if i - 1 in range(GRID_SIZE):
                probabilities[i - 1][j] += Probability_Charge / 2
            if j + 1 in range(GRID_SIZE):
                probabilities[i][j + 1] += Probability_Charge / 2
            if j - 1 in range(GRID_SIZE):
                probabilities[i][j - 1] += Probability_Charge / 2

        # Adjust probabilities based on past hit clusters
        rectangles = find_rectangles_MM(hits, misses, targets)
        commons = common_points_MM(rectangles)
        #print(commons)
        for (i, j), b in commons:
            if b >= 3:  # Adjusted condition to match your logic
                probabilities[i][j] += Probability_Charge 

    else:
         probabilities[a][b] += 0


    return probabilities[a][b]



def alphabeta(board, depth, alpha, beta, maximizing_player, targets, hits,misses):
    if depth == 0:
        return heuristic_probability_MM(board, targets, hits,misses,maximizing_player)
    if maximizing_player:
        value = float('-inf')
        for move in possible_moves(board,hits,misses):
            value = max(value, alphabeta(move, depth - 1, alpha, beta, False,targets, hits,misses))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for move in possible_moves(board,hits,misses):
            value = min(value, alphabeta(move, depth - 1, alpha, beta, True,targets, hits,misses))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def possible_moves(board, hits, misses):
    moves = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if (i,j) not in hits:
                if(i,j) not in misses:
                    pair = (i, j)
                    moves.append(pair)
    return moves

def find_best_move(board,depth,targets,hits,misses):
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    for move in possible_moves(board,hits,misses):
        value = alphabeta(move, depth - 1, alpha, beta, False,targets, hits,misses)
        if value > best_value:
            best_value = value
            best_move = move
    #print(best_move)
    return best_move


# Function to simulate a game between a player and AI opponent
def simulate_game():
    # Create game boards
    player_boards, opponent_boards = create_game_boards()

    # Set ships for both players (random for simplicity)
    player_ships = [
        (5, random.randint(0, 1), 'Carrier'),
        (4, random.randint(0, 1), 'Battleship'),
        (3, random.randint(0, 1), 'Frigate'),
        (3, random.randint(0, 1), 'Submarine'),
        (2, random.randint(0, 1), 'Destroyer')

    ]
    opponent_ships = [
        (5, random.randint(0, 1), 'Carrier'),
        (4, random.randint(0, 1), 'Battleship'),
        (3, random.randint(0, 1), 'Frigate'),
        (3, random.randint(0, 1), 'Submarine'),
        (2, random.randint(0, 1), 'Destroyer')
    ]
    player_targets = {'C': 5, 'B': 4, 'F': 3, 'S': 3, 'D': 2}
    opponent_targets = {'C': 5, 'B': 4, 'F': 3, 'S': 3, 'D': 2}
    ###sum(player_targets.values())


    place_ships(player_boards[1], player_ships)
    place_ships(opponent_boards[1], opponent_ships)

    ## display_board(player_boards[1])
    ## display_board(opponent_boards[1])
    ## stop = input("Continue ?")

    # greedy priority list
    priority = []
    visited = []

    hitcounter = 0
    playcounter = 0

    # Game loop
    player_turn = True
    player_hits = set()
    opponent_hits = set()
    player_misses = set()
    opponent_misses = set()
    TIMEOUT = 400
    count = 0

    while True and count < 200:
        if player_turn:
            # Player's turn
            #guess_row, guess_col = random_guess(player_hits.union(player_misses))
            guess_row, guess_col = greedy(player_boards[0], priority, visited)
            result = check_guess(opponent_boards, guess_row, guess_col,player_targets)
            if result == 'M':
                ##print("Player's Turn: Miss")
                player_turn = False
                player_misses.add((guess_row, guess_col))
            else:
                player_hits.add((guess_row, guess_col))

            player_boards[0][guess_row][guess_col] = result

        else:
            # AI opponent's turn
            #guess_row, guess_col = random_guess(opponent_hits.union(opponent_misses))
            guess_row, guess_col = heuristic_probability_based_Only(opponent_boards, opponent_targets,opponent_hits, opponent_misses)
            #guess_row, guess_col = find_best_move(opponent_boards[0],3,opponent_targets, opponent_hits,opponent_misses)
            #guess_row, guess_col = greedy(opponent_boards[0], priority, visited)
            result = check_guess(player_boards, guess_row, guess_col,opponent_targets)

            if result == 'M':
                ##print("AI Opponent's Turn: Miss")
                player_turn = True
                opponent_misses.add((guess_row, guess_col))
            else:
                hitcounter += 1
                opponent_hits.add((guess_row, guess_col))

            playcounter += 1
            opponent_boards[0][guess_row][guess_col] = result
            #display_board(opponent_boards[0])
            #print()
            # display_board(opponent_boards[1])
            # print()
     
        count += 1
            
        if all(num == 0 for letter, num in player_targets.items()):
            return "Player wins!", 0, 0
        elif all(num == 0 for letter, num in opponent_targets.items()):
            # print(f"Hit Count: {((hitcounter))}")
            # print(f"Play Count: {((playcounter))}")
            # HR = hitcounter/playcounter
            # print(f"Hit Rate: {((HR) * 100)} %")
            return "AI opponent wins!", hitcounter, playcounter
        
    print("All Moves Taken. Something is Wrong")


# Simulate multiple games to test heuristic effectiveness
def simulate_multiple_games():
    player_wins = 0
    ai_opponent_wins = 0
    total_hits = 0
    total_plays = 0
    
    time_start = time.time()
    for _ in range(100):
        result, num_hits, num_plays = simulate_game()
        if result == "Player wins!":
            player_wins += 1
        elif result == "AI opponent wins!":
            ai_opponent_wins += 1
        total_hits += num_hits
        total_plays += num_plays
    
    time_end = time.time()
    print(f"Elapsed time: {time_end - time_start}")
    if total_plays != 0:
        hit_rate = total_hits / total_plays
        print(f"Total hits: {total_hits}  Total plays: {total_plays}")
        print(f"Hit Rate: {((hit_rate) * 100)} %")

    print(f"Player wins: {player_wins}")
    print(f"AI opponent wins: {ai_opponent_wins}")

# Simulate multiple games
simulate_multiple_games()
