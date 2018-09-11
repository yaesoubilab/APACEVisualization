import matplotlib.pyplot as plt
import gonorrhea.GonorrheaClasses as Cls

# series to display on the cost-effectiveness plane
series = [
    Cls.Series('Policy A', '#228B22',
               only_on_frontier=False,
               #resist_thresholds=(0.05, 0.05),
               delta_resist_thresholds=(0, 0.1),
               label=(False, True, True, False)),
    Cls.Series('Policy A', 'red',
               only_on_frontier=True,
               #resist_thresholds=(0.05, 0.05),
               delta_resist_thresholds=(0, 0.1),
               label=(False, True, True, False))
]

# populate series
Cls.populate_series(series, 'csvfiles\SABaseAndA.csv')

# plot
legend = []
for i, ser in enumerate(series):
    # scatter plot
    plt.scatter(ser.xValues, ser.yValue, color=ser.color, alpha=0.5)

    if i == 1:
        plt.plot(ser.xValues, ser.yValue, color=ser.color, alpha=0.75)
        # y-value labels
        #for j, txt in enumerate(ser.yLabels):
            #plt.annotate(txt, (ser.xValues[j]+0.01, ser.yValue[j]-0.05), color=ser.color)
    #legend.append(ser.name)

plt.xlabel('Expected Gonorrhea Infections Averted (Millions)')
plt.ylabel('Expected Additional Drug M Used (Millions)')
plt.xlim(-0.3, 0.3)
plt.ylim(-0.5, 1.1)
plt.axvline(x=0, linestyle='--', color='black', linewidth=1)
plt.axhline(y=0, linestyle='--', color='black', linewidth=1)
plt.savefig('figures/' + '-A Frontier' + '.png')
