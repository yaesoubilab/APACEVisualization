"""
========
Barchart
========

A bar plot with errorbars and height labels on individual bars
"""
import numpy as np
import matplotlib.pyplot as plt

# N = 5
# men_means = (20, 35, 30, 35, 27)
# men_std = (2, 3, 4, 1, 2)
#
# ind = np.arange(N)  # the x locations for the groups
# width = 0.35       # the width of the bars
#
# fig, ax = plt.subplots()
# rects1 = ax.bar(ind, men_means, width, yerr=men_std)
#
# women_means = (25, 32, 34, 20, 25)
# women_std = (3, 5, 2, 3, 3)
# rects2 = ax.bar(ind + width, women_means, width, color='y', yerr=women_std)
#
# # add some text for labels, title and axes ticks
# ax.set_ylabel('Scores')
# ax.set_title('Scores by group and gender')
# ax.set_xticks(ind + width / 2)
# ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
#
# ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))
#
# plt.show()
#

# Fixing random state for reproducibility
np.random.seed(19680801)


#plt.rcdefaults()
fig, ax = plt.subplots()

# Example data
people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
y_pos = np.arange(len(people))
performanceGood = 10 + 1 * np.arange(0, len(people))
performanceBad = 2 + 2 * np.arange(0, len(people))
errorGood = np.random.rand(len(people))
errorBad = 2*np.random.rand(len(people))

#ax.barh(y_pos, performance, xerr=error, align='center',
#        color='green', ecolor='black')

ax.errorbar(performanceGood, y_pos - 0.1, xerr=errorGood, fmt='o', ecolor='blue',
            elinewidth = 3, capsize = 0, markersize = 8, markerfacecolor = 'white',
            markeredgecolor = 'blue', markeredgewidth=2)
ax.errorbar(performanceBad, y_pos + 0.1, xerr=errorBad, fmt='o', ecolor='red',
            elinewidth = 3, capsize = 0, markersize = 8, markerfacecolor = 'white',
            markeredgecolor = 'red', markeredgewidth=2)

ax.set_yticks(y_pos)
ax.set_yticklabels(people)
ax.set_ylim(-0.5, 4.5)

ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Performance')
ax.set_title('How fast do you want to go today?')

ax.legend(('Good', 'Bad'))

plt.show()