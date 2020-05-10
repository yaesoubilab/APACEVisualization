import SimPy.InOutFunctions as io
import SimPy.RegressionClasses as Reg
import numpy as np
import apace.ScenariosClasses as Cls

WTP_LABEL = 'Willingness to keep physical distancing' + \
            '\nin place to avert one death' + \
            '\nper 100,000 population ' + r'$(\omega)$'


class PolicyFt:
    def __init__(self, csv_file_name):

        self.cols = io.read_csv_cols(
            file_name=csv_file_name, n_cols=3, if_ignore_first_row=True, if_convert_float=True)

        self.wtps = self.cols[0]
        self.OnTs = self.cols[1]
        self.OffTs = self.cols[2]
        self.RegToOn = Reg.ExpRegression(x=self.wtps,
                                         y=self.OnTs,
                                         if_zero_at_limit=True)
        self.RegToOff = Reg.ExpRegression(x=self.wtps,
                                          y=self.OffTs,
                                          if_zero_at_limit=True)

    def add_policy_figure_when_relaxed(self, ax, max_f, wtp_range, wtp_delta,
                                       show_data=False, show_x_label=True):
        self.add_plot_to_axis(ax=ax,
                              ys=self.OnTs,
                              reg=self.RegToOn,
                              title="Decision criteria when\nphysical distancing is in Relaxed state",
                              text_turn_off='Maintain \nrelaxed physical distancing',
                              text_turn_on='Switch to tightened\nphysical distancing',
                              panel_label='A)',
                              max_f=max_f,
                              wtp_range=wtp_range,
                              wtp_delta=wtp_delta,
                              show_x_label=show_x_label,
                              show_data=show_data)
        ax.set_ylabel('Estimated\nforce of infection ' + r'$(F_t)$')

    def add_policy_figure_when_tightened(self, ax, max_f, wtp_range, wtp_delta,
                                         show_data=False, show_x_label=True):
        self.add_plot_to_axis(ax=ax,
                              ys=self.OffTs,
                              reg=self.RegToOff,
                              title="Decision criteria when\nphysical distancing is in Tightened state",
                              text_turn_off="Switch to\nrelaxed physical distancing",
                              text_turn_on="Maintain tightened\nphysical distancing",
                              panel_label='B)',
                              max_f=max_f,
                              wtp_range=wtp_range,
                              wtp_delta=wtp_delta,
                              show_x_label=show_x_label,
                              show_data=show_data)

    def add_plot_to_axis(self, ax, ys, reg, title, text_turn_off, text_turn_on, panel_label,
                         max_f, wtp_range, wtp_delta, show_data, show_x_label=True):

        if show_data:
            ax.scatter(self.wtps, ys, marker='+', s=50, color='k', alpha=0.25)

        if reg:
            wtps = np.linspace(wtp_range[0], wtp_range[1], 50)
            reg_ys = reg.get_predicted_y(wtps)
            ax.plot(wtps, reg_ys, label='', color='k', linestyle='-')
            ax.fill_between(wtps, reg_ys, facecolor='b', alpha=0.2)
            ax.fill_between(wtps, [max_f] * len(reg_ys), reg_ys, facecolor='r', alpha=0.2)

        ax.set_title(title, size=10)

        ax.set_ylim(0, max_f)
        ax.set_xlim(wtp_range)
        if show_x_label:
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
        ax.text(0.03, 0.03, text_turn_off, transform=ax.transAxes,
                     size=9, weight='bold')
        ax.text(0.97, 0.97, text_turn_on, transform=ax.transAxes,
                     size=9, weight='bold', ha='right', va='top')


class PolicyFtRangeOfWTP:
    def __init__(self, policy_params, wtps):

        self.policyParams = policy_params
        self.wtps = wtps
        self.FtsToOn = []
        self.FtsToOff = []
        self.wtpAndThresholds = []

        scale = (wtps[0] + wtps[-1]) / 2
        for wtp in wtps:

            on = self.get_threshold_to_on(wtp=wtp, scale=scale)
            off = self.get_threshold_to_off(wtp=wtp, scale=scale)
            self.FtsToOn.append(on)
            self.FtsToOff.append(off)

            row = [wtp, on, off]
            self.wtpAndThresholds.append(row)

    def get_threshold_to_on(self, wtp, scale):
        return np.exp(self.policyParams[0] + self.policyParams[1] * wtp / scale)

    def get_threshold_to_off(self, wtp, scale):
        return np.exp(self.policyParams[2] + self.policyParams[3] * wtp / scale)

    def write_to_csv(self, file_name, directory):
        io.write_csv(rows=self.wtpAndThresholds,
                     file_name=file_name,
                     directory=directory)

    def add_policy_figure_when_relaxed(self, ax, max_r, delta_wtp):
        self.add_plot_to_axis(ax=ax,
                              ys=self.FtsToOn,
                              title="Decision criteria when\nphysical distancing is in Relaxed state",
                              text_turn_off='Maintain \nrelaxed physical distancing',
                              text_turn_on='Switch to tightened\nphysical distancing',
                              panel_label='A)',
                              max_r=max_r,
                              delta_wtp=delta_wtp)
        ax.set_ylabel('Estimated \nforce of infection ' + r'$(F_t)$')

    def add_policy_figure_when_tightened(self, ax, max_r, delta_wtp):
        self.add_plot_to_axis(ax=ax,
                              ys=self.FtsToOff,
                              title="Decision criteria when\nphysical distancing is in Tightened state",
                              text_turn_off="Switch to\nrelaxed physical distancing",
                              text_turn_on="Maintain tightened\nphysical distancing",
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
        # vals = ax.get_xticks()
        # ax.set_xticklabels(['{:,}'.format(int(x)) for x in vals])
        ax.text(-0.2, 1.11, panel_label, transform=ax.transAxes,
                     size=12, weight='bold')
        ax.text(0.03, 0.03, text_turn_off, transform=ax.transAxes,
                     size=9, weight='bold')
        ax.text(0.97, 0.97, text_turn_on, transform=ax.transAxes,
                     size=9, weight='bold', ha='right', va='top')


class PolicyI:
    def __init__(self, policy_params, wtps):

        self.policyParams = policy_params
        self.wtps = wtps
        self.IsToOn = []
        self.IsToOff = []
        self.wtpAndThresholds = []

        scale = (wtps[0] + wtps[-1]) / 2
        for wtp in wtps:

            on = self.get_threshold_to_on(wtp=wtp, scale=scale)
            off = self.get_threshold_to_off(wtp=wtp, scale=scale)
            self.IsToOn.append(on)
            self.IsToOff.append(off)

            row = [wtp, on, off]
            self.wtpAndThresholds.append(row)

    def get_threshold_to_on(self, wtp, scale):
        return self.policyParams[0] * np.exp(self.policyParams[1] * wtp / scale)

    def get_threshold_to_off(self, wtp, scale):
        return self.policyParams[2] * self.get_threshold_to_on(wtp, scale)

    def write_to_csv(self, file_name, directory):
        io.write_csv(rows=self.wtpAndThresholds,
                     file_name=file_name,
                     directory=directory)


class PolicyRtI:
    def __init__(self, policy_params, wtps):

        self.policyParams = policy_params
        self.wtps = wtps
        self.RtsOff = []
        self.RtOn = []
        self.IsOff = []
        self.IsOn = []
        self.wtpAndThresholds = []

        scale = (wtps[0] + wtps[-1])/2
        for wtp in wtps:
            r_thresholds = self.get_r_thresholds(wtp=wtp,scale=scale)
            i_thresholds = self.get_i_thresholds(wtp=wtp,scale=scale)

            self.RtsOff.append(r_thresholds[0])
            self.RtOn.append(r_thresholds[1])
            self.IsOff.append(i_thresholds[0])
            self.IsOn.append(i_thresholds[1])

            row = [wtp]
            row.extend(r_thresholds)
            row.extend(i_thresholds)
            self.wtpAndThresholds.append(row)

    def get_r_thresholds(self, wtp, scale):

        to_close = self.policyParams[0] * np.exp(self.policyParams[1] * wtp / scale)
        to_open = to_close * self.policyParams[2]
        return [to_close, to_open]

    def get_i_thresholds(self, wtp, scale):
        to_close = self.policyParams[3] * np.exp(self.policyParams[4] * wtp / scale)
        to_open = to_close * self.policyParams[5]
        return [to_close, to_open]

    def write_to_csv(self, file_name, directory):
        io.write_csv(rows=self.wtpAndThresholds,
                     file_name=file_name,
                     directory=directory)


class PolicyRt:
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
        ax.set_ylabel('Estimated effective\nreproductive number ' + r'$(R_t)$')

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



