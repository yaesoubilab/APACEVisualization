import matplotlib.pyplot as plt
import gonorrhea.GonorrheaClasses as Cls

# series to display on the cost-effectiveness plane
series = [
    Cls.Series('0.1% Tested for Drug-Resistance', 'blue',
               only_on_frontier=True, percent_tested_values=(0.001, 0.001)),
    Cls.Series('10% Tested for Drug-Resistance', 'red',
               only_on_frontier=True, percent_tested_values=(0.1, 0.1))
]

# populate series
Cls.populate_series(series, 'csvfiles\SAPolicyBaseWithNoise.csv')

# plot
legend = []
for i, ser in enumerate(series):
    # scatter plot
    plt.scatter(ser.xValues, ser.yValue, color=ser.color, alpha=0.5)
    plt.plot(ser.xValues, ser.yValue, color=ser.color, alpha=0.5)
    # y-value labels
    for j, txt in enumerate(ser.yLabels):
        plt.annotate(txt, (ser.xValues[j], ser.yValue[j]), color=ser.color)
    legend.append(ser.name)

plt.xlabel('Expected Gonorrhea Infections Averted (Millions)')
plt.ylabel('Expected Additional Drug M Used (Millions)')
plt.legend(legend)
#plt.xlim(-60, 10)
plt.axvline(x=0, linestyle='--', color='black', linewidth=1)
plt.axhline(y=0, linestyle='--', color='black', linewidth=1)
plt.savefig('figures/' + 'Policy A with Noise' + '.png')
