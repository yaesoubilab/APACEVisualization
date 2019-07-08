import apace.ScenariosClasses as Cls
import gonorrhea.GonoSettings as Set
import apace.VisualizeScenarios as Vis


SIM_LENGTH = 50     # years
POP_RATE = 0.1e6/5e6

Cls.HEALTH_MEASURE = 'DALY'
Cls.COST_MEASURE = 'Average ratio: Effective life of AB'
effect_mult = -1 / SIM_LENGTH * POP_RATE
cost_mult = SIM_LENGTH
wtp_mult = 1 # -effect_mult / cost_mult
switch_cost_effect = True
Set.X_RANGE = (-3, 3)
Set.Y_RANGE = (-60, 60)
labels = ('Change in Effective Life of First-Line Antibiotic Drugs (Years)',
          'Change in Annual Gonorrhea Cases\n(Per 100,000 MSM Population)')

Vis.multi_plot_series(
    list_list_series=[
        [Set.base, Set.baseQuart],
        [Set.base, Set.policyDualQuartEnhanced]
    ],
    list_of_titles=[
        'Threshold vs.\nThreshold-Quarterly',
        'Threshold vs.\nEnhanced Threshold+Trend'
    ],
    x_range=Set.X_RANGE,
    y_range=Set.Y_RANGE,
    effect_multiplier=effect_mult,
    cost_multiplier=cost_mult,
    switch_cost_effect_on_figure=switch_cost_effect,
    wtp_multiplier=wtp_mult,
    labels=labels,
    fig_size=(5.4, 2.8),
    file_name='SMDM'
)


