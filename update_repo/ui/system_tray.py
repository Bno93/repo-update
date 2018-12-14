""" UI Module """
import wx
from wx import adv
from wx.adv import TaskBarIcon


UPDATE_ALL = wx.NewId()


class SystemTray(TaskBarIcon):
    """ SystemTray impl. for the app """
    def __init__(self, parent):
        TaskBarIcon.__init__(self)
        self.parent_app = parent
        self.system_icon = wx.Icon('update_repo\\res\\icon\\icon_white.png', wx.BITMAP_TYPE_PNG)
        self.SetIcon(self.system_icon, "update")
        self.create_menu()
    # end

    def create_menu(self):
        """ make context menu """
        self.Bind(adv.EVT_TASKBAR_RIGHT_UP, self.show_menu)
        self.Bind(wx.EVT_MENU, self.parent_app.update_repos, id=UPDATE_ALL)
        self.menu = wx.Menu()
        self.menu.Append(UPDATE_ALL, "Update alle Repos")
        self.menu.Append(wx.ID_EXIT, "exit")
    # end

    def show_menu(self, event):
        self.PopupMenu(self.menu)
    # end
# end
