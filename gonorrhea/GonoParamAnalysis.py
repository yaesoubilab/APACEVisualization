import apace.ParametersClasses as Param
import gonorrhea.GonoSettings as Set

# parameters ID
ids = [7, 8, 9, 10, 14, 15, 16, 19]
ids.extend(range(27, 30+1))           # initial conditions
ids.extend(range(45, 48+1))           # time until events

# create a dictionary of parameters
paramDict = Param.Parameters(Set.SELECTED_POSTERIOR_FILE_NAME)

# calculate parameter estimates and uncertainty intervals
paramDict.calculate_means_and_intervals(0.05, ids)

# ratio (probability of getting screened)
text = paramDict.get_ratio_mean_interval(
    numerator_par_name='Annual screening rate',
    denominator_par_names=['Annual screening rate', 'Natural recovery'],
    deci=2,
    form='%'
)
print(text)

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
