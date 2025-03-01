
import csv
import os
import pandas as pd
import numpy as np

def addNoiseToRecording(trajectory: list[list], noiseRatio=0.1):
    if not trajectory:
        return trajectory
    
    trajectory = np.array(trajectory, dtype=float)
    col_std = np.std(trajectory, axis=0)
    noise = np.random.uniform(-noiseRatio, noiseRatio, trajectory.shape) * col_std
    
    return (trajectory + noise).tolist()

def saveMatrixToCsv(data, columns, fileName):
    with open(fileName, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(data)

def findAllFilesOfExtensionIn(path, extension):
    files = []
    for file in os.listdir(path):
        if file.endswith(extension):
            files.append(file)
    return files

filesToAddNoiseTo = [0]
datafiles = findAllFilesOfExtensionIn(os.getcwd(), ".csv")
for i, datafile in enumerate(datafiles):
    if "_noised" in datafile or i not in filesToAddNoiseTo: continue
    
    df = pd.read_csv(datafile, index_col=None)
    df_cols = df.columns
    trajectory = df.values.tolist()

    trajectory = addNoiseToRecording(trajectory, noiseRatio=0.1)
    newDatafileName = datafile[:datafile.find(".")] + "_noised.csv"
    saveMatrixToCsv(trajectory, df_cols, newDatafileName)