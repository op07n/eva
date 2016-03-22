import pynmea2

print('Reading gps track points from file...')
# for line in csv.reader(open("TFN-20160315_drivetest.nmea"), delimiter='\t'):
with open("TFN-20160315_drivetest.nmea", "r") as nmea_file:
    for line in nmea_file:
        if line.startswith( '$GNGGA' ) :
            # lat, _, lon = line.strip().split(',')[2:5]
            # try :
            #     lat = float( lat )
            #     lon = float( lon )
            # except :
            #     # something wrong happens with your data, print some error messages
            #     pass
            print line
            msg = pynmea2.parse(line)
            print msg.timestamp
            print float(msg.lat)/100
            print float(msg.lon)/100
            print msg.gps_qual
