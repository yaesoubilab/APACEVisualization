import SimPy.InOutFunctions as io
import SimPy.RegressionClasses as Reg
import numpy as np
import apace.ScenariosClasses as Cls


class RBasedPolicy:
    def __init__(self, policy_params, scale, wtps):

        self.policyParams = policy_params
        self.wtps = wtps
        self.tsOff = []
        self.tsOn = []
        self.wtpToffTon = []

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
        ax.set_ylim(0, max_r)
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


class OutcomesAndUtilization:

    def __init__(self, csv_file_name, wtps, poly_degree=2):

        scenario_df = Cls.ScenarioDataFrame(csv_file_name=csv_file_name)

        self.wtps = wtps
        self.selectWTPs = []
        self.costs = []
        self.effects = []
        self.utilization = []
        self.nSwitches = []

        for scenario_name in scenario_df.scenarios:

            if scenario_name[0:3] == 'D:2':
                # store wtp value
                i = scenario_name.find('WTP')
                self.selectWTPs.append(float(scenario_name[i+5:]))

                # total cost
                cost_mean, cost_CI = scenario_df.get_mean_interval(
                    scenario_name=scenario_name,
                    outcome_name='Total Cost')
                self.costs.append(cost_mean)

                # QALY
                effect_mean, effect_CI = scenario_df.get_mean_interval(
                    scenario_name=scenario_name,
                    outcome_name='DALY')
                self.effects.append(effect_mean)

                # utilization of social distancing
                utilization_mean, utilization_CI = scenario_df.get_mean_interval(
                    scenario_name=scenario_name,
                    outcome_name='Utilization (unit of time): Social Distancing')
                self.utilization.append(utilization_mean)

                # Number of Switches
                n_switches_mean, n_switches_CI = scenario_df.get_mean_interval(
                    scenario_name=scenario_name,
                    outcome_name='Number of Switches')
                self.nSwitches.append(n_switches_mean)

        self.costRegression = Reg.PolyRegression(
            self.selectWTPs, [c*1e-6 for c in self.costs], degree=poly_degree)

        self.dalyRegression = Reg.PolyRegression(
            self.selectWTPs, [e * 1e-3 for e in self.effects], degree=poly_degree)

        self.utilRegression = Reg.PolyRegression(
            self.selectWTPs, self.utilization, degree=poly_degree)

        self.nSwitchesRegression = Reg.PolyRegression(
            self.selectWTPs, self.nSwitches, degree=poly_degree
        )

        print(self.nSwitches)

    def add_affordability_to_axis(self, ax, title, y_label, panel_label,
                                  max_y_cost, max_y_qaly, delta_wtp, show_data):
        if show_data:
            ax.scatter(self.selectWTPs, [c*1e-6 for c in self.costs])
        ys = self.costRegression.get_predicted_y(x=self.wtps)
        self.add_plot_to_axis(ax=ax, wtps=self.wtps, ys=ys,
                              title=title, y_label=y_label, panel_label=panel_label, max_y=max_y_cost, delta_wtp=delta_wtp)

        ax2 = ax.twinx()
        if show_data:
            ax2.scatter(self.selectWTPs, [e * 1e-3 for e in self.effects])
        ys = self.dalyRegression.get_predicted_y(x=self.wtps)
        ax2.plot(self.wtps, ys, label='QALYs loss', color='r', linestyle='--')
        ax2.set_ylabel('QALYs lost (Thousands)\n')
        ax2.spines['right'].set_color('r')
        ax2.tick_params(axis='y', colors='r')
        # ax2.yaxis.label.set_color('r')
        ax2.set_ylim(0, max_y_qaly)

    def add_utilization_to_axis(self, ax, title, y_label, panel_label, max_y, delta_wtp, show_data):

        if show_data:
            ax.scatter(self.selectWTPs, self.utilization)
        ys = self.utilRegression.get_predicted_y(x=self.wtps)
        self.add_plot_to_axis(ax=ax, wtps=self.wtps, ys=ys,
                              title=title, y_label=y_label, panel_label=panel_label, max_y=max_y, delta_wtp=delta_wtp)

    def add_plot_to_axis(self, ax, wtps, ys, title, y_label, panel_label, max_y, delta_wtp):

        ax.plot(wtps, ys, label='', color='k', linestyle='-')
        ax.set_title(title, size=10)
        ax.set_ylabel(y_label)
        ax.set_ylim(0, max_y)
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
