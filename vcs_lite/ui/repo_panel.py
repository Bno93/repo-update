""" UI Module """
import wx

class RepoPanel(wx.Panel):
    """ Object which represents a Repo Configuration of the Settings JSON file """

    def __init__(self, parent, repo):
        super(RepoPanel, self).__init__(parent, wx.ID_ANY, wx.DefaultPosition,
                                        wx.DefaultSize, wx.SIMPLE_BORDER, wx.PanelNameStr)
        self.repo = repo
        self.setup()
    # end



    def setup(self):
        """ handels the creation of all ui elements on this panel """
        grid_bag = wx.GridBagSizer(0, 0)

        lbl_name = wx.StaticText(self, label='Name:', style=wx.ALIGN_LEFT)
        grid_bag.Add(lbl_name, pos=(0, 0), flag=wx.ALL)

        txc_name = wx.TextCtrl(self, value=self.repo['label'])
        grid_bag.Add(txc_name, pos=(0, 1), span=(1, 2), flag=wx.ALL)

        lbl_folder = wx.StaticText(self, label='Folder:', style=wx.ALIGN_LEFT)
        grid_bag.Add(lbl_folder, pos=(1, 0), flag=wx.ALL)

        txc_folder = wx.TextCtrl(self, value=self.repo['folder'])
        grid_bag.Add(txc_folder, pos=(1, 1), flag=wx.ALL)

        lbl_vsc = wx.StaticText(self, label='VCS:', style=wx.ALIGN_LEFT)
        grid_bag.Add(lbl_vsc, pos=(2, 0), flag=wx.ALL)

        cbx_vcs = wx.ComboBox(self, value=self.repo['vcs']['program'], choices=['git', 'svn'])
        grid_bag.Add(cbx_vcs, pos=(2, 1), flag=wx.ALL)

        lbl_cmd = wx.StaticText(self, label='Command:', style=wx.ALIGN_LEFT)
        grid_bag.Add(lbl_cmd, pos=(3, 0), flag=wx.ALL)

        txc_cmd = wx.TextCtrl(self, value=self.repo['vcs']['command'])
        grid_bag.Add(txc_cmd, pos=(3, 1), flag=wx.ALL)

        lbl_enabled = wx.StaticText(self, label='Enabeld:', style=wx.ALIGN_LEFT)
        grid_bag.Add(lbl_enabled, pos=(4, 0), flag=wx.ALL)

        ckb_enabled = wx.CheckBox(self)
        ckb_enabled.SetValue(self.repo['enabled'])
        grid_bag.Add(ckb_enabled, pos=(4, 1), flag=wx.ALL)

        self.SetSizer(grid_bag)

    # end
# end
