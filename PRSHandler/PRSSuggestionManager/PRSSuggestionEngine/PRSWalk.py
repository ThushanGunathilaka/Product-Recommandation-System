'''
Generalized behavior for random pickup, one grid cell at a time.
'''

import random

class Walk(object):
    '''
    Class implementing random walker methods in a generalized manner.
    Not indended to be used on its own, but to inherit its methods to multiple
    other agents.
    '''
    grid = None
    x = None
    y = None

    def __init__(self, grid, pos):
        '''
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        '''
        self.grid = grid
        self.pos = pos

    def random_move(self):
        '''
        Step one cell in any allowable direction.
        '''
        # Pick the next cell from the adjacent cells.
        next_moves = self.grid.get_neighborhood(self.pos, True, True)
        next_move = random.choice(next_moves)
        #print('Current Position : {}, Next Position : {}'.format(self.pos,next_move))
        # Now move:
        self.grid._remove_agent(self.pos, self)
        self.grid._place_agent(next_move, self)
        self.pos = next_move

    def moveUp(self):
        '''
        Step one cell in Downwards.
        '''
        x,y = self.pos
        if y > 0 and y<=100:
            y = y -1
        try:
            self.grid.move_agent(self,(x,y))
            self.pos = (x,y)
        except:
            pass

    def moveLeft(self):
        '''
        Step one cell in Leftwards.
        '''
        x,y = self.pos
        if x > 0 and x<=100:
            x = x -1
        try:
            self.grid.move_agent(self,(x,y))
            self.pos = (x,y)
        except:
            pass

    def moveTowards(self,point):
        '''
        move towards a Picker
        '''
        Tx,Ty = point
        x,y = self.pos
        if x > Tx and x > 0 and x <= 100:
            x = x - 1
        elif x < Tx and x >= 0 and x < 100:
            x = x + 1
        if y > Ty and y > 0 and y <= 100:
            y = y - 1
        elif x < Tx and y >= 0 and y < 100:
            y = y + 1
        try:
            self.grid.move_agent(self,(x,y))
            self.pos = (x,y)
        except:
            pass
