import apace.ScenariosClasses as Cls
import apace.VisualizeScenarios as Vis
import covid19.Support as Sup

Cls.POLY_DEGREES = 2
scenarioDfFixed = Cls.ScenarioDataFrame(csv_file_name='csv_files/PolicyEvals/PolicyEvalFixed.csv')
scenarioDfPeriodic = Cls.ScenarioDataFrame(csv_file_name='csv_files/PolicyEvals/PolicyEvalPeriodic.csv')

policy_definitions = Sup.PolicyDefinitions()

# series to display on the cost-effectiveness plane
fixed_interval = Cls.SetOfScenarios(name='Predetermined Duration',
                                    scenario_df=scenarioDfFixed,
                                    color='blue',
                                    marker='o',
                                    conditions_on_variables=policy_definitions.FixedIntervalVarConditions,
                                    if_find_frontier=False,
                                    if_show_fitted_curve=True,
                                    labels_shift_x=-0.025,
                                    labels_shift_y=0.02)

periodic = Cls.SetOfScenarios(name='Periodic',
                              scenario_df=scenarioDfPeriodic,
                              color='red',
                              marker='D',
                              #x_y_labels=['O', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'G', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'S', 'R', 'T'],
                              conditions_on_variables=policy_definitions.PeriodicInfVarConditions,
                              conditions_on_outcomes=policy_definitions.PeriodicInfOutcomeConditions,
                              if_find_frontier=False,
                              if_show_fitted_curve=False,
                              labels_shift_x=0.02,
                              labels_shift_y=0)

Vis.plot_sets_of_scenarios(list_of_scenario_sets=[fixed_interval, periodic],
                           x_range=[0, 10],
                           y_range=[0, 1000],
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

#names = [s.name for s in periodic.CEA.get_strategies_on_frontier()]
names = [s.name for s in periodic.CEA.strategies]

for name in names:
    print(name)
    mean_interval = scenario_df.get_mean_interval(
        scenario_name=name,
        outcome_name='Number of Switches')
    print('# of switches:', mean_interval)
    mean_interval = scenario_df.get_mean_interval(
        scenario_name=name,
        outcome_name='Average ratio: % Death While Waiting for ICU')
    print('% death while waiting for ICU', mean_interval)