""" UI Module """
import wx
from wx import adv
from wx.adv import TaskBarIcon
from util import utils



UPDATE_ALL = wx.NewId()
SETTINGS = wx.NewId()


class SystemTray(TaskBarIcon):
    """ SystemTray impl. for the app """
    def __init__(self, parent):
        TaskBarIcon.__init__(self)
        self.parent_app = parent
        icon_path = utils.get_resource_path('res\\icon\\icon_white.png')
        print("Icon path from exe: {}".format(icon_path))
        self.system_icon = wx.Icon(icon_path, wx.BITMAP_TYPE_PNG)
        # self.system_icon = wx.Icon('update_repo\\res\\icon\\icon_white.png', wx.BITMAP_TYPE_PNG)
        self.SetIcon(self.system_icon, "update")
        self.create_menu()
    # end


    def create_menu(self):
        """ make context menu """
        self.Bind(adv.EVT_TASKBAR_RIGHT_UP, self.show_menu)
        self.Bind(wx.EVT_MENU, self.parent_app.update_repos, id=UPDATE_ALL)
        self.Bind(wx.EVT_MENU, self.parent_app.show_settings, id=SETTINGS)
        self.menu = wx.Menu()
        self.menu.Append(UPDATE_ALL, "Update alle Repos")
        self.menu.Append(SETTINGS, "Settings")
        self.menu.Append(wx.ID_EXIT, "exit")
    # end

    def show_menu(self, event):
        """ makes context menu visible """
        self.PopupMenu(self.menu)
    # end
# end
