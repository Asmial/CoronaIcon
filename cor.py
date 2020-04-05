# Timeloop
import time
from timeloop import Timeloop
from datetime import timedelta

# Data
from spaindata import spaindata

# UI
import wx
import wx.adv
import wx.aui

# Pillow
from PIL import ImageFont, Image, ImageDraw


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

        CCAA_radioBoxChoices = sd.ccaa()
        self.CCAA_radioBox = wx.RadioBox(self, wx.ID_ANY, u"Comunidades Autónomas",
                                         wx.DefaultPosition, wx.DefaultSize, CCAA_radioBoxChoices, 1, wx.RA_SPECIFY_COLS)
        self.CCAA_radioBox.SetSelection(0)
        gbSizer1.Add(self.CCAA_radioBox, wx.GBPosition(
            0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        dato_radioBoxChoices = sd.cols()
        self.dato_radioBox = wx.RadioBox(self, wx.ID_ANY, u"Dato a mostrar", wx.DefaultPosition,
                                         wx.DefaultSize, dato_radioBoxChoices, 1, wx.RA_SPECIFY_COLS)
        self.dato_radioBox.SetSelection(0)
        gbSizer1.Add(self.dato_radioBox, wx.GBPosition(
            0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        gbSizer1.AddGrowableCol(0)

        self.SetSizer(gbSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        self.img = Image.open("virus.png", 'r')
        self.CCAA_radioBox.Bind(wx.EVT_RADIOBOX, self.updateIcon)
        self.dato_radioBox.Bind(wx.EVT_RADIOBOX, self.updateIcon)

    def updateIcon(self, event):
        frame = self
        img = self.img

        CCAA = frame.CCAA_radioBox.GetSelection()
        dato = frame.dato_radioBox.GetStringSelection()
        back = (0, 0, 0, 128)
        border = (255, 255, 255, 128)

        data = Image.new('RGBA', img.size, color=(0, 0, 0, 0))
        fnt = ImageFont.truetype('ImpactCondensed.ttf', 100)
        d = ImageDraw.Draw(data)
        d.rectangle([(0, 150), (256, 256)], fill=back, outline=border, width=5)
        d.text((5, 150), str(int(sd.gimme(CCAA, dato))), font=fnt, fill='white')
        img = Image.alpha_composite(img, data)
        img.save('ico.png')

        frame.SetIcon(wx.Icon('ico.png', wx.BITMAP_TYPE_PNG, -1, -1))

    def start(self):
        self.SetIcon(wx.Icon('virus.png', wx.BITMAP_TYPE_PNG, -1, -1))
        self.Show()

    def __del__(self):
        pass


class CoronaIcon (wx.App):

    def __init__(self):
        super().__init__()
        self.frame = CoronaTracker(None)

    def start(self):
        self.frame.start()
        self.MainLoop()

    def updateIcon(self):
        self.frame.updateIcon()


app = CoronaIcon()

@tm.job(interval=timedelta(hours=1))
def reload():
    sd.update()
    app.updateIcon()

def main():
    tm.start(False)
    app.start()
    tm.stop()


if __name__ == '__main__':
    main()
