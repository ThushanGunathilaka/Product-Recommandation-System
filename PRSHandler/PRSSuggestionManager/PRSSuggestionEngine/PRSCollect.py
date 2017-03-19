import numpy as np

class Collect(object):
    """Collect Product Suggestion Data"""
    data = None
    meanPoints = None
    categories = None
    socialData = None
    globalData = None
    personalData = None
    sourceSet = None
    def __init__(self,collectedData):
        '''
        Initializes the instance with all suggestion data
        '''
        self.data = []
        self.meanPoints = []
        self.categories = collectedData['categories']
        self.socialData = collectedData['SOCIAL']
        self.globalData = collectedData['GLOBAL']
        self.personalData = collectedData['PERSONAL']
        self.sourceSet = list(dict(collectedData).keys())
        self.sourceSet.remove('categories')

    def getMeanPoints(self):
        result = []
        result.extend(self.generateMeanPoints(None,self.categories,'None'))
        result.extend(self.generateMeanPoints(self.socialData,self.categories,'SOCIAL'))
        result.extend(self.generateMeanPoints(self.globalData,self.categories,'GLOBAL'))
        result.extend(self.generateMeanPoints(self.personalData,self.categories,'PERSONAL'))
        data  = []
        data.extend(self.socialData)
        data.extend(self.globalData)
        data.extend(self.personalData)
        result.extend(self.generateMeanPoints(data,self.categories,'ALL'))
        count = 0
        for item in result:
            item.update({'meanPoint': count })
            count = count + 1
        return result

    def generateMeanPoints(self,data,categories,source):
        result = []
        categoryData = {}
        meanPoints = []
        if data is not None and len(data)>0:
            for item in data:
                if item['category'] in categories:
                    if item['category'] in list(categoryData.keys()):
                        categoryValueSet = categoryData[item['category']]
                        if categoryValueSet is not None:
                            categorySet = []
                            categorySet.append(list([item['score'],item['weight']]))
                            for element in categoryValueSet:
                                categorySet.append(element)
                            categoryData.update({item['category']: categorySet })
                        else:
                            categoryData.update({item['category']: [[item['score'],item['weight']]]})
                    else:
                        categoryData.update({item['category']: [[item['score'],item['weight']]]})


            for key, value in dict(categoryData).items():
                score =[]
                weight = []
                for item in list(value):
                    score.append(item[0])
                    weight.append(item[1])
                meanProduct = {}
                meanProduct.update({'score': int(np.mean(score)) })
                meanProduct.update({'weight': int(np.mean(weight)) })
                meanProduct.update({'category': key })
                meanProduct.update({'suggestionType': source })
                meanPoints.append(meanProduct)
        return meanPoints

    def getFixedInputs(self):
        for  item in list(self.socialData):
            item.update({'suggestionType': 'SOCIAL'})
        for  item in list(self.globalData):
            item.update({'suggestionType': 'GLOBAL'})
            item.update({'strength': 0})
        for  item in list(self.personalData):
            item.update({'suggestionType': 'PERSONAL'})
            item.update({'strength': 0})
        data  = []
        data.extend(self.socialData)
        data.extend(self.globalData)
        data.extend(self.personalData)
        count = 0
        for item in data:
            item.update({'gridID': count })
            count = count + 1
        return data

                

