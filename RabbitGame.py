import os
import keyboard
import random
import sys
from collections import deque

board_size = int(input("Enter the grid size: "))
rabbit_position = [0, 0]
rabbit_holding_carrot = False  # To track if the rabbit is holding a carrot

rabbit = 1
carrot = int(input("Enter number of carrots: "))
holes = int(input("Enter the number of Rabbit Holes: "))
pathway = (board_size**2) - (rabbit + carrot + holes)

element_counts = {"r": rabbit, "o": holes, "c": carrot, "-": pathway}

def create_game_map(size, element_counts):
    elements_list = [element for element, count in element_counts.items() for _ in range(count)]
    random.shuffle(elements_list)
    game_map = [['-' for _ in range(size)] for _ in range(size)]

    for element, count in element_counts.items():
        for _ in range(count):
            while True:
                row = random.randint(0, size - 1)
                col = random.randint(0, size - 1)
                if game_map[row][col] == '-':
                    game_map[row][col] = element
                    if element == 'r':
                        rabbit_position[0] = row
                        rabbit_position[1] = col
                    break

    return game_map

def display_board(game_map):
    os.system('cls')  # Use 'clear' instead of 'cls' for Unix-like systems
    for row in game_map:
        for element in row:
            print(element, end=" ")
        print()



# Main game loop
game_map = create_game_map(board_size, element_counts)
display_board(game_map)


while True:
    try: 
        event = keyboard.read_event()
        event_list = []
            
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'q':
                print("Exiting the program.")
                break
            elif event.name == 'w':
                next_row, next_col = rabbit_position[0] - 1, rabbit_position[1]
                if rabbit_position[0] > 0 and game_map[next_row][next_col] not in ('c', 'o'):
                    
                    # Move the rabbit up
                    game_map[rabbit_position[0]][rabbit_position[1]] = '-'
                    rabbit_position[0] -= 1
                    # if Rabbit has carrot then 'R' else 'r'
                    if(rabbit_holding_carrot):
                        game_map[rabbit_position[0]][rabbit_position[1]] = 'R'
                    else:
                        game_map[rabbit_position[0]][rabbit_position[1]] = 'r'
                display_board(game_map)
            elif event.name == 'a':
                next_row, next_col = rabbit_position[0] , rabbit_position[1] - 1
                if rabbit_position[0] > 0 and game_map[next_row][next_col] not in ('c', 'o'):
                    # Move the rabbit left
                    game_map[rabbit_position[0]][rabbit_position[1]] = '-'
                    rabbit_position[1] -= 1

                    # if Rabbit has carrot then 'R' else 'r'
                    if(rabbit_holding_carrot):
                        game_map[rabbit_position[0]][rabbit_position[1]] = 'R'
                    else:
                        game_map[rabbit_position[0]][rabbit_position[1]] = 'r'

                display_board(game_map)
            elif event.name == 's':
                next_row, next_col = rabbit_position[0] + 1, rabbit_position[1]
                if rabbit_position[0] > 0 and game_map[next_row][next_col] not in ('c', 'o'):
                    # Move the rabbit down
                    game_map[rabbit_position[0]][rabbit_position[1]] = '-'
                    rabbit_position[0] += 1
                    # if Rabbit has carrot then 'R' else 'r'
                    if(rabbit_holding_carrot):
                        game_map[rabbit_position[0]][rabbit_position[1]] = 'R'
                    else:
                        game_map[rabbit_position[0]][rabbit_position[1]] = 'r'
                display_board(game_map)
            elif event.name == 'd':
                next_row, next_col = rabbit_position[0] , rabbit_position[1] + 1
                if rabbit_position[0] > 0 and game_map[next_row][next_col] not in ('c', 'o'):
                    # Move the rabbit right
                    game_map[rabbit_position[0]][rabbit_position[1]] = '-'
                    rabbit_position[1] += 1

                    # if Rabbit has carrot then 'R' else 'r'
                    if(rabbit_holding_carrot):
                        game_map[rabbit_position[0]][rabbit_position[1]] = 'R'
                    else:
                        game_map[rabbit_position[0]][rabbit_position[1]] = 'r'
                        
                display_board(game_map)
            
            # For jumping over holes

            elif event.name == 'j':
                row, col = rabbit_position[0], rabbit_position[1]
                adjacent_positions = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                # Inside the 'j' key event block
                for adj_row, adj_col in adjacent_positions:
                    if (
                        0 <= adj_row < board_size
                        and 0 <= adj_col < board_size
                        and game_map[adj_row][adj_col] == 'o'
                    ):
                        # Check if the next position is empty for the jump
                        jump_row, jump_col = (2 * adj_row - row, 2 * adj_col - col)
                        if (
                            0 <= jump_row < board_size
                            and 0 <= jump_col < board_size
                            and game_map[jump_row][jump_col] == '-'
                        ):
                            # Perform the jump by creating a new tuple for rabbit_position
                            new_rabbit_position = [jump_row, jump_col]
                            game_map[row][col] = '-'
                            if rabbit_holding_carrot:
                                game_map[jump_row][jump_col] = 'R'
                            else:
                                game_map[jump_row][jump_col] = 'r'
                            rabbit_position = new_rabbit_position  # Update rabbit_position
                            display_board(game_map)
                            break  # Exit the loop after the first successful jump
                    else:
                        print("No hole to jump over in the current direction.")

            # For picking up and dropping carrots

            elif event.name == 'p':
                # Check if the rabbit is adjacent to a carrot
                row, col = rabbit_position[0], rabbit_position[1]
                adjacent_positions = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

                for adj_row, adj_col in adjacent_positions:
                    if (
                        0 <= adj_row < board_size
                        and 0 <= adj_col < board_size
                        and game_map[adj_row][adj_col] == 'c'
                        and not rabbit_holding_carrot
                    ):
                        # Found an adjacent carrot to pick up
                        game_map[row][col] = 'R'  # Change the symbol to 'R'
                        game_map[adj_row][adj_col] = '-'  # Remove the carrot from its position
                        display_board(game_map)
                        rabbit_holding_carrot = True
                    elif (
                        0 <= adj_row < board_size
                        and 0 <= adj_col < board_size
                        and game_map[adj_row][adj_col] == 'o' # Checking for a hole
                        and rabbit_holding_carrot
                    ):
                        game_map[row][col] = 'r' # Change symbol to 'r'
                        game_map[adj_row][adj_col] = 'O'
                        display_board(game_map)
                        rabbit_holding_carrot = False
                        print("Game Over, Press enter to exit")
                        input()
                        sys.exit()
            else:
                display_board(game_map)
                print("Invalid move.")
    except KeyboardInterrupt:
        break

    
    
    