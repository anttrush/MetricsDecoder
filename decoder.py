import csv
import sys
import os
import math
from functools import reduce

class myFile(object):
    # to collect file-level info from class-level reports
    argsField = ['Name', 'AvgCyclomatic', 'AvgCyclomaticModified', 'AvgCyclomaticStrict', 'AvgEssential', 'AvgLine', 'AvgLineBlank', 'AvgLineCode', 'AvgLineComment', 'CountClassBase', 'CountClassCoupled', 'CountClassDerived', 'CountDeclClass', 'CountDeclClassMethod', 'CountDeclClassVariable', 'CountDeclFile', 'CountDeclFunction', 'CountDeclInstanceMethod', 'CountDeclInstanceVariable', 'CountDeclMethod', 'CountDeclMethodAll', 'CountDeclMethodDefault', 'CountDeclMethodPrivate', 'CountDeclMethodProtected', 'CountDeclMethodPublic', 'CountInput', 'CountLine', 'CountLineBlank', 'CountLineCode', 'CountLineCodeDecl', 'CountLineCodeExe', 'CountLineComment', 'CountOutput', 'CountPath', 'CountSemicolon', 'CountStmt', 'CountStmtDecl', 'CountStmtExe', 'Cyclomatic', 'CyclomaticModified', 'CyclomaticStrict', 'Essential', 'MaxCyclomatic', 'MaxCyclomaticModified', 'MaxCyclomaticStrict', 'MaxEssential', 'MaxInheritanceTree', 'MaxNesting', 'PercentLackOfCohesion', 'RatioCommentToCode', 'SumCyclomatic', 'SumCyclomaticModified', 'SumCyclomaticStrict', 'SumEssential']
    fileField = ['prediction','AvgCyclomatic', 'AvgCyclomaticModified', 'AvgCyclomaticStrict', 'AvgEssential', 'AvgLine', 'AvgLineBlank', 'AvgLineCode', 'AvgLineComment', 'AvgClassBase', 'AvgClassCoupled', 'AvgClassDerived', 'CountDeclClass', 'CountDeclClassMethod', 'CountDeclClassVariable', 'Ca', 'CountDeclFunction', 'CountDeclInstanceMethod', 'CountDeclInstanceVariable', 'CountDeclMethod', 'AvgDeclMethodAll', 'CountDeclMethodDefault', 'CountDeclMethodPrivate', 'CountDeclMethodProtected', 'CountDeclMethodPublic', 'CountLine', 'CountLineBlank', 'CountLineCode', 'CountLineCodeDecl', 'CountLineCodeExe', 'CountLineComment', 'CountSemicolon', 'CountStmt', 'CountStmtDecl', 'CountStmtExe', 'MaxCyclomatic', 'MaxCyclomaticModified', 'MaxCyclomaticStrict', 'MaxEssential', 'MaxInheritanceTree', 'MaxNesting', 'AvgPercentLackOfCohesion', 'RatioCommentToCode', 'SumCyclomatic', 'SumCyclomaticModified', 'SumCyclomaticStrict', 'SumEssential']
    def __init__(self, args, ProjStars):
        # args = [ [0]  'Name'
        # [1:5]   'AvgCyclomatic', 'AvgCyclomaticModified', 'AvgCyclomaticStrict', 'AvgEssential'
        # [5:9]   'AvgLine', 'AvgLineBlank', 'AvgLineCode', 'AvgLineComment'
        ##[9:12]  'CountClassBase', 'CountClassCoupled', 'CountClassDerived' ##### CLASS #####
        # [12:15] 'CountDeclClass', 'CountDeclClassMethod', 'CountDeclClassVariable' [15] 'CountDeclFile' NULL
        # [16:20] 'CountDeclFunction', 'CountDeclInstanceMethod', 'CountDeclInstanceVariable', 'CountDeclMethod'
        ##[20]    'CountDeclMethodAll' [25,32,33] 'CountInput', 'CountOutput', 'CountPath' NULL
        # [21:25] 'CountDeclMethodDefault', 'CountDeclMethodPrivate', 'CountDeclMethodProtected', 'CountDeclMethodPublic'
        # [26:32] 'CountLine', 'CountLineBlank', 'CountLineCode', 'CountLineCodeDecl', 'CountLineCodeExe', 'CountLineComment'
        # [34:38] 'CountSemicolon', 'CountStmt', 'CountStmtDecl', 'CountStmtExe'
        ##[38:42] 'Cyclomatic', 'CyclomaticModified', 'CyclomaticStrict', 'Essential' ##### CLASS #####
        # [42:46] 'MaxCyclomatic', 'MaxCyclomaticModified', 'MaxCyclomaticStrict', 'MaxEssential'
        ##[46,48] 'MaxInheritanceTree','PercentLackOfCohesion' ##### CLASS #####
        # [47]    'MaxNesting',
        # [49:54] 'RatioCommentToCode', 'SumCyclomatic', 'SumCyclomaticModified', 'SumCyclomaticStrict', 'SumEssential']
        # self.args get from file-level reports, so some item maybe 0 or null
        self.args = args
        # the following metrics will add up from 0 and finally divid self.CountClass to get self.avgsth.
        self.CountClassBase = 0 # AvgClassBase
        self.CountClassCoupled = 0
        self.CountClassDerived = 0
        self.CountDeclMethodAll = 0
        self.CountPercentLackOfCohesion = 0
        self.AvgClassBase = 0
        self.AvgClassCoupled = 0
        self.AvgClassDerived = 0
        self.AvgDeclMethodAll = 0
        self.AvgPercentLackOfCohesion = 0
        # this metrics remain what it means, that is, not do avg math
        self.MaxInheritanceTree = 0
        # self.CountClass is used for get self.avgsth, and will not output to file.
        self.CountClass = 0
        # self.Ca and self.ProjStars is used to calculate prediction
        self.Ca = 0
        self.ProjStars = int(ProjStars)
        # set by self.setprediction()
        self.prediction = 0

    def setprediction(self, pre):
        self.prediction = pre

    def output(self):
        self.res = [self.prediction]+self.args[1:9]+[self.AvgClassBase, self.AvgClassCoupled, self.AvgClassDerived]
        self.res += self.args[12:15] +[self.Ca]+ self.args[16:20]+[self.AvgDeclMethodAll]
        self.res += self.args[21:25]+self.args[26:32]+self.args[34:38]+self.args[42:46]+[self.MaxInheritanceTree]
        self.res += [self.args[47],self.AvgPercentLackOfCohesion]+self.args[49:]
        return reduce(lambda str1,str2: str1+','+str2, map(str, self.res))

class myClass(object):
    # to collect class-level info from Understand reports and restore the full_name of the file which it belong to
    def __init__(self,fileName):
        self.belongToFile = fileName
        #self.args = args

if len(sys.argv) != 5:
    print(len(sys.argv))
    print( 'wrong call. usage: python decoder.py <projName> <AnalysisDir> <codeDir> <starsNum>')
    # python decoder.py butterknifeAnalysis D:\科研\CodeQualityAnalysis\CodeAnalysis\JavaSampling\butterknifeAnalysis\ D:\CodeRepertory\Java\butterknife
    exit()
_, projName, projDir, codeDir, starsNum = sys.argv
csvFilePath = os.path.join(projDir, projName+".csv")
resultFilePath = os.path.join(projDir, projName+'Decode.csv')
fileClassFilePath = os.path.join(projDir, projName+'_text', 'Files.txt')
importFilePath = os.path.join(projDir, projName+'_text', 'Imports.txt')
projMetricsFilePath = os.path.join(projDir, projName+'_text', 'ProjectMetrics.txt')
classDict = {}
fileDict = {}
fileName = ""
projFileNum = 0

# get projFileNum from projectMetrics report file
with open(projMetricsFilePath, 'r') as projFile:
    for line in projFile.readlines():
        if line.find('Files:') == 0:
            projFileNum = int(line.split(':')[1].strip())
            break

# build up classDict which contain all the myClass object
with open(fileClassFilePath, 'r', encoding='UTF-8') as fileClassFile:
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
                    line = fileClassFile.readline()
                fileName = ""
            else:
                line = fileClassFile.readline()
        else:
            line = fileClassFile.readline()


with open(resultFilePath, 'w') as resFile:
    # get fieldnames for csv
    fieldnames = myFile.fileField
    writer = csv.DictWriter(resFile, fieldnames=fieldnames)
    writer.writeheader()
    with open(csvFilePath, 'r') as csvFile:
        # build up fileDict which contains all myFile object to collect file-level metrics
        readCSV = csv.reader(csvFile, delimiter=',')
        for row in readCSV:
            if row[0] == 'File':
                # file record
                fileName = row[1]
                fileDict[fileName] = myFile(row[1:], starsNum)
            elif row[0].find("Class") != -1 or row[0].find("Interface") != -1:
                # class record
                className = row[1]
                if className in classDict:
                    fileName = classDict[className].belongToFile
                    if fileName in fileDict:
                        fileDict[fileName].CountClass += 1
                        fileDict[fileName].CountClassBase += int(row[10])
                        fileDict[fileName].CountClassCoupled += int(row[11])
                        fileDict[fileName].CountClassDerived += int(row[12])
                        fileDict[fileName].CountDeclMethodAll += int(row[21])
                        fileDict[fileName].MaxInheritanceTree = max(fileDict[fileName].MaxInheritanceTree, int(row[47]))
                        fileDict[fileName].CountPercentLackOfCohesion += int(row[49])

    with open(importFilePath, 'r') as imFile:
        # to calculate file.Ca
        fileName = ''
        readIm = imFile.readline()
        while readIm:
            if readIm.find(codeDir) == 0:
                fileName = readIm.strip()
                readIm = imFile.readline()
                while readIm.find('| ') == 0:
                    importName = readIm[2:].strip().split('.')
                    importFile = ''
                    for item in importName:
                        importFile += item + '\\'
                    importFile = importFile[:-1] + '.java'
                    for (fileName, file) in fileDict.items():
                        if fileName.find(importFile) != -1:
                            file.Ca += 1
                            break
                    readIm = imFile.readline()
            else:
                readIm = imFile.readline()

    for (fileName,file) in fileDict.items():
        # get myFileObject.avgsth metrics
        if file.CountClass:
            file.AvgClassBase = file.CountClassBase / file.CountClass
            file.AvgClassCoupled = file.CountClassCoupled / file.CountClass
            file.AvgClassDerived = file.CountClassDerived / file.CountClass
            file.AvgDeclMethodAll = file.CountDeclMethodAll / file.CountClass
            file.AvgPercentLackOfCohesion = file.CountPercentLackOfCohesion / file.CountClass
            if file.CountClass > 1:
                # debug log
                print(fileName + ' CountClass: ' + str(file.CountClass))
        else:
            file.AvgClassBase = 0
            file.AvgClassCoupled = 0
            file.AvgClassDerived = 0
            file.AvgDeclMethodAll = 0
            file.AvgPercentLackOfCohesion = 100

        file.setprediction(math.log(file.ProjStars/projFileNum * (1 + file.Ca)))
        resFile.write(file.output()+'\n')
        # for debug
        if file.Ca != 0:
            print('Ca: '+ str(file.Ca) + '\t| ' + file.args[0])

