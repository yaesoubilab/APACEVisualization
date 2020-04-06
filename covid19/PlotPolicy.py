import numpy as np
import matplotlib.pyplot as plt
import SimPy.InOutFunctions as io
import os

# ---- settings ----
policyParams = [5.0096096195,-1.0157278249,0.0033164372] # [5,-1,0.25] # [4,-0.5e-5, 1, -0.5e-54.3077E-06]
WTPS = np.linspace(50000, 150000, 25)  # [min, max, number of points]

WTP_DELTA = 50000
R_EFF_MIN_DELTA = [0, 1]
MAX_R_EFF = 4
# ------------------

# change the current working directory
os.chdir('..')


def get_t_off(wtp, poliy_param, scale):

    return poliy_param[0]*np.exp(poliy_param[1]*wtp/scale)


def get_t_on(wtp, poliy_param, scale):
    return get_t_off(wtp, poliy_param, scale) * poliy_param[2] # *np.exp(poliy_param[3]*wtp)


def add_plot_to_axis(ax, ys, title, panel_label):
    ax.plot(WTPS, ys, label='', color='k', linestyle='-')
    ax.set_title(title)
    ax.fill_between(WTPS, ys, facecolor='b', alpha=0.2)
    ax.fill_between(WTPS, [MAX_R_EFF] * len(ys), ys, facecolor='r', alpha=0.2)
    ax.set_ylim(0, 4)
    ax.set_xlim([WTPS[0], WTPS[-1]])
    ax.set_xlabel('Willingness-to-pay for one QALY')

    # x axis ticks and labels
    x_ticks = []
    x = WTPS[0]
    while x <= WTPS[-1]:
        x_ticks.append(x)
        x += WTP_DELTA
    ax.set_xticks(x_ticks)
    vals = ax.get_xticks()
    ax.set_xticklabels(['{:,}'.format(int(x)) for x in vals])
    ax.text(-0.2, 1.11, panel_label, transform=ax.transAxes,
                 size=12, weight='bold')
    ax.text(0.05, 0.05, 'Relax\nSocial Distancing', transform=ax.transAxes,
                 size=9, weight='bold')
    ax.text(0.95, 0.95, 'Tighten Social Distancing', transform=ax.transAxes,
                 size=9, weight='bold', ha='right', va='top')


ts_off_on = []
ts_off = []
ts_on = []
scale = (WTPS[0]+WTPS[-1])/2
for wtp in WTPS:
    t_off = get_t_off(wtp, policyParams, scale)
    t_on = get_t_on(wtp, policyParams, scale)

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
                 title="If Social Distancing\nis Relaxed",
                 panel_label='A)')
axes[0].set_ylabel('Estimated Effective\nProduction Number')

add_plot_to_axis(ax=axes[1],
                 ys=ts_on,
                 title="If Social Distancing\nis Tightened",
                 panel_label='B)')

fig.tight_layout()
fig.savefig('covid19/figures/Policy.png', dpi=300, bbox_inches='tight')
fig.show()
