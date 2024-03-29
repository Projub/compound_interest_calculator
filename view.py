import getpass
import os
import platform
import sys
import webbrowser

import wx
import wx.adv

import cfg
import compound_interest as ci


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self,
            parent=None,
            title=f"Compound interest calculator {cfg.version}",
            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER  # no resize borders
        )

        menu_bar = wx.MenuBar()
        self.SetMenuBar(menu_bar)
        menu = wx.Menu()
        explanation_item = menu.Append(
            wx.NewId(),
            "Explanation page",
            "",
        )
        self.Bind(wx.EVT_MENU, self.open_ci_calc_page, explanation_item)
        support_us_item = menu.Append(
            wx.NewId(),
            "Support us",
            "",
        )
        self.Bind(wx.EVT_MENU, self.open_support_us_page, support_us_item)
        copyrights_item = menu.Append(
            wx.NewId(),
            "Copyright",
            "",
        )
        self.Bind(wx.EVT_MENU, self.show_copyright_notice, copyrights_item)
        menu_bar.Append(menu, "&Menu")

        MainPanel(self)

        self.Fit()
        self.Show()
        self.EnableMaximizeButton(False)  # disables fullscreen
        self.Centre()
        self.Raise()

    def open_ci_calc_page(self, event):
        webbrowser.open("https://projub.com/compound_interest_calculator")

    def open_support_us_page(self, event):
        webbrowser.open("https://projub.com/support_us")

    def show_copyright_notice(self, event):
        wx.MessageBox("MIT License\n"
                      "Copyright © 2022 Robin Boone\n\n"
                      "pandas package:\n"
                      "Copyright © 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData "
                      "Development Team All rights reserved. Copyright (c) 2011-2021, Open source contributors.\n"
                      "xlsxwriter package:\n"
                      "Copyright © 2013-2022, John McNamara jmcnamara@cpan.org",
                      "Copyright notice",
                      wx.ICON_INFORMATION)


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.AddSpacer(10)
        invested_title = wx.StaticText(self, label="Amount already invested:")
        self.invested_txt = wx.TextCtrl(self)
        self.invested_txt.SetBackgroundColour(wx.Colour(255, 223, 200))
        self.invested_txt.Bind(wx.EVT_TEXT, self.number_field_changed)
        invested_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        invested_hsizer.Add(invested_title, 0, wx.ALL | wx.CENTER, 5)
        invested_hsizer.Add(self.invested_txt, 0, wx.ALL, 5)
        main_sizer.Add(invested_hsizer, 0, wx.CENTER)
        main_sizer.AddSpacer(10)

        date_title = wx.StaticText(self, label="Starting date:")
        main_sizer.Add(date_title, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.CENTER, 5)
        # TODO Tabbing gets stuck in the CalendarCtrl
        self.date_picker = wx.adv.CalendarCtrl(self)
        main_sizer.Add(self.date_picker, 0, wx.ALL | wx.CENTER, 5)
        date_title = wx.StaticText(self, label="Calculating until:")
        self.end_date_txt = wx.TextCtrl(self, value=wx.DateTime.Today().Format("%Y-%m"))
        self.end_date_txt.Disable()
        date_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        date_hsizer.Add(date_title, 0, wx.ALL | wx.CENTER, 5)
        date_hsizer.Add(self.end_date_txt, 0, wx.ALL, 5)
        main_sizer.Add(date_hsizer, 0, wx.CENTER)
        main_sizer.AddSpacer(10)

        self.param_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(self, label="Amount of months:")
        title2 = wx.StaticText(self, label="Monthly investment amount:")
        h_sizer.Add(title, 1, wx.TOP | wx.LEFT | wx.RIGHT | wx.CENTER, 5)
        h_sizer.Add(title2, 1, wx.TOP | wx.LEFT | wx.RIGHT | wx.CENTER, 5)
        self.param_sizer.Add(h_sizer, 1, wx.ALL | wx.EXPAND, 0)

        # dict with param textctrl as key and amount_txt textctrl as amount_txtue
        self.textctrl_dict = {}

        # 2 textctrls for a new parameter with amount_txtue
        # dict with months_txt textctrl as key and amount_txt textctrl als amount_txtue
        for i in range(3):
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            months_txt = wx.TextCtrl(self)
            months_txt.SetBackgroundColour(wx.Colour(255, 223, 200))
            months_txt.Bind(wx.EVT_TEXT, self.month_field_changed)
            amount_txt = wx.TextCtrl(self)
            amount_txt.SetBackgroundColour(wx.Colour(255, 223, 200))
            amount_txt.Bind(wx.EVT_TEXT, self.number_field_changed)
            self.textctrl_dict[months_txt] = amount_txt
            h_sizer.Add(months_txt, 1, wx.BOTTOM | wx.LEFT | wx.RIGHT, 5)
            h_sizer.Add(amount_txt, 1, wx.BOTTOM | wx.LEFT | wx.RIGHT, 5)
            self.param_sizer.Add(h_sizer, 1, wx.ALL | wx.EXPAND, 0)
        side_padding = 30  # general side padding is done here !
        main_sizer.Add(self.param_sizer, 0, wx.LEFT | wx.RIGHT | wx.CENTER, side_padding)

        # "+" button to add 2 more textctrls for yet another new parameter with amount_txtue
        self.plus_btn = wx.Button(self, label="+")
        self.plus_btn.Bind(wx.EVT_BUTTON, self.add_months_txt_row)
        main_sizer.Add(self.plus_btn, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.AddSpacer(10)

        dir_label = wx.StaticText(self, label="Save directory:")
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            if platform.system() == "Darwin":  # Mac can use cache folders etc.
                application_path = os.path.join(os.environ["HOME"], "Desktop")
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        self.dir_picker = wx.DirPickerCtrl(self,
                                           path=application_path,
                                           message="Please choose where to save the generated excel")
        self.dir_picker.SetMinSize((self.param_sizer.GetMinSize()[0], -1))
        self.dir_picker.GetChildren()[0].SetBackgroundColour(wx.Colour(255, 223, 200))
        dir_label.SetMinSize((self.dir_picker.GetMinSize()[0], -1))
        main_sizer.Add(dir_label, 0, wx.LEFT | wx.RIGHT | wx.CENTER, side_padding)
        main_sizer.Add(self.dir_picker, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.CENTER, 5)
        main_sizer.AddSpacer(20)

        calc_button = wx.Button(self, label="Generate Excel")
        calc_button.SetMinSize((self.param_sizer.GetMinSize()[0], -1))
        calc_button.Bind(wx.EVT_BUTTON, self.generate_compound_interest_excel)
        main_sizer.Add(calc_button, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.AddSpacer(10)

        self.SetSizer(main_sizer)

        self.Fit()

    def add_months_txt_row(self, evt):
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        months_txt = wx.TextCtrl(self)
        months_txt.MoveBeforeInTabOrder(self.plus_btn)
        months_txt.SetBackgroundColour(wx.Colour(255, 223, 200))
        months_txt.Bind(wx.EVT_TEXT, self.month_field_changed)
        amount_txt = wx.TextCtrl(self)
        amount_txt.SetBackgroundColour(wx.Colour(255, 223, 200))
        amount_txt.MoveBeforeInTabOrder(self.plus_btn)
        amount_txt.Bind(wx.EVT_TEXT, self.number_field_changed)
        self.textctrl_dict[months_txt] = amount_txt
        h_sizer.Add(months_txt, 1, wx.BOTTOM | wx.LEFT | wx.RIGHT, 5)
        h_sizer.Add(amount_txt, 1, wx.BOTTOM | wx.LEFT | wx.RIGHT, 5)
        self.param_sizer.Add(h_sizer, 1, wx.ALL | wx.EXPAND, 0)

        self.Fit()
        self.parent.Fit()

    def number_field_changed(self, event):
        txt = event.GetEventObject()
        val = txt.GetValue()
        if val != "":
            try:
                # allow whitespaces
                float("".join(val.split()))
            except ValueError:
                txt.SetValue(val[:-1])
                txt.SetInsertionPointEnd()

    def month_field_changed(self, event):
        # force round number
        txt = event.GetEventObject()
        val = txt.GetValue()
        if val != "":
            try:
                # allow whitespaces
                int("".join(val.split()))
            except ValueError:
                txt.SetValue(val[:-1])
                txt.SetInsertionPointEnd()

        # update end_date_txt
        months = self.get_total_months()
        picked_date = self.date_picker.GetDate()
        end_date = picked_date.Add(wx.DateSpan(months=months))
        self.end_date_txt.SetValue(end_date.Format("%Y-%m"))

    def get_total_months(self):
        """Calculate total amount of months."""
        months = 0
        for month_txt in self.textctrl_dict.keys():
            val = month_txt.GetValue()
            if val != "":
                months += float(val)
        return months

    def generate_compound_interest_excel(self, evt):
        # parameters
        path = self.dir_picker.GetPath()
        if not os.path.exists(path):
            wx.MessageBox("Save Directory doesn't exist",
                          "Can't generate",
                          style=wx.ICON_WARNING)
        else:
            start_date = self.date_picker.GetDate().Format("%Y/%m/%d")
            portfolio_worth = self.invested_txt.GetValue()
            if portfolio_worth != "":
                portfolio_worth = float("".join(portfolio_worth.split()))  # ignore whitespaces + cast to float
            else:
                portfolio_worth = 0
            periods = []
            for month_txt in self.textctrl_dict.keys():
                months = month_txt.GetValue()
                if months != "":  # no point doing anything if 0 months
                    months = int("".join(months.split()))  # ignore whitespaces + cast to int
                    monthly_deposit = self.textctrl_dict[month_txt].GetValue()
                    if monthly_deposit != "":
                        monthly_deposit = float("".join(monthly_deposit.split()))  # ignore whitespaces + cast to float
                    else:
                        monthly_deposit = 0
                    if months > 0:
                        periods.append(
                            ci.Period(
                                months=months,
                                monthly_deposit=monthly_deposit
                            )
                        )

            # progress bar
            progress_bar = wx.ProgressDialog(title="Generating possibilities...",
                                             message="Generating possibilities, then saving them into an excel file.",
                                             maximum=100)
            progress_bar.Pulse()

            # calculate
            ci.generate_cic_excel(period_list=periods, start_date=start_date, start_portfolio=portfolio_worth,
                                  path=path)
