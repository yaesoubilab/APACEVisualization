import apace.ScenariosClasses as Cls


class PolicyDefinitions:

    def __init__(self, if_spatial=False):

        # conditions of variables to define scenarios to display
        # on each series of cost-effectiveness plane
        self.VarFixedInterval = [
            Cls.VariableCondition('Decision Rule (0: fixed, 1: adaptive)', 0, 0,
                                  if_included_in_label=False),
            # Cls.VariableCondition('Time of starting social distancing', 0.035, 0.065,
            #                       if_included_in_label=True, label_format='{:.1%}'),
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
            Cls.VariableCondition('Decision Rule (0: fixed, 1: adaptive)', 1, 1,
                                  if_included_in_label=False),
            # Cls.VariableCondition('Time of starting social distancing', 0.035, 0.065,
            #                       if_included_in_label=True, label_format='{:.1%}'),
            # Cls.VariableCondition(' Time of lifting social distancing', 1, 1,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is off', 
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False),
            # Cls.VariableCondition('Switch threshold if social distancing is on', 
            #                       DS_TESTS, DS_TESTS,
            #                       if_included_in_label=False)
        ]