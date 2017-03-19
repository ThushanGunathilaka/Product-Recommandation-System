import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Suggestion Response")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
from PRSHandler.PRSSuggestionManager.PRSSuggestionEngine.PRSManager import Manager

LOGGER.addHandler(handler)
class ResponseModel(object):
    ''' Append Other Required Attributes to the Response'''

    def applyResponseAttributes(self,userID,suggestionList):
        """
        Response Facade
        """
        tempList = []
        for product in suggestionList:
            if str(product['id']) and len(str(product['id']))>0:
                query = 'SELECT DISTINCT p.id as \'ID\',p.UPC as \'UPC\',p.IMAGE as \'PRODUCT_IMAGE\',p.CATEGORYID as \'CAT_ID\','
                query = query + 'c.CATEGORY as \'CATEGORY\',p.ORIGINAL_COST as \'PRODUCT_PRICE\',p.ITEM_DESCRIPTION as \'PRODUCT_DESC\','
                query = query + 's.stallName as \'STALL_NAME\',s.address as \'STALL_ADDRESS\',s.phone as \'STALL_PHONE\','
                query = query + 's.picture as \'STALL_IMAGE\',s.email as \'STALL_EMAIL\' FROM products p LEFT JOIN category c '
                query = query + 'ON p.CATEGORYID = c.CATEGORY_ID LEFT JOIN stall s ON p.VENDORID = s.stallId WHERE '
                query = query + 'p.id = '+ str(product['id']) +';'
                data = list(Manager.makeConnection(query))
                #print(data)
                for row in data:
                    tempDict = {}
                    tempDict.update({'ID': row[0]})
                    tempDict.update({'UPC': row[1]})
                    tempDict.update({'PRODUCT_IMAGE': row[2]})
                    tempDict.update({'CAT_ID': row[3]})
                    tempDict.update({'CATEGORY': row[4]})
                    tempDict.update({'PRODUCT_PRICE': row[5]})
                    tempDict.update({'PRODUCT_DESC': row[6]})
                    tempDict.update({'STALL_NAME': row[7]})
                    tempDict.update({'STALL_ADDRESS': row[8]})
                    tempDict.update({'STALL_PHONE': row[9]})
                    tempDict.update({'STALL_IMAGE': row[10]})
                    tempDict.update({'STALL_EMAIL': row[11]})
                    tempDict.update({'COMMENTS': Manager.getCommentCount(row[1])})
                    tempDict.update({'LIKES': Manager.getLikesCount(row[1])})
                    tempDict.update({'USERLIKES': Manager.getUserLikeStatus(userID,row[1])})
                    tempDict.update({'suggestionType':str(product['suggestionType'])})
                    tempDict.update({'score': str(product['score'])})
                    tempDict.update({'weight': str(product['weight'])})
                    tempDict.update({'strength': str(product['strength'])})
                    tempDict.update({'modelType': str(product['modelType'])})
                    tempDict.update({'suggestionID': str(product['suggestionID'])})
                    tempDict.update({'categoryID': str(product['category'])})
                    #print(tempDict)
                    tempList.extend([tempDict])
        return tempList






        #currentProducts = (self.get_argument('currentProducts', None))
        #print (currentProducts)
        #if userId !='-1' and count !='-1':
        #    record = list(self._db['PRS'].find({'id':int(userId)}))
        #    print ('select',record)
        #    if len(record) > 0:
        #        print ('User ID          : %s' % userId)
        #        print ('Suggestion count : %s' % count)
        #        print ('User Status      : %s' % record[0]['ready'])
        #        print ('User suggestions : %s' % record[0]['suggestion_list'])
        #        if  record[0]['ready']=='TRUE' and len(record[0]['suggestion_list'])>=int(count):
        #            tempList = SuggestionHandlerPRS.getCatalogData(userId,list(record[0]['suggestion_list'][:int(count)]))
        #            self.write(dumps({'status':'TRUE','suggestion_list':tempList}))
        #        else:
        #            SuggestionHandlerPRS.generateSuggestions(self,userId,count)#,currentProducts)
        #    else:
        #        SuggestionHandlerPRS.generateSuggestions(self,userId,count)#,currentProducts)
        #else:
        #    print ('Invalid request')
        #    self.write(dumps({'status':'FALSE'}))


        #    if self.disLikeData:
        #        self.disLikeDataSet = list(set(Manager.getDislikeData(2)))
        #    self.deductableSuggestions = self.disLikeDataSet + list(set(self.currentProducts))
        #    print ('User ID                         : %s' % str(self.userId))
        #    print ('Requested Suggestion count      : %s' % str(self.count))
        #    print ('Current Products in Wishlist    : %s' % self.currentProducts)
        #    if len(self.record) > 0:
        #        self.suggestions = self.record[0]['suggestion_list']
        #        print ('Available suggestions : %s' % self.suggestions)
        #        self.suggestions = list(set(self.suggestions).difference(self.deductableSuggestions))
        #        print ('User Status                     : %s' % self.record[0]['ready'])
        #        print ('Deductible Suggestions: %s' % self.deductableSuggestions)
        #        print ('Suggestions after deduction: %s' % self.suggestions)
        #        if  self.record[0]['ready']=='TRUE' and len(self.suggestions)>=self.count:
        #            print ('NOT Generating suggestions!')
        #            print ('Genarated Suggestions : []')
        #            print ('Finalized Suggestions : %s' % self.suggestions[:self.count])
        #            self.suggestions = list(self.suggestions[:self.count])
        #            if not self.OnlyID:
        #                self.suggestions = Manager.getCatalogData(self.suggestions)
        #            self.write(dumps({'status':'TRUE','suggestion_list':self.suggestions}))
        #        else:
        #            SuggestionHandler.generateSuggestions(self,self.suggestions)
        #    else:
        #        print ('User Status                     : FALSE')
        #        print ('Available suggestions : %s' % [])
        #        SuggestionHandler.generateSuggestions(self,[])
        #    print ('Success: Suggestions Request Completed')
        #    self.write(dumps({'status':'TRUE'}))


















    def generateSuggestions(self,readyToGoSuggestions=[]):
        manageSuggestions = self.deductableSuggestions + readyToGoSuggestions
        manageSuggestions = list(set(manageSuggestions))
        print ('Remove Suggestions: %s' % self.deductableSuggestions)
        print ('Save Suggestions: %s' % readyToGoSuggestions)
        productsToGenerate = self.count - len(readyToGoSuggestions)
        self.manager = Manager(self.userId,self.count,manageSuggestions,self.globle)    #(user id,reuired suggestion count,wishlist,with globle recommandaions)
        if productsToGenerate>0:
            print ('Generating %s suggestions...' % str(productsToGenerate))
            if self.suggestionType == self.modelState[2]:    #Random
                    self.suggestions = self.manager.getSuggestionsListPRS(0,int(productsToGenerate),manageSuggestions)
            elif self.suggestionType == self.modelState[1]:  #RecommendWithOutGloble
                model = Prediction(userId,self.count,deductableSuggestions,True) #(id,count,currentProducts)
                self.suggestions = model.run_model()
            elif self.suggestionType == self.modelState[0]:   #RecommendWithGloble
                model = Prediction(userId,self.count,deductableSuggestions,False) #(id,count,currentProducts)
                self.suggestions = model.run_model()
            else:   #Type Error in self.suggestionType
                print ('Suggestion Model Not Selected.')
                print ('Using Random Model as default...')
                model = Prediction(self.userId,self.count,deductableSuggestions) #(id,count,currentProducts)
                self.suggestions = model.run_model()
        print ('Genarated Suggestions : %s' % self.suggestions)
        self.suggestions = self.suggestions + readyToGoSuggestions
        print ('Finalized Suggestions : %s' % self.suggestions)

        try:
            self._db['PRS'].update({'id':self.userId}, {"$set": {'ready':'TRUE','suggestion_list':self.suggestions}}, upsert=True)
            if  not self.OnlyID:
                self.suggestions = Manager.getCatalogData(list(self.suggestions))
            self.write(dumps({'status':'TRUE','suggestion_list':self.suggestions}))
        except Exception as e:
            print ('Update Failed')
            self.write(dumps({'status':'FALSE'}))