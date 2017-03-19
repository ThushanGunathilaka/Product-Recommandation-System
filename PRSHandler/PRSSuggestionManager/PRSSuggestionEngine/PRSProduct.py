import random
from collections import defaultdict

from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSManager import Manager

class Product(Agent):
    '''
    A square in the grid represents a product
    '''
    eligible = False
    productList = []

    def __init__(self, items,eligible):
        '''
        Initialize a Product Post in the Grid

        Args:
            eligible   : Product post eligible to pick as a suggestion
            items: Product Post details
                |-- id              :   product ID
                |-- score           :   Customer Attitiude towards the product
                |-- weight          :   Customer repeatability towards the product
                |-- category        :   category ID
                |-- strength        :   relationship strength between the user and a friend
        '''
        self.productList = items
        self.eligible = eligible

    def step(self, model):
        suggestionIDList = Manager.getSelectedProductIDList()
        if len(self.productList)>0 and len(suggestionIDList)>0:
            productIDList = []
            for product in self.productList:
                productIDList.append(product['id'])
            if len(productIDList)>0:
                alreadyPickedProductIDList = list(set(productIDList).intersection(set(suggestionIDList)))
                if (len(alreadyPickedProductIDList)>0):
                    print('Already Picked Products : {}, Grid List : {}, Suggestion List : {}'.format(alreadyPickedProductIDList,productIDList,suggestionIDList) )
                    for pickedProduct in alreadyPickedProductIDList:
                        for product in self.productList:
                            if product['id'] == pickedProduct:
                                #print('Before : {}, Eligible : {}'.format(self.productList,self.eligible))
                                self.productList.remove(product)
                                if len(self.productList)>0:
                                    self.eligible = True
                                else:
                                    self.eligible = False
                                #print('After : {}, Eligible : {}'.format(self.productList,self.eligible))