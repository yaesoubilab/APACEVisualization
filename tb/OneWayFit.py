import SimPy.SensitivityAnalysis as SA
import SimPy.InOutFunctions as IO
from apace import ScenariosClasses as Sce

scenario_keys = ['Base',
                 '75% PTFU | No >1 FU | Drop % | No IPT',
                 '75% PTFU | With >1 FU | Drop 15% | No IPT',
                 '75% PTFU | No >1 FU | Drop % | With IPT',
                 '75% PTFU | With >1 FU | Drop 15% | With IPT']

# data frame for scenario analysis
scenario_df = Sce.ScenarioDataFrame('csv_files\TBScenarios.csv')

# create a dictionary of DALYs and cost
dict_DALY = {}
dict_cost = {}
for key in scenario_keys:
    dict_DALY[key] = scenario_df.scenarios[key].outcomes['DALY']
    dict_cost[key] = scenario_df.scenarios[key].outcomes['Total Cost']

# read parameter samples
parameter_values = IO.read_csv_cols_to_dictionary(
    file_name='csv_files/SampledParams.csv',
    delimiter=',',
    if_convert_float=True)

# do DALY
fit = SA.LinearFit(
    dic_parameter_values=parameter_values,
    dic_output_values=dict_DALY
)

fit.export_to_csv(file_name='results/LinearFit-DALY.csv',
                  max_p_value=0.1)

# do cost
fit = SA.LinearFit(
    dic_parameter_values=parameter_values,
    dic_output_values=dict_cost
)

fit.export_to_csv(file_name='results/LinearFit-Cost.csv',
                  max_p_value=0.1)
