####### COULD BE DELETED ###############



import SimPy.EconEvalClasses as Econ
from apace import ScenariosClasses as Scen


class Series:
    def __init__(self,
                 name,
                 color,
                 only_on_frontier = True,
                 decision_periods=(364, 364),
                 resist_thresholds=(0, 1),
                 delta_resist_thresholds=(0, 1),
                 percent_tested_values=(0, 1),
                 label=(False, False, False, False), # (decision period, threshold, change in threshold, % tested)
                 shift_x=0,
                 shift_y=0
                 ):

        self.name = name
        self.color = color
        self.onlyOnFrontier = only_on_frontier
        self.decisionPeriods = decision_periods
        self.resistThresholds = resist_thresholds
        self.deltaResistThresholds = delta_resist_thresholds
        self.percentTestedValues = percent_tested_values
        self.xValues = []
        self.yValue = []
        self.yLabels = []
        self.strategies = []
        self.CEA = None
        self.labels = label
        self.shiftX = shift_x
        self.shiftY = shift_y

    def if_acceptable(self, scenario):
        if self.decisionPeriods[0] <= scenario.variables['Decision Period'] <= self.decisionPeriods[1] \
                and self.resistThresholds[0] <= scenario.variables['% Resistant Threshold'] <= self.resistThresholds[1] \
                and self.deltaResistThresholds[0] <= scenario.variables['Change in % Resistant Threshold'] <= self.deltaResistThresholds[1] \
                and self.percentTestedValues[0] <= scenario.variables['% of Cases Tested for Resistance'] <= self.percentTestedValues[1]:
            return True

    def fine_points(self):
        self.CEA = Econ.CEA(self.strategies, if_paired=True, if_find_frontier=self.onlyOnFrontier)

        if self.onlyOnFrontier:
            strategies = self.CEA.get_shifted_strategies_on_frontier()
        else:
            strategies = self.CEA.get_shifted_strategies()
            del strategies[0]  # remove the base strategy

        for idx, shiftedStr in enumerate(strategies):
            #if idx>0:
            self.xValues.append(shiftedStr.aveEffect/1e6)
            self.yValue.append(shiftedStr.aveCost/1e6)
            self.yLabels.append(shiftedStr.name)


def populate_series(series, csv_filename):
    # data frame for scenario analysis
    df = Scen.ScenarioDataFrame(csv_filename)

    # create the base strategy
    scn = df.scenarios['Base']
    base_strategy = Econ.Strategy(
        name='',
        cost_obs=scn.outcomes['Total Cost'],
        effect_obs=-1 * scn.outcomes['DALY'])

    # populate series to display on the cost-effectiveness plane
    for i, ser in enumerate(series):
        # add base
        ser.strategies = [base_strategy]
        # add other scenarios
        for key, scenario in df.scenarios.items():
            # add only non-Base strategies
            if scenario.name != 'Base' and ser.if_acceptable(scenario):

                # find shorten strategy name
                label_list = []
                # if ser.labels[0]:
                #     label_list.append(scenario.variables['Decision Period']+',')
                # if ser.labels[1]:
                #     label_list.append('{:.1%}'.format(scenario.variables['% Resistant Threshold'])+',')
                # if ser.labels[2]:
                #     label_list.append('{:.1%}'.format(scenario.variables['Change in % Resistant Threshold'])+',')
                # if ser.labels[3]:
                #     label_list.append(scenario.variables['% of Cases Tested for Resistance'])

                name = " ".join(str(x) for x in label_list)[:-1]

                ser.strategies.append(
                    Econ.Strategy(
                        name=name,
                        cost_obs=scenario.outcomes['Total Cost'],
                        effect_obs=-1 * scenario.outcomes['DALY'])
                )

                #if scenario.variables['Decision Period'] == ser.decisionPeriods[0]:
                #ser.yLabels.append()

        # create the CEA class
        ser.fine_points()
