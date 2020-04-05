import time
from spaindata import spaindata
from datetime import timedelta
import wx
import wx.adv
import wx.aui
from PIL import ImageFont, Image, ImageDraw
from timeloop import Timeloop

sd = spaindata()
tm = Timeloop()

class CoronaTracker (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size(
            497, 500), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)

        m_radioBox2Choices = sd.ccaa()
        self.m_radioBox2 = wx.RadioBox(self, wx.ID_ANY, u"wxRadioBox", wx.DefaultPosition,
                                        wx.DefaultSize, m_radioBox2Choices, 1, wx.RA_SPECIFY_COLS)
        self.m_radioBox2.SetSelection(0)
        gbSizer1.Add(self.m_radioBox2, wx.GBPosition(
            0, 0), wx.GBSpan(4, 1), wx.ALL, 5)

        self.Casos_checkBox = wx.CheckBox(
            self, wx.ID_ANY, u"Casos", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Casos_checkBox, wx.GBPosition(
            0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Fallecidos_checkBox = wx.CheckBox(
            self, wx.ID_ANY, u"Fallecidos", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Fallecidos_checkBox, wx.GBPosition(
            1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Recuperados_checkBox = wx.CheckBox(
            self, wx.ID_ANY, u"Recuperados", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Recuperados_checkBox, wx.GBPosition(
            2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        gbSizer1.AddGrowableCol(0)

        self.SetSizer(gbSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

class CoronaIcon (wx.App):

    def __init__(self):
        super().__init__()
        self.frame = CoronaTracker(None)
    
    def start(self):
        self.frame.SetIcon(wx.Icon('virus.png', wx.BITMAP_TYPE_PNG, -1, -1))
        self.frame.Show()
        self.MainLoop()
    
    def updateIcon(self):
        img = Image.open("virus.png", 'r')
        fnt = ImageFont.truetype('ImpactCondensed.ttf', 250)
        d = ImageDraw.Draw(img)
        d.text((0, 202), str(int(sd.gimme(self.frame.m_radioBox2.GetStringSelection(),'Casos '))), font=fnt, fill='#00ff00ff')
        img.save('ico.png')
        self.frame.SetIcon(wx.Icon('ico.png', wx.BITMAP_TYPE_PNG, -1, -1))

app = CoronaIcon()

@tm.job(interval=timedelta(seconds=5))
def reload():
    app.updateIcon()

def init():
    tm.start(False)
    app.start()
    tm.stop()

init()