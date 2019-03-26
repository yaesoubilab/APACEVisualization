import numpy as np
import matplotlib.pyplot as plt
import SimPy.InOutFunctions as io


def get_tau(wtp, poliy_param):

    return poliy_param[0]*np.exp(poliy_param[1]*wtp)


def get_rho(wtp, poliy_param):
    return poliy_param[2] + poliy_param[3] * wtp


# ---- settings ----
policyParams = [0.185,-0.1117,0.2229, 0]
wtps = np.linspace(4, 7, 9) # [min, max, number of points]
# ------------------

data = []
taus = []
thetas = []
for wtp in wtps:
    tau = get_tau(wtp, policyParams)
    rho = get_rho(wtp, policyParams)

    taus.append(tau)
    thetas.append(tau*rho)
    data.append([tau, tau*rho])

io.write_csv(rows=data,
             file_name='DualPolicy.csv',
             directory='csvfiles')


plt.scatter(wtps, taus, label='Tau')
plt.scatter(wtps, thetas, label='Theta')
#plt.xlim(1.5,  2.5)
plt.ylim(bottom=0)
plt.legend()
plt.show()