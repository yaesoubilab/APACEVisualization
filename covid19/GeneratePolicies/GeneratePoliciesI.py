import SimPy.InOutFunctions as IO
from covid19 import Support as Support


I_on = [300, 400]   # 150, 75
I_off = [75, 125]
N = 3


IO.write_csv(rows=Support.generate_square_policies(I_on, I_off, N),
             file_name='../csv_files/ThresholdsI.csv')


# I = [10/10000, 60/10000]
# IO.write_csv(rows=Support.generate_triangular_scenarios(I[0], I[1], N),
#              file_name='../csv_files/ThresholdsI.csv')
