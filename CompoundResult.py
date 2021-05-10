class CompoundResult:
    monthly_returns = [None]*101
    for i in range(101):
        monthly_returns[i] = (1 + (i/100)) ** (1 / float(12))

    def __init__(self, parent, annual_return, months, monthly_deposit, initial_amount=None):
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

    def get_compoundresults(self):
        results = []
        pointer = self
        results.insert(0, pointer)
        while pointer.has_parent():
            pointer = pointer.parent
            results.insert(0, pointer)
        return results


def make_initial_compoundresult(initial_amount):
    return CompoundResult(parent=None, annual_return=None, months=None, monthly_deposit=None, initial_amount=initial_amount)


max_rate = 16

init = make_initial_compoundresult(initial_amount=20000)

period1 = []
for r in range(max_rate):
    period1.append(CompoundResult(parent=init, annual_return=r, monthly_deposit=1250, months=24))

period2 = []
for res in period1:
    for r in range(max_rate):
        period2.append(CompoundResult(parent=res, annual_return=r, monthly_deposit=1000, months=50))

period3 = []
for res in period2:
    for r in range(max_rate):
        period3.append(CompoundResult(parent=res, annual_return=r, monthly_deposit=0, months=75))

period4 = []
for res in period3:
    for r in range(max_rate):
        period4.append(CompoundResult(parent=res, annual_return=r, monthly_deposit=0, months=75))

period5 = []
for res in period4:
    for r in range(max_rate):
        period5.append(CompoundResult(parent=res, annual_return=r, monthly_deposit=0, months=75))

for res in period5:
    compound_results = res.get_compoundresults()
    row = str(compound_results[0].result)
    for i in range(1, len(compound_results)):
        row = row + f" --{compound_results[i].annual_return}--> {compound_results[i].result}"
    print(row)



