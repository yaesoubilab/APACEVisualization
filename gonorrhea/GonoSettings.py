import apace.ScenariosClasses as Cls

INDX = 0
SHOW_FEASIBLE_RANGES = False
X_RANGE = (-100, 100)
Y_RANGE = (-0.5, 0.5)

# file names for scenario analysis
SA_FILE_NAMES = ['csvfiles\SA50YrCalib.csv',
                 'csvfiles\SAPolicyA.csv',
                 'csvfiles\SA50YrCalibNoise.csv',
                 'csvfiles\SADebug.csv']
SELECTED_SA_FILE_NAME = SA_FILE_NAMES[INDX]

# file names for parameter analysis
POSTERIOR_FILE_NAMES \
    = ['csvfiles\ParamSamples50YrCalib.csv',
       'csvfiles\ParamSamples10YrCalib.csv',
       '']
SELECTED_POSTERIOR_FILE_NAME = POSTERIOR_FILE_NAMES[INDX]

# file names for calibration
CALIB_FILE_NAMES \
    = ['csvfiles\Trajs50YrCalib.csv',
       '',
       'csvfiles\Trajs.csv']
SELECTED_CALIB_FILE_NAME = CALIB_FILE_NAMES[INDX]

# -------------------------------------------------------
# ------------------ Defining Scenarios -----------------
# -------------------------------------------------------

DS_TESTS = 5000  # annual number of cases tested for drug-resistance

# conditions of variables to define scenarios to display on each series of cost-effectiveness plane
varBase = [
    Cls.VariableCondition('Decision Period', 364, 364,
                          if_included_in_label=False),
    Cls.VariableCondition('% Resistant Threshold', 0.035, 0.1,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 1, 1,
                          if_included_in_label=False),
    Cls.VariableCondition('# of Cases Tested for Resistance', DS_TESTS, DS_TESTS,
                          if_included_in_label=False)
]
varBaseQuart = [
    Cls.VariableCondition('Decision Period', 91, 91,
                          if_included_in_label=False),
    Cls.VariableCondition('% Resistant Threshold', 0.05, 0.1,
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
varA = [
    Cls.VariableCondition('Decision Period', 364, 364,
                          if_included_in_label=False),
    Cls.VariableCondition('% Resistant Threshold', 0.01, 0.5,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 0, 0.1,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('# of Cases Tested for Resistance', DS_TESTS, DS_TESTS,
                          if_included_in_label=False)
]

# read scenarios data frames
baseDF = Cls.ScenarioDataFrame(csv_file_name=SA_FILE_NAMES[0])
policyADF = Cls.ScenarioDataFrame(csv_file_name=SA_FILE_NAMES[1])


# series to display on the cost-effectiveness plane
base = Cls.Series(name='Base',
                  scenario_df=baseDF,
                  color='blue',
                  variable_conditions=varBase,
                  if_find_frontier=False,
                  labels_shift_x=-0.3,
                  labels_shift_y=3)

baseQuarterly = Cls.Series(name='Base-Quarterly',
                           scenario_df=baseDF,
                           color='red',
                           variable_conditions=varBaseQuart,
                           if_find_frontier=False,
                           labels_shift_x=0.1,
                           labels_shift_y=-4)
baseEnhancedTesting = Cls.Series(name='Base with Enhanced Testing',
                                 scenario_df=baseDF,
                                 color='red',
                                 variable_conditions=varBaseEnhancedTesting,
                                 if_find_frontier=False,
                                 labels_shift_x=2.5,
                                 labels_shift_y=-0.11)
baseQuarterlyEnhancedTesting = Cls.Series(name='Base-Quarterly with Enhanced Testing',
                                          scenario_df=baseDF,
                                          color='red',
                                          variable_conditions=varBaseQuartEnhancedTesting,
                                          if_find_frontier=False,
                                          labels_shift_x=2.5,
                                          labels_shift_y=-0.11)
policyA = Cls.Series(name='A',
                     scenario_df=baseDF,
                     color='red',
                     variable_conditions=varA,
                     if_find_frontier=False,
                     labels_shift_x=-0.3,
                     labels_shift_y=3)
