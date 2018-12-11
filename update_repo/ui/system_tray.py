import sys
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
        self.Bind(adv.EVT_TASKBAR_RIGHT_UP, self.show_menu)
        self.Bind(wx.EVT_MENU, self.parent_app.print_something, id=UPDATE_ALL)
        self.menu = wx.Menu()
        self.menu.Append(UPDATE_ALL, "Update alle Repos")
        self.menu.Append(wx.ID_EXIT, "exit")

    # end

    def show_menu(self, event):
        self.PopupMenu(self.menu)
    # end
# end


class UpdateFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size=(1,1),
                          style=wx.FRAME_NO_TASKBAR | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.tb_icon = SystemTray(self)

        self.tb_icon.Bind(wx.EVT_MENU, self.exit_app, id=wx.ID_EXIT)
        self.Show(True)
    # end

    def print_something(self, event):
        print("something with: " + event)

    def exit_app(self, event):
        print("exit app")
        self.tb_icon.RemoveIcon()
        self.tb_icon.Destroy()
        sys.exit(0)
# end
