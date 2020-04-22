import SimPy.InOutFunctions as IO
from covid19 import Support as Support


Incidence = [50, 14000]
DeltaIncidence = [10, 3000]

N = 10


IO.write_csv(rows=Support.generate_policies(Incidence, DeltaIncidence, N),
             file_name='../csv_files/IncidencePolicies.csv')
