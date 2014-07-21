"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(60)

import poc_clicker_provided as provided

# Constants
SIM_TIME =10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self.total_cookie=0.0
        self.now_cookie=0.0
        self.time=0.0
        self.cps=1.0
        self.history=[(0.0, None, 0.0, 0.0)]
        
        
    def __str__(self):
        """
        Return human readable state
        """
        return "\nTime:"+str(self.time)+\
               "\nCurrent Cookies:"+str(self.now_cookie)+\
               "\nTotal Cookies:"+str(self.total_cookie)+\
               "\nCPS:"+str(self.cps) 
                             
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self.now_cookie
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self.cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self.time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self.history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        temp_time=0.0
        if cookies>self.now_cookie:
            temp_time=(cookies-self.now_cookie)/self.cps
            temp_inttime=int(temp_time)
            if temp_time>temp_inttime:
                temp_time=temp_inttime+1.0
        return temp_time
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time>0:
            self.time+=time
            self.total_cookie+=time*self.cps
            self.now_cookie+=time*self.cps
        
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self.now_cookie>=cost:
            self.history.append((self.time,item_name,cost,self.total_cookie))
            self.now_cookie-=cost
            self.cps+=additional_cps            
        
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    buildclone=build_info.clone()
    gamestate=ClickerState()
    while gamestate.time<=duration:
        item=strategy(gamestate.now_cookie,gamestate.cps,duration-gamestate.time,buildclone)
        if item==None:
            break
        wtime=gamestate.time_until(buildclone.get_cost(item))
        if (wtime+gamestate.time)>duration:
            break
        gamestate.wait(wtime)
        gamestate.buy_item(item,buildclone.get_cost(item),buildclone.get_cps(item))   
        buildclone.update_item(item)
        #print gamestate
    gamestate.wait(duration-gamestate.time)
    return gamestate


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    cheap strategy
    """
    cheaplist=[]
    for itemc in build_info.build_items():
        if time_left*cps+cookies>=build_info.get_cost(itemc):        	
            if len(cheaplist)==0:
                cheaplist.append([itemc,build_info.get_cost(itemc)])
            elif cheaplist[0][1]==build_info.get_cost(itemc):
                cheaplist.append([itemc,build_info.get_cost(itemc)])
            elif cheaplist[0][1]>build_info.get_cost(itemc):
                cheaplist=[[itemc,build_info.get_cost(itemc)]]       
    if len(cheaplist)==0:
        return None
    else:	
        return cheaplist[-1][0]

def strategy_expensive(cookies, cps, time_left, build_info):    
    """
    expensive strategy
    """
    explist=[]
    for itemc in build_info.build_items():
        if time_left*cps+cookies>=build_info.get_cost(itemc):
            if len(explist)==0:
                explist.append([itemc,build_info.get_cost(itemc)])
            elif explist[0][1]==build_info.get_cost(itemc):
                explist.append([itemc,build_info.get_cost(itemc)])
            elif explist[0][1]<build_info.get_cost(itemc):
                explist=[[itemc,build_info.get_cost(itemc)]]   
    if len(explist)==0:
        return None
    else:	
        return explist[-1][0]                    

def strategy_best(cookies, cps, time_left, build_info):
    """
    best strategy
    """
    best=[]
    temp=[]
    for item in build_info.build_items():
        time_left=time_left-build_info.get_cost(item)/cps
        if time_left>0:
            best.append([item,build_info.get_cps(item)*time_left/build_info.get_cost(item)])
      
    if len(best)==0:
        return None
    elif len(best)==1:
        return best[0][0]
    else:
        temp=best[0]
        for looper in range(1,len(best)):
            if temp[1]<=best[looper][1]:
                temp=best[looper]
    return temp[0]

        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history = [(math.log(item[0]), math.log(item[3])) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
