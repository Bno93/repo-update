""" UI Module """
import sys
import webbrowser
import wx
from ui import SystemTray
from ui import SettingsFrame
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
        self.Show(True)
    # end

    def show_settings(self, event):
        SettingsFrame(self)
    # end

    def update_repos(self, event):
        """ update all confiured repos  """
        self.tb_icon.set_icon(True)
        self.tb_icon.disable_update_entry(True)
        if self.tb_icon.IsIconInstalled:
            self.tb_icon.ShowBalloon("updating", "updating repos", 500)
        # end
        settings = Settings()
        updater = Updater()

        loaded_settings = settings.load_settings()

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
        # end
        html_report = HtmlReport(report)

        report_filename = 'report.html'

        with open(settings.settings_dir + '\\' + report_filename, 'w') as report_file:
            report_file.write(html_report.get_html_report())
        # html_report = HtmlReport(report)
        report_file = 'file:///' + settings.settings_dir + '\\' + report_filename
        webbrowser.open_new_tab(report_file)
        # input('Debug') # for debug use
        # sys.exit(0)
    # end

    def exit_app(self, event):
        """ exit app """
        self.tb_icon.RemoveIcon()
        self.tb_icon.Destroy()
        sys.exit('exit')
    # end
# end
