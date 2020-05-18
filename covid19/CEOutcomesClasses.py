import apace.ScenariosClasses as Cls
import SimPy.RegressionClasses as Reg
import numpy as np

WTP_LABEL = 'Trade-off threshold ' + r'$(\omega)$'


class CEOutcomes:

    def __init__(self, csv_file_name, poly_degree=2):

        scenario_df = Cls.ScenarioDataFrame(csv_file_name=csv_file_name)

        self.wtps = []
        self.costs = []
        self.effects = []
        self.nSwitches = []

        for scenario_name in scenario_df.scenarios:

            if scenario_name[0:3] == 'D:3':
                # store wtp value
                i = scenario_name.find('WTP')
                self.wtps.append(float(scenario_name[i+5:]))

                # total cost
                cost_mean, cost_CI = scenario_df.get_mean_interval(
                    scenario_name=scenario_name,
                    outcome_name='Total Cost')
                self.costs.append(cost_mean)

                # effect
                effect_mean, effect_CI = scenario_df.get_mean_interval(
                    scenario_name=scenario_name,
                    outcome_name='DALY')
                self.effects.append(effect_mean/10)

                # Number of Switches
                n_switches_mean, n_switches_CI = scenario_df.get_mean_interval(
                    scenario_name=scenario_name,
                    outcome_name='Number of Switches')
                self.nSwitches.append(n_switches_mean)

        self.costRegression = Reg.PolyRegression(
            self.wtps, self.costs, degree=poly_degree)
        self.costRegression = Reg.ExpRegression(
            self.wtps, self.costs)

        self.effectRegression = Reg.PolyRegression(
            self.wtps, self.effects, degree=poly_degree)
        self.effectRegression = Reg.ExpRegression(
            self.wtps, self.effects, if_c0_zero=True)# p0=[0, 1, -1])

        self.nSwitchesRegression = Reg.PolyRegression(
            self.wtps, self.nSwitches, degree=poly_degree
        )

    def add_affordability_to_axis(self, ax, max_y_cost, max_y_n_switches,
                                  wtp_range, wtp_delta, show_data=False):

        if show_data:
            ax.scatter(self.wtps, self.costs,
                       marker='+', s=50, color='k', alpha=0.25)

        wtps = np.linspace(wtp_range[0], wtp_range[1], 50)
        ys = self.costRegression.get_predicted_y(x=wtps)
        self.add_plot_to_axis(ax=ax, wtps=wtps, ys=ys,
                              title='Affordability curve',
                              y_label='Expected number of weeks with\ntightened social distancing',
                              panel_label='C)',
                              max_y=max_y_cost,
                              wtp_range=wtp_range, wtp_delta=wtp_delta)

        if False:
            ax2 = ax.twinx()
            if show_data:
                ax2.scatter(self.wtps, self.nSwitches, color='r', alpha=0.25)

            ys = self.nSwitchesRegression.get_predicted_y(x=wtps)
            ax2.plot(wtps, ys, label='Expected number of switches', color='r', linestyle='--')
            ax2.set_ylabel('Expected number of switches', color='r')
            ax2.spines['right'].set_color('r')
            ax2.tick_params(axis='y', colors='r')
            # ax2.yaxis.label.set_color('r')
            ax2.set_ylim(0, max_y_n_switches)

    def add_effect_to_axis(self, ax, max_y,
                           wtp_range, wtp_delta, show_data=False):

        if show_data:
            ax.scatter(self.wtps, self.effects,
                       marker='+', s=50, color='k', alpha=0.25)
        wtps = np.linspace(wtp_range[0], wtp_range[1], 50)
        ys = self.effectRegression.get_predicted_y(wtps)
        self.add_plot_to_axis(ax=ax, wtps=wtps, ys=ys,
                              title='Projected impact on deaths\ndue to COVID-19',
                              y_label='Expected number of deaths\n(per 100,000 population)',
                              panel_label='D)',
                              max_y=max_y,
                              wtp_range=wtp_range, wtp_delta=wtp_delta)

    def add_plot_to_axis(self, ax, wtps, ys, title, y_label, panel_label, max_y, wtp_range, wtp_delta):

        ax.plot(wtps, ys, label='', color='k', linestyle='-')
        ax.set_title(title, size=10)
        ax.set_ylabel(y_label)
        ax.set_ylim(0, max_y)
        ax.set_xlim(wtp_range)
        ax.set_xlabel(WTP_LABEL)

        # x axis ticks and labels
        x_ticks = []
        x = wtp_range[0]
        while x <= wtp_range[1]:
            x_ticks.append(x)
            x += wtp_delta
        ax.set_xticks(x_ticks)
        # vals = ax.get_xticks()
        # ax.set_xticklabels(['{:,}'.format(int(x)) for x in vals])
        ax.text(-0.2, 1.11, panel_label, transform=ax.transAxes,
                size=12, weight='bold')


class RtOutcomesAndUtilization:

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
            self.selectWTPs, self.nSwitches, degree=1
        )

    def add_affordability_to_axis(self, ax, title, y_label, panel_label,
                                  max_y_cost, max_y_qaly, delta_wtp, show_data):
        if show_data:
            ax.scatter(self.selectWTPs, [c*1e-6 for c in self.costs],
                       marker='+', s=50, color='k', alpha=0.25)
        ys = self.costRegression.get_predicted_y(x=self.wtps)
        self.add_plot_to_axis(ax=ax, wtps=self.wtps, ys=ys,
                              title=title, y_label=y_label, panel_label=panel_label, max_y=max_y_cost, delta_wtp=delta_wtp)

        ax2 = ax.twinx()
        if show_data:
            ax2.scatter(self.selectWTPs, [e * 1e-3 for e in self.effects], color='r', alpha=0.25)
        ys = self.dalyRegression.get_predicted_y(x=self.wtps)
        ax2.plot(self.wtps, ys, label='QALYs loss', color='r', linestyle='--')
        ax2.set_ylabel('Expected QALYs lost (Thousands)\n', color='r')
        ax2.spines['right'].set_color('r')
        ax2.tick_params(axis='y', colors='r')
        # ax2.yaxis.label.set_color('r')
        ax2.set_ylim(0, max_y_qaly)

    def add_utilization_to_axis(self, ax, title, y_label, panel_label,
                                max_y, max_y_n_switches, delta_wtp, show_data):

        if show_data:
            ax.scatter(self.selectWTPs, self.utilization,
                       marker='+', s=50, color='k', alpha=0.25)
        ys = self.utilRegression.get_predicted_y(x=self.wtps)
        self.add_plot_to_axis(ax=ax, wtps=self.wtps, ys=ys,
                              title=title, y_label=y_label, panel_label=panel_label, max_y=max_y, delta_wtp=delta_wtp)

        ax2 = ax.twinx()
        if show_data:
            ax2.scatter(self.selectWTPs, [n for n in self.nSwitches], color='r', alpha=0.25)
        ys = self.nSwitchesRegression.get_predicted_y(x=self.wtps)
        ax2.plot(self.wtps, ys, label='Expected number of switches', color='r', linestyle='--')
        ax2.set_ylabel('Expected number of switches', color='r')
        ax2.spines['right'].set_color('r')
        ax2.tick_params(axis='y', colors='r')
        # ax2.yaxis.label.set_color('r')
        ax2.set_ylim(0, max_y_n_switches)

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