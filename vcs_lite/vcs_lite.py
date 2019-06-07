""" main Script"""

import wx
import logging
from ui import UpdateFrame

# TODO
# update status adequat feststellen und

def main():
    """ Main Function """
    app = wx.App(False)
    frame = UpdateFrame(None, -1, '')
    frame.Show(False)
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
