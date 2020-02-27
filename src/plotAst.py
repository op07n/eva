import json
import matplotlib.pyplot as plt


def readFile(fileName):
    '''
    read asterix from json file and return two data structures
    '''

    with open(fileName, 'r') as f:
        data = [json.loads(line[:-2]) for line in f.readlines()[0:-1]]
    
    # f = open(fileName)
    # data = json.load(f)

    trackList = []
    track = {}
    trackIndices = {}
    index = 0

    for e in data[:]:
        try:
            trackNb = e['CAT010']['I161']['TrkNb']
        except:
            trackNb = ''
        if trackNb:
            # if str(trackNb) not in trackIndices:
            if trackNb not in trackIndices:
                trackIndices.update({trackNb: index})
                try:
                    plotLWO = e['CAT010']['I270']
                except:
                    plotLWO = ''
                try:
                    plotXY = e['CAT010']['I042']
                except:
                    plotXY = ''
                if plotLWO and plotXY:
                    track = {'track': trackNb,
                            'data': {'ToD': [e['CAT010']['I140']['ToD']],
                                     'X': [e['CAT010']['I042']['X']],
                                     'Y': [e['CAT010']['I042']['Y']],
                                     'Width': [e['CAT010']['I270']['Width']],
                                     'Length': [e['CAT010']['I270']['Length']],
                                     'Ori': [e['CAT010']['I270']['Ori']]
                                    }
                            }
                elif plotXY and not plotLWO:
                    track = {'track': trackNb,
                            'data': {'ToD': [e['CAT010']['I140']['ToD']],
                                     'X': [e['CAT010']['I042']['X']],
                                     'Y': [e['CAT010']['I042']['Y']],
                                     'Width': [0],
                                     'Length': [0],
                                     'Ori': [0]
                                    }
                            }
                else:
                    track = {'track': trackNb,
                            'data': {'ToD': [e['CAT010']['I140']['ToD']],
                                     'X': [None],
                                     'Y': [None],
                                     'Width': [0],
                                     'Length': [0],
                                     'Ori': [0]
                                    }
                            }
                index += 1
                trackList.append(track)
            else:
                try:
                    plotLWO = e['CAT010']['I270']
                except:
                    plotLWO = ''
                try:
                    plotXY = e['CAT010']['I042']
                except:
                    plotXY = ''
                if plotLWO and plotXY:
                    trackList[trackIndices[trackNb]]['data']['ToD'].append(e['CAT010']['I140']['ToD'])
                    trackList[trackIndices[trackNb]]['data']['X'].append(e['CAT010']['I042']['X'])
                    trackList[trackIndices[trackNb]]['data']['Y'].append(e['CAT010']['I042']['Y'])
                    trackList[trackIndices[trackNb]]['data']['Width'].append(e['CAT010']['I270']['Width'])
                    trackList[trackIndices[trackNb]]['data']['Length'].append(e['CAT010']['I270']['Length'])
                    trackList[trackIndices[trackNb]]['data']['Ori'].append(e['CAT010']['I270']['Ori'])
                elif plotXY:
                    trackList[trackIndices[trackNb]]['data']['ToD'].append(e['CAT010']['I140']['ToD'])
                    trackList[trackIndices[trackNb]]['data']['X'].append(e['CAT010']['I042']['X'])
                    trackList[trackIndices[trackNb]]['data']['Y'].append(e['CAT010']['I042']['Y'])
                    trackList[trackIndices[trackNb]]['data']['Width'].append(0)
                    trackList[trackIndices[trackNb]]['data']['Length'].append(0)
                    trackList[trackIndices[trackNb]]['data']['Ori'].append(0)
                else:
                    trackList[trackIndices[trackNb]]['data']['ToD'].append(e['CAT010']['I140']['ToD'])
                    trackList[trackIndices[trackNb]]['data']['X'].append(None)
                    trackList[trackIndices[trackNb]]['data']['Y'].append(None)
                    trackList[trackIndices[trackNb]]['data']['Width'].append(0)
                    trackList[trackIndices[trackNb]]['data']['Length'].append(0)
                    trackList[trackIndices[trackNb]]['data']['Ori'].append(0)
    return trackList, trackIndices                    


def calcStats(trackList, trackIndices, trackListBig):
    '''
    '''
    totalMissed = 0
    totalPlots = 0
    totalTracks = 0
    trackListMiss = []

    for e in trackList:
        totalTracks +=1
        # print('e[\'data\'][\'ToD\']: ', e['data']['ToD'])
        totalPlots += len(e['data']['ToD'])
        # track = {}
        missFlag = False
        missX, missY = [], []
        for i in range(len(e['data']['ToD'])-1):
            deltaTime = e['data']['ToD'][i+1] - e['data']['ToD'][i]
            if  deltaTime > 1.2:
                totalMissed +=1

                missFlag = True
                if e['data']['X'][i+1] and e['data']['X'][i-1]:
                    missX.append((e['data']['X'][i+1]+e['data']['X'][i-1])/2)
                    missY.append((e['data']['Y'][i+1]+e['data']['Y'][i-1])/2)
                    
        if missFlag:
            trackNb = e['track']
            track = {'track': trackNb, 'data': {'X': missX, 'Y': missY}}
            trackListMiss.append(track)

    print('\n')
    print('Total tracks:\t', totalTracks)
    print('Total plots:\t', totalPlots, '\t\tmissed:\t', totalMissed, '\t\tpercent missed:\t', totalMissed/totalPlots*100)
    print('Prob. of Detection:\t', (totalPlots-totalMissed)/totalPlots*100, '%')
    print('Total tracks with big plots: {0}'.format(len(trackListBig)))
    totalBig = 0
    for t in trackListBig:
        for w, l in zip(t['data']['Width'], t['data']['Length']):
            if w >= maxSize or l >= maxSize:
                totalBig +=1
    print('Total big plots:             {0}'.format(totalBig))

    return totalTracks, totalPlots, totalMissed, totalBig, trackListMiss


def getBiggest(trackList, trackIndices, maxSize=60):
    '''
    '''
    bigPlots = []
    print()
    for e in trackList:
        if max(e['data']['Width']) >= maxSize  or max(e['data']['Length']) >= maxSize:
            bigPlots.append(e)

    return bigPlots


def onclick(event):
    '''
    experimental
    '''
    thisline = event.artist
    
    ind = event.ind
    
    print('onpick points: ', points)


def plotTrackList(trackList):
    for i in range(len(trackList)):
        plt.plot(trackList[i]['data']['X'],
                 trackList[i]['data']['Y'],
                 marker='^',
                 mfc='None',
                 ms=3,
                 mec='b',
                 linestyle='-',
                 lw=.7,
                 color='y',
                 mew=.5,
                 pickradius=5,
                 picker=None)
    for t in trackList:
        try:
            plt.plot(t['data']['X'][0],
                     t['data']['Y'][0],
                        marker='^',
                        mfc='g',
                        ms=3,
                        mec='g',
                        linestyle='-',
                        lw=.7,
                        color='y',
                        mew=.5,
                        picker=5)
        except:
            continue
    for t in trackList:
        try:
            plt.plot(t['data']['X'][-2],
                     t['data']['Y'][-2],
                        marker='^',
                        mfc='r',
                        ms=3,
                        mec='r',
                        linestyle='-',
                        lw=.7,
                        color='y',
                        mew=.5,
                        picker=5)
        except:
            continue

def plotSizeHist(trackList):
    width, length = [], []
    for track in trackList:
        width.append(track['data']['Width'])
        length.append(track['data']['Length'])
    num_bins = 1
    n, bins, patches = plt.hist(width, num_bins)
    plt.show()
    n, bins, patches = plt.hist(length, num_bins)
    plt.show()



fileName =  'bravo2_mlat.json'
fileName2 = '20200214_4001.json'

trackList, trackIndices = readFile(fileName)

#plotSizeHist(trackList)

inches = 16
fig, plotXY = plt.subplots(1, 1, figsize=(inches, inches/1.7778), frameon=True)

j = 0
plotList = []

maxSize = 70

trackListBig = getBiggest(trackList, trackIndices, maxSize)
totalTracks, totalPlots, totalMissed, totalBig, trackListMiss= calcStats(trackList, trackIndices, trackListBig)
textStr = '\n'.join((
    r'$Tracks: %2d$' % (totalTracks),
    r'$Plots: %2d$' % (totalPlots),
    r'$Missed: %2d$' % (totalMissed),
    r'$Big: %2d$' % (totalBig),
    r'$PD: %.2f$' % ((totalPlots-totalMissed)/totalPlots*100)
))

plotTrackList(trackList)
'''
for track in trackListMiss:
    for j in range(len(track['data']['X'])):
        plt.plot(track['data']['X'][j],
                     track['data']['Y'][j],
                     marker='v',
                     mfc='k',
                     ms=10,
                     mec='k',
                     linestyle='-',
                     lw=.7, color='y',
                     mew=.5,
                     alpha=0.75)

for track in trackListBig:
    for j in range(len(track['data']['X'])):
        if track['data']['Length'][j] >= maxSize or track['data']['Width'][j] >= maxSize:
            plt.plot(track['data']['X'][j],
                     track['data']['Y'][j],
                     marker='o',
                     mfc='None',
                     ms=track['data']['Length'][j]*.5,
                     mec='cyan',
                     linestyle='-',
                     lw=.7, color='y',
                     mew=.5,
                     alpha=0.75)
            plt.plot(track['data']['X'][j],
                     track['data']['Y'][j],
                     marker='o',
                     mfc='None',
                     ms=track['data']['Width'][j]*.5,
                     mec='magenta',
                     linestyle='-',
                     lw=.7, color='y',
                     mew=.5,
                     alpha=.75)
'''

# cid = fig.canvas.mpl_connect('pick_event', onclick)
plotActive = []

plt.title('Tracks with bigsized plots, file {0}'.format(fileName))
plt.text(0.85, 0.95, textStr, transform=plotXY.transAxes, fontsize=10, verticalalignment='top')
plt.axis('equal')
plt.grid(linestyle=':', linewidth=1)
plt.grid(True)
plt.tight_layout()
plt.ylim([-250, 1350])
plt.xlim([-2700, 1000])
plt.autoscale(enable=False)
plt.show()


import matplotlib.animation as animation

fig, ax = plt.subplots()
x, y = [], []
plt.show()

x = trackList[0]['data']['X']
y = trackList[0]['data']['X']
line, = ax.plot(x, y, 'r-')

def animate(i):
    line.set_xdata(trackList[i]['data']['X'])
    line.set_ydata(trackList[i]['data']['Y'])
    return line

ani = animation.FuncAnimation(
    fig, animate, interval=2, blit=True, save_count=50
)

plt.show()

trackIndices.clear()
trackList.clear()
############################################### other file ###################################################

# trackList, trackIndices = readFile(fileName2)

# plotSizeHist(trackList)
# plt.show()

# plt.show(block= False)
# inches = 16
# fig2, plotXY2 = plt.subplots(1, 1, figsize=(inches, inches/1.7778), frameon=True)

# j = 0
# plotList = []
# trackListBig = getBiggest(trackList, trackIndices, maxSize)
# totalTracks, totalPlots, totalMissed, totalBig, trackListMiss= calcStats(trackList, trackIndices, trackListBig)
# textStr = '\n'.join((
#     r'$Tracks: %2d$' % (totalTracks),
#     r'$Plots: %2d$' % (totalPlots),
#     r'$Missed: %2d$' % (totalMissed),
#     r'$Big: %2d$' % (totalBig),
#     r'$PD: %.2f$' % ((totalPlots-totalMissed)/totalPlots*100)
# ))

# plotTrackList(trackList)

# for track in trackListMiss:
#     for j in range(len(track['data']['X'])):
#         plt.plot(track['data']['X'][j],
#                      track['data']['Y'][j],
#                      marker='v',
#                      mfc='k',
#                      ms=10,
#                      mec='k',
#                      linestyle='-',
#                      lw=.7, color='y',
#                      mew=.5,
#                      alpha=0.75)

# for track in trackListBig:
#     for j in range(len(track['data']['X'])):
#         if track['data']['Length'][j] >= maxSize or track['data']['Width'][j] >= maxSize:
#             plt.plot(track['data']['X'][j],
#                      track['data']['Y'][j],
#                      marker='o',
#                      mfc='None',
#                      ms=track['data']['Length'][j]*.5,
#                      mec='cyan',
#                      linestyle='-',
#                      lw=.7, color='y',
#                      mew=.5,
#                      alpha=0.75)
#             plt.plot(track['data']['X'][j],
#                      track['data']['Y'][j],
#                      marker='o',
#                      mfc='None',
#                      ms=track['data']['Width'][j]*.5,
#                      mec='magenta',
#                      linestyle='-',
#                      lw=.7, color='y',
#                      mew=.5,
#                      alpha=.75)
#     fig.canvas.draw()
#     input("enter")

# trackIndices.clear()
# trackList.clear()
# # cid = fig.canvas.mpl_connect('pick_event', onclick)
# plotActive = []

# plt.title('Tracks with bigsized plots, file {0}'.format(fileName2))
# plt.text(0.85, 0.95, textStr, transform=plotXY.transAxes, fontsize=10, verticalalignment='top')
# plt.axis('equal')
# plt.grid(linestyle=':', linewidth=1)
# plt.grid(True)
# plt.tight_layout()
# plt.ylim([-250, 1350])
# plt.xlim([-2700, 1000])
# plt.autoscale(enable=False)


# plt.show()
