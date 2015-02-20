#!/usr/bin/python3


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# import matplotlib
# matplotlib.use('Agg')
# from datetime import datetime
import numpy as numpy


data= numpy.genfromtxt('statistics.csv', delimiter=',', names=['Date','Pd','Rp','Ep','Mp','Op','Sm','SM','Notes'], skip_header=1)

datum = numpy.genfromtxt('statistics.csv',dtype=None,usecols=(0), skip_header=1, delimiter=',')
dates = mdates.datestr2num(datum)

f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=(13, 13/1.7778))
f.suptitle('Performance evolution since 2014/09/18', fontsize=15, fontweight='bold')

ax1.plot_date(dates, data['Pd'], label='% PD', ls='-', marker='None')
ax1.tick_params(axis='both', which='major', labelsize=10)
# ax12 = ax1.twinx()
# ax12.plot_date(dates, data['Mp'], label='Missed Plots', color = 'red', ls='-', marker='None', alpha=0.7)
# ax12.tick_params(axis='both', which='major', labelsize=10)

ax2.plot_date(dates, data['Sm'], label='SUC mean delay [ms]', ls='-', marker='None')
ax2.tick_params(axis='both', which='major', labelsize=10)

ax22 = ax2.twinx()
ax22.plot_date(dates, data['SM'], label='SUC max delay [ms]', color = 'red', ls='-', marker='None', alpha=0.7)
ax22.tick_params(axis='both', which='major', labelsize=10)

# Configure x-ticks
# ax.set_xticks(dates) # Tickmark + label at every plotted point

ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y %H:00'))
#ax3.xaxis.set_major_locator(mdates.WeekdayLocator(1))
ax3.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
ax3.xaxis.set_minor_locator(mdates.DayLocator(interval=1))

ax3.tick_params(axis='both', which='major', labelsize=10)
ax3.plot_date(dates,data['Rp'], label='Plots in the file', ls='-', marker='None')

# ax3.set_title('title')
# ax3.set_ylabel('Waterlevel (m)')
# ax3.grid(True)

leg1 = ax1.legend(numpoints=1, prop={'size': 10}, fancybox=1, loc ='center left')
frame1 = leg1.get_frame()
frame1.set_facecolor('k')
frame1.set_alpha(0.2)

# leg12 = ax12.legend(numpoints=1, prop={'size': 10}, fancybox=1, loc ='center right')
# frame1 = leg12.get_frame()
# frame1.set_facecolor('k')
# frame1.set_alpha(0.2)

leg2 = ax2.legend(numpoints=1, prop={'size': 10}, fancybox=1, loc='upper left')
frame2 = leg2.get_frame()
frame2.set_facecolor('k')
frame2.set_alpha(0.2)

leg22 = ax22.legend(numpoints=1, prop={'size': 10}, fancybox=1)
frame2 = leg22.get_frame()
frame2.set_facecolor('k')
frame2.set_alpha(0.2)

leg3 = ax3.legend(numpoints=1, prop={'size': 10}, fancybox=1, loc='upper left')
frame3 = leg3.get_frame()
frame3.set_facecolor('k')
frame3.set_alpha(0.2)

ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

# Format the x-axis for dates (label formatting, rotation)
f.autofmt_xdate(rotation=45)
f.tight_layout()
# f.set_tight_layout(True)
plt.tick_params(axis='both', which='major', labelsize=10)

plt.subplots_adjust(top=0.92)
plt.savefig('PerfEvo.pdf')

plt.show()

