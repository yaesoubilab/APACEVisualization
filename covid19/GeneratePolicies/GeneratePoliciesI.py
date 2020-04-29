import SimPy.InOutFunctions as IO
from covid19 import Support as Support


I_on = [30/10000, 40/10000]
I_off = [7.5/10000, 12.5/10000]
N = 10


IO.write_csv(rows=Support.generate_policies(I_on, I_off, N),
             file_name='../csv_files/ThresholdsI.csv')
