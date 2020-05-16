""" UI Module """
import sys
import os
import webbrowser
import logging
import wx
from wx import adv
from wx.adv import TaskBarIcon
from wx.adv import NotificationMessage


import utils
from updater import Updater
from report import HtmlReport
from settings import Settings



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
        icon_path = None
        updating_path = None
        icon_path = utils.get_resource_path(os.path.join('res', 'icon', 'icon_white.png'))
        updating_path = utils.get_resource_path(os.path.join('res', 'icon', 'updating.png'))


        self.system_icon = wx.Icon(icon_path, wx.BITMAP_TYPE_PNG)
        self.updating_icon = wx.Icon(updating_path, wx.BITMAP_TYPE_PNG)
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

    def show_menu(self, _event):
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


    def show_settings(self, _event):
        # SettingsFrame(self)
        if sys.platform == "win32":
            os.startfile(self.settings._get_sttings_path())
    # end


    def show_report(self, _event):
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


    def cancel_update(self, _event):
        raise KeyboardInterrupt
    # end

    def exit_app(self, _event):
        """ exit app """
        logging.info("close vcs_lite")
        self.RemoveIcon()
        self.Destroy()
        sys.exit('exit')
    # end
# end



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



class UpdateFrame(wx.Frame):
    """ dummy frame for the application """

    def __init__(self, parent, _id, title):

        wx.Frame.__init__(self, parent, -1, title, size=(1, 1),
                          style=wx.FRAME_NO_TASKBAR | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.tb_icon = SystemTray(self)


        self.tb_icon.Bind(wx.EVT_MENU, self.exit_app, id=wx.ID_EXIT)
        self.settings = Settings()
        self.report_filename = 'report.html'

        logging.error("init UpdateFrame and show it")
        # self.Show(True)
    # end

    def show_settings(self, event):
        # SettingsFrame(self)
        # if sys.platform == "win32":
        #     os.startfile(self.settings._get_sttings_path())
        pass

    # end


    def show_report(self, _event):
        report_file = 'file:///' + self.settings.settings_dir + '\\' + self.report_filename
        webbrowser.open_new_tab(report_file)

    # end

    def update_repos(self, event):
        """ update all confiured repos  """
        self.tb_icon.set_icon(True)
        self.tb_icon.disable_update_entry(True)


        updater = Updater()
        # check if settings could be laoded
        loaded_settings = self.settings.load_settings()

        if not loaded_settings:
            wx.MessageBox("couldn't load settings", "Error", wx.OK | wx.ICON_ERROR)

        update_list = loaded_settings['toUpdate']
        report = {
            'repos': []
        }
        try:
            for repo in update_list:
                try:
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
                except KeyError as ke:
                    # wx.MessageBox("couldn't update  '{}' cause of typo in {} porperty".format(repo['label'], ke))
                    repo = {
                        'label': repo['label'],
                        'path': repo['folder'],
                        'status': 'warning',
                        'message': ["couldn't update  '{}' cause of typo in {} porperty".format(repo['label'], ke)]
                    }
                    report['repos'].append(repo)
                # end
            # end
        except KeyboardInterrupt:
            pass
        finally:
            self.tb_icon.disable_update_entry(False)
            self.tb_icon.set_icon(False)
            if self.tb_icon.IsIconInstalled:
                notify  = NotificationMessage(title="update finished",
                                              message="all repos are updated",
                                              parent=self,
                                              flags=wx.ICON_INFORMATION)
                notify.Show(timeout=1)
                notify.Close()
                # self.tb_icon.ShowBalloon("updated", "all repos are updated", 500)
            # end
        # end
        html_report = HtmlReport(report)



        with open(self.settings.settings_dir + '\\' + self.report_filename, 'w') as report_file:
            report_file.write(html_report.get_html_report())

        self.show_report(event)

        # input('Debug') # for debug use
        # sys.exit(0)
    # end


    def cancel_update(self, _event):
        raise KeyboardInterrupt
    # end

    def exit_app(self, _event):
        """ exit app """
        self.tb_icon.RemoveIcon()
        self.tb_icon.Destroy()
        sys.exit('exit')
    # end
# end
