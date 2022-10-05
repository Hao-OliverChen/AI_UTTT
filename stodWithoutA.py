from ast import Try
from cmath import inf
from enum import Enum
from multiprocessing.connection import wait
import os
from os.path import exists
from collections import Counter
from time import sleep, time
import numpy as np

# --------------------------------------------------------
# state: a long string that stores the current board configuration (each positioin is either a "X" which is the first player, a "O" which is the second player or a "*" which is empty)
# global_num: a number indicate the position on the global_board [0 to 80]
# move: a list [x, y] where x - "int" - is the local_board [0 to 8],  y - "int" - is the position on local_board x [0 to 8]
# move_info: a list [x, y] where x - "string" - is the team name,  y - "list" - a move that team x made 
#
# The following is a global board containing the 9 local boards [local_board_0: [0 to 8] , local_board_1: [9 to 17] , ... , local_board_8: [72 to 80]]
#  --------------------------------
# |  0  1  2 | 9  10 11 | 18 19 20 |
# |  3  4  5 | 12 13 14 | 21 22 23 |
# |  6  7  8 | 15 16 17 | 24 25 26 |
#  --------------------------------
# | 27 28 29 | 36 37 38 | 45 46 47 |
# | 30 31 32 | 39 40 41 | 48 49 50 |
# | 33 34 35 | 42 43 44 | 51 52 53 |
#  --------------------------------
# | 54 55 56 | 63 64 65 | 72 73 74 |
# | 57 58 59 | 66 67 68 | 75 76 77 |
# | 60 61 62 | 69 70 71 | 78 79 80 |
#  --------------------------------
#
# --------------------------------------------------------

class PlayerOrder(Enum):
    UNDECIDE = 0
    FIRST = 1
    SECOND = 2

def main():
    # vector array for both players
    firstPlayerMoves = []
    secondPlayerMoves = []
    myMove = 0
    my_order = PlayerOrder.UNDECIDE 
    my_symbol = ""
    DEPTH = 5
    isRead = False
    roundCounter = 0

    # initialize the state, global_board and the win_condition
    state = "*" * 81
    global_board = ["*"] * 9 # local boards on the global board
    win_condition = [(0, 4, 8), (2, 4, 6),
                      (0, 1, 2), (3, 4, 5),
                      (6, 7, 8), (0, 3, 6),
                      (1, 4, 7), (2, 5, 8)] # all 8 possible winning conditions
    
    print("--------------------------Game start--------------------------")
    
   # basic game loop
    while True:
        
        # if end_game exist break the loop
        end_game_exists = exists("end_game")
        if end_game_exists:
            break

        # wait for the .go file to show up
        while not exists("stodWithoutA.go"):
            pass

        # start timer
        start_time = time()
        
        # keep track of rounds
        roundCounter+=1
        print("----------------Round " + str(roundCounter) + " ----------------")
        
        # reading the first four move (but just for once)
        if not isRead: 
            # open first_four_moves file with r - read only access mode
            first_four_moves = open("first_four_moves", "r")
            # get the contents of the first_four_moves file
            first_four_moves_contents = first_four_moves.readlines()
            # close first_four_moves
            first_four_moves.close()

            # move counter for first 4 moves
            move_count = 1

            # adding the moves to its corresponding array
            for move in first_four_moves_contents:
                # get move_info
                teamname,temp_arr = extractMoveInfo(move)
                global_pos = local_to_global(temp_arr)
                
                # determine the order
                if move_count == 1:
                    if teamname == "stodWithoutA": my_order = PlayerOrder.FIRST
                    else: my_order = PlayerOrder.SECOND

                # append move to corresponding player array
                if move_count % 2 == 1:
                    firstPlayerMoves.append(global_pos)
                    state = add_move(state, global_pos, "X")
                else: 
                    secondPlayerMoves.append(global_pos)
                    state = add_move(state, global_pos, "O")

                # increment the move count after each iteration
                move_count+=1

            # set the flag to true
            isRead = True
            
            # decide my symbol
            my_symbol = mySymbol(my_order)
            print(my_order)
            print("my symbol: " + my_symbol)
            print("--------------End of first_four_moves processing--------------")
            
        # check if the move_file is empty
        isMoveFileEmpty = os.path.getsize("move_file") == 0

        if not isMoveFileEmpty:
            # after receiving the signal
            # read, write, close
            move_file = open("move_file","r")
            
            lastLine = ""
            #print("------------------reading---------------")
            for line in move_file:
                #print(line)
                lastLine = line
            #print("------------------reading done---------------")
            
            opponentMove = lastLine # get the last move_info my opponent made
            move_file.close()
            opponentMove = extractMoveInfo(opponentMove)[1] # get the last move my opponent made
            opponentMove = local_to_global(opponentMove) # convert the local board position to global_board position
            
            # store the opponent move accordingly
            if my_order == PlayerOrder.FIRST:
                secondPlayerMoves.append(opponentMove)
            elif my_order ==  PlayerOrder.SECOND:
                firstPlayerMoves.append(opponentMove)
            
            # update state and global_board
            state = add_move(state, opponentMove, opponent(my_symbol))
            global_board = update_global_board(state, win_condition)
        
        
        if my_order == PlayerOrder.FIRST:
            last_move = global_to_local(secondPlayerMoves[-1])
            print("My moves - X")
            print(firstPlayerMoves)
            print("Opponent - O")
            print(secondPlayerMoves)
            print("Last move from O:")
            print(last_move)
            myMove = UTTTAI(state, last_move, DEPTH, start_time, my_symbol, global_board, win_condition)
        elif my_order == PlayerOrder.SECOND:
            last_move = global_to_local(firstPlayerMoves[-1])
            print("My moves - O")
            print(secondPlayerMoves)
            print("Opponent - X")
            print(firstPlayerMoves)
            print("Last move from X:")
            print(last_move)
            myMove = UTTTAI(state, last_move, DEPTH, start_time, my_symbol, global_board, win_condition)
            
        # update state and global_board
        print("My choice:")
        print(myMove[1])
        myMove = local_to_global(myMove[1])
        state = add_move(state, myMove, my_symbol)
        global_board = update_global_board(state, win_condition)

        # store the my move accordingly
        if my_order == PlayerOrder.FIRST:
            firstPlayerMoves.append(myMove)
        elif my_order ==  PlayerOrder.SECOND:
            secondPlayerMoves.append(myMove)
        
        # write the move to the move_file
        myMove = global_to_local(myMove)
        myName = "stodWithoutA"
        final_move = myName + " " + str(myMove[0]) + " " + str(myMove[1])
        # using 'r+' to avoid timestamp modification at the beginning 
        file = open('move_file', 'r+')
        file.seek(0)
        file.write(final_move)
        file.truncate()
        file.close()
        # To avoid chaos in communication, wait 0.1 second before heading to the next game loop
        sleep(0.3)

    # ends program when end_game is found
    print("File 'end_game' is found! Game is over!")
      

# Ultimate Tic Tac Toe AI aka the beast of UTTT
def UTTTAI(state, last_move, depth, start_time, my_symbol, global_board, win_condition):
    return minimax(state, last_move, depth, start_time, my_symbol, global_board, win_condition)

# decide on my symbol
def mySymbol(my_order):
    # deciding my symbol 
    if my_order == PlayerOrder.FIRST:
       return "X"
    else: return "O"

# last_move is a move
# info - [x, y] where x is a state with a corresponding global_num y
def minimax(state, last_move, depth, start_time, my_symbol, global_board, win_condition):
    # evaluate each possible move
    potential_moves_info = findValidMoves(state, my_symbol, last_move, global_board)
    # for id in potential_moves_info:
    #     print("potential_moves_info")
    #     print(id[1])
    #     print("state")
    #     print(id[0])
    optimal_move = (-inf, None)
    for info in potential_moves_info:
        val = min_turn(info[0], info[1], opponent(my_symbol), depth - 1, start_time, -inf, inf, global_board, win_condition)
        if val > optimal_move[0]:
            optimal_move = (val, info)
    return optimal_move[1] # return the optimal move [state, move]

def max_turn(state, last_move, my_symbol, depth, start_time, alpha, beta, global_board, win_condition):
    if depth <= 0 or check_board_winner(global_board, win_condition) != "*" or time() - start_time >= 9.5:
        # print("MAX_score:")
        # print(evaluateTotalScore(state, my_symbol, global_board ,win_condition))
        return evaluateTotalScore(state, my_symbol, global_board ,win_condition)
    potential_moves_info = findValidMoves(state, my_symbol, last_move, global_board)
    for info in potential_moves_info:
        val = min_turn(info[0], info[1], opponent(my_symbol), depth - 1, start_time, alpha, beta, global_board, win_condition)
        if alpha < val:
            alpha = val
        if alpha >= beta:
            break
    return alpha

def min_turn(state, last_move, my_symbol, depth, start_time, alpha, beta, global_board, win_condition):
    if depth <= 0 or check_board_winner(global_board, win_condition) != "*" or time() - start_time >= 9.5:
        # print("MIN_score:")
        # print(evaluateTotalScore(state, opponent(my_symbol), global_board ,win_condition))
        return evaluateTotalScore(state, opponent(my_symbol), global_board ,win_condition)
    potential_moves_info = findValidMoves(state, my_symbol, last_move, global_board)
    for info in potential_moves_info:
        val = max_turn(info[0], info[1], opponent(my_symbol), depth - 1, start_time, alpha, beta, global_board, win_condition)
        if val < beta:
            beta = val
        if alpha >= beta:
            break
    return beta

# check the winnner of any board
def check_board_winner(board, win_condition):
    for idxs in win_condition:
        (x, y, z) = idxs
        if (board[x] == board[y] == board[z]) and board[x] != "*":
            return board[x]
    return "*"
    

# return all the valid moves 
def findValidMoves(state, symbol, last_move, global_board):
    board_to_play = last_move[1]
    global_idxs = indices_of_board(board_to_play)
    
    # array for tuples
    possible_indices = []
    possible_states = []
    # for the condition where the local board has been won
    if global_board[board_to_play] != "*":
        # find all possible moves across the board and return them in a tuple
        for a in range(9):
            if global_board[a] == "*":
                for slot in indices_of_board(a):
                    if state[slot] == "*":
                        local_slot = global_to_local(slot)
                        possible_indices.append(local_slot)
                        possible_states.append(add_move(state, slot, symbol))
    else: 
        for slot in global_idxs:
            if state[slot] == "*":
                local_slot = global_to_local(slot)
                possible_indices.append(local_slot)
                possible_states.append(add_move(state, slot, symbol))      
                 
    return zip(possible_states, possible_indices)

# evaluate the overall player score
def evaluateTotalScore(state, symbol, global_board, win_condition):
    score = 0
    score += evaluateUtilityScorePerBoard(global_board, symbol, win_condition) * 200
    for slot in range(9):
        idxs = indices_of_board(slot)
        board = state[idxs[0]: idxs[-1]+1]
        score += evaluateUtilityScorePerBoard(board, symbol, win_condition)
    return score

# evaluate function for each board
def evaluateUtilityScorePerBoard(board, symbol, win_condition):
    score = 0
    three_in_a_row = Counter(symbol * 3)
    two_in_a_row = Counter(symbol * 2 + "*")
    one_in_a_row = Counter(symbol * 1 + "*" * 2)
    three_in_a_row_opponent = Counter(opponent(symbol) * 3)
    two_in_a_row_opponent = Counter(opponent(symbol) * 2 + "*")
    one_in_a_row_opponent = Counter(opponent(symbol) * 1 + "*" * 2)

    # check each win condition and grant a score 
    for idxs in win_condition:
        (a, b, c) = idxs
        current = Counter([board[a], board[b], board[c]])

        if current == three_in_a_row:
            score += 150
        elif current == two_in_a_row:
            score += 30
        elif current == one_in_a_row:
            score += 2
        elif current == three_in_a_row_opponent:
            score -= 100
            # if opponent got three in a row, return immediately
            return score
        elif current == two_in_a_row_opponent:
            score -= 10
        elif current == one_in_a_row_opponent:
            score -= 1

    return score

# takes in a move_info(string with team name and move) and return the team name and move 
def extractMoveInfo(move_info):
    space_counter = 0
    teamname = ""
    temp_arr = []
    # get the team name and move
    for char in move_info:
        if char == " ":
            space_counter+=1
        elif space_counter == 0:
            teamname = teamname + char
        else:
            temp_arr.append(char)
    return  teamname,temp_arr

# update the global_board with the most recent state
def update_global_board(state, win_condition):
    temp_global_board = ["*"] * 9
    for slot in range(9):
        idxs_board = indices_of_board(slot)
        board = state[idxs_board[0]: idxs_board[-1]+1]
        temp_global_board[slot] = check_board_winner(board, win_condition)
    return temp_global_board
    
# convert local board to global board
def global_to_local(global_num):
    board_num = int(np.floor(global_num/9))
    localBoard_num = global_num - board_num * 9
    return [ board_num ,localBoard_num]
    
# convert global board to local board
def local_to_global(global_local_coord):
    return int(global_local_coord[0]) * 9 + int(global_local_coord[1])

# get opponent symbol
def opponent(player):
    return "O" if player == "X" else "X"

# pass in a local board number and return all the corresponding global numbers
def indices_of_board(local_board_num):
    return list(range(local_board_num*9, local_board_num*9 + 9))

# adding move to the state with the corresponding player symbol
def add_move(state, move, symbol):
    return state[: move] + symbol + state[move+1:]

if __name__ == "__main__":
    main()
