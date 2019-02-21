import apace.ScenariosClasses as Cls
import gonorrhea.GonoSettings as Set
import apace.VisualizeScenarios as Vis

# change this to false to show M used
SHOW_EFFECTIVE_LIFE = True
SIM_LENGTH = 50     # years
POP_RATE = 0.1e6/5e6

if SHOW_EFFECTIVE_LIFE:
    Cls.HEALTH_MEASURE = 'DALY'
    Cls.COST_MEASURE = 'Average ratio: Effective life of AB'
    effect_mult = -1 / SIM_LENGTH * POP_RATE
    cost_mult = SIM_LENGTH
    switch_cost_effect = True
    Set.X_RANGE = (-3, 3)
    Set.Y_RANGE = (-50, 75)
    labels = ('Increase in Effective Life of Drugs A and B (Years)',
              'Increase in Annual Gonorrhea Cases\n(Per 100,000 MSM Population)')
else:
    Cls.HEALTH_MEASURE = 'DALY'  # 'Average ratio: Annual rate of gonorrhea cases'
    Cls.COST_MEASURE = 'Total Cost'
    effect_mult = 1 / SIM_LENGTH * POP_RATE
    cost_mult = 1 / 1e6
    switch_cost_effect = False
    Set.X_RANGE = (-100, 100)
    Set.Y_RANGE = (-0.6, 0.6)
    labels = ('Additional Gonorrhea Cases Averted Annually\nPer 100,000 MSM Population',
              'Additional Drug M Used (Millions)')

# find the wtp multiplier
wtp_mult = effect_mult / cost_mult


Vis.multi_plot_series(
    list_list_series=[
        [Set.base, Set.baseQuarterly],
        [Set.base, Set.policyA],
        [Set.base, Set.policyAQuart]
    ],
    list_of_titles=[
        'Base vs. Quarterly Base', 'Base vs. A', 'Base vs. Quarterly A'
    ],
    x_range=Set.X_RANGE,
    y_range=Set.Y_RANGE,
    effect_multiplier=effect_mult,
    cost_multiplier=cost_mult,
    switch_cost_effect_on_figure=switch_cost_effect,
    wtp_multiplier=wtp_mult,
    labels=labels,
    file_name='Performance.png'
)

# base vs. base with enhanced testing
Vis.plot_series(list_series=[Set.base, Set.baseEnhancedTesting],
                x_range=Set.X_RANGE,
                y_range=Set.Y_RANGE,
                effect_multiplier=effect_mult,
                cost_multiplier=cost_mult,
                switch_cost_effect_on_figure=switch_cost_effect,
                wtp_multiplier=wtp_mult,
                labels=labels,
                title='Base vs. Base with Enhanced Testing.png')
# base vs. quarterly base with enhanced testing
Vis.plot_series(list_series=[Set.base, Set.baseQuarterlyEnhancedTesting],
                x_range=Set.X_RANGE,
                y_range=Set.Y_RANGE,
                effect_multiplier=effect_mult,
                cost_multiplier=cost_mult,
                switch_cost_effect_on_figure=switch_cost_effect,
                wtp_multiplier=wtp_mult,
                labels=labels,
                title='Base vs. Quarterly Base with Enhanced Testing.png')

included = False
if included:
    # base vs. quarterly base
    Vis.plot_series(list_series=[Set.base, Set.baseQuarterly],
                    x_range=Set.X_RANGE,
                    y_range=Set.Y_RANGE,
                    effect_multiplier=effect_mult,
                    cost_multiplier=cost_mult,
                    switch_cost_effect_on_figure=switch_cost_effect,
                    wtp_multiplier=wtp_mult,
                    labels=labels,
                    title='Base vs. Quarterly Base')

    # base vs. A
    Vis.plot_series(list_series=[Set.base, Set.policyA],
                    x_range=Set.X_RANGE,
                    y_range=Set.Y_RANGE,
                    effect_multiplier=effect_mult,
                    cost_multiplier=cost_mult,
                    switch_cost_effect_on_figure=switch_cost_effect,
                    wtp_multiplier=wtp_mult,
                    labels=labels,
                    title='Base vs. A')

    # base vs. quarterly A
    Vis.plot_series(list_series=[Set.base, Set.policyAQuart],
                    x_range=Set.X_RANGE,
                    y_range=Set.Y_RANGE,
                    effect_multiplier=effect_mult,
                    cost_multiplier=cost_mult,
                    switch_cost_effect_on_figure=switch_cost_effect,
                    wtp_multiplier=wtp_mult,
                    labels=labels,
                    title='Base vs. Quarterly A')



