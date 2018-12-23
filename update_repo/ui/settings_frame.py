""" UI Module """

import wx
from setting import Settings
class SettingsFrame(wx.Frame):
    """ Settings frame """
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Settings", size=(300, 400))
        self.settings = Settings()
        properties = self.settings.load_settings()
        repos = properties['toUpdate']


        self.Show(True)
    # end


# end
