import numpy as np
import matplotlib.pyplot as plt
import time
import random
import sys
import json

xdata = []
ydata = []

plt.show()

axes = plt.gca()

axes.axis('equal')
axes.grid(linestyle=':', linewidth=1)
axes.grid(True)
# axes.tight_layout()

# axes.set_ylim([-15000, 13500])
# axes.set_xlim([-30000, 10000])

axes.set_ylim(-50000, 33000)
axes.set_xlim(-30000, 8000)

trackList = {}
plotList = {}

track, = axes.plot(xdata, ydata, marker='.',
                    mfc='b',
                     ms=2,
                    #  mec='k',
                     linestyle='-',
                     lw=0.0,
                     mew=.5,
                     alpha=.5)

plot, = axes.plot(xdata, ydata, marker='s',
                    mfc='r',
                     ms=5,
                     mec='r',
                     linestyle='-',
                     lw=0.0,
                     mew=.5,
                     alpha=1)



# for i in range(200):
for data in sys.stdin:
    # print(line)
    json_line = json.loads(data[:-2])
    if 'I042' in data:
        
        # print(json_line['CAT010']['I042'])

        xdata.append(int(json_line['CAT010']['I042']['X']))
        ydata.append(int(json_line['CAT010']['I042']['Y']))

        plot.set_xdata(xdata[-1])
        plot.set_ydata(ydata[-1])

        track.set_xdata(xdata)
        track.set_ydata(ydata)
    plt.draw()
    plt.pause(1e-255)
    #time.sleep(1e-255)

plt.show()
