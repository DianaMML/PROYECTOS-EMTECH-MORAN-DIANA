# -*- coding: utf-8 -*-
"""
@author: DIANA MORAN

"""

import pandas as pd 
#%%

#Se abre el archivo:
    
synergy_dataframe = pd.read_csv('synergy_logistics_database.csv', 
                                index_col=0,
                                encoding='utf-8', 
                                parse_dates=[4, 5])

#%%

#A continuacion se realiza el analisis de datos correspondinete a la opcion
#numero uno del proyecto para despues explicar en el reporte si es viable.
#Para encontrar las 10 rutas mas demandadas acorde a los flujos de importacion 
#y exportacion de la empresa se busca la sigueinte combinacion:
    
#Combinacion unica de "origin", "destination", "transport_mode", "direction".
#Con "direction" podremos distinguir si los movimientos son importaciones o 
#exportaciones y cuales aportan mas ganacias a la empresa:

combinaciones = synergy_dataframe.groupby(by=["origin", "destination",
                                           "transport_mode", "direction"])

#Ahora se obtiene el dataframe con la descripcion de cada una de las
#combinaciones. Se prestara especial atencion en "total value", "count" y 
#"mean" para realizar el analisis de las 10 rutas mas demandadas y conocer 
#si esta estrategia es viable:

descripcion = combinaciones.describe()["total_value"]

#%%

#Ahora se obtiene la serie "mean" para observar el promedio del valor de 
#ingresos (ganancias) de cada ruta. Se ordena de mayor a menor:

mean = descripcion["mean"]

#Se ordena la serie de mayor a menor:
mean_sort = mean.sort_values(ascending=False)

#%%

#Ahora se obtiene la serie "count" para observar cuantas veces es requerida 
#cada ruta. Se ordena de mayor a menor:

count = descripcion["count"]

#Se ordena la serie de mayor a menor:
count_sort = count.sort_values(ascending=False)

#%%

#A continuacion se realiza el analisis de datos correspondinete a la opcion
#numero dos del proyecto para despues explicar en el reporte si es viable.

#Se hace el analisis del medio de transporte desde el año 2015 a 2020. 
#Es decir, se obtendra la suma de los ingresos de todos los años para cada uno 
#de los medios de transporte para determinar cuales son los 3 mas importantes:

import seaborn as sns

datos = synergy_dataframe.copy()   
datos['year_month'] = datos['date'].dt.strftime('%Y-%m')
datos_year_month = datos.groupby(['year_month', 'transport_mode'])

#Se usa la serie sum para el valor total:
serie = datos_year_month.sum()['total_value']                                     
         
#Se transforma de serie a dataframe:                                     
dym = serie.to_frame().reset_index()

#Se modififca la forma en que se requiere se muestre el grafico:
dym = dym.pivot('year_month', 'transport_mode', 'total_value')

#Se crea el grafico:
sns.lineplot(data=dym)

#%%

#Se hace el analisis del medio de transporte desde el año 2015 a 2020 pero 
#ahora se obtendran resultados respecto a la frecuencia del uso de cada
#transporte a lo largo del periodo 2015-2020.

datos = synergy_dataframe.copy()
datos['year_month'] = datos['date'].dt.strftime('%Y-%m')
datos_year_month = datos.groupby(['year_month', 'transport_mode'])

#Se usa la serie count para el obtener la frecuencia:
serie = datos_year_month.count()['total_value']                                     
                                              
#Se transforma de serie a dataframe:
dym = serie.to_frame().reset_index()

#Se modififca la forma en que se requiere se muestre el grafico:
dym = dym.pivot('year_month', 'transport_mode', 'total_value')

#Se crea el grafico:
sns.lineplot(data=dym)

#%%

#A continuacion se realiza el analisis de datos correspondinete a la opcion
#numero tres del proyecto para despues explicar en el reporte si es viable.

#Se separan importaciones y exportaciones en diferentes listas:

exports = synergy_dataframe[synergy_dataframe['direction'] == 'Exports']
imports = synergy_dataframe[synergy_dataframe['direction'] == 'Imports']

#Se obtiene la solucion a la opcion 3 del proyecto:

def sol_3(df):
    
    #Primero se agrupa por pais de origen y se obtiene la suma de total value 
    #correspondiente a cada uno:
    pais_total_value = df.groupby('origin').sum()['total_value'].reset_index()
    
    #Se obtienen los ingresos totales para exportaciones o importaciones:
    total_value_for_percent = pais_total_value['total_value'].sum()
    
    #Se calcula el porcentaje:
    pais_total_value['percent'] = 100 * pais_total_value['total_value'] / total_value_for_percent
    
    #Se ordenan los datos:
    pais_total_value.sort_values(by='percent', ascending=False, inplace=True)
    
    #Se obtiene la suma acumulada:
    pais_total_value['cumsum'] = pais_total_value['percent'].cumsum()
    lista_final = pais_total_value[pais_total_value['cumsum'] <80]
    
    return lista_final

print('Paises que generan el 80% del valor de las exportaciones:\n', sol_3(exports))

#%%

#Para facilitar la lectura del codigo se obtebdra a continuacion 
#el analisis de datos correspondiente a la lista de las importaciones
#en realcion a la celda anterior para obtener los paises que generan el 80% del
#valor de las importaciones:

def sol_3(df):
    
    #Primero se agrupa por pais de origen y se obtiene la suma de total value 
    #correspondiente a cada uno:
    pais_total_value = df.groupby('origin').sum()['total_value'].reset_index()
    
    #Se obtienen los ingresos totales para exportaciones o importaciones:
    total_value_for_percent = pais_total_value['total_value'].sum()
    
    #Se calcula el porcentaje:
    pais_total_value['percent'] = 100 * pais_total_value['total_value'] / total_value_for_percent
    
    #Se ordenan los datos:
    pais_total_value.sort_values(by='percent', ascending=False, inplace=True)
    
    #Se obtiene la suma acumulada:
    pais_total_value['cumsum'] = pais_total_value['percent'].cumsum()
    lista_final = pais_total_value[pais_total_value['cumsum'] <80]
    
    return lista_final

print('Paises que generan el 80% del valor de las importaciones:\n', sol_3(imports))
               
                 













                                              
                                              
                                              
                                              
                                              
                                              
                                              
                                              
                                              
                                              
                                              