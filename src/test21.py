import numpy as np
import matplotlib.pyplot as plt
import time
import random
import sys
import json
import math

# ysample = random.sample(range(-50, 150), 200)
# ysample2 = random.sample(range(-150, 50), 200)
# xsample = random.sample(range(-50, 150), 200)
# xsample2 = random.sample(range(-150, 50), 200)

xdata = []
# xdata2 = []
ydata = []
# ydata2 = []

plt.show()

axes = plt.gca()

axes.axis('equal')
axes.grid(linestyle=':', linewidth=1)
axes.grid(True)
# axes.tight_layout()

# axes.set_ylim([-15000, 13500])
# axes.set_xlim([-30000, 10000])

axes.set_ylim(-50000, 330000)
axes.set_xlim(-300000, 80000)

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
    if 'I131' in data:
        # print(json_line['CAT021']['I131'])

        y = float(json_line['CAT021']['I131']['Lat'])# * math.pi / 180
        x = float(json_line['CAT021']['I131']['Lon'])# * math.pi / 180
        # print(lat, lon)
        # x = 6371 * math.cos(lat) * math.cos(lon)
        # y = 6371 * math.cos(lat) * math.sin(lon)
        # print(x, y)
        xdata.append(x)
        ydata.append(y)
        track.set_xdata(xdata)
        track.set_ydata(ydata)
        plot.set_xdata(xdata[-1])
        plot.set_ydata(ydata[-1])
    plt.draw()
    plt.pause(1e-24)
    # time.sleep(0.0001)

plt.show()
