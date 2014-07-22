"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    count=0
    while 0 in line:
        count=count + 1
        line.remove(0)
    for dump_num in range(0, count):
        line.append(0)
    for looper in range(0,len(line)-1):
        if line[looper]==line[looper+1]:
            line[looper]=line[looper]+line[looper+1]
            line.remove(line[looper+1])
            line.append(0)
            looper=looper+1
    return line


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.height=grid_height
        self.width=grid_width
        self.reset()
        cordarray=[]
        self.corddic={1:[],2:[],3:[],4:[]}
        for looper in range(self.width):
            cordarray.append((0,looper))
            self.corddic[1]=cordarray
        cordarray=[]
        for looper in range(self.width):
            cordarray.append((self.height-1,looper))
            self.corddic[2]=cordarray
        cordarray=[]
        for looper in range(self.height):
            cordarray.append((looper,0))
            self.corddic[3]=cordarray
        cordarray=[]
        for looper in range(self.height):
            cordarray.append((looper, self.width-1))
            self.corddic[4]=cordarray
        print self.corddic
        pass
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.grid = [[0 for row in range(self.height)] for col in range(self.width)]
        pass
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        msg="Tangbin's 2048 game col "+self.height+" row "+self.width
        return msg
        pass

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """        
        moveflag=0
        for looper in range(len(self.corddic[direction])):
            arraylen=0
            tempcord=[]
            originlist=[]
            templist=[]
            if direction==UP or direction==DOWN:
                arraylen=self.height    
            else:
                arraylen=self.width
            for looper2 in range(arraylen):
                tempcord.append((self.corddic[direction][looper][0]+OFFSETS[direction][0]*looper2,
                                  self.corddic[direction][looper][1]+OFFSETS[direction][1]*looper2))	
            for looper2 in range(len(tempcord)):
                templist.append(self.grid[tempcord[looper2][1]][tempcord[looper2][0]])    
            originlist=templist[:]
            merge(templist)
            if originlist!=templist:
                for looper2 in range(len(tempcord)):
                    self.grid[tempcord[looper2][1]][tempcord[looper2][0]]=templist[looper2]
                moveflag=1
        if moveflag==1:
            self.new_tile()
                
        pass
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        zerocord=[]
        cordchoice=[]
        if random.randrange(0,10,1)==0:
            num=4
        else:
            num=2
         
        for col in range(self.height):
            for row in range(self.width):
                if self.grid[row][col]==0:
                    zerocord.append([col,row])
        cordchoice=random.choice(zerocord)[:]
        self.grid[cordchoice[1]][cordchoice[0]]=num
        pass
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.grid[row][col]=value
        pass

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """              
        return self.grid[col][row]
 
print	TwentyFortyEight
poc_2048_gui.run_gui(TwentyFortyEight(5,9))
