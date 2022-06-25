import datetime as dt

import wx
import wx.adv
import cfg


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self,
            parent=None,
            title=f"Compound interest calculator {cfg.version}",
        )

        menu_bar = wx.MenuBar()
        self.SetMenuBar(menu_bar)
        help_menu = wx.Menu()
        wiki_item = help_menu.Append(
            wx.NewId(),
            "Explanation page",
            "Open explanation page in the browser",
        )
        # self.Bind(wx.EVT_MENU, open_wiki_page, wiki_item)
        menu_bar.Append(help_menu, "&Help")
        support_menu = wx.Menu()
        donate_item = support_menu.Append(
            wx.NewId(),
            "Donate",
            "Go to donation page",
        )
        # self.Bind(wx.EVT_MENU, open_wiki_page, wiki_item)
        menu_bar.Append(support_menu, "&Support us")

        MainPanel(self)

        self.Show()
        self.Raise()

    def test(self, event):
        print("Donate menu pressed")


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.AddSpacer(10)

        invested_title = wx.StaticText(self, label="Amount already invested:")
        self.invested_txt = wx.TextCtrl(self, value="0")
        invested_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        invested_hsizer.Add(invested_title, 0, wx.ALL | wx.CENTER, 5)
        invested_hsizer.Add(self.invested_txt, 0, wx.ALL, 5)
        main_sizer.Add(invested_hsizer, 0, wx.CENTER)

        date_title = wx.StaticText(self, label="Starting date:")
        main_sizer.Add(date_title, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.CENTER, 5)
        self.date_picker = wx.adv.CalendarCtrl(self)
        main_sizer.Add(self.date_picker, 0, wx.ALL | wx.CENTER, 5)

        date_title = wx.StaticText(self, label="End date:")
        self.date_txt = wx.TextCtrl(self, value=dt.datetime.today().strftime("%Y-%m-%d"))
        self.date_txt.Disable()
        date_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        date_hsizer.Add(date_title, 0, wx.ALL | wx.CENTER, 5)
        date_hsizer.Add(self.date_txt, 0, wx.ALL, 5)
        main_sizer.Add(date_hsizer, 0, wx.CENTER)

        main_sizer.AddSpacer(5)

        self.param_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(self, label="Amount of months:")
        title2 = wx.StaticText(self, label="Monthly investment amount:")
        h_sizer.Add(title, 1, wx.TOP | wx.LEFT | wx.RIGHT, 5)
        h_sizer.Add(title2, 1, wx.TOP | wx.LEFT | wx.RIGHT, 5)
        self.param_sizer.Add(h_sizer, 1, wx.ALL | wx.EXPAND, 0)

        # dict with param textctrl as key and amount_txt textctrl as amount_txtue
        self.textctrl_dict = {}

        # 2 textctrls for a new parameter with amount_txtue
        # dict with months_txt textctrl as key and amount_txt textctrl als amount_txtue
        for i in range(3):
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            months_txt = wx.TextCtrl(self)
            amount_txt = wx.TextCtrl(self)
            self.textctrl_dict[months_txt] = amount_txt
            h_sizer.Add(months_txt, 1, wx.ALL, 5)
            h_sizer.Add(amount_txt, 1, wx.ALL, 5)
            self.param_sizer.Add(h_sizer, 1, wx.ALL | wx.EXPAND, 0)

        main_sizer.Add(self.param_sizer, 0, wx.ALL | wx.CENTER, 0)

        # "+" button to add 2 more textctrls for yet another new parameter with amount_txtue
        self.plus_btn = wx.Button(self, label="+")
        self.plus_btn.Bind(wx.EVT_BUTTON, self.add_months_txt_line)
        main_sizer.Add(self.plus_btn, 0, wx.ALL | wx.CENTER, 5)

        main_sizer.AddSpacer(10)

        calc_button = wx.Button(self, label="Generate Excel")
        calc_button.SetMinSize((self.param_sizer.GetMinSize()[0], -1))
        # save_btn.Bind(wx.EVT_BUTTON, self.push_changes_to_database)
        main_sizer.Add(calc_button, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(main_sizer)

        self.Fit()
        self.parent.Fit()

    def add_months_txt_line(self, evt):
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        months_txt = wx.TextCtrl(self)
        months_txt.MoveBeforeInTabOrder(self.plus_btn)
        amount_txt = wx.TextCtrl(self)
        amount_txt.MoveBeforeInTabOrder(self.plus_btn)
        self.textctrl_dict[months_txt] = amount_txt
        h_sizer.Add(months_txt, 1, wx.ALL, 5)
        h_sizer.Add(amount_txt, 1, wx.ALL, 5)
        self.param_sizer.Add(h_sizer, 1, wx.ALL | wx.EXPAND, 0)

        self.Refresh()
        self.Fit()

        self.parent.Fit()
