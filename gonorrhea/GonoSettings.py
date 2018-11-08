
INDX = 0
X_RANGE = (-100, 100)  # (-75, 75)
Y_RANGE = (-2, 4) #(-1, 2)

# file names for scenario analysis
SA_FILE_NAMES = ['csvfiles\SA50YrCalib.csv',
                 'csvfiles\SA50YrCalibNoise.csv',
                 'csvfiles\SADebug.csv']
SELECTED_SA_FILE_NAME = SA_FILE_NAMES[INDX]

# file names for parameter analysis
POSTERIOR_FILE_NAMES \
    = ['csvfiles\ParamSamples10YrCalib.csv',
       'csvfiles\ParamSamples10YrCalib.csv',
       '']
SELECTED_POSTERIOR_FILE_NAME = POSTERIOR_FILE_NAMES[INDX]

# file names for calibration
CALIB_FILE_NAMES \
    = ['csvfiles\Trajs50YrCalib.csv',
       '',
       'csvfiles\Trajs.csv']
SELECTED_CALIB_FILE_NAME = CALIB_FILE_NAMES[INDX]
