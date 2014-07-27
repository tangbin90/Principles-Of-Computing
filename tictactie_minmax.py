"""
Mini-max Tic-Tac-Toe Player
"""
#http://www.codeskulptor.org/#user36_VWsFfAi9wYuyVGc_27.py
import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    empty=board.get_empty_squares()
    best_move=(3,(-1,-1))

    for items in empty:
        board_test=board.clone()
        board_test.move(items[0],items[1],player)
        winner=board_test.check_win()#check the new board not the old one
        if winner!=None:
            temp=SCORES[winner]*SCORES[player]
            if temp==1:#last player
                return SCORES[winner],items          
            elif best_move[0]==3:             	
                best_move=(SCORES[winner],items)
            elif best_move[0]*SCORES[player]<temp:
                best_move=(SCORES[winner],items)  
                    
            continue
        cal_move=mm_move(board_test,provided.switch_player(player))
        if cal_move[0]*SCORES[player]==1:
            return (cal_move[0],items)#注意return的值
        elif best_move[0]==3:
            best_move=(cal_move[0],items)
        elif cal_move[0]*SCORES[player]>best_move[0]*SCORES[player]:
            best_move=(cal_move[0],items)
    return best_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    print move
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
