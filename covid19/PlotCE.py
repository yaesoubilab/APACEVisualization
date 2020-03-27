import apace.ScenariosClasses as Cls
import apace.VisualizeScenarios as Vis
import covid19.Support as Sup


scenario_df = Cls.ScenarioDataFrame(csv_file_name='covid19/Policies.csv')

policy_definitions = Sup.PolicyDefinitions()

# series to display on the cost-effectiveness plane
fixed_interval = Cls.SetOfScenarios(name='Fixed',
                                    scenario_df=scenario_df,
                                    color='blue',
                                    marker='o',
                                    conditions=policy_definitions.VarFixedInterval,
                                    if_find_frontier=False,
                                    labels_shift_x=-0.8 / 8,
                                    labels_shift_y=2 / 80)

adaptive = Cls.SetOfScenarios(name='Adaptive',
                              scenario_df=scenario_df,
                              color='red',
                              marker='D',
                              conditions=policy_definitions.VarAdaptive,
                              if_find_frontier=False,
                              labels_shift_x=0.1 / 8,
                              labels_shift_y=-4 / 80)

Vis.plot_sets_of_scenarios(list_of_scenario_sets=[fixed_interval, adaptive],
                           # x_range=[],
                           # y_range=[],
                           effect_multiplier=1,
                           cost_multiplier=1,
                           switch_cost_effect_on_figure=False,
                           wtp_multiplier=1,
                           labels=['Cost', 'QALY Gained'],
                           title='',
                           fig_size=(3.6, 3.3),
                           l_b_r_t=(0.22, 0.13, 0.9, 0.9),
                           file_name='CE.png')
