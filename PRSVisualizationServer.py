from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSPicker import Picker
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSSweeper import Sweeper
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSProduct import Product
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSPrediction import Prediction
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSCollect import Collect
from PRSHandler.PRSSuggestionManager.PRSSuggestionManager import Manager
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule

import logging
import random

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Simulation")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class VisualizationServer(object):
    gridID = 0
    def map_agents(agent):
        if agent is None:
            return

        portrayal = {"Shape": "circle",
                        "Filled": "true"}

        if type(agent) is Sweeper:
            portrayal["Color"] = "#666666"
            portrayal["r"] = 0.8
            portrayal["Layer"] = 1

        elif type(agent) is Picker:
            portrayal["Color"] = "#AA0000"
            portrayal["r"] = 0.5
            portrayal["Layer"] = 2

        elif type(agent) is Product:
            if agent.eligible:
                portrayal["Color"] = "#00AA00"
            else:
                portrayal["Color"] = "#D6F5D6"
            portrayal["Shape"] = "rect"
            portrayal["Layer"] = 0
            portrayal["w"] = 1
            portrayal["h"] = 1
        return portrayal

    def start_server(self):
        source = Manager().processInputSources()
        collect = Collect(source)
        meanPoints = collect.getMeanPoints()
        gridProducts = collect.getFixedInputs()
        canvas_element = CanvasGrid(VisualizationServer.map_agents, 100, 100, 500, 500)
        chart_element = ChartModule([{"Label": "Picker", "Color": "#AA0000"},{"Label": "Product", "Color": "#666666"}])
        server = ModularServer(Prediction, [canvas_element],"Product Suggestion Simulation",0,10,gridProducts,meanPoints,True)   #(id,count,wishlist,globle) #, chart_element
        server.launch()
if __name__ == "__main__":
    VisualizationServer().start_server()

#chart_element