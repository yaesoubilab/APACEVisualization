import SimPy.InOutFunctions as IO
from covid19 import Support as Support


R_On = [1, 3]
R_Off = [0.2, 1.5]

N = 10


IO.write_csv(rows=Support.generate_square_policies(R_On, R_Off, N),
             file_name='../csv_files/RtPolicies.csv')
