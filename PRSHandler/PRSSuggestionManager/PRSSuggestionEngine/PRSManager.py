import pymysql
import random

class Manager(object):
    '''Manage data from other modules'''
    count = None
    skipList = []
    globle = True

    personalPreferenceList = None
    socialPreferenceList = None
    friendList = None
    overallSuggestions = None
    productList = []
    productCount = None
    friendPersonalStrengthFavour = 1    #[0-1]
    friendSocialStrengthFavour = 1      #[0-1]
    userPersonalStrength = 100  #[0-100]
    userSocialStrength = 100    #[0-100]
    categoryList = []
    categoryListCount = None
    #eligibleProducts = []
    #eligibleProductsCount = None
    numberOfProdutsInGrid = 0

    selectedProducts = []
    selectedGrid = []

    def collectDataLength(self):
        return self.productCount



    def getCategoryList(self):
        return self.categoryList

    def getCategoryListCount(self):
        return self.categoryListCount


    #def getEligibleProductsList(self):
    #    return self.eligibleProducts

    #def getEligibleProductsCount(self):
    #    self.eligibleProductsCount = len(self.eligibleProducts)
    #    return self.eligibleProductsCount

    #def addToEligibleProductsList(self,id):
    #    beforeCount = len(self.eligibleProducts)
    #    self.eligibleProducts.extend([id])
    #    list(filter((2).__ne__, self.eligibleProducts))
    #    afterCount = len(self.eligibleProducts)
    #    if afterCount == beforeCount + 1 :
    #        return True
    #    else:
    #        return False

    def getSelectedProductIDList():
        return Manager.selectedProducts

    def getSelectedGridIDList():
        return Manager.selectedGrid

    def getSelectedProductsCount():
        return len(Manager.selectedProducts)

    def addToSelectedProductsList(id,gridID):
        #list(filter((id).__ne__, Manager.selectedProducts)) # Remove all occurances of id
        try:
            if not id in Manager.selectedProducts:
                Manager.selectedGrid.extend([int(gridID)])  # add id
                Manager.selectedGrid = list(set(Manager.selectedGrid))
            Manager.selectedProducts.extend([int(id)])  # add id
            Manager.selectedProducts = list(set(Manager.selectedProducts))
        except Exception as e:
            print(e)

#   MySQL Connection
    def makeConnection(query):
        connection = None
        try:
                #open connection
                connection=pymysql.connect("localhost","root","","beforecart") #localhost-url with port; root -username- ""-password beforecart-database_name
                #prepare a cursor object using cusor() method
                cursor = connection.cursor()
                #execute SQL query using execute() methods
                cursor.execute(query)
                #Fetch Result to variable
                data = cursor.fetchall()
                return data
        except:
            print ("Error: unable to fecth data")
        finally:
            connection.close()

    def makeConnectionSingleTransaction(query):
        connection = None
        data  =[]
        try:
                 #open connection
             connection=pymysql.connect("localhost","root","","beforecart") #localhost-url with port; root -username- ""-password beforecart-database_name
             #prepare a cursor object using cusor() method
             cursor = connection.cursor()
             #execute SQL query using execute() methods
             cursor.execute(query)
             #Fetch Result to variable
             data = cursor.fetchone()
             
        except:
             print ("Error: unable to fecth data")
        finally:
             connection.close()
             return data

#   Random Model
    def getSuggestionsListPRS(self,id,required_suggestion_count,excludeList):
        sampleSet = list(set(range(Manager.getMaxProductID())).difference(set(excludeList)))
        return random.sample(sampleSet, int(required_suggestion_count))  

    def getDislikeData(userId):
        query = 'SELECT distinct PRODUCTID FROM likes WHERE USERID = '+str(userId)+' AND STATUS =0;'
        productSet = []
        for row in Manager.makeConnection(query):
            productSet.extend([int(row[0])])
        return list(set(productSet))

    def getDislikeData(userId):
        query = 'SELECT distinct PRODUCTID FROM likes WHERE USERID = '+str(userId)+' AND STATUS =0;'
        productSet = []
        for row in Manager.makeConnection(query):
            productSet.extend([int(row[0])])
        return list(set(productSet))

    def getCommentCount(productId) :
        query = 'SELECT count(distinct USERID) FROM comments WHERE PRODUCTID = '+str(productId)+';' 
        comments =  Manager.makeConnectionSingleTransaction(query)
        return comments[0]

    def getMaxProductID():
        query = 'SELECT max(id) FROM products;'
        return Manager.makeConnection(query)[0][0]

    def getLikesCount(productId):
        query = 'SELECT count(distinct USERID) FROM likes WHERE PRODUCTID = '+str(productId)+' AND STATUS =1;'
        return Manager.makeConnection(query)[0][0]

    def getCommentData(productId):
        query = 'SELECT ID,USERID,USERNAME,IMAGE,STATUS FROM comments WHERE PRODUCTID = '+str(productId)+' ORDER BY ID ASC;'
        commentSet = []
        for row in Manager.makeConnection(query):
            columns = {}
            columns.update({'ID': row[0]})
            columns.update({'USERID': row[1]})
            columns.update({'USERNAME': row[2]})
            columns.update({'IMAGE': row[3]})
            columns.update({'STATUS': row[3]})
            commentSet.extend([columns])
        return commentSet

    def getCatalogData(productIdList):
        rowSet = []
        for productId in productIdList:
            productId = str(productId)
            if productId and len(productId)>0:
                query = 'SELECT DISTINCT p.id as \'ID\',p.UPC as \'UPC\',p.IMAGE as \'PRODUCT_IMAGE\',p.CATEGORYID as \'CAT_ID\','
                query = query + 'c.CATEGORY as \'CATEGORY\',p.ORIGINAL_COST as \'PRODUCT_PRICE\',p.ITEM_DESCRIPTION as \'PRODUCT_DESC\','
                query = query + 's.stallName as \'STALL_NAME\',s.address as \'STALL_ADDRESS\',s.phone as \'STALL_PHONE\','
                query = query + 's.picture as \'STALL_IMAGE\',s.email as \'STALL_EMAIL\' FROM products p LEFT JOIN category c '
                query = query + 'ON p.CATEGORYID = c.CATEGORY_ID LEFT JOIN stall s ON p.VENDORID = s.stallId WHERE '
                query = query + 'p.id = '+ productId +';'
                dataSet = list(Manager.makeConnection(query))

                for row in dataSet:
                    columns = {}
                    columns.update({'ID': row[0]})
                    columns.update({'UPC': row[1]})
                    columns.update({'PRODUCT_IMAGE': row[2]})
                    columns.update({'CAT_ID': row[3]})
                    columns.update({'CATEGORY': row[4]})
                    columns.update({'PRODUCT_PRICE': row[5]})
                    columns.update({'PRODUCT_DESC': row[6]})
                    columns.update({'STALL_NAME': row[7]})
                    columns.update({'STALL_ADDRESS': row[8]})
                    columns.update({'STALL_PHONE': row[9]})
                    columns.update({'STALL_IMAGE': row[10]})
                    columns.update({'STALL_EMAIL': row[11]})
                    columns.update({'COMMENTS': Manager.getCommentData(row[0])})
                    columns.update({'LIKES': sManager.getLikesCount(row[0])})
                    columns.update({'bascketType': 'Reduced'})
                    columns.update({'suggestionType': 'Reduced'})
                    columns.update({'score': 0})
                    columns.update({'weight': 0})
                    columns.update({'strength': 0})
                    columns.update({'modelType': ''})
                    rowSet.extend([columns])
        return rowSet

    def getUserLikeStatus(userId,productId):
        try:
            query = 'SELECT STATUS FROM likes where USERID = '+str(userId)+' and PRODUCTID = '+str(productId)+';'
            result = Manager.makeConnection(query)[0][0]
        except:
            result = 0
        return result
#################################################
#################################################
    def collectModelData(manager):
        manager.personalPreferenceList = manager.getPersonalPreference(manager.id,manager.userPersonalStrength)
        manager.socialPreferenceList = manager.getSocialPreference(manager.id,manager.userSocialStrength)
        manager.friendList = manager.getFriendList(manager.id)

        for item  in manager.personalPreferenceList:
            manager.categoryList.extend([item['category']])
            item.update({'userType': 'User'})
        for item  in manager.socialPreferenceList:
            manager.categoryList.extend([item['category']])
            item.update({'userType': 'User'})
        list(filter((2).__ne__, manager.categoryList))
        manager.categoryListCount = len(manager.categoryList)

        for friend in manager.friendList:
            friendPersonalList = manager.getPersonalPreference(friend['id'],manager.friendPersonalStrengthFavour*int(friend['weight']))
         #   friendSocialList = manager.getSocialPreference(friend['id'],manager.friendSocialStrengthFavour*friend['weight'])
            manager.productList = manager.productList + friendPersonalList
        #    manager.productList = manager.productList + friendSocialList

        for item  in manager.productList:
            item.update({'userType': 'Friend'})

        manager.productList = manager.productList + manager.personalPreferenceList
        manager.productList = manager.productList + manager.socialPreferenceList
        manager.productCount = len(manager.productList)
        return manager.productList