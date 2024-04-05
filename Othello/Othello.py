def read_board(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    color = lines[0].strip()
    if color == 'O':
        color = 1
    else:
        color = -1
    lines = lines[2:]
    size = len(lines)
    board = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if lines[i][j] == 'O':
                board[i][j] = 1
            elif lines[i][j] == 'X':
                board[i][j] = -1
    return board, color

def check_num_flips(position, color, board):
    num_flips = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dir in directions:
        dx, dy = dir
        x, y = position
        x += dx
        y += dy
        while 0 <= x < len(board) and 0 <= y < len(board[0]) and board[x][y] == -color:
            x += dx
            y += dy
        if 0 <= x < len(board) and 0 <= y < len(board[0]) and board[x][y] == color:
            while True:
                x -= dx
                y -= dy
                if (x, y) == position:
                    break
                num_flips += 1
    return num_flips
    
def take_step(position, color, board):
    new_board = [row[:] for row in board]
    x, y = position
    new_board[x][y] = color
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dir in directions:
        dx, dy = dir
        nx, ny = x + dx, y + dy
        while 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == -color:
            nx += dx
            ny += dy
        if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == color:
            while (nx, ny) != position:
                nx -= dx
                ny -= dy
                new_board[nx][ny] = color
    return new_board

def check_stability(board, color, position):
    x, y = position
    if (x, y) in [(0, 0), (0, 11), (11, 0), (11, 11)]:
        return True
    if x == 0 or x == 11 or y == 0 or y == 11:
        return True
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(board) and 0 <= ny < len(board) and board[nx][ny] == color:
            return True
    return False

def get_candidates(board, color, all_positions):
    candidates = []
    for position in all_positions:
        x,y = position
        flips = check_num_flips(position, color, board)
        if flips > 0 and board[x][y] == 0:
            candidates.append(position)
    return candidates

def get_candidates_flips(board, candidates):
    candidate_flips = {}
    for position in candidates:
        flips = check_num_flips(position, color, board)
        if flips > 0:
            candidate_flips[position] = flips
    return candidate_flips

def get_self_mobility(board, color, candidates, all_positions):
    self_mobility = {}
    for candidate in candidates:
        new_board = take_step(candidate, color, board)
        self_mobility[candidate] = len(get_candidates(new_board, color, all_positions))
    return self_mobility

def get_opponent_mobility(board, color, candidates, all_positions):
    opponent_mobility = {}
    for candidate in candidates:
        new_board = take_step(candidate, color, board)
        opponent_mobility[candidate] = len(get_candidates(new_board, -color, all_positions))
    return opponent_mobility

def output_file(output_filename, position):
    x , y = position
    row = ['a','b','c','d','e','f','g','h','i','j','k','l']
    column = ['1','2','3','4','5','6','7','8','9','10','11','12']
    output = row[y] + column[x]
    with open(output_filename, 'w') as file:
        file.write(output)
        
def get_best_move(board, color, candidates, all_positions):
        opponent_mobility = get_opponent_mobility(board, color, candidates, all_positions)
        min_opponent_mobility = min(opponent_mobility.values())
        min_opponent_positions = [key for key, value in opponent_mobility.items() if value == min_opponent_mobility]
        self_mobility = get_self_mobility(board, color, min_opponent_positions, all_positions)
        max_self_mobility = max(self_mobility.values())
        max_self_positions = [key for key, value in self_mobility.items() if value == max_self_mobility]
        best_move = max(get_candidates_flips(board, max_self_positions))
        return best_move

input_filename = 'input.txt'
board, color = read_board(input_filename)
opponent_color = -color

all_positions = []
for i in range(0, len(board)):
    for j in range(0, len(board[0])):
        all_positions.append((i,j))
        
candidates = get_candidates(board, color, all_positions)

output_filename = 'output.txt'
for position in candidates:
    if check_stability(board, color, position):
        output_file(output_filename, position)
        break
    elif position[0] not in [1,3,8,10] or position[1] not in [1,3,8,10]:
        output = get_best_move(board, color, candidates, all_positions)
        output_file(output_filename, output)
        break
    elif position[0] not in [1,10] or position[1] not in [1,10]:
        output = get_best_move(board, color, candidates, all_positions)
        output_file(output_filename, output)
        break
    else:
        output = get_best_move(board, color, candidates, all_positions)
        output_file(output_filename, output)
        break