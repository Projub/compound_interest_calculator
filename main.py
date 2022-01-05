import CompoundResult as Cr

periods = [Cr.Period(months=24, monthly_deposit=1250), Cr.Period(months=50, monthly_deposit=1000), Cr.Period(months=75), Cr.Period(months=75), Cr.Period(months=75)]
given_date = '01/09/2020'
Cr.generate_cic_excel(period_list=periods, date_string=given_date)
