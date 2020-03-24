""" UI Module """
import sys
import os
import webbrowser
import logging
import wx
from wx import adv
from wx.adv import TaskBarIcon

from util import utils
from updater import Updater
from report import HtmlReport
from setting import Settings



UPDATE_ALL = wx.NewId()
SHOW_REPORT = wx.NewId()
SETTINGS = wx.NewId()



class SystemTray(TaskBarIcon):
    """ SystemTray impl. for the app """
    def __init__(self, parent):
        self.parent_app = parent
        super(SystemTray, self).__init__()
        # vcs_lite/res/icon/icon_white.png
        self.report_filename = 'report.html'
        # icon_path = utils.get_resource_path(os.path.join('vcs_lite','res','icon','icon_white.png'))
        icon_path = utils.get_resource_path(os.path.join('res','icon','icon_white.png'))
        # updating_path = utils.get_resource_path(os.path.join('vcs_lite','res','icon','updating.png'))
        updating_path = utils.get_resource_path(os.path.join('res','icon','updating.png'))
        self.system_icon = wx.Icon(icon_path, wx.BITMAP_TYPE_PNG)
        self.updating_icon = wx.Icon(updating_path, wx.BITMAP_TYPE_PNG)
        # self.system_icon = wx.Icon('update_repo\\res\\icon\\icon_white.png', wx.BITMAP_TYPE_PNG)
        self.settings = Settings()
        self.set_icon()
        self.create_menu()
    # end


    def create_menu(self):
        """ make context menu """
        self.Bind(adv.EVT_TASKBAR_RIGHT_DOWN, self.show_menu)
        self.Bind(wx.EVT_MENU, self.update_repos, id=UPDATE_ALL)
        self.Bind(wx.EVT_MENU, self.show_report, id=SHOW_REPORT)
        self.Bind(wx.EVT_MENU, self.show_settings, id=SETTINGS)
        self.Bind(wx.EVT_MENU, self.exit_app, id=wx.ID_EXIT)
        self.menu = wx.Menu()
        self.menu.Append(UPDATE_ALL, "Update alle Repos")
        self.menu.Append(SHOW_REPORT, "Show last Report")
        self.menu.Append(SETTINGS, "Settings")
        self.menu.Append(wx.ID_EXIT, "Exit")
    # end

    def show_menu(self, event):
        """ makes context menu visible """
        self.PopupMenu(self.menu)
    # end

    def disable_update_entry(self, disable=False):
        update_menu_item = self.menu.FindItemById(UPDATE_ALL)
        if update_menu_item:
            update_menu_item.Enable(not disable)

    def set_icon(self, is_loading=False):

        if(is_loading):
            self.SetIcon(self.updating_icon, "updating")
        else:
            self.SetIcon(self.system_icon, "vcs-lite")
    # end


    def show_settings(self, event):
        # SettingsFrame(self)
        os.startfile(self.settings._get_sttings_path())
        pass
    # end


    def show_report(self, event):
        report_file = 'file:///' + os.path.join(self.settings.settings_dir, self.report_filename)
        webbrowser.open_new_tab(report_file)

    # end

    def update_repos(self, event):
        """ update all confiured repos  """
        self.set_icon(True)
        self.disable_update_entry(True)


        updater = Updater()
        # check if settings could be laoded
        loaded_settings = self.settings.load_settings()

        if(not loaded_settings):
            wx.MessageBox("couldn't load settings", "Error", wx.OK | wx.ICON_ERROR)

        update_list = loaded_settings['toUpdate']
        report = {
            'repos': []
        }
        try:
            for repo in update_list:
                if repo['enabled']:
                    vcs = repo['vcs']
                    result = updater.update(repo['label'],
                                            repo['folder'], vcs)
                    report['repos'].append(result)
                else:
                    repo = {
                        'label': repo['label'],
                        'path': repo['folder'],
                        'status': 'disabled',
                        'message': ["repo not enabled to update"]
                    }
                    report['repos'].append(repo)
                # end
            # end
        except KeyboardInterrupt:
            pass
        finally:
            self.disable_update_entry(False)
            self.set_icon(False)
            if self.IsIconInstalled:
                self.ShowBalloon("updated", "all repos are updated", 500)
            # end
        # end
        html_report = HtmlReport(report)


        report_path = os.path.join(self.settings.settings_dir, self.report_filename)
        with open(report_path, 'w') as report_file:
            report_file.write(html_report.get_html_report())

        self.show_report(event)

        # input('Debug') # for debug use
        # sys.exit(0)
    # end


    def cancel_update(self, event):
        raise KeyboardInterrupt
    # end

    def exit_app(self, event):
        """ exit app """
        logging.info("close vcs_lite")
        self.RemoveIcon()
        self.Destroy()
        sys.exit('exit')
    # end
# end
