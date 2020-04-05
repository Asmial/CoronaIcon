import pandas as pd
import numpy as np


class spaindata():
    def __init__(self):
        self.iso = pd.read_csv('isocodes.csv')
        self.update()

    def update(self):
        csv = pd.read_csv("https://covid19.isciii.es/resources/serie_historica_acumulados.csv",
                          delimiter=',', encoding='cp1252')
        df = pd.DataFrame.truncate(csv, after=len(csv) - 3)
        df['Casos '] = pd.to_numeric(df['Casos '])
        df = df.groupby('CCAA Codigo ISO').max()
        df = df.sort_values(by=['Casos '], ascending=False)
        df = df.join(self.iso.set_index('code'), on='CCAA Codigo ISO')
        df = df.drop('Fecha', axis=1)
        df = df.set_index('name')
        self.df = df

    def ccaa(self):
        return self.df.index.values
    
    def gimme(self, index, data):
        return self.df[data][index]
