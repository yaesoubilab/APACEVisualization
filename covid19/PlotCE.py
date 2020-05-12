import apace.ScenariosClasses as Cls
import apace.VisualizeScenarios as Vis
import covid19.Support as Sup
import SimPy.FormatFunctions as F

SUFX = ''
# SUFX = '4WeekMin'


Cls.POLY_DEGREES = 2
scenarioDfFixedPeriodic = Cls.ScenarioDataFrame(
    csv_file_name='csv_files/PolicyEvals/PolicyEvalsFixedPeriodic{}.csv'.format(SUFX))
scenarioDfAdaptiveIt = Cls.ScenarioDataFrame(
    csv_file_name='csv_files/PolicyEvals/PolicyEvalAdaptiveIt{}.csv'.format(SUFX))

policy_definitions = Sup.PolicyDefinitions()

# series to display on the cost-effectiveness plane
fixed_interval = Cls.SetOfScenarios(name='Predetermined Duration',
                                    scenario_df=scenarioDfFixedPeriodic,
                                    color='blue',
                                    marker='o',
                                    conditions_on_variables=policy_definitions.FixedIntervalVarConditions,
                                    if_find_frontier=False,
                                    if_show_fitted_curve=True,
                                    labels_shift_x=0.01,
                                    labels_shift_y=0.01)

periodic = Cls.SetOfScenarios(name='Periodic',
                              scenario_df=scenarioDfFixedPeriodic,
                              color='purple',
                              marker='s',
                              #x_y_labels=['O', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'G', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'S', 'R', 'T'],
                              conditions_on_variables=policy_definitions.PeriodicVarConditions,
                              if_find_frontier=False,
                              if_show_fitted_curve=True,
                              labels_shift_x=-0.04,
                              labels_shift_y=0.01)

icuBased = Cls.SetOfScenarios(name='Adaptive to maximize ICU service rate',
                              scenario_df=scenarioDfFixedPeriodic,
                              color='red',
                              marker='D',
                              #x_y_labels=['O', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'G', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'S', 'R', 'T'],
                              conditions_on_variables=policy_definitions.ICUInfVarConditions,
                              conditions_on_outcomes=policy_definitions.ICUInfOutcomeConditions,
                              if_find_frontier=False,
                              if_show_fitted_curve=True,
                              reg_type='exponential',
                              labels_shift_x=-0.1,
                              labels_shift_y=0.02)

adaptiveIt = Cls.SetOfScenarios(name='Adaptive to minimize loss in NMB',
                                scenario_df=scenarioDfAdaptiveIt,
                                color='green',
                                marker='s',
                                x_y_labels=['O', 'A', 'B', 'C', 'D', '', '', '', 'E', '', '', '', '', '', '', 'O', 'P', 'Q', 'S', 'R', 'T'],
                                conditions_on_variables=policy_definitions.AdaptiveItVarConditions,
                                if_find_frontier=False,
                                if_show_fitted_curve=True,
                                reg_type='exponential',
                                labels_shift_x=0.02,
                                labels_shift_y=-0.02)


Vis.plot_sets_of_scenarios(list_of_scenario_sets=[fixed_interval, periodic, icuBased, adaptiveIt],
                           x_range=[0, 1500],
                           y_range=[0, 450],
                           effect_multiplier=1,
                           cost_multiplier=1,
                           switch_cost_effect_on_figure=False,
                           wtp_multiplier=1,
                           labels=['Death due to COVID-19 averted\n(per 100,000 population)',
                                   'Expected number of weeks with\ntightened social distancing'],
                           title='',
                           fig_size=(4.6, 4),  # (3.6, 3.2),
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

    print('% served in ICU')
    for name in names:
        mean_interval = scenario_df.get_mean_interval(
            scenario_name=name,
            outcome_name='Average ratio: % served in ICU')
        print('  ', name, ':', F.format_number(mean_interval[0], deci=1, format='%'))


print()
print('\n------- PERIODIC I ---------------')
print_switch_icu_info(icuBased, scenarioDfFixedPeriodic)
print('\n------- ADAPTIVE I ---------------')
# print_switch_icu_info(adaptiveI, scenarioDfAdaptiveI)