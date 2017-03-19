import random
from collections import defaultdict

from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSWalk import Walk
#from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSManager import Manager

class Activation(RandomActivation):
    '''
    A scheduler which activates each type of agent once per step, in random 
    order, with the order reshuffled every step.

    Assumes that all agents have a step(model) method.
    '''
    agents_list = defaultdict(list)

    def __init__(self, model):
        super().__init__(model)
        self.agents_list = defaultdict(list)

    def add(self, agent):
        '''
        Add an Agent object to the schedule

        Args:
            agent: An Agent to be added to the schedule.
        '''

        self.agents.append(agent)
        agent_class = type(agent)
        self.agents_list[agent_class].append(agent)


    def remove(self, agent):
        '''
        Remove all instances of a given agent from the schedule.
        '''

        while agent in self.agents:
            self.agents.remove(agent)

        agent_class = type(agent)
        while agent in self.agents_list[agent_class]:
            self.agents_list[agent_class].remove(agent)


    def step(self):
        '''
        Executes the step of each agent type, one at a time, in random order.
       the next one.
        '''
        for agent_class in  self.agents_list:
            self. step_by_agent_type(agent_class)
        self.steps += 1
        self.time += 1

    def step_by_agent_type(self, type):
        '''
        Shuffle order and run all agents of a given type.(Activation order)

        Args:
            type: Class object of the breed to run.
        '''
        agents = self.agents_list[type]
        random.shuffle(agents)
        for agent in agents:
            agent.step(self.model)

    def get_agent_count_by_type(self, type):
        '''
        Returns the current number of agents of certain type in the queue.
        '''
        return len(self.agents_list[type])