# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import datetime
import csv


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
                                     'Lat': [e['CAT010']['I041']['Lat']],
                                     'Lon': [e['CAT010']['I041']['Lon']],
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
                                     'Lat': [e['CAT010']['I041']['Lat']],
                                     'Lon': [e['CAT010']['I041']['Lon']],
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
                                     'Lat': [None],
                                     'Lon': [None],
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
                    trackList[trackIndices[trackNb]]['data']['Lat'].append(e['CAT010']['I041']['Lat'])
                    trackList[trackIndices[trackNb]]['data']['Lon'].append(e['CAT010']['I041']['Lon'])
                    trackList[trackIndices[trackNb]]['data']['Width'].append(e['CAT010']['I270']['Width'])
                    trackList[trackIndices[trackNb]]['data']['Length'].append(e['CAT010']['I270']['Length'])
                    trackList[trackIndices[trackNb]]['data']['Ori'].append(e['CAT010']['I270']['Ori'])
                elif plotXY:
                    trackList[trackIndices[trackNb]]['data']['ToD'].append(e['CAT010']['I140']['ToD'])
                    trackList[trackIndices[trackNb]]['data']['X'].append(e['CAT010']['I042']['X'])
                    trackList[trackIndices[trackNb]]['data']['Y'].append(e['CAT010']['I042']['Y'])
                    trackList[trackIndices[trackNb]]['data']['Lat'].append(e['CAT010']['I041']['Lat'])
                    trackList[trackIndices[trackNb]]['data']['Lon'].append(e['CAT010']['I041']['Lon'])
                    trackList[trackIndices[trackNb]]['data']['Width'].append(0)
                    trackList[trackIndices[trackNb]]['data']['Length'].append(0)
                    trackList[trackIndices[trackNb]]['data']['Ori'].append(0)
                else:
                    trackList[trackIndices[trackNb]]['data']['ToD'].append(e['CAT010']['I140']['ToD'])
                    trackList[trackIndices[trackNb]]['data']['X'].append(None)
                    trackList[trackIndices[trackNb]]['data']['Y'].append(None)
                    trackList[trackIndices[trackNb]]['data']['Lat'].append(None)
                    trackList[trackIndices[trackNb]]['data']['Lon'].append(None)
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
    experimental...
    '''
    
    
    print('onpick points: ')


def plotTrackList(trackList):
    # plot every track
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
    # plot the start point of every track in green
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
    # plot the ending point of every track in red
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


def plotTrackListLatLon(trackList):
    # plot every track
    for i in range(len(trackList)):
        plt.plot(trackList[i]['data']['Lon'],
                 trackList[i]['data']['Lat'],
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
    # plot the start point of every track in green
    for t in trackList:
        try:
            plt.plot(t['data']['Lon'][0],
                     t['data']['Lat'][0],
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
    # plot the ending point of every track in red
    for t in trackList:
        try:
            plt.plot(t['data']['Lon'][-2],
                     t['data']['Lat'][-2],
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

def plotTrackDGPS(trackList):
    # plot every track
    for i in range(len(trackList)):
        plt.plot(trackList[i]['data']['Lon'],
                 trackList[i]['data']['Lat'],
                 marker='x',
                 mfc='None',
                 ms=3,
                 mec='grey',
                 linestyle='-',
                 lw=.7,
                 color='grey',
                 mew=.5,
                 pickradius=5,
                 picker=None)
    # plot the start point of every track in green
    for t in trackList:
        try:
            plt.plot(t['data']['Lon'][0],
                     t['data']['Lat'][0],
                        marker='x',
                        mfc='grey',
                        ms=3,
                        mec='grey',
                        linestyle='-',
                        lw=.7,
                        color='grey',
                        mew=.5,
                        picker=5)
        except:
            continue
    # plot the ending point of every track in red
    for t in trackList:
        try:
            plt.plot(t['data']['Lon'][-2],
                     t['data']['Lat'][-2],
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


def readDGPSfile(fileName):
    Lat = []
    Lon = []
    ToD = []
    # track = {}
    with open(fileName, "r") as DGPSfile:
        csv_reader = csv.reader(DGPSfile, delimiter='\t')
        next(csv_reader)
        for line in csv_reader:
            Lat.append(float(line[1]))
            Lon.append(float(line[2]))
            ToD.append(datetime.datetime.strptime(' ' + line[5] + ' ', " %H %M %S.%f "))
    
    return [{'track': 0, 'data': {'Lat': Lat, 'Lon': Lon, 'Tod': ToD}}]




asterixDecodedFile =  '/home/avidalh/Desktop/GNSS/DriveTests/SMR/20200129/200129-gcxo-230611.gps.json'
asterixDecodedFile =  '/home/avidalh/Desktop/GNSS/DriveTests/SMMS/20200129/200129-gcxo-230614.gps_mike6.json'

DGPStrackFile = '/home/avidalh/Desktop/GNSS/ASCII/20200129/20200129.cst'

trackList, trackIndices = readFile(asterixDecodedFile)
trackDGPS = readDGPSfile(DGPStrackFile)

#plotSizeHist(trackList)

inches = 16
fig, plotXY = plt.subplots(1, 1, figsize=(inches, inches/1.7778), frameon=True)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

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

plotTrackListLatLon(trackList)
plotTrackDGPS(trackDGPS)
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


plt.title('Drive Test Analysis script, file {0}'.format(asterixDecodedFile))
plt.text(0.85, 0.95, textStr, transform=plotXY.transAxes, fontsize=10, verticalalignment='top')
plt.axis('equal')
plt.grid(linestyle=':', linewidth=1)
plt.grid(True)
plt.tight_layout()
# plt.ylim([-250, 1350])
# plt.xlim([-2700, 1000])
plt.autoscale(enable=False)

plt.show()


