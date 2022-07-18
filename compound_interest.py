import os
import sys

import pandas as pd
import datetime as dt


class CompoundResult:
    """A CompoundResult instance points to the CompoundResult that preceded itself (self.parent). This way it can use
    it's parent's result to calculate it's own result.

    The class variable monthly_returns can be used to quickly get
    the mom equivalent for a certain yoy return (e.g. monthly_returns[10] ** 12 == 1.10)"""

    monthly_returns = [None]*101
    for i in range(101):
        monthly_returns[i] = (1 + (i/100)) ** (1 / float(12))
    # example use: monthly_returns[10] returns the month-over-month that results in a 10% year-over-year return

    def __init__(self, parent, annual_return, months, monthly_deposit=0, initial_amount=None):
        self.parent = parent
        self.annual_return = annual_return
        self.months = months
        self.monthly_deposit = monthly_deposit
        if self.parent is not None:
            monthly_return = CompoundResult.monthly_returns[annual_return]
            temp_result = parent.result
            for m in range(months):
                temp_result = (temp_result + monthly_deposit) * monthly_return
            self.result = int(temp_result)
        elif initial_amount:  # First CompoundResult in a chain
            self.result = initial_amount
        else:
            raise Exception("CompoundResult constructor without a parent and no initial_amount was given!")

    def has_parent(self):
        return self.parent is not None

    def get_compound_results(self):
        """Return a list of all results (floats) in the order they were calculated, to reach this CompoundResult."""
        results = []
        pointer = self
        results.insert(0, pointer.result)
        while pointer.has_parent():
            pointer = pointer.parent
            results.insert(0, pointer.result)
        return results


class Period:
    """A Period contains a certain amount of months and how much is invested each month during this time."""
    def __init__(self, months, monthly_deposit=0):
        self.months = months
        self.monthly_deposit = monthly_deposit

    def return_monthly_periods(self):
        """Split up a Period into a list of periods of 1 month + return this list."""
        months = []
        for m in range(self.months):
            months.append(Period(months=1, monthly_deposit=self.monthly_deposit))
        return months


def generate_compound_result_array(initial_amount, periods, avg_return):
    """creates CompoundResults based on given parameters. Once the last one is created, returns a list of results (
    floats)."""
    last_compound_result = CompoundResult(parent=None, annual_return=avg_return, months=None, monthly_deposit=0, initial_amount=initial_amount)
    for p in periods:
        last_compound_result = CompoundResult(parent=last_compound_result, annual_return=avg_return, months=p.months, monthly_deposit=p.monthly_deposit)
    results = last_compound_result.get_compound_results()

    return results


def generate_cic_excel(period_list, start_date, start_portfolio, path=None):
    """Generate a user friendly excel file containing the results of CompoundResult calculations for given periods,
    start-date and current portfolio worth"""
    # path + filename
    if not path:
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)
        path = os.path.join(application_path, "temp")
        if not os.path.exists(path):
            os.makedirs(path)
    file_name = "ci_possibilities"
    excel_path = os.path.join(path, f"{file_name}.xlsx")
    # adjust filename suffix if name already exists:
    orig_path = excel_path
    counter = 1
    while os.path.exists(excel_path):
        counter += 1
        excel_path = os.path.splitext(orig_path)[0] + f" ({counter}).xlsx"
    writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')

    # First sheet is an overview of the periods chosen and their dates
    sheet_name = 'periods'
    df = pd.DataFrame()
    period_indices = range(1, len(period_list)+1)
    df.insert(loc=0, column='period', value=pd.Series(period_indices))
    dates = [dt.datetime.strptime(start_date, '%Y/%m/%d')]  # start date in dates list
    for p in period_list:
        # add new date that is last date + # of months
        dates.append(dates[-1] + pd.DateOffset(months=p.months))
    month_strings = []  # readable format
    for d in dates:
        month_strings.append(dt.date.strftime(d, '%Y-%m'))
    df.insert(loc=1, column='start', value=pd.Series(month_strings[:-1]))  # last date is not a start date
    df.insert(loc=2, column='end', value=pd.Series(month_strings[1:]))  # first date is not an end-date
    monthly_deposits = []
    for p in period_list:
        monthly_deposits.append(p.monthly_deposit)
    df.insert(loc=3, column='monthly deposit', value=pd.Series(monthly_deposits))
    df.to_excel(writer, sheet_name=sheet_name, index=False)  # send df to writer
    # Excel layout
    worksheet = writer.sheets[sheet_name]  # pull worksheet object
    adjust_excelsheet_column_widths(dataframe=df, worksheet=worksheet)

    # Second sheet contains yoy returns as rows + months as columns and all possibilities calculated for period
    #  sequence on the first sheet
    sheet_name = 'possibilities'
    periods_months = []  # 1m periods
    date = dt.datetime.strptime(start_date, '%Y/%m/%d')
    dates = [date]
    # split up all Periods into 1m Periods
    for p in period_list:
        periods_months = periods_months + p.return_monthly_periods()
    for m in periods_months:
        date = date + pd.DateOffset(months=1)
        dates.append(date)
    year_months = []  # column titles
    for date in dates:
        year_months.append(date.strftime('%Y-%m'))
    # nested list rows containing possibilities
    rows = []
    yoy_returns = range(41)  # calculating 40 rows: 0 -> 40 yoy
    for ret in yoy_returns:
        rows.append(generate_compound_result_array(start_portfolio, periods_months, ret))
    df = pd.DataFrame(rows, columns=year_months)
    # Insert first column with year-on-year returns
    yoy_return_strings = []
    for yoy in yoy_returns:
        yoy_return_strings.append(f'{yoy}%')
    df.insert(loc=0, column='avg_yoy', value=pd.Series(yoy_return_strings))
    df.to_excel(writer, sheet_name=sheet_name, index=False)  # send df to writer
    # Excel layout
    worksheet = writer.sheets[sheet_name]  # pull worksheet object
    adjust_excelsheet_column_widths(dataframe=df, worksheet=worksheet)
    # freeze first row (months) and first column (percentages)
    worksheet.freeze_panes(1, 1)

    # Third sheet contains the mom return equivalents for yoy returns from 0 - 100%
    sheet_name = 'yoy_mom'
    df = pd.DataFrame()
    df.insert(loc=0, column='avg_yoy(%)', value=pd.Series(range(101)))
    avg_monthly_returns = []
    for ret in CompoundResult.monthly_returns:
        avg_monthly_returns.append(round((ret-1)*100, 3))
    df.insert(loc=1, column='avg_mom(%)', value=pd.Series(avg_monthly_returns))
    df.to_excel(writer, sheet_name=sheet_name, index=False)  # send df to writer
    # Excel layout
    worksheet = writer.sheets[sheet_name]  # pull worksheet object
    adjust_excelsheet_column_widths(dataframe=df, worksheet=worksheet)

    writer.save()


def adjust_excelsheet_column_widths(dataframe, worksheet):
    """Adjusts excel worksheet column widths dynamically depending on item for readability."""
    for idx, col in enumerate(dataframe):  # loop through all columns
        series = dataframe[col]
        max_len = max((
            series.astype(str).map(len).max(),  # len of largest item
            len(str(series.name))  # len of column name/header
        )) + 2  # adding extra space

        if max_len > 13:  # excel uses scientific notation from 1e11 onwards.
            max_len = 13

        worksheet.set_column(idx, idx, max_len)  # set column width
