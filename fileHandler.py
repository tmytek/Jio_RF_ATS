
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

    @classmethod
    def copyFileFromNaToLocal(cls, fileToLocalPath:str):

        try:
            funcName = 'copyFileFromNaToLocal()'

            time.sleep(0.1)

            fileFromNa = fileToLocalPath.split('/')[-1]

            shutil.copyfile(f'{NA.getNaRootPath()}\{fileFromNa}', fileToLocalPath)
            # shutil.copy(src, dst)
            # shutil.copyfile(f'{os.getcwd()}/measureReport/AAA.txt', f'{naSaveFileRemotePath}/AAA.txt', follow_symlinks=True)
        except Exception as e:
            msg = f'[{cls.fileName}][{cls.className}][{funcName}][copy file NA to local PC][exception] {e}'
            print(msg); #LogHandler.log(msg, 'error')