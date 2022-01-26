import os
import pandas as pd
#import xlsxwriter
import numpy as np
from datetime import datetime
import string
from clases import IndicesDesdeExcel


# Indices que se calcularán y letras que se usarán
indices_nombres = ['Nombre' ,'CVcl', 'Mca', 'Ask%', 'TF%', 'Syi', 'A1', 'A']
N_indices = len(indices_nombres)

# DataFrame que almacenará los indices por cada archivo
df = pd.DataFrame(columns=indices_nombres)

# Cargamos los excels y agregamos los índices al dataframe
#df_index=0
path_entrada = './excels_entrada/'
for excel in os.listdir(path_entrada):
    indices_clase = IndicesDesdeExcel(path_entrada + excel)
    indices_valores = [indices_clase.cvcl(), indices_clase.mca(), indices_clase.askp(), indices_clase.tfp(),
                       indices_clase.syi(), indices_clase.a1(), indices_clase.a()]
    excel_nombre = excel.split('.xls')[0]
    
    df.loc[len(df)+1] = [excel_nombre] + indices_valores


# Creamos el excel resultante
fecha_hoy = datetime.now().strftime(r"%d-%m-%Y %Hh%Mm%Ss") 
excel_nombre = f'Indices {fecha_hoy}.xlsx'
excel_resultado = df.to_excel(f'./excels_salida/{excel_nombre}', index=False)


