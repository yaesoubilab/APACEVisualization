import apace.ParametersClasses as Param
import gonorrhea.GonoSettings as Set

# parameters ID
ids = []
ids.extend(range(6, 11+1))                  # resistance
ids.extend([16, 20, 21, 22, 25])
ids.extend(range(33, 36+1))           # initial conditions
ids.extend(range(51, 54+1))           # time until events

# create a dictionary of parameters
paramDict = Param.Parameters(Set.SELECTED_POSTERIOR_FILE_NAME)

# calculate parameter estimates and uncertainty intervals
paramDict.calculate_means_and_intervals(significance_level=0.05,
                                        ids=ids,
                                        csv_file_name_prior='csvfiles\ParamPriorDists.csv')

# ratio (probability of getting screened)
text = paramDict.get_ratio_mean_interval(
    numerator_par_name='Annual screening rate',
    denominator_par_names=['Annual screening rate', 'Natural recovery'],
    deci=2,
    form='%'
)
print('Probability of getting screened before natural recovery:', text)

# histogram of probability of getting screened
paramDict.plot_ratio_hist(
    numerator_par_name='Annual screening rate',
    denominator_par_names=['Annual screening rate', 'Natural recovery'],
    title='Probability of Getting Screened',
    output_fig_loc='figures\param_posteriors'
)

# posterior histograms
paramDict.plot_histograms(ids=ids,
                          csv_file_name_prior='csvfiles\ParamPriorDists.csv',
                          posterior_fig_loc='figures\param_posteriors')
