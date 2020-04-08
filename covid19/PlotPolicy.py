import numpy as np
import matplotlib.pyplot as plt
import SimPy.InOutFunctions as io
import os

# ---- settings ----
POLICY_PARAMS = [5, -1, 0.25] # [5,-1,0.25] # [5.0096096195,-1.0157278249,0.0033164372]
WTPS = np.linspace(50000, 150000, 25)  # [min, max, number of points]

WTP_DELTA = 50000
R_EFF_MIN_DELTA = [0, 1]
MAX_R_EFF = 4
# ------------------


class RBasedPolicy:
    def __init__(self, policy_params, wtps):

        self.policyParams = policy_params
        self.wtps = wtps
        self.tsOff = []
        self.tsOn = []
        self.wtpToffTon = []

        scale = (wtps[0] + wtps[-1]) / 2
        for wtp in wtps:
            t_off = self.get_t_off(wtp, scale)
            t_on = self.get_t_on(wtp, scale)

            self.tsOff.append(t_off)
            self.tsOn.append(t_on)
            self.wtpToffTon.append([wtp, t_off, t_on])

    def get_t_off(self, wtp, scale):

        return self.policyParams[0]*np.exp(self.policyParams[1]*wtp/scale)

    def get_t_on(self, wtp, scale):
        return self.get_t_off(wtp, scale) * self.policyParams[2] # *np.exp(poliy_param[3]*wtp)

    def write_to_csv(self, file_name, directory):
        io.write_csv(rows=self.wtpToffTon,
                     file_name=file_name,
                     directory=directory)

    def add_policy_figure_when_relaxed(self, ax, max_r, delta_wtp):
        self.add_plot_to_axis(ax=ax,
                              ys=self.tsOff,
                              title="Decision criteria when\nsocial distancing is in Relaxed state",
                              text_turn_off='Maintain \nrelaxed social distancing',
                              text_turn_on='Switch to tightened\nsocial distancing',
                              panel_label='A)',
                              max_r=max_r,
                              delta_wtp=delta_wtp)
        ax.set_ylabel('Estimated effective\nproduction number ' + r'$(R_t)$')

    def add_policy_figure_when_tightened(self, ax, max_r, delta_wtp):
        self.add_plot_to_axis(ax=ax,
                              ys=self.tsOn,
                              title="Decision criteria when\nsocial distancing is in Tightened state",
                              text_turn_off="Switch to\nrelaxed social distancing",
                              text_turn_on="Maintain tightened\nsocial distancing",
                              panel_label='B)',
                              max_r=max_r,
                              delta_wtp=delta_wtp)

    def add_plot_to_axis(self, ax, ys, title, text_turn_off, text_turn_on, panel_label, max_r, delta_wtp):
        ax.plot(self.wtps, ys, label='', color='k', linestyle='-')
        ax.set_title(title, size=10)
        ax.fill_between(self.wtps, ys, facecolor='b', alpha=0.2)
        ax.fill_between(self.wtps, [max_r] * len(ys), ys, facecolor='r', alpha=0.2)
        ax.set_ylim(0, 4)
        ax.set_xlim([self.wtps[0], self.wtps[-1]])
        ax.set_xlabel('Willingness-to-pay ($ per QALY)')

        # x axis ticks and labels
        x_ticks = []
        x = self.wtps[0]
        while x <= self.wtps[-1]:
            x_ticks.append(x)
            x += delta_wtp
        ax.set_xticks(x_ticks)
        vals = ax.get_xticks()
        ax.set_xticklabels(['{:,}'.format(int(x)) for x in vals])
        ax.text(-0.2, 1.11, panel_label, transform=ax.transAxes,
                     size=12, weight='bold')
        ax.text(0.03, 0.03, text_turn_off, transform=ax.transAxes,
                     size=9, weight='bold')
        ax.text(0.97, 0.97, text_turn_on, transform=ax.transAxes,
                     size=9, weight='bold', ha='right', va='top')


# change the current working directory
os.chdir('..')


policy = RBasedPolicy(policy_params=POLICY_PARAMS, wtps=WTPS)
policy.write_to_csv(file_name='Policies.csv',
                    directory='covid19/csv_files')

fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.5))

# policy when off
policy.add_policy_figure_when_relaxed(ax=axes[0], max_r=MAX_R_EFF, delta_wtp=WTP_DELTA)

# policy when on
policy.add_policy_figure_when_tightened(ax=axes[1], max_r=MAX_R_EFF, delta_wtp=WTP_DELTA)

fig.tight_layout()
fig.savefig('covid19/figures/Policy.png', dpi=300, bbox_inches='tight')
fig.show()
