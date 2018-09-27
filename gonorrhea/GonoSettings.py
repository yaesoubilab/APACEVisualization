
INDX = 0
X_RANGE = (-70, 70)
Y_RANGE = (-0.7, 1.9)

# file names for scenario analysis
SA_FILE_NAMES = ['csvfiles\SAAll.csv',
                 'csvfiles\SAAll_NoDR.csv',
                 'csvfiles\SAAll_NoDR_Noise100.csv',
                 'csvfiles\SAAll_NoDR_Noise1000.csv']
SELECTED_SA_FILE_NAME = SA_FILE_NAMES[INDX]

# file names for parameter analysis
POSTERIOR_FILE_NAMES \
    = ['csvfiles\ParamSamplesWithDR.csv', 'csvfiles\ParamSamplesNoDR.csv', 'csvfiles\ParamSamplesNoDR_v2.csv','']
SELECTED_POSTERIOR_FILE_NAME = POSTERIOR_FILE_NAMES[INDX]

# file names for calibration
CALIB_FILE_NAMES \
    = ['csvfiles\Trajs.csv', '', '']
SELECTED_CALIB_FILE_NAME = CALIB_FILE_NAMES[INDX]
