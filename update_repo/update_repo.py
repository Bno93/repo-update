""" main Script"""

import wx

from ui import UpdateFrame

# TODO
# update status adequat feststellen und

def main():
    """ Main Function """
    print("show app")
    app = wx.App(False)
    frame = UpdateFrame(None, -1, '')
    frame.Show(False)
    app.MainLoop()
# end



if __name__ == '__main__':
    main()
# end
