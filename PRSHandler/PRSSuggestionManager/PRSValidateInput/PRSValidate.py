import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Input Validate")
from PRSBoot.PRSConfig import Conf
#LOGGER.propagate = Conf().getVerbose()
LOGGER.propagate = False

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class Validate(object):
    '''
    Validate Inputs
    '''
    def checkUserInput(self,list):
        tempList = []
        for item in list:
            item['id'] = self.setID(item['id'])
            item['strength'] = self.setValue(item['strength'])
            if self.checkID(item['id']) and self.checkValue(item['strength']):
                tempList.extend([item])
                LOGGER.info ('User Input Item Accepted : {}'.format(item))
            else:
                LOGGER.info ('User Input Item Rejected : {}'.format(item))
                pass
        if len(tempList) > 0:
            LOGGER.info ('User Input Source Validated, Size : [{}]'.format(len(tempList)))
            return tempList
        else:
            LOGGER.info ('User Input Source Rejected, Size : [{}]'.format(len(tempList)))
            return None

    def checkSuggestionInput(self,list):
        tempList = []
        for item in list:
            item['id'] = self.setID(item['id'])
            item['score'] = self.setValue(item['score'])
            item['weight'] = self.setValue(item['weight'])
            if self.checkID(item['id']) and self.checkValue(item['score'])  and self.checkValue(item['weight']):
                tempList.extend([item])
                LOGGER.info ('Suggestion Input Item Accepted : {}'.format(item))
            else:
                LOGGER.info ('Suggestion Input Item Rejected : {}'.format(item))
                pass
        if len(tempList) > 0:
            LOGGER.info ('Suggestion Input Source Validated, Size : [{}]'.format(len(tempList)))
            return tempList
        else:
            LOGGER.info ('Suggestion Input Source Rejected, Size : [{}]'.format(len(tempList)))
            return None

    def setValue(self,value):
        result = 0
        try:
            value = int(value)
            if value <0:
                result = 0
            elif value > 100:
                result = 100
            else:
                result = value
        except:
            result = 0
        return result

    def setID(self,value):
        result = None
        try:
            value = int(value)
            if value >= 0:
                result = value
            else:
                result = None
        except:
            result = None
        return result

    def checkValue(self,inputValue):
        value = inputValue
        result = False
        try:
            value = int(value)
            if value <0:
                result = False
            elif value > 100:
                result = False
            else:
                result = True
        except:
            result = False
        LOGGER.info(' checkID : input = {} ==> output = {}'.format(inputValue,result))
        return result

    def checkID(self,inputValue):
        value = inputValue
        result = False
        try:
            value = int(value)
            if value >= 0:
                result = True
            else:
                result = False
        except:
            result = False
        LOGGER.info(' checkID : input = {} ==> output = {}'.format(inputValue,result))
        return result

    def checkValidInt(self,inputValue):
        value = inputValue
        result = False
        try:
            value = int(value)
            if value >= 0:
                result = True
            else:
                result = False
        except:
            result = False
        LOGGER.info(' checkValidInt : input = {} ==> output = {}'.format(inputValue,result))
        return result

    def convertToInt(self,inputValue):
        value = inputValue
        result = None
        try:
            value = int(value)
            if value >= 0:
                result = value
            else:
                result = None
        except:
            result = None
        LOGGER.info(' convertToInt : input = {} ==> output = {}'.format(inputValue,result))
        return result
