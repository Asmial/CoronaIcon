import time
from datetime import timedelta
import wx
import wx.adv
from PIL import ImageFont, Image, ImageDraw
from timeloop import Timeloop
import pandas as pd
import numpy as np



class coronaMonitor(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.Bind(wx.EVT_ICONIZE, self.nope)
        self.Show()
        self.Iconize()

    def nope(self, event):
        if not self.IsIconized():
            self.Iconize(True)

class data():

    cod_iso = '''code,name
AN,Andalucía
AR,Aragón
AS,"Asturias, Principado de"
CN,Canarias
CB,Cantabria
CM,Castilla-La Mancha
CL,Castilla y León
CT,Catalunya (Cataluña)
EX,Extremadura
GA,Galicia (Galicia)
IB,Illes Balears (Islas Baleares)
RI,La Rioja
MD,"Madrid, Comunidad de"
MC,"Murcia, Región de"
NC,"Navarra, Comunidad Foral de/Nafarroako Foru Komunitatea​"
PV,País Vasco/Euskadi
VC,"Valenciana, Comunidad/Valenciana, Comunitat​"
'''

    def __init__(self):
        self.update()
        iso = pd.read_csv(self.cod_iso)
        print(self.df.join(iso.set_index('code'),on='CCAA Codigo ISO'))

    
    def update(self):
        csv = pd.read_csv("https://covid19.isciii.es/resources/serie_historica_acumulados.csv",delimiter=',',encoding='cp1252')
        df = pd.DataFrame.truncate(csv, after=len(csv) - 3)
        df['Fecha'] = pd.to_datetime(df['Fecha'],dayfirst=True,format='%d/%m/%Y')
        df['Casos '] = pd.to_numeric(df['Casos '])
        df = df.groupby('CCAA Codigo ISO').max()
        df = df.sort_values(by=['Casos '], ascending=False)
        self.df = df

class App():
    num = 1
    tm = Timeloop()

    def __init__(self):
        super().__init__()
        app = wx.App()
        self.frame = coronaMonitor(None, 'hola!')
        try:
            self.tm.start(False)
            self.app.MainLoop()
        finally:
            self.tm.stop()
    
    @tm.job(interval=timedelta(seconds=5))
    def updateIcon(self):
        img = Image.open("virus.png", 'r')
        fnt = ImageFont.truetype('C:/Windows/Fonts/Impact.ttf', 120)
        d = ImageDraw.Draw(img)
        d.text((10, 10), str(num), font=fnt, fill='#ffffffff')
        num += 1
        img.save('ico.png')
        frame.SetIcon(wx.Icon('ico.png', wx.BITMAP_TYPE_PNG, -1, -1))

