import SimPy.InOutFunctions as IO
from covid19 import Support as Support


R_On = [1, 3]
R_Off = [0.3, 1]
I = [100, 500]
N = 3

RPolicies = Support.generate_square_policies(R_On, R_Off, N)
IPolicies = Support.generate_square_policies(I, I, N)

RIPolicies = []
for R in RPolicies:
    for I in IPolicies:
        RI = R.copy()
        RI.extend(I)
        RIPolicies.append(RI)

IO.write_csv(rows=RIPolicies,
             file_name='../csv_files/ThresholdsRtI.csv')
