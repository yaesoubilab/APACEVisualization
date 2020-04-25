import SimPy.InOutFunctions as IO
from covid19 import Support as Support


R_On = [1, 2]
R_Off = [0.2, 1]
I = [0.01, 0.05]
N = 3

RPolicies = Support.generate_policies(R_On, R_Off, N)
IPolicies = Support.generate_policies(I, I, N)

RIPolicies = []
for R in RPolicies:
    for I in IPolicies:
        RI = R.copy()
        RI.extend(I)
        RIPolicies.append(RI)

IO.write_csv(rows=RIPolicies,
             file_name='../csv_files/PoliciesRtI.csv')
