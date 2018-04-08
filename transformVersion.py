import csv
import os

rootDir = r"D:\科研\CodeQualityAnalysis\CodeAnalysis\Java1H-2H"

for proj in os.listdir(rootDir):
    if os.path.isdir(os.path.join(rootDir,proj)):
        for file in os.listdir(os.path.join(rootDir,proj)):
            if file == proj+".csv":
                fileDir = os.path.join(rootDir, proj, file)
                with open(fileDir[:-4]+"_t.csv", "w") as transFile:
                    with open(fileDir, 'r') as oriFile:
                        # build up fileDict which contains all myFile object to collect file-level metrics
                        readCSV = oriFile.readline()
                        while readCSV:
                            row = readCSV.split(',')
                            if len(row) == 59:
                                row.pop(35)
                                row.pop(43)
                                row.pop(47)
                                row.pop(49)
                            transFile.write(','.join(row))
                            readCSV = oriFile.readline()
                os.remove(fileDir)
                os.rename(fileDir[:-4]+"_t.csv", fileDir)

