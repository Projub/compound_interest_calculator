import os

import view
import wx

# pyinstaller.exe --clean --paths "C:\repos\personal_repos\compound_interest_calculator" --windowed --add-data "media;media" --icon=media/cic.ico --onefile -n ci_calc --noconfirm main.py

# import CompoundResult as Cr
#
# # My personal schedule:
# start_date = '01/09/2020'
# start_portfolio = 20000
# periods = [Cr.Period(months=24, monthly_deposit=1250), Cr.Period(months=50, monthly_deposit=1000), Cr.Period(months=75), Cr.Period(months=75), Cr.Period(months=75)]
# Cr.generate_cic_excel(period_list=periods, start_date=start_date, start_portfolio=start_portfolio)


app = wx.App()
frame = view.MainFrame()
frame.SetIcon(wx.Icon(os.path.join(os.path.dirname(__file__), "media/cic.ico")))
app.MainLoop()
