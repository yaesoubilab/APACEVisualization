import apace.ScenariosClasses as Cls
import apace.VisualizeScenarios as Vis
import covid19.Support as Sup

Cls.POLY_DEGREES = 2
scenario_df = Cls.ScenarioDataFrame(csv_file_name='csv_files/PolicyEval.csv')

for scenario_name in scenario_df.scenarios:

    if scenario_name[0:3] == 'D:2':

        print(scenario_name)
        cost_mean, cost_CI = scenario_df.get_mean_interval(
            scenario_name=scenario_name,
            outcome_name='Total Cost')
        print(cost_mean, cost_CI)

        utilization_mean, utilization_CI = scenario_df.get_mean_interval(
            scenario_name=scenario_name,
            outcome_name='Utilization (unit of time): Social Distancing')
        print(utilization_mean, utilization_CI)

