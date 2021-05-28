import os
import zipfile
import pandas as pd

def open_newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    mais_novo=  max(paths, key=os.path.getctime)
    df = pd.DataFrame()
    #ler arquivo zip mais novo
    thezip = zipfile.ZipFile(mais_novo) 
    # para cada aquivo na lista de informações do atquivo mais novo...
    for zipinfo in thezip.infolist():
    #abrir o arquivo
        with thezip.open(zipinfo) as thefile:
        #Ler o csv
            df_part = pd.read_csv(thezip.open(zipinfo), sep=';')
            print(df_part.info())
            df = pd.concat([df, df_part], ignore_index=True)
    return df
        
df = open_newest('./data/')

print(df.info())

