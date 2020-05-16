""" main Script"""

import logging
import wx
from gui import SystemTray


class App(wx.App):

    def OnInit(self):
        frame = wx.Frame(None) # UpdateFrame(None, -1, '')
        self.SetTopWindow(frame)
        SystemTray(frame)
        return True
    # end
# end

def main():
    """ Main Function """
    app = App(False)
    app.MainLoop()
# end


if __name__ == '__main__':
    # setupt logging
    logging.basicConfig(filename="vcs-lite.log",
                        level=logging.INFO,
                        format='[%(asctime)s] %(levelname)s - %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S')

    main()
# end
