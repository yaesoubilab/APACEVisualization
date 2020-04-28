import SimPy.FittingProbDist_MM as Fit
import scipy.stats as scs
import SimPy.FormatFunctions as F

# [mean, stDev, min, max]
R0 = [2.5, 0.7, 1.5, 4]
TimeToInf = [5, 0.5, 3, 7]
TimeInf = [4, 1.5, 2, 8]
ProbHosp = [0.326, 0.018, 0, 1]
ProbDeath = [0.330, 0.032, 0, 1]


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

    print(name, F.format_interval([l, u], deci=2))


print_intervals('R0:', R0)
print_intervals('Time to infectious:', TimeToInf)
print_intervals('Time infectious:', TimeInf)
print_intervals('Probability of hospitalization:', ProbHosp)
print_intervals('Probability of death if needing ICU:', ProbDeath)
