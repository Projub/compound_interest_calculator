import datetime

import numpy as np
import pandas as pd
import datetime as dt


class CompoundResult:
    monthly_returns = [None]*101
    for i in range(101):
        monthly_returns[i] = (1 + (i/100)) ** (1 / float(12))

    def __init__(self, parent, annual_return, months, monthly_deposit=0, initial_amount=None):
        self.parent = parent
        self.annual_return = annual_return
        self.months = months
        self.monthly_deposit = monthly_deposit
        if initial_amount:
            self.result = initial_amount
        else:
            temp_result = parent.result
            monthly_return = CompoundResult.monthly_returns[annual_return]
            for m in range(months):
                # TODO think about multiplying first, then adding deposit after
                temp_result = (temp_result + monthly_deposit) * monthly_return
            self.result = int(temp_result)

    def has_parent(self):
        return self.parent is not None

    def get_compound_results(self):
        results = []
        pointer = self
        results.insert(0, pointer.result)
        while pointer.has_parent():
            pointer = pointer.parent
            results.insert(0, pointer.result)
        return results


class Period:
    def __init__(self, months, monthly_deposit=0):
        self.months = months
        self.monthly_deposit = monthly_deposit

    def return_monthly_periods(self):
        months = []
        for m in range(self.months):
            months.append(Period(months=1, monthly_deposit=self.monthly_deposit))
        return months


# Not used: user friendly / results would get too big for excel file
def generate_compound_possibilities(initial_amount, periods, min_rate, max_rate):
    base = [CompoundResult(parent=None, annual_return=None, months=None, monthly_deposit=0, initial_amount=initial_amount)]
    results = []
    for p in periods:
        for res in base:
            for r in range(min_rate, max_rate+1):
                results.append(CompoundResult(parent=res, annual_return=r, months=p.months, monthly_deposit=p.monthly_deposit))
        base = results
        if p != periods[-1]:
            results = []

    for res in results:
        compound_results = res.get_compound_results()
        row = str(compound_results[0].result)
        for i in range(1, len(compound_results)):
            row = row + f" --{compound_results[i].annual_return}--> {compound_results[i].result}"
        print(row)


def generate_compound_result_array(initial_amount, periods, avg_return):
    last_compound_result = CompoundResult(parent=None, annual_return=None, months=None, monthly_deposit=0, initial_amount=initial_amount)
    for p in periods:
        last_compound_result = CompoundResult(parent=last_compound_result, annual_return=avg_return, months=p.months, monthly_deposit=p.monthly_deposit)
    results = last_compound_result.get_compound_results()
    # row = []
    # for res in results:
    #     row.append(f"{res.result} ({res.annual_return})")
    # print(row)
    return results


# testing the code:
periods = [Period(months=24, monthly_deposit=1250), Period(months=50, monthly_deposit=1000), Period(months=75), Period(months=75), Period(months=75)]
periods_months = []
given_date = '01/09/2020'
date = dt.datetime.strptime(given_date, '%d/%m/%Y')
dates = [date]
for p in periods:
    periods_months = periods_months + p.return_monthly_periods()
for m in periods_months:
    date = date + pd.DateOffset(months=1)
    dates.append(date)
periods = []
for date in dates:
    periods.append(date.strftime('%Y-%m'))

df = pd.DataFrame([], columns=periods)

yoy_returns = range(26)
for ret in yoy_returns:
    df = df.append(pd.DataFrame([generate_compound_result_array(20000, periods_months, ret)], columns=periods))
yoy_return_strings = []
for yoy in yoy_returns:
    yoy_return_strings.append(f'{yoy}%')
df.insert(loc=0, column='avg_yoy', value=yoy_return_strings)

print(df)

# TODO: excel sheet with period info (first) / period info in excel name

file_name = 'CIC'
today = dt.date.strftime(dt.date.today(), '%d_%m_%Y')
excel_path = f"excels/{file_name}.xlsx"
writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')

sheet_name = 'possibilities'
df.to_excel(writer, sheet_name=sheet_name, index=False)  # send df to writer
worksheet = writer.sheets[sheet_name]  # pull worksheet object
for idx, col in enumerate(df):  # loop through all columns
    series = df[col]
    max_len = max((
        series.astype(str).map(len).max(),  # len of largest item
        len(str(series.name))  # len of column name/header
    )) + 2  # adding extra space
    worksheet.set_column(idx, idx, max_len)  # set column width

df = pd.DataFrame()
df.insert(loc=0, column='avg_yoy(%)', value=range(101))
avg_monthly_returns = []
for ret in CompoundResult.monthly_returns:
    avg_monthly_returns.append(round((ret-1)*100, 3))
df.insert(loc=1, column='avg_mom(%)', value=avg_monthly_returns)
sheet_name = 'yoy_mom'
df.to_excel(writer, sheet_name=sheet_name, index=False)  # send df to writer
worksheet = writer.sheets[sheet_name]  # pull worksheet object
for idx, col in enumerate(df):  # loop through all columns
    series = df[col]
    max_len = max((
        series.astype(str).map(len).max(),  # len of largest item
        len(str(series.name))  # len of column name/header
    )) + 2  # adding extra space
    worksheet.set_column(idx, idx, max_len)  # set column width

writer.save()

# print("goal amount printed for every month:")
# goal_monthly = []
# for period in test_periods:
#     temp_periods = period.return_monthly_periods()
#     for month in temp_periods:
#         goal_monthly.append(month)
# generate_compound_possibilities(test_initial_amount, goal_monthly, test_min_rate, test_max_rate)
