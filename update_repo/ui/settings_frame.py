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

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        test_text = wx.StaticText(panel, -1, style=wx.ALIGN_CENTER)
        box.Add(test_text, 0, wx.ALIGN_LEFT)
        panel.SetSizer(box)
        self.Show(True)
    # end


    def _init_frame(self, repos):
        for repo in repos:
            vcs = repo["vcs"]
            is_endabled = repo["enabled"]
            folder = repo["folder"]
            label = repo["label"]

        # end
    # end

# end
