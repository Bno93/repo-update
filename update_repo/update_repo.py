import sys

import webbrowser
import time

from setting import Settings
from updater import Updater
from report import HtmlReport
from pprint import pprint



# TODO
# update status adequat feststellen und 
# SystemTray Ui fuer Windows https://stackoverflow.com/questions/9494739/how-to-build-a-systemtray-app-for-windows


def main():
    """ Main Function """

    settings = Settings()
    updater = Updater()

    loaded_settings = settings.load_settings()

    updateList = loaded_settings['toUpdate']
    report = {
        'repos': []
    }
    try:
        for repo in updateList:
            if(repo['enabled']):
                vcs = repo['vcs']
                result = updater.update(repo['label'],
                    repo['folder'], vcs, loaded_settings['execpath'])
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
    # end
    html_report = HtmlReport(report)

    report_filename = 'report.html'

    with open(settings.settings_dir + '\\' + report_filename, 'w') as report_file:
        report_file.write(html_report.get_html_report())
    # end
    report_file = 'file:///' + settings.settings_dir + '\\' + report_filename
    webbrowser.open_new_tab(report_file)
    # input('Debug') # for debug use
    sys.exit(0)

# end


if __name__ == '__main__':
  main()
# end
