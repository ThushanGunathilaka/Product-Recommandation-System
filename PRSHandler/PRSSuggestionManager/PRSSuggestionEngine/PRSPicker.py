import random
from collections import defaultdict

from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSWalk import Walk
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSProduct import Product
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSSweeper import Sweeper
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSManager import Manager

class Picker(Walk, Agent):
    '''
    Pickes suggestion for products
    '''
    gridID = -1
    category = None
    suggestionType = None

    def __init__(self, grid, pos,gridID,category,suggestionType):
        super().__init__(grid, pos)
        self.gridID = gridID
        self.category = category
        self.suggestionType = suggestionType

    def step(self, model):
        # If there are products present, pick one
        this_cell = model.grid.get_cell_list_contents([self.pos])
        try:
            SweeperAgent = [obj for obj in this_cell if isinstance(obj, Sweeper)][0]
            if SweeperAgent is not None and SweeperAgent.selectedItem is not None:
                if SweeperAgent.selectedItem['category']  == self.category and SweeperAgent.selectedItem['suggestionType']  == self.suggestionType:
                    Manager.addToSelectedProductsList(int(SweeperAgent.selectedItem['id']),int(SweeperAgent.selectedItem['gridID']))
                    print('On Picker ID : {}, Sweeper ID : {}, Product selected : {}, After : Suggestion List : {}'.format(self.gridID, SweeperAgent.gridID, SweeperAgent.selectedItem['id'], Manager.getSelectedProductsList()))
                    SweeperAgent.selectedItem = None
        except:
            pass