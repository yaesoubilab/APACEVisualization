import apace.ScenariosClasses as Cls

INDX = 0
SHOW_FEASIBLE_RANGES = False
X_RANGE = (-100, 100)  # (-75, 75)
Y_RANGE = (-2, 4) #(-1, 2)

# file names for scenario analysis
SA_FILE_NAMES = ['csvfiles\SA50YrCalib.csv',
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
    Cls.VariableCondition('% Resistant Threshold', 0.01, 0.1,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 1, 1,
                          if_included_in_label=False),
    Cls.VariableCondition('# of Cases Tested for Resistance', DS_TESTS, DS_TESTS,
                          if_included_in_label=False)
]
varBaseQuart = [
    Cls.VariableCondition('Decision Period', 91, 91,
                          if_included_in_label=False),
    Cls.VariableCondition('% Resistant Threshold', 0.03, 0.5,
                          if_included_in_label=True, label_format='{:.1%}'),
    Cls.VariableCondition('Change in % Resistant Threshold', 1, 1,
                          if_included_in_label=True, label_format='{:.1%}'),
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

# series to display on the cost-effectiveness plane
base = Cls.Series('Base', 'blue',
                  variable_conditions=varBase,
                  if_find_frontier=False,
                  labels_shift_x=-10,
                  labels_shift_y=0.04)
baseQuarterly = Cls.Series('Policy Base-Quarterly', 'red',
                           variable_conditions=varBaseQuart,
                           if_find_frontier=False,
                           labels_shift_x=2.5,
                           labels_shift_y=-0.11)
baseEnhancedTesting = Cls.Series('Policy Base-Enhanced Testing', 'red',
                                 variable_conditions=varBaseEnhancedTesting,
                                 if_find_frontier=False,
                                 labels_shift_x=2.5,
                                 labels_shift_y=-0.11)
