import SimPy.Plots.EffectiveSampleSize as P
import SimPy.InOutFunctions as IO

# read likelihoods
data = IO.read_csv_cols(file_name='csv_files/TBLikelihoods.csv', n_cols=1,
                        if_ignore_first_row=True, if_convert_float=True)

P.plot_eff_sample_size(likelihood_weights=data[0], if_randomize=True,
                       y_range=(0, 10),
                       file_name='results/EffSampleSize.png')
