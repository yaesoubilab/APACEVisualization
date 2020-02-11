import apace.ParametersClasses as Param

# create a dictionary of parameters
paramDict = Param.Parameters('csv_files\SampledParams.csv')

# calculate parameter estimates and uncertainty intervals
paramDict.calculate_means_and_intervals(poster_file='Posteriors.csv')

# parameters ID
ids=[2, 3, 4, 7, 8, 9, 77, 78]
ids.extend(range(85, 92+1))
ids.extend([129, 137, 145, 161])    # progression probability
ids.extend([163, 164, 165])         # reactivation rate (HIV-)
ids.extend([170, 171, 172])         # reactivation rate (HIV+nIC)
ids.extend([177, 178, 179])         # reactivation rate (HIV+IC)
ids.extend(range(229, 232))         # time until detection
ids.extend(range(236, 239))
ids.extend(range(243, 246))
ids.extend(range(250, 253))

paramDict.plot_histograms(ids=ids,
                          csv_file_name_prior='csv_files\ParamPriorDists.csv',
                          posterior_fig_loc='figures\posteriors')
