# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import datetime
import csv
from CoordConv import CoordTranslator
import math

def readFile(fileName):
    '''
    read asterix from json file and return two data structures
    '''

    with open(fileName, 'r') as f:
        data = [json.loads(line[:-2]) for line in f.readlines()[0:-1]]
    
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
                    plotLWO = {'Length': None, 'Width': None, 'Ori': None}
                try:
                    plotXY = e['CAT010']['I042']
                except:
                    plotXY = {'X': None, 'Y': None}
                try:
                    plotLL = e['CAT010']['I041']
                    XY_UTM = latLon2local([plotLL['Lat'], plotLL['Lon']])
                    X_UTM = XY_UTM[0]
                    Y_UTM = XY_UTM[1]
                except:
                    plotLL = {'Lat': None, 'Lon': None}
                    X_UTM = None
                    Y_UTM = None


                # if plotLWO and plotXY:
                track = {'track': trackNb,
                            'data': {'ToD': [e['CAT010']['I140']['ToD']],
                                     'X': [plotXY['X']],
                                     'Y': [plotXY['Y']],
                                     'Lat': [plotLL['Lat']],
                                     'Lon': [plotLL['Lon']],
                                     'Width': [plotLWO['Width']],
                                     'Length': [plotLWO['Length']],
                                     'Ori': [plotLWO['Ori']],
                                     'X_UTM': [X_UTM],
                                     'Y_UTM': [Y_UTM]
                                    }
                            }
                
                index += 1
                trackList.append(track)
            else:
                try:
                    plotLWO = e['CAT010']['I270']
                except:
                    plotLWO = {'Length': None, 'Width': None, 'Ori': None}
                try:
                    plotXY = e['CAT010']['I042']
                except:
                    plotXY = {'X': None, 'Y': None}
                try:
                    plotLL = e['CAT010']['I041']
                    XY_UTM = latLon2local([plotLL['Lat'], plotLL['Lon']])
                    X_UTM = XY_UTM[0]
                    Y_UTM = XY_UTM[1]
                except:
                    plotLL = {'Lat': None, 'Lon': None}
                    X_UTM = None
                    Y_UTM = None

                if plotLWO and plotXY:
                    trackList[trackIndices[trackNb]]['data']['ToD'].append(e['CAT010']['I140']['ToD'])
                    trackList[trackIndices[trackNb]]['data']['X'].append(plotXY['X'])
                    trackList[trackIndices[trackNb]]['data']['Y'].append(plotXY['Y'])
                    trackList[trackIndices[trackNb]]['data']['Lat'].append(plotLL['Lat'])
                    trackList[trackIndices[trackNb]]['data']['Lon'].append(plotLL['Lon'])
                    trackList[trackIndices[trackNb]]['data']['Width'].append(plotLWO['Width'])
                    trackList[trackIndices[trackNb]]['data']['Length'].append(plotLWO['Length'])
                    trackList[trackIndices[trackNb]]['data']['Ori'].append(plotLWO['Ori'])
                    trackList[trackIndices[trackNb]]['data']['X_UTM'].append(X_UTM)
                    trackList[trackIndices[trackNb]]['data']['Y_UTM'].append(Y_UTM)
                    
    return trackList, trackIndices                    


def latLon2local(coords, smr=True):
    # smr_latlon = [28.477493, -16.332522]
    # mlat_latlon = [28.482653, -16.341537]
    # Kx = 0.9999
    # Ky = 0.9998
    # theta = -0.6488 * 2 * math.pi / 360
    coordTrans = CoordTranslator()
    # smr_xy = coordTrans.LLtoUTM(smr_latlon)[2:]
    # temp1 = smr_xy[0] * math.cos(theta) - smr_xy[1] * math.sin(theta)
    # temp2 = smr_xy[0] * math.sin(theta) + smr_xy[1] * math.cos(theta)
    # smr_xy = [temp1 * Kx, temp2 * Ky]

    pointXY = coordTrans.LLtoUTM(coords)[2:]
    # temp1 = pointXY[0] * math.cos(theta) - pointXY[1] * math.sin(theta)
    # temp2 = pointXY[0] * math.sin(theta) + pointXY[1] * math.cos(theta)

    # print([temp1 * Kx - smr_xy[0], temp2 * Ky - smr_xy[1]])
    return pointXY    


def calcStats(trackList, trackIndices, trackListBig, maxSize):
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
        try:
            if max(e['data']['Width']) >= maxSize  or max(e['data']['Length']) >= maxSize:
                bigPlots.append(e)
        except:
            continue
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


def plotTrackListXY_calc(trackList):
    # plot every track
    for i in range(len(trackList)):
        plt.plot(trackList[i]['data']['X_UTM'],
                 trackList[i]['data']['Y_UTM'],
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
            plt.plot(t['data']['X_UTM'][0],
                     t['data']['Y_UTM'][0],
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
            plt.plot(t['data']['X_UTM'][-2],
                     t['data']['Y_UTM'][-2],
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


def plotTrackDGPS(trackList, UTM=True):
    # plot every track
    if UTM:
        xkey = 'X_UTM'
        ykey = 'Y_UTM'
    else:
        xkey = 'Lon'
        ykey = 'Lat'
    for i in range(len(trackList)):
        plt.plot(trackList[i]['data'][xkey],
                 trackList[i]['data'][ykey],
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
            plt.plot(t['data'][xkey][0],
                     t['data'][ykey][0],
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
            plt.plot(t['data'][xkey][-2],
                     t['data'][ykey][-2],
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
    '''
    doc string here
    '''
    # smr_latlon = [28.477493, -16.332522]
    # mlat_latlon = [28.482653, -16.341537] 
    # Kx = 0.9999
    # Ky = 0.9998
    # theta = -0.6488 * 2 * math.pi / 360
    Lat = []
    Lon = []
    X_UTM = []
    Y_UTM = []
    ToD = []
    # track = {}
    # coordTrans = CoordTranslator()
    # smr_xy = coordTrans.LLtoUTM(smr_latlon)[2:]
    # print(smr_xy)
    with open(fileName, "r") as DGPSfile:
        csv_reader = csv.reader(DGPSfile, delimiter='\t')
        next(csv_reader)
        for line in csv_reader:
            Lat.append(float(line[1]))
            Lon.append(float(line[2]))
            ToD.append(int(line[5][:2])*60*60 + int(line[5][3:5])*60 + float(line[5][6:11]))
            XY_UTM = latLon2local([Lat[-1], Lon[-1]])
            X_UTM.append(XY_UTM[0])
            Y_UTM.append(XY_UTM[1])
    
    return [{'track': 0, 'data': {'Lat': Lat, 'Lon': Lon, 'ToD': ToD, 'X_UTM': X_UTM, 'Y_UTM': Y_UTM}}]


def objectCorrelator(trackList, trackDGPS):
    '''
    correlates plots and DGPS points.

    '''
    maxTimeOffset = 0.5
    maxSeparation = 15
    trackListOutput = []
    for track in trackList:
        for points in trackDGPS:
            for timeStampt in points['data']['ToD']:
                if abs(track['data']['ToD'][0] - timeStampt) < maxTimeOffset:
                    indexPoint = points['data']['ToD'].index(timeStampt)
                    sizeArray = len(track['data']['ToD'])
                    track['data']['ToDDGPS'] = points['data']['ToD'][indexPoint:indexPoint+sizeArray]
                    track['data']['LatDGPS'] = points['data']['Lat'][indexPoint:indexPoint+sizeArray]
                    track['data']['LonDGPS'] = points['data']['Lon'][indexPoint:indexPoint+sizeArray]
                    trackListOutput.append(track)
                    break
    return trackListOutput

def main():

    asterixDecodedFile =  '/home/avidalh/Desktop/GNSS/DriveTests/SMR/20200129/200129-gcxo-230611.gps.json'
    asterixDecodedFile =  'recordings/200129-gcxo-230614.gps_mike6.json'
    #asterixDecodedFile =  '/home/avidalh/Desktop/GNSS/DriveTests/SMR/20200130/200130-gcxo-223713.gps.json'
    #asterixDecodedFile =  'recordings/200130-gcxo-223713.gps.json'
    # asterixDecodedFile =  'recordings/080001.gps.json'
    
    DGPStrackFile = 'recordings/20200129.cst'
    # DGPStrackFile = 'recordings/20140220.txt'


    trackList, trackIndices = readFile(asterixDecodedFile)
    trackDGPS = readDGPSfile(DGPStrackFile)

    trackList = objectCorrelator(trackList, trackDGPS)

    #plotSizeHist(trackList)

    inches = 16
    fig, plotXY = plt.subplots(1, 1, figsize=(inches, inches/1.7778), frameon=True)

    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    j = 0
    plotList = []

    maxSize = 70

    trackListBig = getBiggest(trackList, trackIndices, maxSize)
    totalTracks, totalPlots, totalMissed, totalBig, trackListMiss= calcStats(trackList, trackIndices, trackListBig, maxSize)
    textStr = '\n'.join((
        r'$Tracks: %2d$' % (totalTracks),
        r'$Plots: %2d$' % (totalPlots),
        r'$Missed: %2d$' % (totalMissed),
        r'$Big: %2d$' % (totalBig),
        r'$PD: %.2f$' % ((totalPlots-totalMissed)/totalPlots*100)
    ))

    plotTrackListLatLon(trackList)
    plotTrackList(trackList)
    plotTrackListXY_calc(trackList)
    plotTrackDGPS(trackDGPS, UTM=True)
    plotTrackDGPS(trackDGPS, UTM=False)

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


if __name__ == '__main__':
    main()