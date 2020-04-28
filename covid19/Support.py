import apace.ScenariosClasses as Cls
import numpy as np


class PolicyDefinitions:

    def __init__(self, if_spatial=False):

        # conditions of variables to define scenarios to display
        # on each series of cost-effectiveness plane
        self.VarFixedInterval = [
            Cls.VariableCondition('Decision Rule', 0, 0,
                                  if_included_in_label=False),
            Cls.VariableCondition('Duration of Social Distancing', 0, 72, # 200
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
        self.VarPeriodicI = [
            Cls.VariableCondition('Decision Rule', 1, 1,
                                  if_included_in_label=False),
            Cls.VariableCondition('% I Switch threshold if social distancing is off', 0, 1,  # 1, 5
                                  if_included_in_label=False, label_format='{:.5f}'),
            Cls.VariableCondition('% I Switch threshold if social distancing is on', 0, 1,  # 0, 5
                                  if_included_in_label=False, label_format='{:.5f}'),
            # Cls.VariableCondition(' Time of lifting social distancing', 1, 1,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is off',
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is on',
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False)
        ]
        self.VarAdaptiveR = [
            Cls.VariableCondition('Decision Rule', 2, 2,
                                  if_included_in_label=False),
            Cls.VariableCondition('R_t Switch threshold if social distancing is off', 1, 5,
                                  if_included_in_label=False, label_format='{:.1f}'),
            Cls.VariableCondition('R_t Switch threshold if social distancing is on', 0, 5,
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


def generate_policies(t1_range, t2_range, n_of_samples):

    t1_samples = np.linspace(t1_range[0], t1_range[1], n_of_samples)
    t2_samples = np.linspace(t2_range[0], t2_range[1], n_of_samples)

    policies = []
    for t1 in t1_samples:
        for t2 in t2_samples:
            policies.append([t1, t2])

    return policies
