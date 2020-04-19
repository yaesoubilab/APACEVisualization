import apace.ScenariosClasses as Cls
import apace.VisualizeScenarios as Vis
import covid19.Support as Sup

Cls.POLY_DEGREES = 2
scenario_df = Cls.ScenarioDataFrame(csv_file_name='csv_files/PolicyEval.csv')

policy_definitions = Sup.PolicyDefinitions()

# series to display on the cost-effectiveness plane
fixed_interval = Cls.SetOfScenarios(name='Predetermined Duration',
                                    scenario_df=scenario_df,
                                    color='blue',
                                    marker='o',
                                    conditions=policy_definitions.VarFixedInterval,
                                    if_find_frontier=False,
                                    if_show_fitted_curve=True,
                                    labels_shift_x=-0.06,
                                    labels_shift_y=2 / 80)

adaptive = Cls.SetOfScenarios(name='Adaptive (ICU)',
                              scenario_df=scenario_df,
                              color='red',
                              marker='D',
                              #x_y_labels=['O', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'G', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'S', 'R', 'T'],
                              conditions=policy_definitions.VarAdaptiveICU,
                              if_find_frontier=True,
                              if_show_fitted_curve=False,
                              labels_shift_x=0.1 / 8,
                              labels_shift_y=-4 / 80)

Vis.plot_sets_of_scenarios(list_of_scenario_sets=[fixed_interval, adaptive],
                           x_range=[0, 70],
                           y_range=[0, 700],
                           effect_multiplier=1/1000,
                           cost_multiplier=1/10e6,
                           switch_cost_effect_on_figure=False,
                           wtp_multiplier=10e6/1000,
                           labels=['QALYs Gained (Thousand)',
                                   'Additional Cost (Million Dollars)'],
                           title='',
                           fig_size=(6, 5.2), # (3.6, 3.2),
                           l_b_r_t=(0.22, 0.13, 0.9, 0.9),
                           file_name='figures/CE.png')

names = [s.name for s in adaptive.CEA.get_strategies_on_frontier()]
print(names)

for name in names:
    mean_interval = scenario_df.get_mean_interval(
        scenario_name=name,
        outcome_name='Number of Switches')
    print(mean_interval)