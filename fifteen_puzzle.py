"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""
#http://www.codeskulptor.org/#user37_iaspfZKamv_58.py
import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row,target_col)!=0:
            return False
        height=self.get_height()
        width=self.get_width()
        for row in range(target_row+1,height):
            for col in range(width):
                if self.get_number(row,col)!=row*width+col:                   
                    return False
        for right_col in range(target_col+1,width):
            if self.get_number(target_row,right_col)!=target_row*width+right_col:
                return False
        return True
    def find_num(self,num):
        """
        find the num,return row,col
        """
        width=self.get_width()
        height=self.get_height()
        for row in range(height):
            for col in range(width):
                if num==self.get_number(row,col):
                    return row,col
    def position_with_num(self,target_row,target_col,target_num):
        """
        find the target by num
        """
        move=""
        num_temp=self.find_num(target_num)
        num_pos=[num_temp[0],num_temp[1]]
        if num_pos[1]!=target_col:
            up_step=target_row-num_pos[0]
            for dummy_looper in range(up_step):
                move+="u"
            if num_pos[1]>target_col:
                r_step=num_pos[1]-target_col
                for dummy_looper in range(r_step):
                    move+="r"
                num_pos[1]-=1
                while num_pos[1]!=target_col:
                    if num_pos[0]==0:
                        move+="dllur"
                    else:
                        move+="ulldr"
                    num_pos[1]-=1
                if num_pos[0]==0:
                    move+="dllu"
                else:
                    move+="ulld"
            if num_pos[1]<target_col:
                l_step=target_col-num_pos[1]
                for dummy_looper in range(l_step):
                    move+="l"
                num_pos[1]+=1
                while num_pos[1]!=target_col:                  
                    if num_pos[0]==0:
                        move+="drrul"
                    else:
                        move+="urrdl"
                    num_pos[1]+=1
        elif num_pos[1]==target_col:
            move+="l"
            up_step=target_row-num_pos[0]
            for dummy_looper in range(up_step):
                move+="u"  
        #move to the  target
        while num_pos[0]!= target_row:
            move+="druld"
            num_pos[0]+=1
        print move
        return move
    def position_tile(self,target_row,target_col):
        """
        move the tiles to the target
        """
        move=""
        num_temp=self.current_position(target_row,target_col)
        num_pos=[num_temp[0],num_temp[1]]
        if num_pos[1]!=target_col:
            up_step=target_row-num_pos[0]
            for dummy_looper in range(up_step):
                move+="u"
            if num_pos[1]>target_col:
                r_step=num_pos[1]-target_col
                for dummy_looper in range(r_step):
                    move+="r"
                num_pos[1]-=1
                while num_pos[1]!=target_col:
                    if num_pos[0]==0:
                        move+="dllur"
                    else:
                        move+="ulldr"
                    num_pos[0]+=1
                if num_pos[0]==0:#adjusting position attantion
                    move+="dllu"
                else:
                    move+="ulld"
            if num_pos[1]<target_col:
                l_step=target_col-num_pos[1]
                for dummy_looper in range(l_step):
                    move+="l"
                num_pos[1]+=1
                while num_pos[1]!=target_col:                  
                    if num_pos[0]==0:
                        move+="drrul"
                    else:
                        move+="urrdl"
                    num_pos[1]+=1
        elif num_pos[1]==target_col:
            move+="l"
            up_step=target_row-num_pos[0]
            for dummy_looper in range(up_step):
                move+="u"  
        #move to the  target
        while num_pos[0]!= target_row:
            move+="druld"
            num_pos[0]+=1
        return move
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert target_row>1 and target_col>0,"function input invalid!"
        assert self.lower_row_invariant(target_row, target_col),"wrong position!"
        move=""
        num_temp=self.current_position(target_row,target_col)
        num_pos=[num_temp[0],num_temp[1]]
        assert target_row>=num_pos[0],"Wrong num position!"
        #when number is in the same row
        if num_pos[0]==target_row:
            assert target_col>num_pos[1],"Wrong num col num!"
            l_step=target_col-num_pos[1]
            for dummy_looper in range(l_step):
                move+="l"
            num_pos[1]+=1
            while num_pos[1]!=target_col:
                move+="urrdl"
                num_pos[1]+=1
            self.update_puzzle(move)
            return move
        move+=self.position_tile(target_row,target_col)
        self.update_puzzle(move)
        assert self.lower_row_invariant(target_row,target_col-1),"Wrong move!"
        return move

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert target_row>1,"wrong input row!"
        assert self.lower_row_invariant(target_row, 0),"wrong template!"
        move=""
        num_temp=self.current_position(target_row,0)
        #when target num is just up the zero
        width=self.get_width()
        if num_temp[0]+1==target_row and num_temp[1]==0:
            move+="u"            
            for dummy_looper in range(width-1):
                move+="r"
            self.update_puzzle(move)
            return move
        move+="ur"#move to i-1,1
        if num_temp==(target_row-1,1):
            num_temp=(num_temp[0],num_temp[1]+1)
        temp_board=self.clone()
        temp_board.update_puzzle(move)
        zero_row=target_row-1
        zero_col=1
        print temp_board
        move_temp=temp_board.position_with_num(zero_row,zero_col,target_row*width)
        move+=move_temp
        temp_board.update_puzzle(move_temp)
        print temp_board
        print "here?"
        move+="ruldrdlurdluurddlur"
        #move to the right most side
        for dummy_looper in range(width-2):
            move+="r"
        self.update_puzzle(move)
        assert self.lower_row_invariant(target_row-1,width-1),"wrong template"
        return move

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        #assert target_col>1,"col out of permission value"        
        if target_col==0:
            return self.lower_row_invariant(0,0)
        if self.get_number(0,target_col)!=0:
            return False
        temp=self.get_number(1,target_col-1)
        self.set_number(1,target_col-1,0)
        if self.lower_row_invariant(1,target_col-1)==False:
            return False 
        self.set_number(1,target_col-1,temp)
        width=self.get_width()
        for col in range(target_col+1,width):
            if col!=self.get_number(0,col):
                return False        
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        #assert target_col>1,"col out of permission value"       
        if self.lower_row_invariant(1,target_col)==False:
            return False 
        width=self.get_width()
        for col in range(target_col+1,width):
            if col!=self.get_number(0,col):
                return False        
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        move=""
        num_temp=self.current_position(0,target_col)
        if num_temp[0]==0 and num_temp[1]==target_col-1:
            move+="l"
            move+="d"
            self.update_puzzle(move)
            return move
        move+="ld"
        board_temp=self.clone()
        board_temp.update_puzzle(move)#key!!!!
        num_temp=board_temp.current_position(0,target_col)
        num_pos=[num_temp[0],num_temp[1]]
        zero_col=target_col-1
        if num_pos[0]==0:
            for dummy_looper in range(num_temp[1],zero_col):
                move+="l"
            move+="u"
            num_pos[0]+=1
            while num_pos[1]!=zero_col:
                move+="rdlur"
                num_pos[1]+=1
            move+="ld"
        elif num_pos[0]==1:
            for dummy_looper in range(num_temp[1],zero_col):
                move+="l"
            num_pos[1]+=1
            
            while num_pos[1]!=zero_col:
                move+="urrdl"
                num_pos[1]+=1
        else:
            assert False,"wrong target!!"
        move+="urdlurrdluldrruld"
        self.update_puzzle(move)
        return move
        
        
        
        
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        move=""
        num_temp=self.current_position(1,target_col)
        num_pos=[num_temp[0],num_temp[1]]
        if num_pos[0]==1:
            assert target_col>num_pos[1],"Wrong num col num!"
            l_step=target_col-num_pos[1]
            for dummy_looper in range(l_step):
                move+="l"
            num_pos[1]+=1
            while num_pos[1]!=target_col:
                move+="urrdl"
                num_pos[1]+=1
            move+="ur"
            self.update_puzzle(move)
            return move
        move+=self.position_tile(1,target_col)
        move+="ur"
        self.update_puzzle(move)
        return move

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        dic_mov={0:"l",1:"u",2:"r",3:"d"}       
        move=""
        temp_num=0
        while self.lower_row_invariant(0,0)!=True:
            move_temp=dic_mov[temp_num]
            temp_num+=1
            temp_num=temp_num%4
            self.update_puzzle(move_temp)
            move+=move_temp
        
        return move

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        move=""
        width=self.get_width()
        height=self.get_height()
        zero_pos=self.find_num(0)
        for dummy_looper in range(zero_pos[1],width-1):
            move+="r"
        for dummy_looper in range(zero_pos[0],height-1):
            move+="d"
 
        self.update_puzzle(move) 
        for row in range(height-1,1,-1):
            for col in range(width-1,0,-1):
                move+=self.solve_interior_tile(row,col)
            move+=self.solve_col0_tile(row)   
        for col in range(width-1,1,-1):
            move+=self.solve_row1_tile(col)
            move+=self.solve_row0_tile(col)    	
        move+=self.solve_2x2()
        return move

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(5, 5))
#obj=Puzzle(4, 5, [[12, 11, 10, 9, 8], [7, 6, 5, 4, 3], [2, 1, 0, 13, 14], [15, 16, 17, 18, 19]])
#print obj.lower_row_invariant(2,2)
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print obj.solve_interior_tile(2, 2) 
#obj = Puzzle(3, 3, [[3, 2, 1], [7, 5, 4], [6, 8, 0]])
#print obj.solve_interior_tile(2, 2)
#print obj
#obj = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0, 7, 8]])
#obj.solve_col0_tile(2)
#print obj
#obj = Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
#print obj.solve_col0_tile(3)
#print obj
#obj=Puzzle(4, 5, [[7, 6, 5, 3, 2], [4, 1, 9, 8, 0], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#obj.solve_row1_tile(4)
#print obj
#obj = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]])
#print obj
#obj.solve_row0_tile(2)
#print obj
#obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#print obj
#obj.solve_2x2()
#print obj
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#obj.solve_puzzle() 
#print obj
#obj=Puzzle(5, 5, [[24, 10, 6, 7, 8], [5, 11, 1, 2, 3], [15, 16, 12, 9, 4], [20, 22, 17, 14, 13],[21,23,19,18,0]])
#obj.solve_puzzle()
#print obj
#obj = Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
#obj.solve_col0_tile(3)
#print obj