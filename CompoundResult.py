#!/usr/bin/env python

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
        results.insert(0, pointer)
        while pointer.has_parent():
            pointer = pointer.parent
            results.insert(0, pointer)
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


###### Not user friendly / results would get too big for excel
# def generate_compound_possibilities(initial_amount, periods, min_rate, max_rate):
#     base = [CompoundResult(parent=None, annual_return=None, months=None, monthly_deposit=0, initial_amount=initial_amount)]
#     results = []
#     for p in periods:
#         for res in base:
#             for r in range(min_rate, max_rate+1):
#                 results.append(CompoundResult(parent=res, annual_return=r, months=p.months, monthly_deposit=p.monthly_deposit))
#         base = results
#         if p != periods[-1]:
#             results = []
#
#     for res in results:
#         compound_results = res.get_compound_results()
#         row = str(compound_results[0].result)
#         for i in range(1, len(compound_results)):
#             row = row + f" --{compound_results[i].annual_return}--> {compound_results[i].result}"
#         print(row)


def generate_compound_row(initial_amount, periods, avg_return):
    last_compound_result = CompoundResult(parent=None, annual_return=None, months=None, monthly_deposit=0, initial_amount=initial_amount)
    for p in periods:
        last_compound_result = CompoundResult(parent=last_compound_result, annual_return=avg_return, months=p.months, monthly_deposit=p.monthly_deposit)
    results = last_compound_result.get_compound_results()

    row = []
    for res in results:
        row.append(f"{res.result} ({res.annual_return})")
    print(row)


# testing the code:
test_periods = [Period(months=24, monthly_deposit=1250), Period(months=50, monthly_deposit=1000), Period(months=75), Period(months=75), Period(months=75)]
for avg_return in range(26):
    generate_compound_row(20000, test_periods, avg_return)

# print("goal amount printed for every month:")
# goal_monthly = []
# for period in test_periods:
#     temp_periods = period.return_monthly_periods()
#     for month in temp_periods:
#         goal_monthly.append(month)
# generate_compound_possibilities(test_initial_amount, goal_monthly, test_min_rate, test_max_rate)
