import random
from collections import defaultdict

from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSWalk import Walk
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSProduct import Product
#from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSPrediction import Prediction

class Sweeper(Walk, Agent):
    '''
    Pickes eligible suggestion for products
    The init is the same as the Walk.
    '''
    eligibleItems = []
    selectedItem = None
    moveable = True
    gridID = -1
    MoveDownValue = True
    moveToPicker = False

    def __init__(self, grid, pos, gridID,MoveDownValue,moveToPicker):
        super().__init__(grid, pos)
        #self.selectedItem = None
        self.moveable = True
        self.gridID = gridID
        self.MoveDownValue = MoveDownValue
        self.moveToPicker = moveToPicker

    def step(self, model):
        '''
        If there are products present, pick an eligible product
        '''
        if self.moveable and not self.moveToPicker:
            if self.MoveDownValue:
                self.moveUp()
            else:
                self.moveLeft()

        if self.moveToPicker:
            picker = self.selectedItem['assignedPicker']
            if picker is not None:
                point = picker['weight'],picker['score']
                self.moveTowards(point)
            else:
                print('Error')

        if self.selectedItem == None:
            this_cell = model.grid.get_cell_list_contents([self.pos])
            productAgent = [obj for obj in this_cell if isinstance(obj, Product)][0]
            if productAgent.eligible and len(productAgent.productList)>0:
                self.selectedItem = productAgent.productList[0]
                foundItem = productAgent.productList[0]
                #print(foundItem)
                print('Sweeper ID : {}, Selected Item : {}'.format(self.gridID, self.selectedItem['id']))
                nextID = -1
                sweeper = Sweeper(self.grid, (foundItem['weight'], foundItem['score']), nextID,False,True)
                sweeper.selectedItem = productAgent.productList[0]
                model.grid.place_agent(sweeper, (foundItem['weight'], foundItem['score']))
                model.schedule.add(sweeper)

