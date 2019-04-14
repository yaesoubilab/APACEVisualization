import apace.ScenariosClasses as Cls

INDX = 0
SHOW_FEASIBLE_RANGES = False
X_RANGE = (-100, 100)
Y_RANGE = (-0.5, 0.5)

# file names for scenario analysis
SA_FILE_NAMES = ['csvfiles\SABasePolicies.csv',
                 'csvfiles\SAPolicyA.csv',
                 'csvfiles\SA50YrCalibNoise.csv',
                 'csvfiles\SADebug.csv']

# file names for parameter analysis
POSTERIOR_FILE_NAMES \
    = ['csvfiles\ParamSamples50YrCalib.csv',
       'csvfiles\ParamSamples10YrCalib.csv',
       '']

# file names for calibration
CALIB_FILE_NAMES \
    = ['csvfiles\Trajs50YrCalib.csv',
       '',
       'csvfiles\Trajs.csv']

SELECTED_POSTERIOR_FILE_NAME = POSTERIOR_FILE_NAMES[INDX]
SELECTED_SA_FILE_NAME = SA_FILE_NAMES[INDX]
SELECTED_CALIB_FILE_NAME = CALIB_FILE_NAMES[INDX]

# -------------------------------------------------------
# ------------------ Defining Scenarios -----------------
# -------------------------------------------------------

DS_TESTS = 5000  # annual number of cases tested for drug-resistance

# conditions of variables to define scenarios to display on each series of cost-effectiveness plane
varBase = [
    Cls.VariableCondition('Decision Period', 364, 364,
                          if_included_in_label=False),
    Cls.VariableCondition('% Resistant Threshold', 0.035, 0.065,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 1, 1,
                          if_included_in_label=False),
    Cls.VariableCondition('# of Cases Tested for Resistance', DS_TESTS, DS_TESTS,
                          if_included_in_label=False)
]
varBaseQuart = [
    Cls.VariableCondition('Decision Period', 91, 91,
                          if_included_in_label=False),
    Cls.VariableCondition('% Resistant Threshold', 0.07, 0.105,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 1, 1,
                          if_included_in_label=False, label_format='{:.1%}'),
    Cls.VariableCondition('# of Cases Tested for Resistance', DS_TESTS/4, DS_TESTS/4,
                          if_included_in_label=False)
]
varBaseEnhancedTesting = [
    Cls.VariableCondition('Decision Period', 364, 364,
                          if_included_in_label=False),
    Cls.VariableCondition('% Resistant Threshold', 0.01, 0.1,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 1, 1,
                          if_included_in_label=False),
    Cls.VariableCondition('# of Cases Tested for Resistance', 2*DS_TESTS, 2*DS_TESTS,
                          if_included_in_label=False)
]
varBaseQuartEnhancedTesting = [
    Cls.VariableCondition('Decision Period', 91, 91,
                          if_included_in_label=False),
    Cls.VariableCondition('% Resistant Threshold', 0.03, 0.5,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 1, 1,
                          if_included_in_label=False, label_format='{:.1%}'),
    Cls.VariableCondition('# of Cases Tested for Resistance', DS_TESTS/2, DS_TESTS/2,
                          if_included_in_label=False)
]
varDual = [
    Cls.VariableCondition('Decision Period', 364, 364,
                          if_included_in_label=False),
    Cls.VariableCondition('% Resistant Threshold', 0.01, 0.13,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 0, 0.1,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('# of Cases Tested for Resistance', DS_TESTS, DS_TESTS,
                          if_included_in_label=False)
]
varDualQuarterly = [
    Cls.VariableCondition('Decision Period', 91, 91,
                          if_included_in_label=False),
    Cls.VariableCondition('% Resistant Threshold', 0.01, 0.5,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 0, 0.2,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('# of Cases Tested for Resistance', DS_TESTS/4, DS_TESTS/4,
                          if_included_in_label=False)
]
varDualQuarterlyEnhanced = [
    Cls.VariableCondition('Decision Period', 91, 91,
                          if_included_in_label=False),
    Cls.VariableCondition('% Resistant Threshold', 0.01, 0.13,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 0, 0.2,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('# of Cases Tested for Resistance', DS_TESTS, DS_TESTS,
                          if_included_in_label=False)
]

# read scenarios data frames
dfBase = Cls.ScenarioDataFrame(csv_file_name='csvfiles\SABasePolicies.csv')
dfPolicyA = Cls.ScenarioDataFrame(csv_file_name='csvfiles\SADual.csv')
dfPolicyAQuart = Cls.ScenarioDataFrame(csv_file_name='csvfiles\SADualQuart.csv')
dfPolicyAQuartEnhanced = Cls.ScenarioDataFrame(csv_file_name='csvfiles\SADualQuartEnhanced.csv')

# series to display on the cost-effectiveness plane
base = Cls.SetOfScenarios(name='Threshold',
                          scenario_df=dfBase,
                          color='blue',
                          conditions=varBase,
                          if_find_frontier=False,
                          labels_shift_x=-0.7/8,
                          labels_shift_y=3/80)

baseQuart = Cls.SetOfScenarios(name='Threshold-Quarterly',
                               scenario_df=dfBase,
                               color='red',
                               conditions=varBaseQuart,
                               if_find_frontier=False,
                               labels_shift_x=0.1/8,
                               labels_shift_y=-4/80)
baseEnhancedTesting = Cls.SetOfScenarios(name='Threshold with Enhanced Testing',
                                         scenario_df=dfBase,
                                         color='red',
                                         conditions=varBaseEnhancedTesting,
                                         if_find_frontier=False,
                                         labels_shift_x=2.5/8,
                                         labels_shift_y=-0.11/80)
baseQuartEnhancedTesting = Cls.SetOfScenarios(name='Threshold-Quarterly with Enhanced Testing',
                                              scenario_df=dfBase,
                                              color='red',
                                              conditions=varBaseQuartEnhancedTesting,
                                              if_find_frontier=False,
                                              labels_shift_x=2.5/8,
                                              labels_shift_y=-0.11/80)
policyA = Cls.SetOfScenarios(name='Threshold+Trend',
                             scenario_df=dfPolicyA,
                             color='red',
                             conditions=varDual,
                             if_find_frontier=False,
                             labels_shift_x=0.1/8,
                             labels_shift_y=-4/80)
policyAQuart = Cls.SetOfScenarios(name='Quarterly Threshold+Trend',
                                  scenario_df=dfPolicyAQuart,
                                  color='red',
                                  conditions=varDualQuarterly,
                                  if_find_frontier=False,
                                  labels_shift_x=0.1/8,
                                  labels_shift_y=-4/80)
policyAQuartEnhanced = Cls.SetOfScenarios(name='Enhanced Threshold+Trend',
                                          scenario_df=dfPolicyAQuartEnhanced,
                                          color='red',
                                          conditions=varDualQuarterlyEnhanced,
                                          if_find_frontier=False,
                                          labels_shift_x=0.1/8,
                                          labels_shift_y=-4/80)
