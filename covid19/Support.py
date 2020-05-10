import apace.ScenariosClasses as Cls
import numpy as np


class PolicyDefinitions:

    def __init__(self, if_spatial=False):

        # conditions of variables to define scenarios to display
        # on each series of cost-effectiveness plane
        self.FixedIntervalVarConditions = [
            Cls.ConditionOnVariable('Decision Rule', 0, 0,
                                    if_included_in_label=False),
            Cls.ConditionOnVariable('Duration of Social Distancing', 0, 300,  # 200
                                    if_included_in_label=True, label_format='{:.0f}'),
            # Cls.VariableCondition(' Time of lifting social distancing', 1, 1,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is off', 
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is on', 
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False)
        ]
        self.ICUInfVarConditions = [
            Cls.ConditionOnVariable('Decision Rule', 2, 2,
                                    if_included_in_label=False),
            Cls.ConditionOnVariable('% I Switch threshold if social distancing is off', 0, 1000,  # 1, 5
                                    if_included_in_label=False, label_format='{:.0f}'),
            Cls.ConditionOnVariable('% I Switch threshold if social distancing is on', 0, 1000,  # 0, 5
                                    if_included_in_label=False, label_format='{:.0f}'),
            Cls.ConditionOnVariable('WTP', 0, 0,  # 0, 5
                                    if_included_in_label=False, label_format='{:.0f}'),
            # Cls.VariableCondition(' Time of lifting social distancing', 1, 1,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is off',
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is on',
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False)
        ]
        self.ICUInfOutcomeConditions = [
            Cls.ConditionOnOutcome(
                outcome_name='Average ratio: % served in ICU',
                minimum=0.9,
                maximum=1,
                if_included_in_label=False,
                label_format='{:.1f}'),
            Cls.ConditionOnOutcome(
                outcome_name='Number of Switches',
                minimum=0,
                maximum=100,
                if_included_in_label=False,
                label_format='{:.0f}')
        ]

        self.PeriodicVarConditions = [
            Cls.ConditionOnVariable('Decision Rule', 1, 1,
                                    if_included_in_label=False),
            Cls.ConditionOnVariable('Periodicity (weeks)', 2, 8,  # 1, 5
                                    if_included_in_label=True, label_format='{:.0f}'),
            # Cls.VariableCondition(' Time of lifting social distancing', 1, 1,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is off',
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is on',
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False)
        ]
        self.AdaptiveFtVarConditions = [
            Cls.ConditionOnVariable('Decision Rule', 3, 3,
                                    if_included_in_label=False),
            Cls.ConditionOnVariable('WTP', 0, 1.1,  # 1, 5
                                    if_included_in_label=True, label_format='{:.2f}'),
            # Cls.VariableCondition(' Time of lifting social distancing', 1, 1,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is off',
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is on',
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False)
        ]
        self.AdaptiveRVarConditions = [
            Cls.ConditionOnVariable('Decision Rule', 2, 2,
                                    if_included_in_label=False),
            Cls.ConditionOnVariable('R_t Switch threshold if social distancing is off', 1, 5,
                                    if_included_in_label=False, label_format='{:.1f}'),
            Cls.ConditionOnVariable('R_t Switch threshold if social distancing is on', 0, 5,
                                    if_included_in_label=False, label_format='{:.1f}'),
            # Cls.VariableCondition(' Time of lifting social distancing', 1, 1,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is off', 
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is on', 
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False)
        ]


def generate_square_policies(t1_range, t2_range, n_of_samples):

    t1_samples = np.linspace(t1_range[0], t1_range[1], n_of_samples)
    t2_samples = np.linspace(t2_range[0], t2_range[1], n_of_samples)

    policies = []
    for t1 in t1_samples:
        for t2 in t2_samples:
            policies.append([t1, t2])

    return policies


def generate_triangular_scenarios(t1_min, t1_max, n_of_samples):

    t1_samples = np.linspace(t1_min, t1_max, n_of_samples)

    scenarios = []
    for t1 in t1_samples:

        t1_index = 0
        while True:
            t2 = t1_samples[t1_index]
            scenarios.append([t1, t2])

            t1_index += 1
            if t1_index >= len(t1_samples) \
                    or t1_samples[t1_index] > t1:
                break

    return scenarios
