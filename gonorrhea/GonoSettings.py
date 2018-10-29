
INDX = 0
X_RANGE = (-120, 100) # (-75, 75)
Y_RANGE = (-3.5, 5) #(-1, 2)

# file names for scenario analysis
SA_FILE_NAMES = ['csvfiles\SA10YrCalib.csv',
                 'csvfiles\SA10YrCalibNoise.csv',
                 'csvfiles\SADebug.csv',
                 'csvfiles\SAAll_NoDR_Noise1000.csv']
SELECTED_SA_FILE_NAME = SA_FILE_NAMES[INDX]

# file names for parameter analysis
POSTERIOR_FILE_NAMES \
    = ['csvfiles\ParamSamples10YrCalib.csv',
       'csvfiles\ParamSamples10YrCalib.csv', '','']
SELECTED_POSTERIOR_FILE_NAME = POSTERIOR_FILE_NAMES[INDX]

# file names for calibration
CALIB_FILE_NAMES \
    = ['csvfiles\Trajs10YrCalib.csv',
       'csvfiles\Trajs50YrCalib.csv',
       'csvfiles\Trajs.csv']
SELECTED_CALIB_FILE_NAME = CALIB_FILE_NAMES[INDX]
