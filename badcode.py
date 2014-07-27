    
            
    '''        
    if player==provided.PLAYERO:
        for items in empty:
            board_test=board.clone()            
            board_test.move(items[0],items[1],player)
            winner=board_test.check_win()
            if winner==provided.PLAYERO:
                return (SCORES[provided.PLAYERO],items)
            elif winner==provided.DRAW:
                score.append((SCORES[provided.DRAW],items))
            elif winner==provided.PLAYERO:
                score.append((SCORES[provided.PLAYERO],items))	
            else:
                score.append(mm_move(board_test,provided.PLAYERX))
        for items in score:
            if items[0]==SCORES[provided.PLAYERO]:
                return items
        for items in score:
            if items[0]==SCORES[provided.DRAW]:
                return items
        for items in score:
            if items[0]==SCORES[provided.PLAYERX]:
                return items
    '''