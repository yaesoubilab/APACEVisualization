import numpy as np
import matplotlib.pyplot as plt
import SimPy.InOutFunctions as io
import os

# ---- settings ----
policyParams = [10,-2e-5, 5, -2e-5]
wtps = np.linspace(50000, 250000, 16)  # [min, max, number of points]

WTP_MIN_DELTA = [50000, 100000]
R_EFF_MIN_DELTA = [0, 1]
MAX_R_EFF = 4
# ------------------

# change the current working directory
os.chdir('..')


def get_t_off(wtp, poliy_param):

    return poliy_param[0]*np.exp(poliy_param[1]*wtp)


def get_t_on(wtp, poliy_param):
    return poliy_param[2]*np.exp(poliy_param[3]*wtp)


def add_plot_to_axis(ax, ys, title,):
    ax.plot(wtps, ys, label='', color='k', linestyle='-')
    ax.set_title(title)
    ax.fill_between(wtps, ys, facecolor='b', alpha=0.2)
    ax.fill_between(wtps, [MAX_R_EFF] * len(ys), ys, facecolor='r', alpha=0.2)
    ax.set_ylim(0, 4)
    ax.set_xlim([wtps[0], wtps[-1]])
    ax.set_ylabel('Estimated Effective\nProduction Number')
    ax.set_xlabel('WTP for one QALY')
    vals = ax.get_xticks()
    ax.set_xticklabels(['{:,}'.format(int(x)) for x in vals])
    ax.text(-0.2, 1.11, 'A)', transform=axes[0].transAxes,
                 size=12, weight='bold')
    ax.text(0.05, 0.05, 'Lift Social Distancing', transform=axes[0].transAxes,
                 size=9, weight='bold')
    ax.text(0.95, 0.95, 'Continue with \nSocial Distancing', transform=axes[0].transAxes,
                 size=9, weight='bold', ha='right', va='top')


ts_off_on = []
ts_off = []
ts_on = []
for wtp in wtps:
    t_off = get_t_off(wtp, policyParams)
    t_on = get_t_on(wtp, policyParams)

    ts_off.append(t_off)
    ts_on.append(t_on)
    ts_off_on.append([t_off, t_on])

io.write_csv(rows=ts_off_on,
             file_name='Policies.csv',
             directory='covid19/csv_files')


fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))

# policy when off
add_plot_to_axis(ax=axes[0],
                 ys=ts_off,
                 title="If Social Distancing\nis Not in Use")


axes[1].plot(wtps, ts_on, label='', color='b', linestyle='-')
axes[1].set_title("If Social Distancing\nis in Use")
axes[1].fill_between(wtps, ts_on, facecolor='b', alpha=0.2)
axes[1].fill_between(wtps, [MAX_R_EFF]*len(ts_on), ts_on, facecolor='r', alpha=0.2)
axes[1].set_ylim(0, 4)
axes[1].set_xlim([wtps[0], wtps[-1]])
axes[1].set_xlabel('WTP for one QALY')
vals = axes[1].get_xticks()
axes[1].set_xticklabels(['{:,}'.format(int(x)) for x in vals])
axes[1].text(-0.2, 1.11, 'B)', transform=axes[1].transAxes,
             size=12, weight='bold')
axes[1].text(0.05, 0.05, 'Lift Social Distancing', transform=axes[1].transAxes,
             size=9, weight='bold')
axes[1].text(0.95, 0.95, 'Continue with \nSocial Distancing', transform=axes[1].transAxes,
             size=9, weight='bold', ha='right', va='top')
#
# #plt.xlim(1.5,  2.5)
# ax.set_ylim(bottom=0, top=0.15)
# ax.set_xlabel('Years of effective lifespan'
#               '\nwilling to give up to save 1 case of gonorrhea '
#               '\nper 100,000 MSM population 'r'($\omega$)') # r'$\omega$')
# vals = ax.get_yticks()
# ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])
# ax.legend()
fig.tight_layout()
fig.savefig('covid19/figures/Policy.png', dpi=300, bbox_inches='tight')
fig.show()
