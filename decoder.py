import csv
import sys
import os
from functools import reduce

class myFile(object):
    argsKind = ['Name', 'AvgCyclomatic', 'AvgLine', 'AvgLineCode', 'CountClassBase', 'CountClassCoupled', 'CountClassDerived', 'CountDeclClass', 'CountDeclClassMethod', 'CountDeclClassVariable', 'CountDeclFunction', 'CountDeclInstanceMethod', 'CountDeclInstanceVariable', 'CountDeclMethod', 'CountDeclMethodAll', 'CountDeclMethodPrivate', 'CountDeclMethodProtected', 'CountDeclMethodPublic', 'CountStmt', 'CountStmtDecl', 'CountStmtExe', 'MaxCyclomatic', 'MaxInheritanceTree', 'MaxNesting', 'PercentLackOfCohesion', 'RatioCommentToCode', 'SumCyclomatic']
    def __init__(self, args):
        # args = [
        # [0:3]   'Name', 'AvgCyclomatic', 'AvgLine', 'AvgLineCode',
        # [4-10]  'CountClassBase', 'CountClassCoupled', 'CountClassDerived', 'CountDeclClass', 'CountDeclClassMethod', 'CountDeclClassVariable', 'CountDeclFunction',
        # [11:17] 'CountDeclInstanceMethod', 'CountDeclInstanceVariable', 'CountDeclMethod', 'CountDeclMethodAll', 'CountDeclMethodPrivate', 'CountDeclMethodProtected', 'CountDeclMethodPublic',
        # [18:20] 'CountStmt', 'CountStmtDecl', 'CountStmtExe',
        # [21:26] 'MaxCyclomatic', 'MaxInheritanceTree', 'MaxNesting', 'PercentLackOfCohesion', 'RatioCommentToCode', 'SumCyclomatic']
        self.args = args
        self.CountClassBase = 0 # AvgClassBase
        self.CountClassCoupled = 0
        self.CountClassDerived = 0
        self.CountDeclMethodAll = 0
        self.MaxInheritanceTree = 0
        self.CountPercentLackOfCohesion = 0
        self.CountClass = 0

    def output(self):
        return reduce(lambda str1,str2: str1+','+str2, map(str, self.args[1:4]+self.args[7:14]+self.args[15:22]+self.args[23:24]+self.args[25:27]))

class myClass(object):
    def __init__(self,fileName):
        self.belongToFile = fileName
        #self.args = args

    def setArgs(self,args):
        self.args = args


if len(sys.argv) != 4:
    print(len(sys.argv))
    print( 'wrong call. usage: python decoder.py <projName> <AnalysisDir> <codeDir>')
    exit()
_, projName, projDir, codeDir = sys.argv
csvFilePath = os.path.join(projDir, projName+".csv")
resultFilePath = os.path.join(projDir, projName+'Decode.txt')
fileClassFilePath = os.path.join(projDir, projName+'_text', 'Files.txt')
classDict = {}
fileDict = {}
fileName = ""
#FileClassDict = {}
#fileKey = ""
#classList = []
with open(fileClassFilePath, 'r') as fileClassFile:
    #for line in fileClassFile.readlines():
    line = fileClassFile.readline()
    while line:
        if line.find(codeDir) == 0:
            fileName = line.strip()
            line = fileClassFile.readline()
            if line == '  Classes\n' or line == '  Interfaces\n':
                line = fileClassFile.readline()
                while line[0:4] == '    ':
                    className = line.strip()
                    classDict[className] = myClass(fileName)
                    #classList.append(line.strip())
                    line = fileClassFile.readline()
                #FileClassDict[fileKey] = classList
                #fileKey = ""
                #classList = []
                fileName = ""
            else:
                line = fileClassFile.readline()
        else:
            line = fileClassFile.readline()


with open(resultFilePath, 'w') as resFile:
    with open(csvFilePath, 'r') as csvFile:
        readCSV = csv.reader(csvFile, delimiter=',')
        for row in readCSV:
            if row[0] == 'File':
                fileName = row[1]
                fileDict[fileName] = myFile(row[1:])
            elif row[0].find("Class") != -1 or row[0].find("Interface") != -1:
                className = row[1]
                if className in classDict:
                    fileName = classDict[className].belongToFile
                    if fileName in fileDict:
                        fileDict[fileName].CountClass += 1
                        fileDict[fileName].CountClassBase += int(row[5])
                        fileDict[fileName].CountClassCoupled += int(row[6])
                        fileDict[fileName].CountClassDerived += int(row[7])
                        fileDict[fileName].CountDeclMethodAll += int(row[15])
                        fileDict[fileName].MaxInheritanceTree = max(fileDict[fileName].MaxInheritanceTree, int(row[23]))
                        fileDict[fileName].CountPercentLackOfCohesion += int(row[25])
    for (fileName,file) in fileDict.items():
        if file.CountClass:
            file.AvgClassBase = file.CountClassBase / file.CountClass
            file.AvgClassCoupled = file.CountClassCoupled / file.CountClass
            file.AvgClassDerived = file.CountClassDerived / file.CountClass
            file.AvgDeclMethodAll = file.CountDeclMethodAll / file.CountClass
            file.AvgPercentLackOfCohesion = file.CountPercentLackOfCohesion / file.CountClass
            if file.CountClass > 1:
                print(fileName + ' CountClass: ' + str(file.CountClass))
        else:
            file.AvgClassBase = 0
            file.AvgClassCoupled = 0
            file.AvgClassDerived = 0
            file.AvgDeclMethodAll = 0
            file.AvgPercentLackOfCohesion = 100

        resFile.write(file.output() +','+str(file.AvgClassBase) +','+str(file.AvgClassCoupled) +','+str(file.AvgClassDerived) +','+str(file.AvgDeclMethodAll) +','+str(file.MaxInheritanceTree) +','+str(file.AvgPercentLackOfCohesion) +'\n')

