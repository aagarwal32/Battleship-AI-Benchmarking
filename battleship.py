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
    print("  A B C D E F G H I J")
    for i, row in enumerate(board):
        print(f"{i+0} {' '.join(str(cell) if cell is not None else ' ' for cell in row)}")


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
    prev_x1, prev_y1, offset_x, offset_y = -1, -1, 0, 0
    heuristic = 0

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # make sure same coord is not considered again
            if (row, col) in visited:
                continue
            
            # hit found -- consider adjacencies
            if board[row][col] == 'H':
                visited.append((row, col))

                # find all coords adjacent to hit
                for x, y in adj:
                    new_row, new_col = row + x, col + y
                    # ensure playable moves then increase heurisitc and add to pq
                    if new_row in range(GRID_SIZE) and new_col in range(GRID_SIZE) and \
                        board[new_row][new_col] == ' ':
                            
                        heuristic = 1
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
    #print(rectangles)
    return rectangles

def find_rectangles_MM(hits, misses):
    rectangles = {2: [], 3: [], 4: [], 5: []}  # Separate sublists for each size ship
    GRID_SIZE = 10  # Assuming GRID_SIZE is defined somewhere
    #print(hits)
    #print(misses)
    shipSize =  [2,3,4,5]
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if((i, j) not in misses and (i, j) not in hits):
                for width in shipSize:
                    valid = True
                    ship = []
                    for varWidth in range(width):
                        if(i + varWidth < GRID_SIZE and (i + varWidth, j) not in misses and (i + varWidth, j) not in hits):
                            ship.append((i + varWidth, j))
                        else:
                            valid = False
                    for ships in rectangles[width]:
                        if((i + varWidth, j) not in ships and (i + varWidth, j) not in ships):
                            valid = False
                    if(valid):
                        rectangles[width].append(ship)
                        
    playcount = 0
    playcount += len(hits) + len(misses)
    if(playcount > 90): 
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if((i, j) not in misses and (i, j) not in hits):
                    for height in shipSize:
                        valid = True
                        ship = []
                        for varHeight in range(height):
                            if(j + varHeight < GRID_SIZE and (i, varHeight + j) not in misses and (i, varHeight + j) not in hits):
                                ship.append((i, varHeight + j))
                            else:
                                valid = False
                        for ships in rectangles[height]:
                            if((i, varHeight + j) not in ships and (i, varHeight + j)  not in ships):
                                valid = False
                        if(valid):
                            rectangles[height].append(ship)         
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

def common_points_MM(rectanglesMap):
    point_counts = {}
    for size, rectangles in rectanglesMap.items():
        for rectangle in rectangles:
            for point in rectangle:
                if point in point_counts:
                    point_counts[point] += 1
                else:
                    point_counts[point] = 1

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

def heuristic_probability_MM(move, targets, hits, misses):
    GRID_SIZE = 10
    probabilities = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    ## Local Probabilty
    Probability_Charge = sum(targets.values()) / (100 - len(hits))
    a, b = move
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
    rectangles = find_rectangles_MM(hits, misses)
    commons = common_points_MM(rectangles)
    ##rectangles = find_rectangles(hits,misses, targets)
    ##commons = common_points(rectangles) 
    ##print(commons)
    
    for (i, j), o in commons:
        if o >= 3:  # Adjusted condition to match your logic
            ##print((i, j))
            probabilities[i][j] += Probability_Charge 

    return probabilities[a][b]



def alphabeta(board, depth, alpha, beta, maximizing_player, targets, hits, misses):
    if depth == 0:
        return heuristic_probability_MM(board, targets, hits, misses)
    
    if maximizing_player:
        value = float('-inf')
        for move in possible_moves(board, hits.copy(), misses.copy()):  # Copy hits and misses
            new_hits = hits.copy()  # Create a copy of hits
            new_hits.add(move)  # Apply the move
            value = max(value, alphabeta(move, depth - 1, alpha, beta, False, targets, new_hits, misses.copy()))  # Pass new_hits
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for move in possible_moves(board, hits.copy(), misses.copy()):  # Copy hits and misses
            new_misses = misses.copy()  # Create a copy of misses
            new_misses.add(move)  # Apply the move
            value = min(value, alphabeta(move, depth - 1, alpha, beta, True, targets, hits.copy(), new_misses))  # Pass new_misses
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
    #print(moves)
    
    return moves

def find_best_move(board,depth,targets,hits,misses,playcounter):
    best_move = None
    best_value = 0
    alpha = float('-inf')
    beta = float('inf')
    hitsCopy = hits
    missesCopy = misses
    if(playcounter > 80):
        for move in possible_moves(board[0],hits,misses):
            value = alphabeta(move, depth - 1, alpha, beta, False,targets, hits.copy(),missesCopy)
            if value > best_value:
                best_value = value
                best_move = move
        if(best_move == None):
           best_move = heuristic_probability_based_Only(board, targets, hitsCopy,missesCopy)
        
    else:
        best_move = heuristic_probability_based_Only(board, targets, hitsCopy,missesCopy)
    
    return best_move


# Function to simulate a game between a player and AI opponent
def simulate_game(strategy):
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
            guess_row, guess_col = random_guess(player_hits.union(player_misses))
            # guess_row, guess_col = greedy(player_boards[0], priority, visited)
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
            if(strategy == 1):
                guess_row, guess_col = random_guess(opponent_hits.union(opponent_misses))
            elif(strategy == 2): 
                guess_row, guess_col = heuristic_probability_based_Only(opponent_boards, opponent_targets,opponent_hits, opponent_misses) 
            elif(strategy == 3):  
                guess_row, guess_col = find_best_move(opponent_boards,3,opponent_targets, opponent_hits,opponent_misses,playcounter)
            else:
                guess_row, guess_col = greedy(opponent_boards[0], priority, visited)

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
def get_coordinates():
    while True:
        try:
            pair = input("Enter Coordinates to Fire on Enemy (row, column) separated by a comma (e.g., 3,4):\n")
            guess_row, guess_col = map(int, pair.split(','))
            return guess_row, guess_col
        except ValueError:
            print("Invalid input. Please enter two integers separated by a comma.")



def play_game(strategy):
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

    # display_board(player_boards[1])
    # display_board(opponent_boards[1])
    ## stop = input("Continue ?")
    print("The opponent has placed their ships.")
    print("Your board:")
    display_board(player_boards[1])

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
            while True:
                guess_row, guess_col = get_coordinates()
                if(guess_row in range(GRID_SIZE) and guess_col in range(GRID_SIZE) and (guess_row,guess_col) not in player_misses and (guess_row,guess_col) not in player_hits):
                  break
                else:
                    print("Invalid Coordinates. Try Again\n")
                

              
            result = check_guess(opponent_boards, guess_row, guess_col,player_targets)
            if result == 'M':
                print("Miss")
                player_turn = False
                player_misses.add((guess_row, guess_col))
            else:
                print("Hit!")
                player_hits.add((guess_row, guess_col))

            player_boards[0][guess_row][guess_col] = result
            player_turn = False
            print()
            print("Opponent board:")
            display_board(player_boards[0])

        else:
            # AI opponent's turn
            if(strategy == 1):
                guess_row, guess_col = random_guess(opponent_hits.union(opponent_misses))
            elif(strategy == 2): 
                guess_row, guess_col = heuristic_probability_based_Only(opponent_boards, opponent_targets,opponent_hits, opponent_misses) 
            elif(strategy == 3):  
                guess_row, guess_col = find_best_move(opponent_boards,3,opponent_targets, opponent_hits,opponent_misses,playcounter)
            else:
                guess_row, guess_col = greedy(opponent_boards[0], priority, visited)


            result = check_guess(player_boards, guess_row, guess_col,opponent_targets)
            if result == 'M':
                print("AI Opponent's Turn: Miss")
                opponent_misses.add((guess_row, guess_col))
            else:
                print("AI Opponent's Turn: Hit")
                hitcounter += 1
                opponent_hits.add((guess_row, guess_col))

            playcounter += 1
            opponent_boards[0][guess_row][guess_col] = result
            player_turn = True
            #display_board(opponent_boards[0])
            print()
            print(f"({guess_row}, {guess_col})")
            print()
            print("Your board:")
            display_board(opponent_boards[0])
            display_board(player_boards[1])
     
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
    strategies = [1,2,3,4]
    time_start = time.time()
    for strategy in strategies:
            total_hits = 0
            total_plays = 0
            player_wins = 0
            ai_opponent_wins = 0
            for _ in range(100):
                result, num_hits, num_plays = simulate_game(strategy)
                if result == "Player wins!":
                    player_wins += 1
                elif result == "AI opponent wins!":
                    ai_opponent_wins += 1
                total_hits += num_hits
                total_plays += num_plays

            if total_plays != 0:
                if(strategy == 1):
                    print(f"Random:")
                elif(strategy == 2): 
                    print(f"Pure Probabilty:")
                elif(strategy == 3):  
                    print(f"Minimax:")
                else:
                    print(f"Greedy:")
                hit_rate = total_hits / total_plays
                print(f"Total hits: {total_hits}  Total plays: {total_plays}")
                print(f"Hit Rate: {((hit_rate) * 100)} %")

            time_end = time.time()
            print(f"Elapsed time: {time_end - time_start}")
            print(f"Player wins: {player_wins}")
            print(f"AI opponent wins: {ai_opponent_wins}")
            print()

def play_games():
    strategies = [1,2,3,4]
    while True:
        print("Please Select the AI for Battleship (1)Random (2)Probabilty (3)Minimax (4)Greedy")
        response = input()
        if(int(response) not in strategies):
            print("Invalid Selection\n")
            continue
        else:
            break
    
    player_wins = 0
    ai_opponent_wins = 0
    total_hits = 0
    total_plays = 0
    strategies = [1,2,3,4]
   
    total_hits = 0
    total_plays = 0
    player_wins = 0
    ai_opponent_wins = 0
    for _ in range(1):
        result, num_hits, num_plays = play_game(response)
        if result == "Player wins!":
            player_wins += 1
        elif result == "AI opponent wins!":
            ai_opponent_wins += 1
        total_hits += num_hits
        total_plays += num_plays

    hit_rate = total_hits / total_plays
    print(f"Total hits: {total_hits}  Total plays: {total_plays}")
    print(f"Hit Rate: {((hit_rate) * 100)} %")
    print(f"Player wins: {player_wins}")
    print(f"AI opponent wins: {ai_opponent_wins}")
    print()


    








play_games()

# Simulate multiple games
#simulate_multiple_games()
