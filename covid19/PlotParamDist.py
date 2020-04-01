import SimPy.FittingProbDist_MM as Fit
import scipy.stats as scs
import SimPy.FormatFunctions as F

# [mean, stDev, min, max]
R0 = [2.5, 0.5, 1.5, 3.5]
TimeToInf = [5, 1, 3, 7]
TimeInf = [4, 1, 2, 8]


def print_intervals(name, mean_std_min_max):
    beta_par = Fit.get_beta_params(
        mean=mean_std_min_max[0],
        st_dev=mean_std_min_max[1],
        minimum=mean_std_min_max[2],
        maximum=mean_std_min_max[3]
    )
    # print(beta_par)
    l = scs.beta.ppf(q=0.025,
                     a=beta_par['a'], b=beta_par['b'], loc=beta_par['loc'], scale=beta_par['scale'])
    u = scs.beta.ppf(q=0.975,
                     a=beta_par['a'], b=beta_par['b'], loc=beta_par['loc'], scale=beta_par['scale'])

    print(name, F.format_interval([l, u], deci=3))


print_intervals('R0:', R0)
print_intervals('Time to infectious:', TimeToInf)
print_intervals('Time infectious:', TimeInf)
