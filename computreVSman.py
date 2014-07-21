"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided


# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 1    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
   
# Add your functions here.
def mc_trial(board, player):
    """
    try move
    """
    while board.check_win()==None:       
        empty_list=board.get_empty_squares()
        chose_place=empty_list[random.randrange(len(empty_list))]
        board.move(chose_place[0],chose_place[1],player)
        player=provided.switch_player(player)
    
def mc_update_scores(scores, board, player):
    """
    update scores
    """
    if board.check_win()==player:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):            	
                if board.square(row, col)==player:
                    scores[row][col]+= MCMATCH
                elif board.square(row, col)==provided.switch_player(player):
                     scores[row][col]-=MCOTHER
    elif board.check_win()==provided.switch_player(player):
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):            	
                if board.square(row, col)==player:
                    scores[row][col]-= MCMATCH
                elif board.square(row, col)==provided.switch_player(player):
                     scores[row][col]+=MCOTHER            	

def get_best_move(board, scores):
    """
    find the best move
    """
    emptylist=board.get_empty_squares()
    bestscore=[]
    bestscore.append(emptylist[0])

    for looper in range(1,len(emptylist)):
        if scores[bestscore[0][0]][bestscore[0][1]]<\
            scores[emptylist[looper][0]][emptylist[looper][1]]:
            bestscore=[]
            bestscore.append(emptylist[looper])
        elif scores[bestscore[0][0]][bestscore[0][1]]==\
            scores[emptylist[looper][0]][emptylist[looper][1]]:
            bestscore.append(emptylist[looper])    
    print bestscore[random.randrange(len(bestscore))]
    return bestscore[random.randrange(len(bestscore))]

def mc_move(board, player, trials):
    """
    move in the board
    """
    scores= [[0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    clone_board=board.clone()
    for dummy_looper in range(trials):
        mc_trial(clone_board, player)
        mc_update_scores(scores, clone_board, player)
    return get_best_move(board, scores)
        
        
# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
