
import csv
import time
import shutil


class FileHandler:

    fileName = 'fileHandler.py'
    className = 'FileHandler'

    @classmethod
    def csvFile(cls, fileName:str, data:list, op:str):
        # op: r/w/a

        with open(fileName, op, newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        
        print(f'Save {fileName} file!')

 