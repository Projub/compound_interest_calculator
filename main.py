import os

import wx

import view

# pyinstaller cmd Windows
# pyinstaller.exe --clean --paths "C:\repos\personal_repos\compound_interest_calculator" --windowed --add-data "media;media" --icon=media/cic.ico --onefile -n ci_calc --noconfirm main.py

# pyinstaller cmd Mac
# pyinstaller --clean --paths “/Users/robin/git/compound_interest_calculator” --windowed --add-data "media:media" --icon=media/cic.ico --onefile -n ci_calc --osx-bundle-identifier com.projub.ci_calc --noconfirm main.py

app = wx.App()
frame = view.MainFrame()
frame.SetIcon(wx.Icon(os.path.join(os.path.dirname(__file__), "media/cic.ico")))
app.MainLoop()
