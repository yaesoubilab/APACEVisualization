from apace import ScenariosClasses as Sce

# data frame for scenario analysis
scenario_df = Sce.ScenarioDataFrame('csvfiles\GonoEffectiveLife.csv')

for key, outcome in scenario_df.scenarios.items():
    a = scenario_df.get_mean_interval(
        scenario_name=key,
        outcome_name='Average ratio: Effective life of AB',
        deci=1, form='%')
    print(key, ' ... ', a)

