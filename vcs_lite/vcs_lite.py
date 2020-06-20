""" main Script"""

import sys
import logging
import wx

from gui import SystemTray
from cli import Cli


class Gui(wx.App):

    def OnInit(self):
        frame = wx.Frame(None) # UpdateFrame(None, -1, '')
        self.SetTopWindow(frame)
        SystemTray(frame)
        return True
    # end
# end

def main():
    """ Main Function """
    app = Gui(False)
    app.MainLoop()
# end

def cli():
    _cli = Cli()
    _cli.execute()
# end

if __name__ == '__main__':
    # setupt logging
    logging.basicConfig(filename="vcs-lite.log",
                        level=logging.INFO,
                        format='[%(asctime)s] %(levelname)s - %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S')

    if len(sys.argv) > 1:
        cli()
    else:
        main()
# end
