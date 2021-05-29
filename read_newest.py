import os
import zipfile
import pandas as pd
import patoolib


def read_newest(path):

    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    mais_novo=  max(paths, key=os.path.getctime).lower()
    # exttensão dos arquivos
    file_ext = mais_novo.split('.')[-1]
    # dataframe vazio
    df = pd.DataFrame()
    print('--->', os.path.basename( mais_novo))

    # caso arquivo rar 
    if file_ext in ['rar']:
        ext_old = len(os.path.basename( mais_novo).split('.')[-1])
        newfile = path + os.path.basename( mais_novo)[:-(ext_old)] + ".zip"
        print('newfile', newfile)
        patoolib.repack_archive(mais_novo, newfile )
        mais_novo = newfile

    comp_file = zipfile.ZipFile(mais_novo) 
    # para cada aquivo na lista de informações do atquivo mais novo...

    for file_info in comp_file.infolist():
    #abrir o arquivo
        with comp_file.open(file_info) as comp_internal_file:
        #Ler o csv
            df_part = pd.read_csv(comp_internal_file, sep=';')
            df = pd.concat([df, df_part], ignore_index=True)

    return df
 
df = read_newest('./data/')

print(df.info())


