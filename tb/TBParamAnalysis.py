import apace.ParametersClasses as Param

# create a dictionary of parameters
paramDict = Param.Parameters('csv_files\SampledParams.csv')

# parameters ID
ids=[2, 3, 4]                       # TB infectivity
ids.extend([7, 8, 9])               # HIV infectivity
ids.extend([95])                    # progression to HIV | IC
ids.extend([96])                    # ration of dead rate exp to naive
ids.extend(range(103, 103+8))       # partial immunity
ids.extend([113])                   # ratio of reactivation >1 to <1
ids.extend([147, 155, 163, 179])    # progression probability
ids.extend(range(181, 181+3))         # reactivation rate (HIV-)
ids.extend(range(188, 188+3))         # reactivation rate (HIV+nIC)
ids.extend(range(195, 195+3))         # reactivation rate (HIV+IC)
ids.extend(range(247, 247+3))             # time until detection
ids.extend(range(254, 254+3))
ids.extend(range(261, 261+3))
ids.extend(range(268, 268+3))

# initial conditions
initial_id = 456
ids.extend(range(initial_id, initial_id+3))
ids.extend(range(initial_id+4, initial_id+4+2))
ids.extend(range(initial_id+7, initial_id+7+2))
ids.extend(range(initial_id+10, initial_id+10+2))
ids.extend(range(initial_id+13, initial_id+13+2))

initial_id = 472
ids.extend([initial_id,
            initial_id+2,
            initial_id+4,
            initial_id+5,
            initial_id+7,
            initial_id+9,
            initial_id+11,
            initial_id+12,
            initial_id+14,
            initial_id+16,
            initial_id+18,
            initial_id+19])


# calculate parameter estimates and uncertainty intervals
paramDict.calculate_means_and_intervals(poster_file='results\Posteriors.csv',
                                        ids=ids, deci=4)

paramDict.plot_histograms(ids=ids,
                          csv_file_name_prior='csv_files\ParamPriorDists.csv',
                          posterior_fig_loc='results\posteriors')
