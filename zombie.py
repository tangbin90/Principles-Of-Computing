"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"

class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._human_list=[]
        self._zombie_list=[]
        poc_grid.Grid.clear(self)
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for item in self._zombie_list:
            yield item
        return

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
   
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for item in self._human_list:
            yield item
        return
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited_field=poc_grid.Grid(self.get_grid_height(),self.get_grid_width())
        temp_num=self.get_grid_height()*self.get_grid_width()
        distance_field=[[temp_num for dummy_col in range(self._grid_width)]
                       for dummy_row in range(self._grid_height)]
        entity_queue=poc_queue.Queue()
        if entity_type == HUMAN:
            for item in self._human_list:
                entity_queue.enqueue(item)
                distance_field[item[0]][item[1]]=0
                visited_field.set_full(item[0],item[1])
        elif entity_type == ZOMBIE:
            for item in self._zombie_list:
                entity_queue.enqueue(item)
                distance_field[item[0]][item[1]]=0
                visited_field.set_full(item[0],item[1])
        while len(entity_queue)!=0:
            cell=entity_queue.dequeue()
            neighbors = self.four_neighbors(cell[0],cell[1])
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    if visited_field.is_empty(neighbor[0],neighbor[1]):
                        visited_field.set_full(neighbor[0],neighbor[1])
                        entity_queue.enqueue(neighbor)
                        distance_field[neighbor[0]][neighbor[1]]=\
                        distance_field[cell[0]][cell[1]]+1
        
        return distance_field

    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
     
        for looper in range(len(self._human_list)):    
            temp_max=[]
            neighbors = self.eight_neighbors(self._human_list[looper][0],self._human_list[looper][1])
            temp_max.append([zombie_distance[self._human_list[looper][0]][self._human_list[looper][1]],self._human_list[looper]])
            for neighbor in neighbors:
                if zombie_distance[neighbor[0]][neighbor[1]]!=self.get_grid_height()*self.get_grid_width():
                    if temp_max[0][0]<zombie_distance[neighbor[0]][neighbor[1]]:
                        temp_max=[]
                        temp_max.append([zombie_distance[neighbor[0]][neighbor[1]],neighbor])
                    elif temp_max[0][0]==zombie_distance[neighbor[0]][neighbor[1]]:
                        temp_max.append([zombie_distance[neighbor[0]][neighbor[1]],neighbor])
            self._human_list[looper]=temp_max[random.randrange(0,len(temp_max))][1]
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        
        for looper in range(len(self._zombie_list)):
            temp_min=[]
            neighbors = self.four_neighbors(self._zombie_list[looper][0],self._zombie_list[looper][1])
            temp_min.append([human_distance[self._zombie_list[looper][0]][self._zombie_list[looper][1]],self._zombie_list[looper]])
            for neighbor in neighbors:
                if human_distance[neighbor[0]][neighbor[1]]!=self.get_grid_height()*self.get_grid_width():
                    if temp_min[0][0]>human_distance[neighbor[0]][neighbor[1]]:
                        temp_min=[]
                        temp_min.append([human_distance[neighbor[0]][neighbor[1]],neighbor])
                    elif temp_min[0][0]==human_distance[neighbor[0]][neighbor[1]]:
                        temp_min.append([human_distance[neighbor[0]][neighbor[1]],neighbor])
            self._zombie_list[looper]=temp_min[random.randrange(0,len(temp_min))][1]



# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))
