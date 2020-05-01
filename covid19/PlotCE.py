import apace.ScenariosClasses as Cls
import apace.VisualizeScenarios as Vis
import covid19.Support as Sup
import SimPy.FormatFunctions as F

SUFX = '4WeekMin'

Cls.POLY_DEGREES = 2
scenarioDfFixedPeriodic = Cls.ScenarioDataFrame(
    csv_file_name='csv_files/PolicyEvals/PolicyEvalsFixedPeriodic{}.csv'.format(SUFX))
scenarioDfAdaptiveI = Cls.ScenarioDataFrame(
    csv_file_name='csv_files/PolicyEvals/PolicyEvalAdaptiveI{}.csv'.format(SUFX))

policy_definitions = Sup.PolicyDefinitions()

# series to display on the cost-effectiveness plane
fixed_interval = Cls.SetOfScenarios(name='Predetermined Duration',
                                    scenario_df=scenarioDfFixedPeriodic,
                                    color='blue',
                                    marker='o',
                                    conditions_on_variables=policy_definitions.FixedIntervalVarConditions,
                                    if_find_frontier=False,
                                    if_show_fitted_curve=True,
                                    labels_shift_x=-0.025,
                                    labels_shift_y=0.02)

periodic = Cls.SetOfScenarios(name='Periodic',
                              scenario_df=scenarioDfFixedPeriodic,
                              color='red',
                              marker='D',
                              #x_y_labels=['O', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'G', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'S', 'R', 'T'],
                              conditions_on_variables=policy_definitions.PeriodicInfVarConditions,
                              conditions_on_outcomes=policy_definitions.PeriodicInfOutcomeConditions,
                              if_find_frontier=False,
                              if_show_fitted_curve=False,
                              labels_shift_x=0.02,
                              labels_shift_y=0)

adaptiveI = Cls.SetOfScenarios(name='Adaptive',
                               scenario_df=scenarioDfAdaptiveI,
                               color='green',
                               marker='s',
                               #x_y_labels=['O', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'G', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'S', 'R', 'T'],
                               conditions_on_variables=policy_definitions.AdaptiveIVarConditions,
                               # conditions_on_outcomes=policy_definitions.PeriodicInfOutcomeConditions,
                               if_find_frontier=False,
                               if_show_fitted_curve=True,
                               labels_shift_x=0.02,
                               labels_shift_y=0)


Vis.plot_sets_of_scenarios(list_of_scenario_sets=[fixed_interval, periodic, adaptiveI],
                           x_range=[0, 8],
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
                           file_name='figures/CE{}.png'.format(SUFX))

#names = [s.name for s in periodic.CEA.get_strategies_on_frontier()]


def print_switch_icu_info(scenarios, scenario_df):

    names = [s.name for s in scenarios.CEA.strategies]
    print('Utilization')
    for name in names:
        mean_interval = scenario_df.get_mean_interval(
            scenario_name=name,
            outcome_name='Utilization (unit of time): Social Distancing')
        print('  ', name, ':', F.format_number(mean_interval[0], deci=1))

    print('# of switches')
    for name in names:
        mean_interval = scenario_df.get_mean_interval(
            scenario_name=name,
            outcome_name='Number of Switches')
        print('  ', name, ':', F.format_number(mean_interval[0], deci=1))

    print('% death while waiting for ICU')
    for name in names:
        mean_interval = scenario_df.get_mean_interval(
            scenario_name=name,
            outcome_name='Average ratio: % Death While Waiting for ICU')
        print('  ', name, ':', F.format_number(mean_interval[0], deci=1, format='%'))


print()
print('\n------- PERIODIC I ---------------')
print_switch_icu_info(periodic, scenarioDfFixedPeriodic)
print('\n------- ADAPTIVE I ---------------')
print_switch_icu_info(adaptiveI, scenarioDfAdaptiveI)