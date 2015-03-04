#!/usr/bin/python3

"""
To run:
mark as executable and run with arguments, if no arguments passed it takes defaults asterix file and debug_level

Usage: eva.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -f filename, --file=filename
                        data FILE to analyse
  -l debug_level, --debug_level=debug_level
                        display more or less info for debugging...
  -b, --batch_mode      batch mode not open the displays
  -s, --speed_mode      don't decode the data file, just use the previous
                        decoded csv file...
  -e eval_mode, --eval_mode=eval_mode
                        eval mode, smr or mlat...
  -g, --gps_eval        evaluate precision using gps track data...
  -t gps_filename, --gps_track_file=gps_filename
                        gps track FILE to compare with
  -m, --display_map     display dxf background map...
  -d, --delay_analysis  display SUC delay analysis..
  -i, --insert_stats    insert statistics into stats file...


TODO:

1.- Associate aircraft tracks to gps tracks, by nearest (in time and space) and calculate errors...

2.- Plot errors vs azimuth, vs range, vs x/y, etc...

3.- Enhance code to interact user and graphics, ie: pick in a plot and open a legend with track number, time, plot sizes...

4.- Export code to run in any machine without python installed on it, pyinstaller, py2exe, etc... investigate in this
line, maybe would be necessary to downgrade the code to python 2.7...??!!!!????!!!!???

5.- Automate the analysis process to pick the file from the recorder, unzipit, analyse it, and save the results to the
statistics file. Finally send the file to external server or update a web with the new data...

6.-





"""

__author__ = 'avidalh'

__version__= 'alpha_0.500'


import sys
import binascii
import numpy as numpy
import matplotlib.pyplot as plt
import operator
import time
import csv
from decoder import *
import dxfgrabber
import os
from collections import Counter
from optparse import OptionParser

from CoordConv import CoordTranslator
import datetime
import math

# import pylab as P


# start time:
secs = time.time()


# options parser:

parser = OptionParser(version=__version__ )

parser.add_option("-f", "--file",
                  dest="filename",
                  help="data FILE to analyse",
                  metavar="filename",
                  default="../../Asterix/SMR/04/21/080001.gps",
                  )

parser.add_option("-l", "--debug_level",
                  dest="debug_level",
                  help="display more or less info for debugging...",
                  metavar="debug_level",
                  default=1)

parser.add_option("-b", "--batch_mode",
                  dest="batch_mode",
                  help="batch mode not open the displays",
                  metavar="batch_mode",
                  default=False,
                  action="store_true",
                  )

parser.add_option("-s", "--speed_mode",
                  dest="speed_mode",
                  help="don't decode the data file, just use the previous decoded csv file...",
                  metavar="do_all",
                  action="store_true",
                  default=False,
                  )

parser.add_option("-e", "--eval_mode",
                  dest="eval_mode",
                  help="eval mode, smr or mlat...",
                  metavar="eval_mode",
                  default='smr',
                  )

parser.add_option("-g", "--gps_eval",
                  dest="gps_eval",
                  help="evaluate precision using gps track data...",
                  metavar="gps_eval",
                  action="store_true",
                  default=False,
                  )

parser.add_option("-t","--gps_track_file",
                  dest="gps_filename",
                  help="gps track FILE to compare with",
                  metavar="gps_filename",
                  default="20140220.txt",
                  )

parser.add_option("-m", "--display_map",
                  dest="display_map",
                  help="display dxf background map...",
                  metavar="display_map",
                  action="store_true",
                  default=False,
                  )

parser.add_option("-d", "--delay_analysis",
                  dest="delay_analy",
                  help="display SUC delay analysis...",
                  metavar="delay_analy",
                  action="store_true",
                  default=False,
                  )

parser.add_option("-i", "--insert_stats",
                  dest="insert_stats",
                  help="insert statistics into statistics file...\n",
                  metavar="insert_stats",
                  action="store_true",
                  default=False,
                  )


(options, args) = parser.parse_args()

print('filename: ', options.filename)
print('debug_level: ', options.debug_level)
print('batch_mode: ', options.batch_mode)
print('speed_mode: ', options.speed_mode)
print('eval_mode:', options.eval_mode)
print('gps_eval:', options.gps_eval)
print('gps_filename:', options.gps_filename)
print('display_map:', options.display_map)
print('insert_stats:', options.insert_stats)

filename = options.filename
debug_level = int(options.debug_level)
do_all = not options.speed_mode
batch_mode = options.batch_mode
eval_mode = options.eval_mode


#limited areas
# try:
#     lim_areas = int(sys.argv[5])
# except:
#     lim_areas = 0
#

def spinning_cursor():
    """
    display a spinning cursor while reading and decoding the frames
    :return: spinning cursor

    ;-) just for fun

    """
    while True:
        for cursor in '|\-/':
            yield cursor


def definition():
    """
    Used to define global var and etc...
    :return:
    """
    return None


    return TYP, DCR, CHN, GBS, CRT, offset


def decode_cat10(frame):

    cat, frame_length, \
    FSPEC, \
    SAC, SIC, \
    TYPE10, \
    TRD10_TYP, TRD10_DCR, TRD10_CHN, TRD10_GBS, TRD10_CRT, \
    TIME, time_at_rec, delta_time, \
    LAT, LON,\
    RHO, THETA, \
    X, Y,\
    V_RHO, V_THETA, \
    VX, VY, \
    TRACK, \
    TRACK_STATUS10, \
    ModeA, \
    TADDR, \
    TID_ID, \
    ModeS, VFI, FL, MeasHeight, TSize, TOri, TWidth, NOGO =\
    None, None, None, None, None, None, None, None, None, None, None, None, \
    None, None, \
    None, None, None, None, None, None, None, None, \
    None, None, None, None, None, None, None, \
    None, None, None, None, None, None, None, None
    FSPEC, offset = read_fspec(frame)
    if debug_level >= 3: print('Frame %s FSPEC:	  %s,' % (frames_counter, binascii.hexlify(FSPEC)))
    if len(FSPEC) >= 1:
        if FSPEC[0] & 128:
            if debug_level >= 3: print('Frame %s Calling decode_SIC_SAC()...' % (frames_counter))
            SIC, SAC, offset = decode_IDEN(frame, offset)
            if debug_level >= 4: print('Frame %s SIC: %s, SAC: %s' % (frames_counter, SIC, SAC))
        if FSPEC[0] & 64:
            if debug_level >= 3: print('Frame %s Calling decode_TYPE10()...' % (frames_counter))
            TYPE10, offset = decode_TYPE10(frame, offset)
            if debug_level >= 4: print('Frame %s TYPE10: %s' % (frames_counter, TYPE10))
        if FSPEC[0] & 32:
            if debug_level >= 3: print('Frame %s Calling decode_TRD10()...' % (frames_counter))
            TRD10_TYP, TRD10_DCR, TRD10_CHN, TRD10_GBS, TRD10_CRT, offset = decode_TRD10(frame, offset)
            if debug_level >= 4: print('Frame %s TRD10 TYPE: %s, TRD10 CHN: %s' \
                                       % (frames_counter, TRD10_TYP, TRD10_CHN))
        if FSPEC[0] & 16:
            if debug_level >= 3: print('Frame %s Calling decode_TIME()...' % (frames_counter))
            TIME, offset = decode_TIME(frame, offset)
            if debug_level >= 4: print('Frame %s TIME: %s' % (frames_counter, TIME))
        if FSPEC[0] & 8:
            if debug_level >= 3: print('Frame %s Calling decode_POS_WGS84()...' % (frames_counter))
            LAT, LON, offset = decode_POS_WGS84(frame, offset)
            if debug_level >= 4: print('Frame %s LAT, LON: %s, %s' % (frames_counter, LAT, LON))
        if FSPEC[0] & 4:
            if debug_level >= 3: print('Frame %s Calling decode_POS_SPOL()...' % (frames_counter))
            RHO, THETA, offset = decode_POS_SPOL(frame, offset)
            if debug_level >= 4: print('Frame %s Rho, Theta: %s, %s' % (frames_counter, RHO, THETA))
        if FSPEC[0] & 2:
            if debug_level >= 3: print('Frame %s Calling decode_POS_CART()...' % (frames_counter))
            X, Y, offset = decode_POS_CART(frame, offset)
            if debug_level >= 4: print('Frame %s X, Y: %s, %s' % (frames_counter, X, Y))

    if len(FSPEC) >= 2:
        if FSPEC[1] & 128:
            if debug_level >= 3: print('Frame %s Calling decode_CTV_POL()...' % (frames_counter))
            V_RHO, V_THETA, offset = decode_CTV_POL(frame, offset)
            if debug_level >= 4: print('Frame %s V_RHO: %s, V_THETA: %s' % (frames_counter, V_RHO, V_THETA))
        if FSPEC[1] & 64:
            if debug_level >= 3: print('Frame %s Calling decode_CTV_CART()...' % (frames_counter))
            VX, VY, offset = decode_CTV_CART(frame, offset)
            if debug_level >= 4: print('Frame %s VX: %s, VY: %s' % (frames_counter, VX, VY))
        if FSPEC[1] & 32:
            if debug_level >= 3: print('Frame %s Calling decode_TRACK()...' % (frames_counter))
            TRACK, offset = decode_TRACK(frame, offset)
            if debug_level >= 4: print('Frame %s TRACK: %s' % (frames_counter, TRACK))
        if FSPEC[1] & 16:
            if debug_level >= 3: print('Frame %s Calling decode_TRACK_STATUS10()...' % (frames_counter))
            TRACK_STATUS10, offset = decode_TRACK_STATUS10(frame, offset)
            if debug_level >= 4: print('Frame %s TRACK_STATUS10: %s' % (frames_counter, TRACK_STATUS10))
        if FSPEC[1] & 8:
            if debug_level >= 3: print('Frame %s Calling decode_ModeA()...' % (frames_counter))
            ModeA, offset = decode_ModeA(frame, offset)
            if debug_level >= 4: print('Frame %s ModeA: %s, %s' % (frames_counter, hex(ModeA), oct(ModeA)))
        if FSPEC[1] & 4:
            if debug_level >= 3: print('Frame %s Calling decode_TADDR()...' % (frames_counter))
            TADDR, offset = decode_TADDR(frame, offset)
            if debug_level >= 4: print('Frame %s TADDR: %s' % (frames_counter, TADDR))
        if FSPEC[1] & 2:
            if debug_level >= 3: print('Frame %s Calling decode_TID()...' % (frames_counter))
            TID_STI, TID_ID, offset = decode_TID(frame, offset)
            if debug_level >= 4: print('Frame %s TID_ID: %s, TID_ID: %s' % (frames_counter, TID_STI, TID_ID))

    if len(FSPEC) >= 3:
        if FSPEC[2] & 128:
            if debug_level >= 3: print('Frame %s Calling decode_ModeS()...' % (frames_counter))
            ModeS, offset = decode_ModeS(frame, offset)
            if debug_level >= 4: print('Frame %s ModeS: %s' % (frames_counter, ModeS))
        if FSPEC[2] & 64:
            if debug_level >= 3: print('Frame %s Calling decode_VFI()...' % (frames_counter))
            VFI, offset = decode_VFI(frame, offset)
            if debug_level >= 4: print('Frame %s VFI: %s' % (frames_counter, VFI))
        if FSPEC[2] & 32:
            if debug_level >= 3: print('Frame %s Calling decode_FL()...' % (frames_counter))
            FL, offset = decode_FL(frame, offset)
            if debug_level >= 4: print('Frame %s FL: %s' % (frames_counter, FL))
        if FSPEC[2] & 16:
            if debug_level >= 3: print('Frame %s Calling decode_Meas_H()...' % (frames_counter))
            MeasHeight, offset = decode_Meas_H(frame, offset)
            if debug_level >= 4: print('Frame %s Meassured Height: %s' % (frames_counter, MeasHeight))
        if FSPEC[2] & 8:
            if debug_level >= 3: print('Frame %s Calling decode_TSizeOri()...' % (frames_counter))
            TSize, TOri, TWidth, offset = decode_TSizeOri(frame, offset)
            if debug_level >= 4: print('Frame %s Target Size: %s, Target Orientation: %s' % (frames_counter, TSize, TOri))
        if FSPEC[2] & 4:
            if debug_level >= 3: print('Frame %s Calling decode_SysStat()...' % (frames_counter))
            NOGO, offset = decode_SysStat(frame, offset)
            if debug_level >= 4: print('Frame %s System Status: %s' % (frames_counter, NOGO))
        if FSPEC[2] & 2:
            if debug_level >= 3: print('Frame %s Calling decode_PrePMess()...' % (frames_counter))
            PrePmess, offset = decode_PrePMess(frame, offset)
            if debug_level >= 4: print('Frame %s Pre-programmed Message: %s' % (frames_counter, PrePmess))


            ## TODO: write the following functions!!!!!!!!!!!!!!!!!!!

    # if len(FSPEC) >= 4:
    #     if FSPEC[3] & 128:
    #         if debug_level >= 3: print('Frame %s Calling decode_sigmaP()...' % (frames_counter))
    #         #sigmaX, sigmaY, covariXY, offset = decode_sigmaP(frame, offset)
    #         if debug_level >= 4: print('Frame %s Sx: %s, Sy: %s, Cxy: %s' % (frames_counter, sigmaX, sigmaY, covariXY))
    #     if FSPEC[3] & 64:
    #         if debug_level >= 3: print('Frame %s Calling decode_Presence()...' % (frames_counter))
    #         #Presence, offset = decode_Presence(frame, offset)
    #         if debug_level >= 4: print('Frame %s Presence: %s' % (frames_counter, Presence))
    #     if FSPEC[3] & 32:
    #         if debug_level >= 3: print('Frame %s Calling decode_AmpPPlot()...' % (frames_counter))
    #         #AmpPPlot, offset = decode_AmpPPlot(frame, offset)
    #         if debug_level >= 4: print('Frame %s Amplitude of Primary Plot: %s' % (frames_counter, AmpPPlot))
    #     if FSPEC[3] & 16:
    #         if debug_level >= 3: print('Frame %s Calling decode_CAccel()...' % (frames_counter))
    #         #CAccelX, CAccelY, offset = decode_CAccel(frame, offset)
    #         if debug_level >= 4: print('Frame %s CAccelX: %s, CAccelY: %s' % (frames_counter, CAccelX, CAccelY))
    #     if FSPEC[3] & 8:
    #         if debug_level >= 3: print('Frame %s Calling decode_SPARE()...' % (frames_counter))
    #     #     SPARE, offset = decode_SPARE(frame, offset)
    #     #     if debug_level >= 4: print('Frame %s SPARE: %s' % (frames_counter, SPARE))
    #     if FSPEC[3] & 4:
    #         if debug_level >= 3: print('Frame %s Calling decode_SField()...' % (frames_counter))
    #         #SField, offset = decode_SField(frame, offset)
    #         if debug_level >= 4: print('Frame %s SField: %s' % (frames_counter, SField))
    #     if FSPEC[3] & 2:
    #         if debug_level >= 3: print('Frame %s Calling decode_ResExpField()...' % (frames_counter))
    #         #ResExpField, offset = decode_ResExpField(frame, offset)
    #         if debug_level >= 4: print('Frame %s ResExpField: %s' % (frames_counter, ResExpField))


    # if it's a gps file: Decode the time of arriving to the recorder device:
    # print(len(frame))
    if gps:
        if debug_level >= 3: print('Frame %s Calling decode_TIME() at recording machine...' % (frames_counter))
        offset = len(frame) - 4
        # print(binascii.hexlify(frame[offset:offset+4]))
        time_at_rec, offset = decode_TIME(frame, offset)
        # print(time_at_rec)
        delta_time = float(time_at_rec - TIME)

    # Saving to the csv file:
    cat = 10
    frame_length = len(frame)
    csv_row = [[cat, frame_length, FSPEC, SAC, SIC, TYPE10,
                TRD10_TYP, TRD10_DCR, TRD10_CHN, TRD10_GBS, TRD10_CRT,
                TIME,

                time_at_rec, delta_time,

                LAT, LON, RHO, THETA, X, Y, V_RHO, V_THETA, VX,
                VY, TRACK, TRACK_STATUS10, ModeA, TADDR, TID_ID,
                ModeS, VFI, FL, MeasHeight, TSize, TOri, TWidth, NOGO]]

    output_writer.writerows(csv_row)

    return None



"""_____________________________________________________________________________________________________________________

main()

________________________________________________________________________________________________________________________
"""

print("Asterix tool", __version__)


# try:  # If a filename is passed as argument use that file, else use the default...
#     filename = sys.argv[1]
#     f = open(filename, "r")
# except:
#     # open the data file
#     filename = '../../Asterix/SMR/04/21/080001.gps'
#     # filename = '../../Asterix/SMMS/04/30/000001.gps'
#     f = open(filename, 'rb')

# filename = options.filename
f = open(filename, 'rb')



if debug_level < 2: spinner = spinning_cursor()


if do_all:
    if debug_level: print('No speed up option selected: Decoding the binary file...')
    definition()  # void function to init vars and other stuff...

    if debug_level: print("Opening the data file: %s" % filename)

    if debug_level: print("Creating the output.csv file: %s" % filename + '.csv')
    # f_csv = open('./output.csv', 'w+', newline='')
    f_csv = open(filename + '.csv', 'w+', newline='')
    output_writer = csv.writer(f_csv, delimiter=',')
    csv_header = [['Cat',       'Length',       'FSPEC',
                   'DI I010/010 SAC',           'DI I010/010 SIC',
                   'DI I010/000 Message Type',
                   'DI I010/020 TRD Type',      'DI I010/020 TRD DCR',    'DI I010/020 TRD CHN',
                   'DI I010/020 TRD GBS',       'DI I010/020 TRD CRT',
                   'DI I010/140 Time of Day',
                   'ADD ON time at recorder',   'ADD ON delta(t)', # for delay analysis
                   'DI I010/041 Lat',           'DI I010/041 Lon',
                   'DI I010/040 Rho',           'DI I010/040 Theta',
                   'DI I010/042 X',             'DI I010/042 Y',
                   'DI I010/200 V_rho',         'DI I010/200 V_theta',
                   'DI I010/202 V_x',           'DI I010/202 V_y',
                   'DI I010/161 Track No.',     'DI I010/170 Track Status',
                   'DI I010/060 ModeA',
                   'DI I010/220 Target Address',
                   'DI I010/245 Target ID',
                   'DI I010/250 Mode S MB Data',
                   'DI I010/300 Vehicle FID',
                   'DI I010/090 Fight Level',
                   'DI I010/091 Measured Height',
                   'DI I010/270 T. Size ',     'DI I010/270 T. Orientation',   'DI I010/270 T. Width',
                   'DI I010/550 System Status',
                   'DI I010/310 PreProgrammed Message',
                   'DI I010/550 Standard Deviation of Position',
                   'DI I010/280 Presence',
                   'DI I010/131 Amplitude of Primary Plot',
                   'DI I010/210 Calculated Acceleration',
                   'SP Special Purpose Field',
                   'RE Reserved Expansion Field']]
    output_writer.writerows(csv_header)

    # check if is a GPS file:
    gps = 0
    if filename.find('.gps') != -1:
        if debug_level: print("GPS file...")
        gps = 1

    # Read the first BYTE and strip the GPS header if necesary...
    # BYTE = numpy.fromfile(f, numpy.uint8, 1)
    # BYTE = numpy.array([BYTE], dtype = numpy.int8)
    if gps:
        if debug_level: print("Stripping the GPS header...")
        # while int(BYTE.encode('hex'), 16) == 205:
        BYTE = numpy.fromfile(f, numpy.uint8, 1)
        while BYTE == 205:
            BYTE = numpy.fromfile(f, numpy.uint8, 1)
        if debug_level: print("End of the GPS header...")

    else:
        if debug_level: print('No GPS file, no header to strip...')

    if gps:
        f.seek(f.tell() - 1, 0)  # Set the file pointer one step back to point the starting data frame

    # Read the Asterix frames
    frames_counter = 0

    if debug_level: print("Reading and decoding the Asterix frames...")


    X = []
    Y = []

    for i in range(8166):  # toggle comment to read the entire file or a few frames..._________________________________
    #while True: 			#toggle comment to read the entire file or a few frames...__________________________________
        cat = numpy.fromfile(f, numpy.int8, 1)

        if len(cat) == 0:
            if debug_level < 2 and not batch_mode: sys.stdout.write('\b')
            if debug_level: print("EOF reached...")
            break

        frame_length = numpy.fromfile(f, numpy.int16, 1)
        frame_length.byteswap(True)
        f.seek(f.tell() - 3, 0)
        frame = numpy.fromfile(f, numpy.uint8, frame_length + gps * 10)
        if debug_level >= 2: print("Frame %s Content: %s" % (frames_counter, binascii.hexlify(frame)))
        if debug_level >= 2: print("Frame %s Type:    %s, Asterix Cat.%s" % (frames_counter, hex(cat), cat))
        if debug_level >= 2: print("Frame %s Length:  %s, %s BYTEs" % (frames_counter, hex(frame_length), frame_length))

        # call to other functions to decode the frame item's
        if debug_level >= 3: print('Frame %s Calling decode function...' % frames_counter)

        # Decoding the frame:
        if cat == 10:
            if debug_level >= 2: print('Frame %s Calling decode_cat10()...' % (frames_counter))
            decode_cat10(frame)

        frames_counter += 1
    #    f.seek(f.tell() + gps * 10, 0)

        if debug_level < 2 and not batch_mode:
            sys.stdout.write('\b')
            sys.stdout.write(next(spinner))
            sys.stdout.flush()

    if debug_level < 2: sys.stdout.write('\b')
    if debug_level: print("Total frames readed: %s" % (frames_counter))
    f.close()

    if debug_level: print('Output csv file plots generated...')

    if debug_level: print('Sorting and jointing plots in tracks...')


    # sorting the output data file...
    reader = csv.reader(open(filename + '.csv'), delimiter=",")
    sortedlist = sorted(reader, key=operator.itemgetter(24), reverse=True)  # <--------------------------------------0j0


    f_csv = open(filename + '.sorted.csv', 'w+', newline='')
    # f_csv = open('output_sorted.csv', 'w+', newline='')


    # f_csv_time_an = open('./output_sorted_time_an.csv', 'w+', newline='')
    csv_row = sortedlist
    output_writer = csv.writer(f_csv, delimiter=',')
    output_writer.writerows(csv_row)
    f.close()

    if debug_level: print('Sorted tracks csv file generated...')


else: # only read the sorted file...
    if debug_level: print('Option -s selected: Reading the sorted csv data file...')
    # reader = csv.reader(open("./output_sorted.csv"), delimiter=",")
    reader = csv.reader(open(filename + '.sorted.csv'), delimiter=",")
    #reader = csv.reader(open('output_sorted.csv'), delimiter=",")

    sortedlist = sorted(reader, key=operator.itemgetter(24), reverse=True)  # <--------------------------------------0j0
    if sortedlist[2][12+1] != None:
        gps = 1
    else:
        gps = 0


if debug_level: print('Reading coordinates and timestamp of every plot...')

t, lat, lon, x, y, trks, delta_t_plots, delta_t_SUC, CHN = [], [], [], [], [], [], [], [], []

plots_outof_bounds =0
for i in range(len(sortedlist) - 1):
# for i in range(20000):
    if sortedlist[i + 1][24+1]:
        if (int(sortedlist[i + 1][18+1]) > -2528) and (int(sortedlist[i + 1][18+1]) < 777) or eval_mode == 'mlat': # to eliminate the out of bounds...
        #if True:
            lat, lon, x, t, y, trks, delta_t_plots = \
                lat + [sortedlist[i + 1][14+1]],\
                lon + [sortedlist[i + 1][15+1]],\
                x + [sortedlist[i + 1][18+1]], \
                t + [sortedlist[i + 1][11+1]], \
                y + [sortedlist[i + 1][19+1]], \
                trks + [sortedlist[i + 1][24+1]], \
                delta_t_plots + [sortedlist[i+1][13+1]]# <-------------------------------------------------0j0
        else:
            plots_outof_bounds += 1

    if debug_level < 2 and not batch_mode:
        sys.stdout.write('\b')
        sys.stdout.write(next(spinner))
        sys.stdout.flush()

for i in range(len(sortedlist) - 1):
    if sortedlist[i + 1][5] == 'Start of Update Cycle':
        delta_t_SUC = delta_t_SUC + [sortedlist[i+1][13+1]]

for i in range(len(sortedlist)-1):
  if (sortedlist[i + 1][5] != 'Start of Update Cycle') and (sortedlist[i + 1][5] != 'Periodic Status Message'):
    #print(sortedlist[i+1][8])
    #print()
    try: 
      CHN = CHN + [float(sortedlist[i+1][8])]
    except:  0
#print(CHN)
#print()
#print()
#print()



if debug_level < 2 and not batch_mode: sys.stdout.write('\b')
if debug_level: print('Counting plots in every track...')
if debug_level: print('Plots out of bounds and not used:', plots_outof_bounds)

count = {}
for trk in trks:
    if trk in count:
        count[trk] += 1
    else:
        count[trk] = 1
if debug_level >= 6: print('Count{}: %s' % count)


'''_____________________________________________________________________________________________________________________
generates list of tracks [x1, x2, x3...]
'''

if debug_level: print('Generating lists of tracks...')

tracks_X = []
tracks_Y = []
tracks_lat, tracks_lon = [], [] #*
x_ = []
y_ = []
lat_, lon_ = [], [] #*
j=0
for key in reversed(sorted(count)):
    for i in range(count[key]):
        x_.append(x[j+i])
        y_.append(y[j+i])
        lat_.append(lat[j+i]) #*
        lon_.append(lon[j+i]) #*
    tracks_X.append(x_)
    tracks_Y.append(y_)
    tracks_lat.append(lat_) #*
    tracks_lon.append(lon_) #*
    x_ = []
    y_ = []
    lat_ = [] #*
    lon_ = [] #*

    j += i+1

# print(tracks_lat)
# print(tracks_lon)


'''_____________________________________________________________________________________________________________________

search the missed...

by now generate ONE (and only one) list of missed plots...

TODO: generate lists of missed with track index...
________________________________________________________________________________________________________________________
'''

if debug_level: print('Searching missed plots...')

xm, ym = [], []
xi, yi = 0, 0
j = 0
for key in reversed(sorted(count)):
    if debug_level >= 6: print('key: %s' % key)
    for i in range(count[key]):
        dt = 1.
        # if len(x) < (j+i-1):
        try:
            x1, y1 = float(x[j + i]), float(y[j + i])
            x2, y2 = float(x[j + i + 1]), float(y[j + i + 1])
            if debug_level >= 6: print('t1 = %s' % (t[j + i]))
            if debug_level >= 6: print('t2 = %s' % (t[j + i + 1]))
            dt = abs(float(t[j + i + 1]) - float(t[j + i]))
            if debug_level >= 6: print('dt: %s' % dt)
            if debug_level >= 6: print('dt: %s' % round(dt))
            if (dt >= 1.1) and (dt <= 20) and (trks[j + i + 1] == trks[j + i]):
                if debug_level >= 5: print('Missed found!, dt= %s <--------' % dt)
                x1, y1 = float(x[j + i]), float(y[j + i])
                x2, y2 = float(x[j + i + 1]), float(y[j + i + 1])
                xi, yi = x1, y1
                if debug_level >= 5: print('(x1,y1)= %s, %s' % (x1, y1))
                if debug_level >= 5: print('(x2,y2)= %s, %s' % (x2, y2))
                for k in range(round(dt) - 1):
                    if debug_level >= 5: print('iteration %s' % k)
                    xi = (xi + (x2 - x1) / round(dt))
                    yi = (yi + (y2 - y1) / round(dt))
                    xm = xm + [xi]
                    ym = ym + [yi]
                    if debug_level >= 5: print('xi: %s, yi: %s' % (xi, yi))
        # else:
        except:
            # print('Exception reached...')
            pass
    j += i


if debug_level: print('Calculating statistics...')

plots_readed = len(trks)
missed_plots = len(xm)
expected_plots = plots_readed + missed_plots
if plots_readed != 0:
    PD = plots_readed / expected_plots
else: PD = 0.0
PD *= 100
PD = float("%.2f" % PD)

for e in range(len(delta_t_plots)):
    delta_t_plots[e] = 1000 * float(delta_t_plots[e])
for i in range(len(delta_t_SUC)):
    delta_t_SUC[i] = 1000 * float(delta_t_SUC[i])

CHN_inAnalysis = 1
CHN_inAnalysis = (sum(CHN)/len(CHN))
# print(CHN_inAnalysis)
# print(round(CHN_inAnalysis))


suc_delay_mean = sum(delta_t_SUC)/len(delta_t_SUC)
suc_delay_mean = float("%.2f" % suc_delay_mean)
suc_delay_max = float(max(delta_t_SUC))
notes = ' '

date = str('2015-' + filename[-16:-14] + '-' + filename[-13:-11] + ' ' + filename[-10:-8] + ':00')
# print(date)




statistics = [date, PD, plots_readed, expected_plots, missed_plots,
              plots_outof_bounds, suc_delay_mean, suc_delay_max, CHN_inAnalysis, notes]

print(' _______________________________________________________________')
print('| Analysis results:')
print('| Missed plots: %s ' % missed_plots)
print('| Total plots: %s  ' % plots_readed)
print('| Expected plots: %s' % expected_plots)
print('| P.D. = %.2f %%' % PD)
print('| RPS number = %.2f ' % CHN_inAnalysis)
print('| SUC mean delay: %.2f ms' % suc_delay_mean)
print('| SUC max delay: %.2f ms' % suc_delay_max)
print('|_______________________________________________________________')

if debug_level and options.insert_stats:
    print('Saving statistics to statistics.csv file...')

    reader = csv.reader(open('statistics.csv'), delimiter=",")
    f.close()

    stat_list = sorted(reader, key=operator.itemgetter(0), reverse=True)

    stat_list.append(statistics)

    stat_list = sorted(stat_list, key=operator.itemgetter(0), reverse=True)


    fstat_csv = open('statistics.csv', 'w+', newline='')
    stat_csv_row = stat_list
    output_writer = csv.writer(fstat_csv, delimiter=',')
    output_writer.writerows(stat_csv_row)
    f.close()

# sys.exit("No plotting... stopping now")



"""_____________________________________________________________________________________________________________________

gps_eval()

testing gps plotting, read the gps tracks from the ascii file and store them in two arrays...

TODO: -add option to evaluate gps tracks to switch on/off this function... DONE!
TODO: evaluate the acurate... in a few days...
________________________________________________________________________________________________________________________
"""
if options.gps_eval:

    smr_latlon = [28.477493 , -16.332522] # [28.477493, -16.332524]
    # mlat_latlon = [28.482653, -16.341537] #28.2858, -16.2030]
    coord = CoordTranslator()
    smr_xy = coord.LLtoUTM(smr_latlon)[2:4]
    # mlat_xy = coord.LLtoUTM(mlat_latlon)[2:4]
    #
    # print(coord.LLtoUTM(smr_latlon))
    # print(smr_xy)
    # print(mlat_xy)
    # delta_x = mlat_xy[0] - smr_xy[0]
    # delta_y = mlat_xy[1] - smr_xy[1]
    # print(delta_x, delta_y)

    gps_lat, gps_lon, timegps = [], [], []
    i = 0
    print('Reading gps track points from file...')
    for r in  csv.reader(open(options.gps_filename), delimiter='\t'):
        gps_lat = gps_lat + [float(r[1])]
        gps_lon = gps_lon + [float(r[2])]
        #timegps = timegps + [(datetime.datetime.strptime(' '+ r[5], " %H %M %S.%f "))]
        timegps = timegps + [(datetime.datetime.strptime(' '+ r[5] + ' ', " %H %M %S.%f "))]

    print('Total gps points: ', len(lat))
    # print(lat[1], lon[1], timegps[1])
    # print((timegps[22]- timegps[21])*2.5)

    gps_trkx, gps_trky = [], []
    for e in range(len(gps_lat)):
        gps_trkx = gps_trkx + [coord.LLtoUTM([gps_lat[e], gps_lon[e]])[2]]
        gps_trky = gps_trky + [coord.LLtoUTM([gps_lat[e], gps_lon[e]])[3]]

    # print(gps_trkx[0:5], gps_trky[0:5])

    if debug_level: print('centering gps tracks to smr coords...')
    for e in range(len(gps_trkx)):
        gps_trkx[e] -= smr_xy[0]
        gps_trky[e] -= smr_xy[1]

    # if eval_mode == 'mlat':
    #     if debug_level: print('evaluating mlat, centering plots in ARP coords...')
    #     for e in range(len(gps_trkx)):
    #         gps_trkx[e] -= mlat_xy[0]
    #         gps_trky[e] -= mlat_xy[1]


"""_____________________________________________________________________________________________________________________

Center the mlat plots to the airport ARP and/or SMR coords...
________________________________________________________________________________________________________________________
"""
Kx = 0.9999
Ky = 0.9998
theta = -0.6488 * 2 * math.pi / 360   #0.6380 translation theta....?????


if eval_mode == 'smr':
    # Kx = 0.9999
    # Ky = 0.9998
    # theta = -0.6488 * 2 * math.pi / 360   #0.6380 translation theta....?????


    for track in range(len(tracks_X)):
        for e in range(len(tracks_X[track])):
            tracks_X[track][e] = float(tracks_X[track][e]) #+ delta_x
            tracks_Y[track][e] = float(tracks_Y[track][e]) #+ delta_y
            temp1 = tracks_X[track][e]*math.cos(theta)-tracks_Y[track][e]*math.sin(theta)
            temp2 = tracks_X[track][e]*math.sin(theta)+tracks_Y[track][e]*math.cos(theta)
            tracks_X[track][e] = temp1 * Kx
            tracks_Y[track][e] = temp2 * Ky


# centering the missed...
for e in range(len(xm)):
    temp1 = xm[e]*math.cos(theta)-ym[e]*math.sin(theta)
    temp2 = xm[e]*math.sin(theta)+ym[e]*math.cos(theta)
    xm[e] = temp1 * Kx
    ym[e] = temp2 * Ky


if eval_mode == 'mlat':
    smr_latlon = [28.477493, -16.332522] # [28.477493, -16.332524]
    mlat_latlon = [28.482653, -16.341537] #[28.482653, -16.341537]

    coord = CoordTranslator()

    smr_xy, mlat_xy = [], []

    smr_xy.append(int(coord.LLtoUTM(smr_latlon)[2]))
    smr_xy.append(int(coord.LLtoUTM(smr_latlon)[3]))

    mlat_xy.append(int(coord.LLtoUTM(mlat_latlon)[2]))
    mlat_xy.append(int(coord.LLtoUTM(mlat_latlon)[3]))

    print('MLAT center: ', mlat_xy)
    print('SMR center: ', smr_xy)
    #print(mlat_xy)
    delta_x = mlat_xy[0] - smr_xy[0]
    delta_y = mlat_xy[1] - smr_xy[1]
    #print(delta_x, delta_y)

    if debug_level: print('centering mlat cartesian x/y to smr coords...')

    Kx = 0.9999
    Ky = 0.9998
    theta = -0.6488 * 2 * math.pi / 360   #0.6380 translation theta....?????

    for track in range(len(tracks_X)):
        for e in range(len(tracks_X[track])):
            if tracks_X[track][e] != '': 
              tracks_X[track][e] = float(tracks_X[track][e]) #+ delta_x
              tracks_Y[track][e] = float(tracks_Y[track][e]) #+ delta_y
              temp1 = tracks_X[track][e]*math.cos(theta)-tracks_Y[track][e]*math.sin(theta)
              temp2 = tracks_X[track][e]*math.sin(theta)+tracks_Y[track][e]*math.cos(theta)
              tracks_X[track][e] = temp1 * Kx
              tracks_Y[track][e] = temp2 * Ky


              tracks_X[track][e] = float(tracks_X[track][e]) + delta_x
              tracks_Y[track][e] = float(tracks_Y[track][e]) + delta_y


            else: print(tracks_X[track][e])   # <---------------------------------DEBUGGING



    if debug_level: print('converting mlat geodetic lat/lon to UTM and centering to smr coords...')

    tracks_mlat_X, tracks_mlat_Y = tracks_lat, tracks_lon # just to fill the arrays...

    delta_theta = []

    for track in range(len(tracks_lat)):
    #for track in range(10):
        for e in range(len(tracks_lat[track])):
          try:
            temp1 = [float(tracks_lat[track][e]), float(tracks_lon[track][e])]
            temp2 = (coord.LLtoUTM(temp1))
            tracks_mlat_X[track][e] = int(temp2[2])
            tracks_mlat_Y[track][e] = int(temp2[3])

            # tracks_mlat_X[track][e] -= mlat_xy[0]
            # tracks_mlat_Y[track][e] -= mlat_xy[1]

            tracks_mlat_X[track][e] -= smr_xy[0]
            tracks_mlat_Y[track][e] -= smr_xy[1]
          except: print("tracks_lat[track][e]:", tracks_lat[track][e])

            # if (tracks_mlat_X[track][e] != 0) and (tracks_Y[track][e] != 0):
            #     delta_theta.append(math.atan(tracks_mlat_Y[track][e]/tracks_mlat_X[track][e]) -
            #                   math.atan(tracks_Y[track][e]/tracks_Y[track][e]))

    # print(max(delta_theta))
    # print(min(delta_theta))
    # print(sum(delta_theta)/len(delta_theta))
    #
    # f, (ax1, ax2) = plt.subplots(2, sharex=True)
    # ax1.hist(delta_theta, bins=100, color='r', normed=1, stacked=1)
    # plt.show()

"""_____________________________________________________________________________________________________________________

Plotting()

plot plots and delay histograms(if it's a gps recording)
________________________________________________________________________________________________________________________
"""

inches = 16
fig, plotXY = plt.subplots(1,1, figsize=(inches, inches/1.7778))
# plotXY.set_title(filename[-17:])
fig.suptitle('Plots display '+filename[-17:], fontsize=15, fontweight='bold')


# plot the base map, dxf file...
if options.display_map:
    if debug_level: print('Plotting the base map...')
    dxf = dxfgrabber.readfile('plano_smr_nov_14.dxf')

    # print("time to read: {:.2f}s".format(endtime-starttime))
    # print("entities: {:d}".format(len(dxf.entities)))
    # print("defined Layers: {}".format(len(dxf.layers)))
    # print_layers(Counter(entity.layer for entity in dxf.entities))

    all_lines = [entity for entity in dxf.entities if entity.dxftype == 'LINE']
    # print(len(all_lines))
    polylines = [entity for entity in dxf.entities if entity.dxftype == 'LWPOLYLINE']
    # print(len(polylines))

    arcs = [entity for entity in dxf.entities if entity.dxftype == 'ARC']
    # print((arcs[0].center))

    for i in range(len(polylines)):
        lines_x = []
        lines_y = []
        for j in range(len(polylines[i])):
            # print(polylines[i].points[j])

            lines_x.append(polylines[i].points[j][0])
            lines_y.append(polylines[i].points[j][1])
            # print(lines_x)

        plt.plot(lines_x,lines_y, marker='None', mfc='None', mec='b',linestyle='-',lw=.7, color='g', ms=6, alpha = 0.5)

    for i in range(len(all_lines)):
        lines_x = []
        lines_y = []
        # print(all_lines[i].start,all_lines[i].end)
        lines_x.append(all_lines[i].start[0])
        lines_y.append(all_lines[i].start[1])
        lines_x.append(all_lines[i].end[0])
        lines_y.append(all_lines[i].end[1])

        plt.plot(lines_x,lines_y, marker='None', mfc='None', mec='b',linestyle='-',lw=.7, color='k', ms=6, alpha=0.2)
        # plt.plot(0,0, marker = '^')


"""_____________________________________________________________________________________________________________________


________________________________________________________________________________________________________________________
"""

if debug_level: print('Plotting the tracks...')

# inches = 16
# fig, plotXY = plt.subplots(1,1, figsize=(inches, inches/1.7778))

for track in range(len(tracks_X)):

    plt.plot(tracks_X[track][:], tracks_Y[track][:], marker='None', mfc='None', mec='b',linestyle='-',
             lw=.7, color='y', ms=6) # plot the lines between points

    plt.plot(tracks_X[track][0:1], tracks_Y[track][0:1], marker='^', mfc='g', mec='k',linestyle='-',
             lw=.7, color='r', ms=6) #init of track

    plt.plot(tracks_X[track][1:-1], tracks_Y[track][1:-1], marker='^', mfc='w', mec='b',linestyle='-',
             lw=.7, color='y', ms=6) # plot track by track

    plt.plot(tracks_X[track][-1:], tracks_Y[track][-1:], marker='^', mfc='y', mec='k',linestyle='-',
             lw=.7, color='r', ms=6) # end of track


if eval_mode == 'mlat':
    for track in range(len(tracks_X)):

        plt.plot(tracks_mlat_X[track][:], tracks_mlat_Y[track][:], marker='None', mfc='None', mec='b',linestyle='-',
                 lw=.7, color='k', ms=6) # plot the lines between points

        plt.plot(tracks_mlat_X[track][0:1], tracks_mlat_Y[track][0:1], marker='+', mfc='g', mec='k',linestyle='-',
                 lw=.7, color='r', ms=6) #init of track

        plt.plot(tracks_mlat_X[track][1:-1], tracks_mlat_Y[track][1:-1], marker='+', mfc='w', mec='b',linestyle='-',
                 lw=.7, color='k', ms=6) # plot track by track

        plt.plot(tracks_mlat_X[track][-1:], tracks_mlat_Y[track][-1:], marker='+', mfc='y', mec='k',linestyle='-',
                 lw=.7, color='r', ms=6) # end of track


plt.plot(0, 0, marker='^', mfc='None', mec='b', linestyle='-', lw=.7, color='y', ms=6, label='Measured Plots')
plt.plot(0, 0, marker='^', mfc='g', mec='k', linestyle='-', lw=.7, color='y', ms=6, label='Start of track')
plt.plot(0, 0, marker='^', mfc='y', mec='k', linestyle='-', lw=.7, color='y', ms=6, label='End of track')
plt.plot(0, 0, marker='^', mfc='r', mec='k', linestyle='-', lw=.7, color='y', ms=6, label='Calculated missed plots')
plt.plot(0, 0, marker='^', mfc='w', mec='w', linestyle='None', ms=10)
plt.plot(0, 0, marker='*', mfc='k', mec='k', lw=2.0, linestyle='None', ms=8, label='SMR')
if options.gps_eval: plt.plot(0, 0, marker='+', mfc='None', mec='k',linestyle='-',lw=.7, color='k', ms=6, label='GPS tracks')


if debug_level: print('Plotting the missed plots...')

plt.plot(xm, ym, marker='^', mfc='r', mec='b', linestyle='None', lw=0.7, color='r', ms=6)


"""_____________________________________________________________________________________________________________________

plot gps data

TODO: add option to switch on/off this piece of code...

________________________________________________________________________________________________________________________
"""
#plt gps tracks...

if options.gps_eval:
    if debug_level:
        print('Plotting the gps tracks...')
    plt.plot(gps_trkx, gps_trky, marker='+', mfc='None', mec='k',linestyle='-',lw=.7, color='k', ms=6)

"""_____________________________________________________________________________________________________________________
"""

# if eval_mode == 'mlat':
#     if debug_level: print('mlat eval mode: centering plots in mlat coords')
#     for e in range(len(x)):
#         tracks_X[e] =tracks_X[e]-delta_x
#         tracks_Y[e] =tracks_Y[e]-delta_y


plotXY.set_xlim((-2750, 1050)) #-3000, 800))
plotXY.set_ylim((-500, 1500))
if eval_mode == 'mlat':
    plotXY.set_xlim((-1900*15, 1900*15)) #-3000, 800))
    plotXY.set_ylim((-1000*15, 1000*15))
# Only draw spine between the y-ticks
plotXY.spines['left'].set_bounds(-1, 1)
# Hide the right and top spines
plotXY.spines['right'].set_visible(False)
plotXY.spines['top'].set_visible(False)
# Only show ticks on the left and bottom spines
plotXY.yaxis.set_ticks_position('left')
plotXY.xaxis.set_ticks_position('bottom')
plt.grid(True)
plotXY.set_aspect('equal', None, None)



textstr = 'Plots missed = %s' \
          '\nExpected plots = %s' \
          '\nMeassured plots = %s' \
          '\nP.D. = %.2f %%' \
          '\nSUC mean delay = %.2f ms' % (missed_plots,expected_plots, plots_readed, PD, suc_delay_mean)



legend = plt.legend(numpoints=1, prop={'size': 10}, fancybox=1)   # <-------------------------------------------------

frame = legend.get_frame()
frame.set_facecolor('k')
frame.set_alpha(0.3)


props = dict(boxstyle='round', facecolor='k', alpha=0.3)

plt.text(0.01, 0.02, textstr, ha='left', va='bottom', transform=plotXY.transAxes, fontsize=10, bbox=props)

# bb = legend.legendPatch.get_bbox().inverse_transformed(plotXY.transAxes)

# print(bb.x0)

# Add text relative to the location of the legend.
# plt.text(1.025 + bb.x0, 0.97 + bb.y0 , textstr, ha='left', va='top', transform=plotXY.transAxes, fontsize=10, bbox=props)



# left, width = .12, .5
# bottom, height = .12, .5
#plt.text(left, bottom, textstr, ha='left', va='top', transform=plotXY.transAxes, fontsize=10, bbox=props)
#plt.text(textstr, xy=(0, 1), xytext=(12, -12), va='top', xycoords='axes fraction', textcoords='offset points', fontsize=10)
#plt.text(left, bottom, textstr, ha='left', va='top', transform=plotXY.transAxes, fontsize=10, bbox=props)



plt.tight_layout(1.5)


plt.savefig(filename + '.pdf')

# plt.savefig(filename + '.png')

########################################################################################################################
# If gps file: plot histogram of plots delay and SUC delays...
if gps and options.delay_analy:
    f, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(inches, inches/1.7778))
    ax1.hist(delta_t_plots, bins=100, color='r', histtype='stepfilled', normed=1, stacked=1)
    ax1.set_title('Plots time delay histogram')
    ax2.set_title('SUC and Status message delay histogram')
    ax2.hist(delta_t_SUC, bins=100, color='r', histtype='stepfilled', normed=1, stacked=1)
    # Fine-tune figure; make subplots close to each other and hide x ticks for
    # all but bottom plot.
    # f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
    ax1.grid(True)
    ax2.grid(True)

    if debug_level: print('Saving SUC delay histogram to graphic file...')
    plt.savefig(filename + '_SUC_delay.pdf')
    # plt.savefig(filename + '_SUC_delay.png')


    #plot the delays vs time, just to display some delays problems in RPS (2015/02/09)
    d, dx = plt.subplots(1, figsize=(inches, inches/1.7778))
    dx.plot(delta_t_SUC)
    dx.plot(delta_t_plots)
    dx.grid(True)
    dx.set_title('Delays vs time')


if debug_level: print('Execution time: %s' % (time.time() - secs))




########################################################################################################################
# plt.tight_layout(1.5)

if batch_mode:
    print('Batch mode ON, so not plotting graphics...')
else:
    plt.show()

if debug_level: print('Program ended normally!')


# [plt.plot(data[0],data[x]) for x in range(1,len(data[:,0]))]

# plot the statistics file


