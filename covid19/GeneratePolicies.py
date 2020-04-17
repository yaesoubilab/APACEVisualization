import SimPy.InOutFunctions as IO

tTightenRange = [0, 1, 10]
tRelaxRange


THRESHOlDS = [0.03, 0.15]
DELTA_THRESHOlD = 0.005
PERCENTAGE_POINT_CHANGES = 0.005


scenarios = []
i = 1
t = (i-1) * DELTA_THRESHOlD + THRESHOlDS[0]
while t <= THRESHOlDS[1]:
    j = 1
    p = j * PERCENTAGE_POINT_CHANGES
    while p <= 3/4*t:
        scenarios.append([round(t, 5), round(p, 5)])
        j += 1
        p = j*PERCENTAGE_POINT_CHANGES

    i += 1
    t = (i-1) * DELTA_THRESHOlD + THRESHOlDS[0]

IO.write_csv('scenarios.csv', scenarios, ',')