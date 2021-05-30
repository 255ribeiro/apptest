import os
import zipfile
import pandas as pd
import patoolib


def read_newest(path):

    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    paths = sorted(paths, key=os.path.getctime)
    newest_file = paths[-1]
    [os.remove(i) for i in paths[:-1]]
    # exttensao dos arquivos
    file_ext = newest_file.split('.')[-1]
    # dataframe vazio
    df = pd.DataFrame()
    print('--->', os.path.basename( newest_file))

    # caso arquivo rar 
    if file_ext.lower() in ['rar']:
        ext_old = len(os.path.basename( newest_file).split('.')[-1])
        new_file = path + os.path.basename( newest_file)[:-(ext_old)] + "zip"
        patoolib.repack_archive(newest_file, new_file )
        os.remove(newest_file)
        newest_file = new_file

    comp_file = zipfile.ZipFile(newest_file) 
    # para cada aquivo na lista de informacoes do atquivo mais novo...

    for file_info in comp_file.infolist():
    #abrir o arquivo
        with comp_file.open(file_info) as comp_internal_file:
        #Ler o csv
            df_part = pd.read_csv(comp_internal_file, sep=';')
            df = pd.concat([df, df_part], ignore_index=True)

    return df
 
df = read_newest('./data/')

print(df.info())


