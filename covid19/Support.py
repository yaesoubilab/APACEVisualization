import apace.ScenariosClasses as Cls

class PolicyDefinitions:

    def __init__(self, if_spatial=False):

        # conditions of variables to define scenarios to display
        # on each series of cost-effectiveness plane
        self.VarFixedInterval = [
            Cls.VariableCondition('Decision Period', 364, 364,
                                  if_included_in_label=False),
            Cls.VariableCondition('% Resistant Threshold', 0.035, 0.065,
                                  if_included_in_label=True, label_format='{:.1%}'),
            Cls.VariableCondition('Change in % Resistant Threshold', 1, 1,
                                  if_included_in_label=False),
            Cls.VariableCondition('# of Cases Tested for Resistance', DS_TESTS, DS_TESTS,
                                  if_included_in_label=False)
        ]
        self.VarAdaptive = [
            Cls.VariableCondition('Decision Period', 91, 91,
                                  if_included_in_label=False),
            Cls.VariableCondition('% Resistant Threshold', 0.055, 0.1,
                                  if_included_in_label=True, label_format='{:.1%}'),
            Cls.VariableCondition('Change in % Resistant Threshold', 1, 1,
                                  if_included_in_label=False, label_format='{:.1%}'),
            Cls.VariableCondition('# of Cases Tested for Resistance', DS_TESTS/4, DS_TESTS/4,
                                  if_included_in_label=False)
                'Change in Annual Gonorrhea Cases\n(Per 100,000 MSM Population)\n')