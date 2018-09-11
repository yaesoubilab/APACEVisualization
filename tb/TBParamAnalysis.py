import apace.ParametersClasses as Param

# create a dictionary of parameters
paramDict = Param.Parameters('csvfiles\SampledParams.csv')

# calculate parameter estimates and uncertainty intervals
paramDict.calculate_means_and_intervals(0.05)

# parameters ID
ids=[4, 9, 78]
ids.extend(range(85, 92))
ids.extend([128, 136, 144, 160])    # progression probability
ids.extend([162, 163, 164])         # reactivation rate (HIV-)
ids.extend([169, 170, 171])         # reactivation rate (HIV+nIC)
ids.extend([176, 177, 178])         # reactivation rate (HIV+IC)
ids.extend(range(228, 255))         # time until detection

paramDict.plot_histograms(ids=ids,
                          csv_file_name_prior='csvfiles\ParamPriorDists.csv',
                          posterior_fig_loc='figures\posteriors')
