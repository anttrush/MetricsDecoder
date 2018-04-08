import os

rootDir = r"D:\科研\CodeQualityAnalysis\CodeAnalysis\Java5H-1K" # 1H-2H 2H-5H 5H-1K 1K-3W
anadir = os.path.join(rootDir, "_analysisML", "CodeQualityData.csv")

with open(anadir, 'w') as anafile:
    for proj in os.listdir(rootDir):
        if os.path.isdir(os.path.join(rootDir, proj)):
            for file in os.listdir(os.path.join(rootDir, proj)):
                if file == proj + "Decode.csv":
                    with open(os.path.join(rootDir, proj, file)) as projfile:
                        line = projfile.readline()
                        line = projfile.readline()
                        line = projfile.readline()
                        while line:
                            anafile.write(line)
                            line = projfile.readline()