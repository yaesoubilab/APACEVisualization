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

# read parameter samples
parameter_values = IO.read_csv_cols_to_dictionary(
    file_name='csv_files/SampledParams.csv',
    delimiter=',',
    if_convert_float=True)

# create a dictionaries of DALYs and cost
dict_DALY = {}
dict_cost = {}
for key in scenario_keys:
    dict_DALY[key] = scenario_df.scenarios[key].outcomes['DALY']
    dict_cost[key] = scenario_df.scenarios[key].outcomes['Total Cost']

# create dictionaries for dDALYS and dCost
dict_dDALY = {}
dict_dCost = {}
for key in scenario_keys:
    if key != 'Base':
        dict_dDALY[key] = scenario_df.scenarios['Base'].outcomes['DALY'] \
                          - scenario_df.scenarios[key].outcomes['DALY']
        dict_dCost[key] = scenario_df.scenarios[key].outcomes['Total Cost'] \
                          - scenario_df.scenarios['Base'].outcomes['Total Cost']

# do DALY
fit = SA.ParameterSA(
    dic_parameter_values=parameter_values,
    dic_output_values=dict_DALY
)

fit.export_to_csv(file_name_linear_fit='results/sensitivity_analysis/LinearFit-DALY.csv',
                  file_name_prcc='results/sensitivity_analysis/PRCC-DALY.csv',
                  max_p_value=0.1)

# do cost
fit = SA.ParameterSA(
    dic_parameter_values=parameter_values,
    dic_output_values=dict_cost
)

fit.export_to_csv(file_name_linear_fit='results/sensitivity_analysis/LinearFit-Cost.csv',
                  file_name_prcc='results/sensitivity_analysis/PRCC-Cost.csv',
                  max_p_value=0.1)

# do dDALY
fit = SA.ParameterSA(
    dic_parameter_values=parameter_values,
    dic_output_values=dict_dDALY
)

fit.export_to_csv(file_name_linear_fit='results/sensitivity_analysis/LinearFit-dDALY.csv',
                  file_name_prcc='results/sensitivity_analysis/PRCC-dDALY.csv',
                  max_p_value=0.1)

# do dCost
fit = SA.ParameterSA(
    dic_parameter_values=parameter_values,
    dic_output_values=dict_dCost
)

fit.export_to_csv(file_name_linear_fit='results/sensitivity_analysis/LinearFit-dCost.csv',
                  file_name_prcc='results/sensitivity_analysis/PRCC-dCost.csv',
                  max_p_value=0.1)
