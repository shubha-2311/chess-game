# two player chess in python with Pygame!
# part one, set up variables images and game loop
import pygame
import time

pygame.init()
WIDTH = 1000
HEIGHT = 825
DISPLAYSUR = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 35)
big_font = pygame.font.Font('freesansbold.ttf', 45)
timer = pygame.time.Clock()
fps = 60

# Game variables and images
white_pieces = ['rook','knight','bishop','queen','king','bishop','knight','rook',
                'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn',]
white_locations = [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),
                   (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]
black_pieces = ['rook','knight','bishop','queen','king','bishop','knight','rook',
                'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn',]
black_locations = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                   (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]
captured_pieces_white = []
captured_pieces_black = []
turn_step = 0 # 0 - whites turn no selection; 1 - white turn piece selected; 2 - black turn no selection; 3 - black turn piece selected
selection = 100 # for handling selection of one piece
valid_moves = []
# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load('assets/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load('assets/images/black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('assets/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('assets/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('assets/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load('assets/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('assets/images/white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('assets/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

counter = 0 # check variable/ flashing counter  
winner = ''

# Castling tracking
white_king_moved = False
black_king_moved = False
white_rook_kingside_moved = False
white_rook_queenside_moved = False
black_rook_kingside_moved = False
black_rook_queenside_moved = False

game_over = False

# Define two input boxes
input_boxes = [
        {"rect": pygame.Rect(350, 150, 300, 50), "text": "", "active": True, "label": "White Player"},
        {"rect": pygame.Rect(350, 250, 300, 50), "text": "", "active": False, "label": "Black Player"},
    ]
active_index = 0

def advertisement():
    DISPLAYSUR.fill('dark gray')
    pygame.display.update()
    pygame.time.delay(1000)

    DISPLAYSUR.blit(medium_font.render('This game is developed by SHUBHADEEP SARKAR', True, 'white'), (60, 10))
    pygame.display.update()
    pygame.time.delay(1000)

    DISPLAYSUR.blit(medium_font.render('Student of Ramakrishna Mission Vidyamandira, Belur', True, 'white'), (35, 60))
    pygame.display.update()
    pygame.time.delay(1000)

    DISPLAYSUR.blit(medium_font.render('Student of B.Sc. 3rd year, Computer Science, 2025', True, 'white'), (60, 110))
    pygame.display.update()
    pygame.time.delay(1000)  # Show all for 2 seconds before ending or transitioning

    # Colors
    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BG = (30, 30, 60)
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running =False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, box in enumerate(input_boxes):
                    if box["rect"].collidepoint(event.pos):
                        # Deactivate all, then activate clicked one
                        for b in input_boxes:
                            b["active"] = False
                        box["active"] = True
                        active_index = i

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    # Switch active box
                    input_boxes[active_index]["active"] = False
                    active_index = (active_index + 1) % len(input_boxes)
                    input_boxes[active_index]["active"] = True

                elif event.key == pygame.K_RETURN:
                    # Proceed if both fields are filled
                    if all(box["text"].strip() for box in input_boxes):
                        running = False

                else:
                    box = input_boxes[active_index]
                    if event.key == pygame.K_BACKSPACE:
                        box["text"] = box["text"][:-1]
                    else:
                        box["text"] += event.unicode

        # Draw input boxes and labels
        for box in input_boxes:
            color = YELLOW if box["active"] else GRAY
            pygame.draw.rect(DISPLAYSUR, color, box["rect"], 2)
            text_surface = font.render(box["text"], True, WHITE)
            DISPLAYSUR.blit(text_surface, (box["rect"].x + 10, box["rect"].y + 10))
            label_surface = font.render(box["label"], True, GREEN)
            DISPLAYSUR.blit(label_surface, (box["rect"].x - 130, box["rect"].y + 10))

        pygame.display.flip()


def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(DISPLAYSUR, 'light gray', [570 - (column * 190), row * 95, 95, 95])
        else:
            pygame.draw.rect(DISPLAYSUR, 'light gray', [665 - (column * 190), row * 95, 95, 95])
        pygame.draw.rect(DISPLAYSUR, 'gray', [0, 760, WIDTH, 95])
        pygame.draw.rect(DISPLAYSUR, 'gold', [0, 760, WIDTH, 65], 5)
        pygame.draw.rect(DISPLAYSUR, 'gold', [760, 0, 240, HEIGHT], 5)
        status_text = [f'{input_boxes[0]["text"]}: Select a piece to Move!', f'{input_boxes[0]["text"]}: Select a Destination!',
                       f'{input_boxes[1]["text"]}: Select a piece to Move!', f'{input_boxes[1]["text"]}: Select a Destination!']
        DISPLAYSUR.blit(big_font.render(status_text[turn_step], True, 'black'),(15,770))
        for i in range(9):
            pygame.draw.line(DISPLAYSUR, 'black', (0, 95 * i), (760, 95 * i), 2)
            pygame.draw.line(DISPLAYSUR, 'black', (95 * i, 0), (95 * i, 760), 2)
        DISPLAYSUR.blit(big_font.render('FORFEIT', True, 'black'), (780, 775))

def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            DISPLAYSUR.blit(white_pawn, (white_locations[i][0] * 95 + 17, white_locations[i][1] * 95 + 25))    
        else:
            DISPLAYSUR.blit(white_images[index], (white_locations[i][0] * 95 + 10, white_locations[i][1] * 95 + 10))
        if turn_step <2: # mark red after selection
            if selection == i:
                pygame.draw.rect(DISPLAYSUR, 'red', [white_locations[i][0] * 95 + 1, white_locations[i][1] * 95 + 1, 95, 95], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            DISPLAYSUR.blit(black_pawn, (black_locations[i][0] * 95 + 17, black_locations[i][1] * 95 + 25))    
        else:
            DISPLAYSUR.blit(black_images[index], (black_locations[i][0] * 95 + 10, black_locations[i][1] * 95 + 10))
        if turn_step >= 2: # mark blue after selection
            if selection == i:
                pygame.draw.rect(DISPLAYSUR, 'blue', [black_locations[i][0] * 95 + 1, black_locations[i][1] * 95 + 1, 95, 95], 2)

def check_options(pieces, locations, turn, allow_king=True):
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]

        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king' and allow_king:
            # Only allow king logic if not in recursive call
            opponent_pieces = black_pieces if turn == 'white' else white_pieces
            opponent_locations = black_locations if turn == 'white' else white_locations
            opponent_options_temp = check_options(opponent_pieces, opponent_locations, 'black' if turn == 'white' else 'white', allow_king=False)
            moves_list = check_king(location, turn, opponent_options_temp)


        all_moves_list.append(moves_list)
    return all_moves_list

'''def is_checkmate(color):
    if color == 'white':
        pieces = white_pieces
        locations = white_locations
        options = white_options
        king_index = pieces.index('king') if 'king' in pieces else -1
        if king_index == -1:
            return False  # Already captured
        king_loc = locations[king_index]
        opponent_options = black_options
    else:
        pieces = black_pieces
        locations = black_locations
        options = black_options
        king_index = pieces.index('king') if 'king' in pieces else -1
        if king_index == -1:
            return False
        king_loc = locations[king_index]
        opponent_options = white_options

    # Check if king is in check
    is_in_check = any(king_loc in option for option in opponent_options)
    if not is_in_check:
        return False

    # Simulate all moves, if none resolve check → checkmate
    for i in range(len(pieces)):
        for move in options[i]:
            orig_pos = locations[i]
            captured_piece = None
            if color == 'white':
                if move in black_locations:
                    captured_index = black_locations.index(move)
                    captured_piece = (black_pieces[captured_index], black_locations[captured_index])
                    black_pieces.pop(captured_index)
                    black_locations.pop(captured_index)
                locations[i] = move
                test_white_options = check_options(white_pieces, white_locations, 'white')
                test_king_loc = white_locations[white_pieces.index('king')]
                if all(test_king_loc not in opt for opt in black_options):
                    # Undo move
                    locations[i] = orig_pos
                    if captured_piece:
                        black_pieces.insert(captured_index, captured_piece[0])
                        black_locations.insert(captured_index, captured_piece[1])
                    return False
                locations[i] = orig_pos
                if captured_piece:
                    black_pieces.insert(captured_index, captured_piece[0])
                    black_locations.insert(captured_index, captured_piece[1])
            else:
                if move in white_locations:
                    captured_index = white_locations.index(move)
                    captured_piece = (white_pieces[captured_index], white_locations[captured_index])
                    white_pieces.pop(captured_index)
                    white_locations.pop(captured_index)
                locations[i] = move
                test_black_options = check_options(black_pieces, black_locations, 'black')
                test_king_loc = black_locations[black_pieces.index('king')]
                if all(test_king_loc not in opt for opt in white_options):
                    locations[i] = orig_pos
                    if captured_piece:
                        white_pieces.insert(captured_index, captured_piece[0])
                        white_locations.insert(captured_index, captured_piece[1])
                    return False
                locations[i] = orig_pos
                if captured_piece:
                    white_pieces.insert(captured_index, captured_piece[0])
                    white_locations.insert(captured_index, captured_piece[1])
    return True
'''

def is_checkmate(color):
    if color == 'white':
        pieces = white_pieces
        locations = white_locations
        options = white_options
        king_index = pieces.index('king') if 'king' in pieces else -1
        if king_index == -1:
            return False  # Already captured
        king_loc = locations[king_index]
        opponent_pieces = black_pieces
        opponent_locations = black_locations
        opponent_color = 'black'
    else:
        pieces = black_pieces
        locations = black_locations
        options = black_options
        king_index = pieces.index('king') if 'king' in pieces else -1
        if king_index == -1:
            return False
        king_loc = locations[king_index]
        opponent_pieces = white_pieces
        opponent_locations = white_locations
        opponent_color = 'white'

    # Check if king is in check
    opponent_options = check_options(opponent_pieces, opponent_locations, opponent_color)
    is_in_check = any(king_loc in option for option in opponent_options)
    if not is_in_check:
        return False

    # Simulate all moves, if none resolve check → checkmate
    for i in range(len(pieces)):
        original_position = locations[i]
        original_piece = pieces[i]

        for move in options[i]:
            captured_piece = None

            # Simulate move
            if move in opponent_locations:
                captured_index = opponent_locations.index(move)
                captured_piece = (opponent_pieces[captured_index], opponent_locations[captured_index])
                opponent_pieces.pop(captured_index)
                opponent_locations.pop(captured_index)

            locations[i] = move

            # Recalculate opponent options to verify if check is resolved
            new_opponent_options = check_options(opponent_pieces, opponent_locations, opponent_color)
            test_king_loc = locations[pieces.index('king')]
            if all(test_king_loc not in opt for opt in new_opponent_options):
                # Undo move
                locations[i] = original_position
                if captured_piece:
                    opponent_pieces.insert(captured_index, captured_piece[0])
                    opponent_locations.insert(captured_index, captured_piece[1])
                return False

            # Undo move
            locations[i] = original_position
            if captured_piece:
                opponent_pieces.insert(captured_index, captured_piece[0])
                opponent_locations.insert(captured_index, captured_piece[1])

    return True


def check_king(position, color, opponent_options):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations

    # Normal king moves
    directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for dx, dy in directions:
        x, y = position[0] + dx, position[1] + dy
        if 0 <= x <= 7 and 0 <= y <= 7 and (x, y) not in friends_list:
            moves_list.append((x, y))

    # Castling logic
    if color == 'white' and not white_king_moved and position == (4, 7):
        # Kingside
        if not white_rook_kingside_moved and (5, 7) not in white_locations + black_locations and (6, 7) not in white_locations + black_locations:
            if not any((pos in opponent_options[i]) for i in range(len(opponent_options)) for pos in [(4,7), (5,7), (6,7)]):
                moves_list.append((6, 7))  # Castling kingside
        # Queenside
        if not white_rook_queenside_moved and all(pos not in white_locations + black_locations for pos in [(1,7), (2,7), (3,7)]):
            if not any((pos in opponent_options[i]) for i in range(len(opponent_options)) for pos in [(4,7), (3,7), (2,7)]):
                moves_list.append((2, 7))  # Castling queenside

    elif color == 'black' and not black_king_moved and position == (4, 0):
        # Kingside
        if not black_rook_kingside_moved and (5, 0) not in white_locations + black_locations and (6, 0) not in white_locations + black_locations:
            if not any((pos in opponent_options[i]) for i in range(len(opponent_options)) for pos in [(4,0), (5,0), (6,0)]):
                moves_list.append((6, 0))  # Castling kingside
        # Queenside
        if not black_rook_queenside_moved and all(pos not in white_locations + black_locations for pos in [(1,0), (2,0), (3,0)]):
            if not any((pos in opponent_options[i]) for i in range(len(opponent_options)) for pos in [(4,0), (3,0), (2,0)]):
                moves_list.append((2, 0))  # Castling queenside

    return moves_list


def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list

def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True # to check if there is a free space
        chain = 1 # to print the chain of the path
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def check_pawn(position, color): 
    moves_list = []
    if color == 'black':
        if (position[0], position[1] + 1) not in black_locations and \
        (position[0], position[1] + 1) not in white_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in black_locations and \
        (position[0], position[1] + 1) not in black_locations and \
        (position[0], position[1] + 1) not in white_locations and \
        (position[0], position[1] + 2) not in white_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] + 1))

    else:
        if (position[0], position[1] - 1) not in white_locations and \
        (position[0], position[1] -  1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations and \
        (position[0], position[1] - 1) not in white_locations and \
        (position[0], position[1] -  1) not in black_locations and \
        (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    
    return moves_list

def promote_pawn(color, index, location):
    promoting = True
    while promoting:
        DISPLAYSUR.fill('black')
        DISPLAYSUR.blit(big_font.render('Choose promotion piece:', True, 'white'), (250, 300))
        choices = ['queen', 'rook', 'bishop', 'knight']
        for i, piece in enumerate(choices):
            if color == 'white':
                DISPLAYSUR.blit(white_images[piece_list.index(piece)], (200 + i * 120, 400))
            else:
                DISPLAYSUR.blit(black_images[piece_list.index(piece)], (200 + i * 120, 400))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i in range(4):
                    rect = pygame.Rect(200 + i * 120, 400, 80, 80)
                    if rect.collidepoint(x, y):
                        new_piece = choices[i]
                        if color == 'white':
                            white_pieces[index] = new_piece
                        else:
                            black_pieces[index] = new_piece
                        promoting = False


def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else: 
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(DISPLAYSUR, color, (moves[i][0] * 95 + 47, moves[i][1] * 95 + 47), 5)

def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        DISPLAYSUR.blit(small_black_images[index], (790, 5 + 47 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        DISPLAYSUR.blit(small_white_images[index], (890, 5 + 47 * i))

def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(DISPLAYSUR, 'dark red', [white_locations[king_index][0] * 95 + 1,
                                                              white_locations[king_index][1] * 95 + 1, 95, 95], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(DISPLAYSUR, 'dark blue', [black_locations[king_index][0] * 95 + 1,
                                                               black_locations[king_index][1] * 95 + 1, 95, 95], 5)

def draw_game_over():
    pygame.draw.rect(DISPLAYSUR, 'black', [200, 200, 400, 80])
    DISPLAYSUR.blit(font.render(f'{winner} won the game!', True, 'white'), (210,210))
    DISPLAYSUR.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210,240))

# main game loop
white_options = check_options(white_pieces, white_locations, 'white', allow_king=True)
black_options = check_options(black_pieces, black_locations, 'black', allow_king=True)

run = True
advertisement()
print(input_boxes[0]["text"], input_boxes[1]["text"])
if (input_boxes[0]["text"] == '' and input_boxes[1]["text"] == ''):
    run = False
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    DISPLAYSUR.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 95
            y_coord = event.pos[1] // 95
            click_coords = (x_coord, y_coord)
            if turn_step < 2:
                if click_coords == (8, 8) or click_coords == (9, 8): # forfeit
                    winner = input_boxes[1]["text"]
                if click_coords in white_locations: # selection
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords

                    # Track white king movement
                    if white_pieces[selection] == 'king':
                        white_king_moved = True
                        # Kingside castling
                        if click_coords == (6, 7):
                            rook_index = white_locations.index((7, 7))
                            white_locations[rook_index] = (5, 7)
                        # Queenside castling
                        elif click_coords == (2, 7):
                            rook_index = white_locations.index((0, 7))
                            white_locations[rook_index] = (3, 7)

                    # Track white rook movement
                    if white_pieces[selection] == 'rook':
                        if (white_locations[selection] == (0, 7)):
                            white_rook_queenside_moved = True
                        elif (white_locations[selection] == (7, 7)):
                            white_rook_kingside_moved = True

                    # Check for white pawn promotion
                    if white_pieces[selection] == 'pawn' and white_locations[selection][1] == 0:
                        promote_pawn('white', selection, white_locations[selection])

                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = input_boxes[0]["text"]
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black', allow_king=True)
                    white_options = check_options(white_pieces, white_locations, 'white', allow_king=True)
                    turn_step = 2
                    selection = 100
                    valid_moves = []
                    white_options = check_options(white_pieces, white_locations, 'white', allow_king=True)
                    black_options = check_options(black_pieces, black_locations, 'black', allow_king=True)


            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8): # forfeit
                    winner = input_boxes[0]["text"]
                if click_coords in black_locations: # selection
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                
                if click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords

                    # Track black king movement
                    if black_pieces[selection] == 'king':
                        black_king_moved = True
                        # Kingside castling
                        if click_coords == (6, 0):
                            rook_index = black_locations.index((7, 0))
                            black_locations[rook_index] = (5, 0)
                        # Queenside castling
                        elif click_coords == (2, 0):
                            rook_index = black_locations.index((0, 0))
                            black_locations[rook_index] = (3, 0)

                    # Track black rook movement
                    if black_pieces[selection] == 'rook':
                        if (black_locations[selection] == (0, 0)):
                            black_rook_queenside_moved = True
                        elif (black_locations[selection] == (7, 0)):
                            black_rook_kingside_moved = True

                    # Check for black pawn promotion
                    if black_pieces[selection] == 'pawn' and black_locations[selection][1] == 7:
                        promote_pawn('black', selection, black_locations[selection])

                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = input_boxes[1]["text"]
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    white_options = check_options(white_pieces, white_locations, 'white', allow_king=True)
                    black_options = check_options(black_pieces, black_locations, 'black', allow_king=True)
                    turn_step = 0
                    selection = 100
                    valid_moves = []

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook','knight','bishop','queen','king','bishop','knight','rook',
                'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn',]
                white_locations = [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),
                   (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]
                black_pieces = ['rook','knight','bishop','queen','king','bishop','knight','rook',
                'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn',]
                black_locations = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                   (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black', allow_king=True)
                white_options = check_options(white_pieces, white_locations, 'white', allow_king=True)

    if winner != '':
        game_over = True
        draw_game_over()

    if not game_over:
        if is_checkmate('white'):
            winner = input_boxes[1]["text"]  # Black wins
            game_over = True
        elif is_checkmate('black'):
            winner = input_boxes[0]["text"]  # White wins
            game_over = True

    pygame.display.flip()
pygame.quit()
