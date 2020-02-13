import matplotlib.pyplot as plt
import apace.ScenariosClasses as Cls
import numpy as np

markers = ['o', 's', '^', 'D']
colors = ['gray', 'red', 'blue', 'green', 'orange']

PROB_UPTAKE = 0.75      # 0.5, 0.75, 1
PROB_DROPOUT = 0.15     # 0.1, 0.15, 0.25,


def populate_cea(prob_uptake, prob_dropout):

    scenario_name = 'U{:.{prec}f}% '.format(prob_uptake * 100, prec=0) \
                    + 'D{:.{prec}f}%'.format(prob_dropout * 100, prec=0)
    print('Results for:', scenario_name)
    # conditions of variables to define scenarios to display on the cost-effectiveness plane
    # here we want scenarios with
    # 'Prob {Tc+ | Tc}' = PROB,
    # 'Follow-Up (Tc+>1)' = any, and
    # 'IPT' = any
    varConditions = [
        Cls.VariableCondition('Prob {Tc+ | Tc}',
                              minimum=prob_uptake,
                              maximum=prob_uptake,
                              if_included_in_label=False),
        Cls.VariableCondition('Follow-Up (Tc+>1)',
                              minimum=0,
                              maximum=1,
                              if_included_in_label=True,
                              label_rules=[
                                  (0, 'First-year follow-up'),
                                  (1, 'Annual follow-up')]
                              ),
        Cls.VariableCondition('Prob {Drop-Out in Tc+>1}',
                              values=(prob_dropout, 0),
                              if_included_in_label=False),
        Cls.VariableCondition('IPT',
                              minimum=0,
                              maximum=1,
                              if_included_in_label=True,
                              label_rules=[
                                  (0, ''),
                                  (1, 'with 2°IPT')]
                              )
    ]

    # data frame of scenarios
    dfScenarios = Cls.ScenarioDataFrame(csv_file_name='csv_files\TBScenarios.csv')

    # series to display on the cost-effectiveness plane
    series = [
        Cls.SetOfScenarios(name='U{:.{prec}f}%'.format(prob_uptake * 100, prec=0)
                                +'-D{:.{prec}f}%'.format(prob_dropout * 100, prec=0),
                           scenario_df=dfScenarios,
                           color='#4D4D4D',  # '#808A87',
                           conditions=varConditions,
                           if_find_frontier=True,
                           labels_shift_x=-0.04,
                           labels_shift_y=0.01)
    ]

    # populate series
    Cls.SetOfScenarios.populate_sets_of_scenarios(
        series,
        save_cea_results=True,
        colors_of_scenarios=colors,
        interval_type='p',
        effect_multiplier=1,
        cost_multiplier=1 / 1e3,
        wtp_range=[0, 2000])

    # CBA
    #del series[0].CBA.strategies[1:3]
    plt.rc('font', size=9)  # fontsize of texts
    series[0].CBA.plot_incremental_nmbs(
        title='',
        y_label='Incremental Net Monetary Benefit ($)',
        x_label='Cost-Effectiveness Threshold ($ per DALY Averted)',
        interval_type='p',
        transparency_lines=0.1,
        show_legend=True,
        figure_size=(6, 5),
        file_name='results/cea/NMB-' + scenario_name + '.png'
    )
    print('WTP range with the highest expected NMB:')
    # print(series[0].CBA.get_wtp_ranges_with_highest_exp_nmb())

    series[0].CBA.plot_acceptability_curves(
        #title='Cost-Effectiveness Acceptability Curves',
        x_label='Cost-Effectiveness Threshold ($ per DALY Averted)',
        y_label='Probability of Resulting in the Highest NMB',
        y_range=[0, 1],
        fig_size=(4, 3.6),
        legends=['Base',
                 'First-year follow-up',
                 'Annual follow-up',
                 'First-year follow-up with limited 2°IPT',
                 'Annual follow-up with continuous 2°IPT'],
        file_name='results/cea/CEAC ' + scenario_name + '.png'
    )
    print('WTP range with the highest probability of being optimal:')
    # print(series[0].CBA.get_wtp_range_with_highest_prob_of_optimal())

    # print dCost, dEffect and cost-effectiveness ratio with respect to the base
    print('\nRelative cost to Base, Relative DALY to base, CER')
    print(series[0].CEA.get_dCost_dEffect_cer(interval_type='p',
                                              alpha=0.05,
                                              cost_digits=0, effect_digits=0, icer_digits=1,
                                              cost_multiplier=1, effect_multiplier=1))

    withCloud = False

    # plot
    fig, ax = plt.subplots(figsize=(5, 4.4))
    #ax.set_title('Cost-Effectiveness Plane')
    for i, ser in enumerate(series):

        if not withCloud:
            for j, x_value in enumerate(ser.xValues):
                ax.plot(x_value, ser.yValues[j], markers[j], color=colors[j+1],
                        markersize=8, mew=1)

            # # error bars
            # x_err_l = x_value-ser.xIntervals[j][0]
            # x_err_u = ser.xIntervals[j][1] - x_value
            # y_err_l = ser.yValues[j]-ser.yIntervals[j][0]
            # y_err_u = ser.yIntervals[j][1] - ser.yValues[j]
            #
            # # ax.errorbar(x_value, ser.yValues[j],
            # #             xerr=[[x_err_l], [x_err_u]],
            # #             yerr=[[y_err_l], [y_err_u]],
            # #             fmt='none', color='k', linewidth=1, alpha=0.4)

        # add the clouds
        if withCloud:
            for s in [s for s in ser.CEA.strategies if s.idx > 0]:

                # add the center of the cloud
                ax.scatter(s.dEffect.get_mean(), s.dCost.get_mean()/1000,
                           c=s.color,  # color
                           alpha=1,  # transparency
                           linewidth=2,  # line width
                           s=50,
                           marker='o',  # markers
                           label=s.name, # name to show in the legend
                           zorder=2,
                           linewidths=0,
                           #edgecolors='k',
                           )  # marker edge width
                ax.scatter(s.dEffect.get_mean(), s.dCost.get_mean()/1000,
                           marker='x',
                           c='k',
                           zorder=3
                           )  # marker edge width
                # add the cloud
                #if not s.ifDominated:
                if True: # idx >= 2:
                    ax.scatter(s.dEffectObs, np.divide(s.dCostObs, 1000),
                               c=s.color,  # color of dots
                               alpha=0.1,  # transparency of dots
                               s=20,  # size of dots
                               zorder=1
                               )

        # add frontier
        ax.plot(ser.frontierXValues, ser.frontierYValues, color=ser.color, alpha=1)

        if withCloud:
            ax.legend()
        else:
            # legend
            leg = ['First-year follow-up',
                   'Annual follow-up',
                   'First-year follow-up with limited 2°IPT',
                   'Annual follow-up with continuous 2°IPT',
                   'Frontier']
            #ser.legend.append('Frontier')
            ax.legend(leg, loc=1) #ser.legend

    ax.set_xlabel('DALY Averted')
    ax.set_ylabel('Additional Cost (Thousand Dollars)')

    if withCloud:
        ax.set_xlim(-5000, 20000)
        ax.set_ylim(-1000, 1500)
    else:
        ax.set_xlim(-500, 6500)  # (-500, 6500)
        ax.set_ylim(-250, 200)  # (-150, 850)

    ax.axvline(x=0, linestyle='--', color='black', linewidth=.5)
    ax.axhline(y=0, linestyle='--', color='black', linewidth=.5)

    plt.tight_layout()
    plt.savefig('results/cea/'
                + 'CEA ' + scenario_name
                + '.png', dpi=300)

    # pairwise
    # column titles
    titles = ['Base',
              'First-year follow-up',
              'Annual follow-up',
              'First-year follow-up\nwith limited 2°IPT',
              'Annual follow-up\nwith continuous 2°IPT']

    # plot
    series[0].CEA.plot_pairwise_ceas(
        figure_size=(7, 7),
        font_size=7,
        effect_label='DALY Averted (Thousands)',
        cost_label='Additional Cost (Thousand Dollars)',
        center_s=40,
        cloud_s=10,
        transparency=0.1,
        effect_multiplier=1/1000,
        cost_multiplier=1/1000,
        x_range=[-10, 20],
        y_range=[-2000, 2000],
        column_titles=titles,
        row_titles=titles,
        file_name='results\cea\pairwise-' + scenario_name + '.png'
    )


# populate_cea(prob_uptake=PROB_UPTAKE, prob_dropout=PROB_DROPOUT)

for p_uptake in [0.5, 0.75, 1]:
    for p_drop in [0.1, 0.15, 0.25]:
        populate_cea(prob_uptake=p_uptake,prob_dropout=p_drop)

