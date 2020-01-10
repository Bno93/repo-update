""" UI Module """
import sys
# import os
import webbrowser
import wx
import logging
from ui import SystemTray
# from ui import SettingsFrame
from setting import Settings
from updater import Updater
from report import HtmlReport

class UpdateFrame(wx.Frame):
    """ dummy frame for the application """

    def __init__(self, parent, id, title):

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
        #os.startfile(self.settings._get_sttings_path())
        pass
    # end


    def show_report(self, event):
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
            self.tb_icon.disable_update_entry(False)
            self.tb_icon.set_icon(False)
            if self.tb_icon.IsIconInstalled:
                self.tb_icon.ShowBalloon("updated", "all repos are updated", 500)
            # end
        # end
        html_report = HtmlReport(report)



        with open(self.settings.settings_dir + '\\' + self.report_filename, 'w') as report_file:
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
        self.tb_icon.RemoveIcon()
        self.tb_icon.Destroy()
        sys.exit('exit')
    # end
# end
