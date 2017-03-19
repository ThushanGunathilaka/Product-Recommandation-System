from contextlib import closing
from datetime import datetime
import pymysql
import logging
import warnings
import csv

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("Initialize MySQL Database")
from PRSBoot.PRSConfig import Conf
LOGGER.propagate = Conf().getVerbose()

# file handler
handler = logging.FileHandler('PRS.log')
handler.setLevel(logging.INFO)
# logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

class InitMySQL(object):
    '''pymysql related initialization queries '''

    def initCatalogMySQL(self,currentConnection):
        '''
        Create Catalog MySQl Table for Recommandation Models
        '''
        # prepare a cursor object using cursor() method
        currentCursor = currentConnection.cursor(pymysql.cursors.DictCursor)
        # Prepare SQL query

        query = 'CREATE TABLE IF NOT EXISTS `catalog_account` ('
        query = query + '`userID` INT NOT NULL,'
        query = query + '`email` VARCHAR(45) NOT NULL,'
        query = query + '`password` VARCHAR(45) NOT NULL,'
        query = query + '`stallName` VARCHAR(45) NULL,'
        query = query + '`phone` VARCHAR(45) NULL,'
        query = query + '`ownerName` VARCHAR(45) NULL,'
        query = query + '`ownerNIC` VARCHAR(45) NULL,'
        query = query + '`address` VARCHAR(255) NULL,'
        query = query + '`image` BLOB NULL,'
        query = query + '`active` TINYINT(1) NULL,'
        query = query + 'PRIMARY KEY (`userID`),  UNIQUE INDEX `email_UNIQUE` (`email` ASC));'
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                # Execute the SQL command
                currentCursor.execute(query)
                LOGGER.info ('MySQL Table [catalog_account] Created')
        except:
            LOGGER.info ('MySQL Table [catalog_account] Not Created')
            pass
        currentConnection.commit()
        currentCursor.close()

    def initDropCategoryMySQL(self,currentConnection):
        '''
        Drop Category MySQl Table for Recommandation Models
        '''
        # prepare a cursor object using cursor() method
        currentCursor = currentConnection.cursor(pymysql.cursors.DictCursor)
        # Prepare SQL query

        query = 'DROP TABLE IF EXISTS `beforecart`.`category`;'
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                # Execute the SQL command
                currentCursor.execute(query)
                LOGGER.info ('MySQL Table [Category] Dropped')
        except Exception as e:
            LOGGER.info ('MySQL Table[Category] Drop was not successfull {}'.format(e))
            pass
        currentConnection.commit()
        currentCursor.close()
    
    def initCreateCategoryMySQL(self,currentConnection):
        '''
        Create Category MySQl Table for Recommandation Models
        '''
        # prepare a cursor object using cursor() method
        currentCursor = currentConnection.cursor(pymysql.cursors.DictCursor)
        # Prepare SQL query

        query = '''
            CREATE TABLE IF NOT EXISTS `category` (
                `id` int(4)  NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `CATEGORY` varchar(500) NOT NULL,
                `CATEGORY_ID` int(4) NOT NULL UNIQUE
            );
        '''
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                # Execute the SQL command
                currentCursor.execute(query)
                LOGGER.info ('MySQL Table [Category] Created')
        except:
            LOGGER.info ('MySQL Table [Category] Not Created')
            pass
        currentConnection.commit()
        currentCursor.close()

    def initInsertCategoryMySQL(self,currentConnection):
        '''
        Insert Data to Category MySQl Table for Recommandation Models
        '''
        # prepare a cursor object using cursor() method
        currentCursor = currentConnection.cursor(pymysql.cursors.DictCursor)
        # Prepare SQL query

        query = '''
            INSERT INTO `beforecart`.`category`
            (`CATEGORY`,`CATEGORY_ID`)
            VALUES
            ('WOMENS PETITES',1),
            ('DRESSES & SUITS',2),
            ('INTIMATE APPAREL SLEEPWEAR',3),
            ('JUNIORS APPAREL',4),
            ('RALPH LAUREN APPAREL',5),
            ('WOMENS BETTER APPAREL',6),
            ('WOMENS SOCKS & HOSIERY',7),
            ('WOMENS SWIM WEAR',8);
        '''
        try:
            # Execute the SQL command
            currentCursor.execute(query)
            LOGGER.info ('Data Inserted Into MySQL Table [Category]')
        except:
            LOGGER.info ('Data Insertion Failed Into MySQL Table [Category]')
            pass
        currentCursor.close()
        currentConnection.commit()

    def insertFromCSV(self,query,csvFileName):
        '''
        Insert Data to MySQl Table form CSV File
        '''
        LOGGER.info ('Data Inserting Into to MySQL using Query')
        LOGGER.info (query)
        # prepare a cursor object using cursor() method
        currentCursor = currentConnection.cursor(pymysql.cursors.DictCursor)
        # Prepare SQL query
        csvData = csv.reader(file('categoryData.csv'))
        for row in csvData:
            try:
                # Execute the SQL command
                currentCursor.execute(query,row)
                LOGGER.info ('Data Inserted to MySQL Table using File : [{}]'.format(csvFileName))
            except:
                LOGGER.info ('Data Insertion Failed Into MySQL Table using File : [{}]'.format(csvFileName))
                pass
        currentConnection.commit()
        currentCursor.close()

#ALTER TABLE beforecart.category ADD COLUMN IDENTITY INT DEFAULT 0;
#ALTER TABLE beforecart.category DROP COLUMN IDENTITY;
#ALTER TABLE beforecart.products ADD COLUMN inStock INT DEFAULT 1;
#ALTER TABLE beforecart.products DROP COLUMN inStock;
#categoryQuery = 'INSERT INTO category(id, category, categoryID ) VALUES(%s,%s,%s)'
#TRUNCATE TABLE  category;