import os
import keyboard
import json
import time
import msvcrt

def clear_input_buffer():
    while msvcrt.kbhit():
        msvcrt.getch()
        
def save_game(board, cursor_r, cursor_c, player, is_single_player):
    with open("save.json", "w") as f:
        json.dump([board, cursor_r, cursor_c, player, is_single_player], f)

def load_game():
    try:
        with open("save.json", "r") as f:
            return json.load(f)
    except:
        return None

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def create_board():
    board = []
    for _ in range(6):
        board.append([" ", " ", " ", " ", " ", " "])
    return board


def print_board(board, cursor_r, cursor_c, current_player):
    clear_screen()
    print(" ┌───┬───┬───┬───┬───┬───┐")
    for i in range(6):
        row_str = " │ "
        for j in range(6):
            piece = board[i][j]
            if piece == "R":
                char = "●"
                fg_color = "\033[91m"
            elif piece == "B":
                char = "●"
                fg_color = "\033[94m"
            else:
                char = " "
                fg_color = ""


            if i == cursor_r and j == cursor_c:
                bg_color = "\033[42m"
            else:
                bg_color = ""

            reset_color = "\033[0m"

            row_str += f"{bg_color}{fg_color}{char}{reset_color} │ "

        print(row_str)
        if i < 5:
            print(" ├───┼───┼───┼───┼───┼───┤")
    print(" └───┴───┴───┴───┴───┴───┘")
    print("   1   2   3   4   5   6  ")

    player_color = (
        "\033[91mRed move:\033[0m"
        if current_player == 1
        else "\033[94mBlue move:\033[0m"
    )
    print(f"\n{player_color}")
    print(
        "\033[95mControls: [A]Left [D]Right | [E]Enter Piece | [Q]Quit\033[0m"
    )


def check_win(board):
    ROWS = 6
    COLS = 6
    
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (
                board[r][c] != " "
                and board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3]
            ):
                return board[r][c]
           
    for r in range(ROWS - 3):
        for c in range(COLS):
            if (
                board[r][c] != " "
                and board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c]
            ):
                return board[r][c]
    
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (
                board[r][c] != " "
                and board[r][c]== board[r + 1][c + 1]== board[r + 2][c + 2]== board[r + 3][c + 3]
            ):
                return board[r][c]
    
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (
                board[r][c] != " "
                and board[r][c]== board[r - 1][c + 1]== board[r - 2][c + 2]== board[r - 3][c + 3]
            ):
                return board[r][c]

    return None

def check_draw(board):
    for col in range(len(board[0])):
        if board[0][col] == ' ': 
            return False  
    return True

def check_early_draw(board):
   
    ROWS = 6
    COLS = 6
    
    empty_cells = []
    count_R = 0
    count_B = 0
    
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                empty_cells.append((r, c))
            elif board[r][c] == 'R':
                count_R += 1
            elif board[r][c] == 'B':
                count_B += 1
    
    if len(empty_cells) == 1:
        turn = 'R' if count_R == count_B else 'B'
        r, c = empty_cells[0]
        board[r][c] = turn
        winner = check_win(board)
        board[r][c] = ' ' 
        
        if winner is None:
            return True
        return False

    def is_line_dead(line):
        return ('R' in line) and ('B' in line)

    for r in range(ROWS):
        for c in range(COLS - 3):
            if not is_line_dead([board[r][c+i] for i in range(4)]): return False
            if not is_line_dead([board[c+i][r] for i in range(4)]): return False

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if not is_line_dead([board[r+i][c+i] for i in range(4)]): return False
            if not is_line_dead([board[r+3-i][c+i] for i in range(4)]): return False

    return True

def get_computer_move(board, comp_piece='B', player_piece='R'):
    ROWS = 6
    COLS = 6
    valid_cols = [c for c in range(COLS) if board[0][c] == ' ']

    def get_row(c):
        for r in range(ROWS-1, -1, -1):
            if board[r][c] == ' ': return r
            
            
    for piece in [comp_piece, player_piece]:
        for col in valid_cols:
            row = get_row(col)
            board[row][col] = piece        
            winner = check_win(board)      
            board[row][col] = ' '          
            if winner == piece:
                return col   
                         
    for col in [2, 3, 1, 4, 0, 5]:
        if col in valid_cols:
            return col

 
def play_game(loaded_data=None, is_single_player=False):
    if loaded_data:
        game_board, cursor_r, cursor_c, current_player, is_single_player = loaded_data
        msg = "\033[92mGame loaded successfully!\033[0m"
    else:
        game_board = create_board()
        cursor_r = 0
        cursor_c = 0
        current_player = 1
        msg = ""

    while True:
        print_board(game_board, cursor_r, cursor_c, current_player)
        if msg:
            print(msg)
            msg = "" 
            
        if is_single_player and current_player == 2: 
            time.sleep(0.5)
            cursor_c = get_computer_move(game_board, 'B', 'R') 
            move = 'e'
        else:
            kbe = keyboard.read_event()
            if str(kbe.event_type) != "up":
                continue
            move = str(kbe.name).lower()

        if move == 'q':
            print("\n\033[92mDo you want to save the game before exiting? (y/n): \033[0m")
            clear_input_buffer()
            while True:
                ans = keyboard.read_key()
                if ans.lower() == 'y' or ans.lower() == 'n':
                    break
            if ans.lower() == 'y':
                save_game(game_board, cursor_r, cursor_c, current_player, is_single_player)
                print("\033[92mGame saved successfully!\033[0m")
            print("\033[93mGame Over!\033[0m")
            clear_input_buffer()
            input("\n\033[95mPress Enter to return to menu...\033[0m")
            break

        elif move == "d" and cursor_c < 5:
            cursor_c += 1
        elif move == "a" and cursor_c > 0:
            cursor_c -= 1
        elif move == "e":
            piece_dropped = False
            
            for r in range(5, -1, -1):
                if game_board[r][cursor_c] == " ":
                    if current_player == 1:
                        game_board[r][cursor_c] = "R"
                        current_player = 2
                    else:
                        game_board[r][cursor_c] = "B"
                        current_player = 1
                    piece_dropped = True
                    break
                
            if piece_dropped:
                winner = check_win(game_board)
                if winner:
                    print_board(game_board, cursor_r, cursor_c, current_player)
                    winner_color = (
                        "\033[91mRed Wins!\033[0m"
                        if winner == "R"
                        else "\033[94mBlue Wins!\033[0m"
                    )
                    print(f"\n{winner_color}")
                    clear_input_buffer()
                    input("\n\033[95mPress Enter to return to menu...\033[0m")
                    break

                elif check_early_draw(game_board):
                    print_board(game_board, cursor_r, cursor_c, current_player)
                    print("\n\033[93mEarly Draw! No one can win anymore.\033[0m")
                    clear_input_buffer()
                    input("\n\033[95mPress Enter to return to menu...\033[0m")
                    break

                elif check_draw(game_board):
                    print_board(game_board, cursor_r, cursor_c, current_player)
                    print("\n\033[93mDraw! The board is full.\033[0m")
                    clear_input_buffer()
                    input("\n\033[95mPress Enter to return to menu...\033[0m")
                    break
            else:
                msg = "\033[91mColumn is full!\033[0m"

def main_menu():
    while True:
        clear_screen()
        
        print("\033[95m            Connect 4              \033[0m")
        print("\033[95m┌─────────────────────────────────┐\033[0m")
        print("\033[95m│  [1]: Two Player Game           │\033[0m")
        print("\033[95m│  [2]: One Player (vs Computer)  │\033[0m")
        print("\033[95m│  [3]: Load Game                 │\033[0m")
        print("\033[95m│  [4]: Exit                      │\033[0m")
        print("\033[95m└─────────────────────────────────┘\033[0m\n")
        print("\033[95mEnter your choice: \033[0m")

        clear_input_buffer()
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            choice = event.name
            
            if choice == '1':
                play_game() 
            elif choice == '2':
                 play_game(is_single_player=True)
            elif choice == '3':
                saved_data = load_game()
                if saved_data:
                    if len(saved_data) == 4:
                        saved_data.append(False)
                    
                    single_flag = saved_data[4]
                    play_game(loaded_data=saved_data, is_single_player=single_flag)
                else:
                    print("\n\033[91mError: No saved game exists!\033[0m")
                    clear_input_buffer()
                    input("\033[93mPress Enter to return...\033[0m")

            elif choice == '4':
                clear_screen()
                break


if __name__ == "__main__":
    main_menu()
