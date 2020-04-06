import apace.ScenariosClasses as Cls


class PolicyDefinitions:

    def __init__(self, if_spatial=False):

        # conditions of variables to define scenarios to display
        # on each series of cost-effectiveness plane
        self.VarFixedInterval = [
            Cls.VariableCondition('Decision Rule (0: fixed, 1: %I, 2: Rt)', 0, 0,
                                  if_included_in_label=False),
            Cls.VariableCondition('Duration of Social Distancing', 0, 24,
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
        self.VarAdaptive = [
            Cls.VariableCondition('Decision Rule (0: fixed, 1: %I, 2: Rt)', 2, 2,
                                  if_included_in_label=False),
            Cls.VariableCondition('R_t Switch threshold if social distancing is off', 0, 5,
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