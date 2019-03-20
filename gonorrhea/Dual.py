import numpy as np
import SimPy.InOutFunctions as io


def get_tau(wtp, poliy_param):

    return poliy_param[0]*np.exp(poliy_param[1]*wtp)


def get_rho(wtp, poliy_param):
    return poliy_param[2] + poliy_param[3] * wtp


# ---- settings ----
policyParams = [0.1926,-0.4074,0.2195,-0.0254]
wtps = np.linspace(1.5, 2.5, 5) # [min, max, number of points]
# ------------------

data = []
for wtp in wtps:
    tau = get_tau(wtp, policyParams)
    rho = get_rho(wtp, policyParams)

    data.append([tau, tau*rho])

io.write_csv(rows=data,
             file_name='DualPolicy.csv',
             directory='csvfiles')

