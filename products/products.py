from enums.enumsTypes import EnumsType
from productsService.productsService import ProductsService
import re


PATTERNERCARESPECIAL = r'[^a-zA-Z0-9\s]'

class Products():
    def __init__(self):
        self.enumsType = EnumsType()
        self.productsService = ProductsService()
        self.conts = 0
        self.dataDictRefact = {}
        self.stringOfValues = ""
        self.contsData = 0
        self.listOfTuplesOfValues = []

               
    def createColumnsAdd(self, columnsName):
        stringList = []
        stringRow = ', '.join(column for column in columnsName)
        stringList.append(stringRow)
        columnsName[0] = f":{columnsName[0]}"
        stringRowValues = ', :'.join(column for column in columnsName)
        stringList.append(stringRowValues)
        return stringList
    
    def createColumnsAddRow(self, columnsName):
        stringRow = ''
        stringRow = ', '.join(column.upper() for column in columnsName)
        return stringRow
    
    #create the values for add in sql auto
    def createValuesadd(self, listOfValues):
        stringList = []
        for keys , values in listOfValues.items():
            valuesStr = str(values)
            valuesConvert = valuesStr.replace(',' , '.')
            valuesConvert = valuesStr.replace('%' , 'PORCEM')
            valuesConvert = valuesStr.replace('_' , ' ')
            valuesConvert = valuesStr.replace('"' , '')
            valuesConvert = valuesStr.replace("'" , '')
            valuesConvert = valuesStr.replace(':' , ' ')
            valuesConvert = valuesStr.replace('-' , ' ')

            stringList.append(f'{valuesConvert}')
        return stringList

    # ADD in string output and mescle two list for create table
    def createTable(self, listOfColumns, listOfEnumsTypes):
        stringMescle =''
        for row in range(len(listOfColumns)):
            enumsType = self.enumsType.type(listOfEnumsTypes[row])
            if listOfColumns[row] == None:
                pass
            if row == len(listOfColumns)- 1:
                stringMescle += f'{listOfColumns[row].upper()} {enumsType}'
            else:
                stringMescle += f'{listOfColumns[row].upper()} {enumsType} , \n'
        return stringMescle
    
    def getEnumsType(self):
        return self.enumsType.getAllEnumsType()
    
    # Replace special characters with '_'
    def refactEspecialCara(self, listOfColumns):
        listOfRefactColumns = []
        listOfRefactWithdoutCout = []
        for text in listOfColumns:     
            modified_text = re.sub(PATTERNERCARESPECIAL, "_", text)
            modified_text = modified_text.replace(" ", "")
            modified_text = modified_text.replace("â", "a")
            modified_text = modified_text.replace("ç", "c")
            modified_text = modified_text.replace("ú", "u")
            modified_text = modified_text.replace(" ", "")
            modified_text = modified_text.replace("é", "e")
            modified_text = modified_text.replace("á", "a")
            listOfRefactColumns.append(f'{modified_text.upper()}')
            listOfRefactWithdoutCout.append(f'{modified_text}')
        return listOfRefactColumns
    
        # Replace special characters with '_' 
    def refactEspecialCaraSemAS(self, listOfColumns):
        listOfRefactWithdoutCout = []
        for text in listOfColumns:
            modified_text = re.sub(PATTERNERCARESPECIAL, '_', text)
            modified_text = modified_text.replace(" ", "")
            modified_text = modified_text.replace("â", "a")
            modified_text = modified_text.replace("ç", "c")
            modified_text = modified_text.replace("ú", "u")
            modified_text = modified_text.replace(" ", "")
            modified_text = modified_text.replace("é", "e")
            modified_text = modified_text.replace("á", "a")
            listOfRefactWithdoutCout.append(f'{modified_text.upper()}')
        return listOfRefactWithdoutCout

    def createTableAUtoVarchar(self,listOfColumns, varchar = 250):
        listOfColumnsRefact = self.refactEspecialCara(listOfColumns)
        stringMescle =''
        enumsType = self.enumsType.type(1)
        for row in range(len(listOfColumns)):
            if listOfColumnsRefact[row] == None:
                pass
            if row == len(listOfColumns)- 1:
                stringMescle += f'{listOfColumnsRefact[row].upper()} {enumsType}'
            else:
                stringMescle += f'{listOfColumnsRefact[row].upper()} {enumsType} , \n'
        return stringMescle
        
    def checkTables(self, nameOfFile):
        return self.productsService.checkTables(nameOfFile)
    
    def readSheetsOfXlsx(self, path):
        return self.productsService.readSheetsOfXlsx(path)
    
    def getLenXlsxSheets(self,path, sheets):
        return self.productsService.getLenXlsxSheets(path, sheets)
    
    def readXlsxIlocSheets(self, path, rows, sheets):
        return self.productsService.readXlsxIlocSheets(path, rows, sheets)
    
    def addOracleDataAuto(self,stringValues, nameOfBanco, data):
        return self.productsService.addOracleDataAuto(stringValues, nameOfBanco, data)
    
    #convert normal dict for especial dict value OLD VERSION error
    def convertEspecialCarToDict(self, path, sheets, row, listOfColumns): 
        data = {}  
        data.update(self.productsService.readXlsxIlocSheets(path, row, sheets))    
        refactHeadDict = self.refactEspecialCaraSemAS(data.keys())
        self.conts = 0
        for keys , value in data.items():
            self.dataDictRefact.update({refactHeadDict[self.conts] : value})
            self.conts +=1
        return self.dataDictRefact
    
    #convert normal dict for especial dict value
    def convertEspecialCarToDictValues(self,path, row, sheets, listOfColumns):
        self.conts= 0
        dataDict = {}
        
        dataRow = self.productsService.readXlsxIlocSheets(path, row, sheets)
        listOfValues = self.createValuesadd(dataRow)
        for keys in listOfColumns:  
            dataDict.update({keys : listOfValues[self.conts]})
            self.conts+=1
        return dataDict
     
    #add columns name of insert into
    def columnsName(self, path, sheets):
        data = self.productsService.readXlsxIlocSheets(path,0, sheets)
        refactHeadDict = self.refactEspecialCaraSemAS(data.keys())
        return refactHeadDict
        
    #add auto for sql inject
    def createAuto(self, bancoName, path, sheets):
        listOfColumns = self.productsService.getXlsxCOlmunsNameSheets(path, sheets)
        stringDataCreateTable = self.createTableAUtoVarchar(listOfColumns)
        print(self.productsService.createTableAuto(bancoName, stringDataCreateTable))

    def convertRowsOfStringValues(self):
        rows = []
        for i in range(self.contsData):
            rows.append(f':{i + 1}')
        return rows

    def convertColumnsForTrigger(self, columnsName):
        triggerName = ''
        for name in columnsName:
            triggerName.append(f':{name}')
        return triggerName
            
    #convert for string output
    def converDictForStringValues(self, datas):
        stringValues = ""
        print(len(datas))
        for keys , values in datas.items():
            self.conts+= 1
            if self.conts == len(datas):
                stringValues += f'{values} '
            else:
                stringValues += f'{values} ,'
        return stringValues

    #add in database auto
    def addOracle(self, path, sheets, tableName):
        listDictColumns = self.productsService.getColumnsNames(tableName)
        stringsInput = self.createColumnsAdd(listDictColumns)
        rowLen = self.productsService.getLenXlsxSheets(path, sheets)
        for row in range(rowLen):
            listOfCOlumnsName = self.columnsName(path, sheets)
            insertData = self.convertEspecialCarToDictValues(path, 1, sheets, listOfCOlumnsName)
            print(self.productsService.addOracleDataAuto(stringsInput[0], stringsInput[1], tableName, insertData))

 