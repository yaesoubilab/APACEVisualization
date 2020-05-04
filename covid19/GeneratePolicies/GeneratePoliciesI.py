import SimPy.InOutFunctions as IO
from covid19 import Support as Support


I_on = [100, 200]   # 150, 75
I_off = [50, 100]
N = 3


IO.write_csv(rows=Support.generate_square_policies(I_on, I_off, N),
             file_name='../csv_files/ThresholdsI.csv')


# I = [10/10000, 60/10000]
# IO.write_csv(rows=Support.generate_triangular_scenarios(I[0], I[1], N),
#              file_name='../csv_files/ThresholdsI.csv')
