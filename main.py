import CompoundResult as Cr

start_date = '01/09/2020'
start_portfolio = 20000
periods = [Cr.Period(months=24, monthly_deposit=1250), Cr.Period(months=50, monthly_deposit=1000), Cr.Period(months=75), Cr.Period(months=75), Cr.Period(months=75)]

Cr.generate_cic_excel(period_list=periods, start_date=start_date, start_portfolio=start_portfolio)
