import SimPy.InOutFunctions as IO
from covid19 import Support as Support


ICU_CAPACITY = 0.89/10000*2
MAX_I = 0.1

# MAX = 30 * ICU_CAPACITY
# MIN = 0
MAX = MAX_I/5
MIN = 0.0005
N = 20

IO.write_csv(rows=Support.generate_triangular_scenarios(MIN, MAX, N),
             file_name='../csv_files/ICUPolicies.csv')
