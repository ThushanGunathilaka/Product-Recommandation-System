import random
from collections import defaultdict

from mesa import Model, Agent
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSActivation import Activation
from mesa.space import MultiGrid
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSPicker import Picker
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSSweeper import Sweeper
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSProduct import Product
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSManager import Manager
from mesa.datacollection import DataCollector
import datetime

class Prediction(Model):
    '''
    product suggestion Model
    '''
    height = 101
    width = 101

    requiredSuggestionsCount = 0
    userID = 0
    count = 0

    verbose = True # Print-monitoring
    allowProduct = True
    dataset = None
    globle = True

    def __init__(self,userID,requiredSuggestionsCount,productData,meanPoints,globle = True):
        '''
        Create a new simulation with the given parameters.
        '''
        self.globle = globle
        self.requiredSuggestionsCount = requiredSuggestionsCount
        self.dataset = productData
        self.allowProduct = True

        self.schedule = Activation(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector({
            "Picker": lambda m: m.schedule.get_agent_count_by_type(Picker),
            "Sweeper": lambda m: m.schedule.get_agent_count_by_type(Sweeper)
            #"Product": lambda m: m.schedule.get_agent_count_by_type(Product)
        })
        self.count = 0
        # Create Sweeper:
        for index in range(101):
            sweeper = Sweeper(self.grid, (index, 100), self.count,True,False)   #(grid, pos, gridID,MoveDownValue,moveToPicker)
            self.grid.place_agent(sweeper, (index, 100))
            self.schedule.add(sweeper)
            self.count = self.count + 1

        for index in range(101):
            sweeper = Sweeper(self.grid, (100, index), self.count,False,False)  #(grid, pos, gridID,MoveDownValue,moveToPicker)
            self.grid.place_agent(sweeper, (100, index))
            self.schedule.add(sweeper)
            self.count = self.count + 1

        #count = 0
        # Create Pickers
        for meanPoint in meanPoints:
            x = meanPoint['weight']
            y = meanPoint['score']
            picker = Picker(self.grid, (x, y),meanPoint['meanPoint'],meanPoint['category'],meanPoint['suggestionType'])
            self.grid.place_agent(picker, (x, y))
            self.schedule.add(picker)
          #  count = count + 1
        # Create Prodcuts
        for agent, x, y in self.grid.coord_iter():
            items = []
            scoreIndex = [i for i, row in enumerate(self.dataset) if row['score'] == y]
            if len(scoreIndex)>0:
                for index in scoreIndex:
                    if index <= 100 and index >= 0:
                        row = self.dataset[index]
                        if row['weight'] >= 0 and row['weight'] <= 100 and row['weight'] == x :
                            item = {}
                            item.update({'id': row['id']})
                            item.update({'score': row['score']})
                            item.update({'weight': row['weight']})
                            item.update({'category': row['category']})
                            item.update({'strength': row['strength']})
                            item.update({'suggestionType': row['suggestionType']})
                            item.update({'gridID': row['gridID']})
                            assigenPicker = None
                            for picker in meanPoints:
                                if picker["category"] == row['category'] and picker["suggestionType"] == row['suggestionType']:
                                    #print('category = {}, suggestion type = {}, fount picker = {}'.format(row['category'],row['suggestionType'],item))
                                    assigenPicker = picker
                            item.update({'assignedPicker': assigenPicker})
                            items.extend([item])
            if len(items)>0:
                eligible = True
                #print ('X-axis : {}, Y-axis : {}, eligible = {}, Product Count in Cell = {}, Products = {}'.format(x,y,eligible,len(items),items))
            else:
                eligible = False
            patch = Product(items, eligible)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)
        self.running = True

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        print([self.schedule.time, self.schedule.get_agent_count_by_type(Picker),
                self.schedule.get_agent_count_by_type(Sweeper)])


    def run_model(self, step_count=200):
        if self.verbose:
            start_time = datetime.datetime.now()
            print('Initial Selected product : {}'.format(Manager.getSelectedProductIDList()))
            print('Required product count   : {}'.format(self.requiredSuggestionsCount))

        while int(Manager.getSelectedProductsCount())<int(self.requiredSuggestionsCount):
            if self.verbose:
                print('Time Step [{}] : Start, Selected Products : {}'.format(self.schedule.time,Manager.getSelectedProductIDList()))
            self.step()
            if self.verbose:
                print('Time Step : End')
        if self.verbose:
            end_time = datetime.datetime.now()
            print('Time : ',end_time-start_time)
            print('Final Selected product (s) : {}'.format(Manager.getSelectedProductIDList()))
            print('Final Selected Grid ID (s) {}'.format(Manager.getSelectedGridIDList()))
            print('Required product count : {}'.format(self.requiredSuggestionsCount))
        return Manager.getSelectedGridIDList()
