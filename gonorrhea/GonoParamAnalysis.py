import apace.ParametersClasses as Param
import gonorrhea.GonoSettings as Set

# parameters ID
ids = [7, 8, 10, 14, 15, 16, 19]
ids.extend(range(27, 31))           # initial conditions
ids.extend(range(45, 49))           # time until events

paramDict = Param.Parameters(Set.SELECTED_POSTERIOR_FILE_NAME)

# calculate parameter estimates and uncertainty intervals
paramDict.calculate_means_and_intervals(0.05, ids)

# ratio
paramDict.calculate_ratio(
    numerator_par_name='Annual screening rate',
    denominator_par_names=['Annual screening rate', 'Natural recovery'],
    title='Probability of Getting Screened',
    #posterior_fig_loc='figures\param_posteriors'
)

# posterior histograms
paramDict.plot_histograms(ids=ids,
                          csv_file_name_prior='csvfiles\ParamPriorDists.csv',
                          posterior_fig_loc='figures\param_posteriors')
