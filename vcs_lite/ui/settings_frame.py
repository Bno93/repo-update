""" UI Module """

import wx
from setting import Settings
from ui import RepoPanel


class SettingsFrame(wx.Frame):
    """ Settings frame """
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Settings", size=(300, 400))
        self.settings = Settings()
        properties = self.settings.load_settings()
        repos = properties['toUpdate']

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        self._init_frame(repos, panel, box)

        panel.SetSizer(box)
        self.Show(True)
    # end


    def _init_frame(self, repos, parent, sizer):
        for repo in repos:
            sizer.Add(RepoPanel(parent, repo))
        # end
    # end
# end
