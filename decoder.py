__author__ = 'angelvidal'


import numpy as numpy


"""_____________________________________________________________________________________________________________________

FUNCTIONS below this line!
________________________________________________________________________________________________________________________
"""


"""_____________________________________________________________________________________________________________________

Asterix decoding code.
TODO :
1.- end cat10 decoder code
2.- write cat21 decoder for SMMS
3.- write cat 1 decode (for conventional SSR/PSR)? by now stand by... relax and end the first part
________________________________________________________________________________________________________________________
"""


def read_fspec(frame):
    """
    read the fspec byte(s) from the frame passed to the function
    :param frame:
    :return fspec:
    """
    offset = 3
    fspec = numpy.array([frame[3]], dtype=numpy.uint8)
    offset += 1
    if (fspec[0] & 1):
        fspec = numpy.append(fspec, frame[4])
        offset += 1
        if (fspec[1] & 1):
            fspec = numpy.append(fspec, frame[5])
            offset += 1
            if (fspec[2] & 1):
                fspec = numpy.append(fspec, frame[6])
                offset += 1
                if (fspec[3] & 1):
                    fspec = numpy.append(fspec, frame[7])
                    offset += 1
                    if (fspec[4] & 1):
                        fspec = numpy.append(fspec, frame[8])
                        offset += 1
    return fspec, offset


def decode_cat21(frame):
    """
    Function to decode frames Asterix cat21

    ***************************************       Pending to develop/write      ****************************************

    :param frame:
    :return: csv file with decoded frames and csv with decoded frames sorted by track number


    """
    return None


def decode_TYPE10(frame, offset):
    """
    Decode cat10 type of message.
    :param frame: cat10 frame to decode
    :param offset: offset from head of frame to the byte of interest
    :return: message type string and offset
    """
    type10 = numpy.array([frame[offset]], dtype=numpy.int8)
    offset += 1
    if type10 == 1:
        return 'Target Report', offset
    elif type10 == 2:
        return 'Start of Update Cycle', offset
    elif type10 == 3:
        return 'Periodic Status Message', offset
    elif type10 == 4:
        return 'Event-triggered Status Message', offset
    else:
        return 'Unknown', offset


def decode_IDEN(frame, offset):
    """
    Decode data source SIC and SAC
    :param frame
    :param offset
    :return: SIC / SAC and offset
    """
    SAC = numpy.array([frame[offset]], dtype=numpy.uint8)
    offset += 1
    SIC = numpy.array([frame[offset]], dtype=numpy.uint8)
    offset += 1
    return int(SAC), int(SIC), offset


def decode_TRD10(frame, offset):
    """
    Decode Target Report Descriptor cat10
    :param frame:
    :param offset:
    :return: TRD
    """
    TRD10_1 = numpy.array([frame[offset]], dtype=numpy.uint8)
    offset += 1
    if TRD10_1 & 1:
        TRD10_2 = numpy.array([frame[offset]], dtype=numpy.uint8)
        offset += 1
        if TRD10_2 & 1:
            TRD10_3 = numpy.array([frame[offset]], dtype=numpy.uint8)
            offset += 1
            if TRD10_3 & 1:
                TRD10_4 = numpy.array([frame[offset]], dtype=numpy.uint8)
                offset += 1
                if TRD10_4 & 1:
                    TRD10_5 = numpy.array([frame[offset]], dtype=numpy.uint8)
                    offset += 1

    if not (TRD10_1 & 16):
        DCR = 0         # 'No differential correction (ADS-B)'
    else: DCR = 1       #'Differential correction (ADS-B)'

    if not (TRD10_1 & 8):
        CHN = 1         # 'Chain 1'
    else: CHN = 2       # 'Chain 2'

    if not (TRD10_1 & 4):
        GBS = 0         # 'Transponder Ground bit NOT set'
    else: GBS = 1       # 'Transponder Ground bit set'

    if not (TRD10_1 & 2):
        CRT = 0         # 'No Corrupted reply in multilateration'
    else: CRT = 1       # 'Corrupted reply in multilateration'

    TYP = TRD10_1 & 224
    if TYP == 0:
        TYP = 'SSR Multilateration'
    elif TYP == 32:
        TYP =  'Mode S Multilateration '
    elif TYP == 64:
        TYP = 'ADS-B'
    elif TYP == 96:
        TYP = 'PSR'
    elif TYP == 128:
        TYP = 'Magnetic Loop System'
    elif TYP == 160:
        TYP = 'HF Multilateration'
    elif TYP == 192:
        TYP = 'Not defined'
    elif TYP == 224:
        TYP = 'Other types'
    else:
        TYP = 'Unknown'

    return TYP, DCR, CHN, GBS, CRT, offset


def decode_TIME(frame, offset):
    TIMEOD = (numpy.array([frame[offset]], dtype=numpy.uint32))
    offset += 1
    TIMEOD = TIMEOD << 8
    TIMEOD = TIMEOD + (numpy.array([frame[offset]], dtype=numpy.uint32))
    offset += 1
    TIMEOD = TIMEOD << 8
    TIMEOD = TIMEOD + (numpy.array([frame[offset]], dtype=numpy.uint32))
    offset += 1
    TIMEOD = (TIMEOD / 128)
    return float(TIMEOD), offset


def decode_POS_WGS84(frame, offset):
    LAT = numpy.array([frame[offset]], dtype=numpy.int32)
    offset += 1
    LAT = LAT << 8
    LAT = LAT + numpy.array([frame[offset]], dtype=numpy.int32)
    offset += 1
    LAT = LAT << 8
    LAT = LAT + numpy.array([frame[offset]], dtype=numpy.int32)
    offset += 1
    LAT = LAT << 8
    LAT = LAT + numpy.array([frame[offset]], dtype=numpy.int32)
    offset += 1
    LON = numpy.array([frame[offset]], dtype=numpy.int32)
    offset += 1
    LON = LON << 8
    LON = LON + numpy.array([frame[offset]], dtype=numpy.int32)
    offset += 1
    LON = LON << 8
    LON = LON + numpy.array([frame[offset]], dtype=numpy.int32)
    offset += 1
    LON = LON << 8
    LON = LON + numpy.array([frame[offset]], dtype=numpy.int32)
    offset += 1
    LAT = float(LAT) * 180 / 2 ** 31
    LON = float(LON) * 180 / 2 ** 31
    return LAT, LON, offset


def decode_POS_SPOL(frame, offset):
    RHO = numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    RHO = RHO << 8
    RHO = RHO + numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    THETA = numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    THETA = THETA << 8
    THETA = THETA + numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    THETA = (float(THETA) * 360 / 2 ** 16)
    return float(RHO), THETA, offset


def decode_POS_CART(frame, offset):
    X = numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    X = X << 8
    X = X + numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    Y = numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    Y = Y << 8
    Y = Y + numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    return int(X), int(Y), offset


def decode_CTV_POL(frame, offset):
    V_RHO = numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    V_RHO = V_RHO << 8
    V_RHO = V_RHO + numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    V_THETA = numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    V_THETA = V_THETA << 8
    V_THETA = V_THETA + numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    V_THETA = (float(V_THETA) * 360 / 2 ** 16)
    return float(V_RHO), V_THETA, offset


def decode_CTV_CART(frame, offset):
    V_X = numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    V_X = V_X << 8
    V_X = V_X + numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    V_Y = numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    V_Y = V_Y << 8
    V_Y = V_Y + numpy.array([frame[offset]], dtype=numpy.int16)
    offset += 1
    return int(V_X), int(V_Y), offset


def decode_TRACK(frame, offset):
    TRACK = numpy.array([frame[offset]], dtype=numpy.uint8)
    offset += 1
    TRACK = TRACK * 256
    TRACK = TRACK + numpy.array([frame[offset]], dtype=numpy.uint8)
    offset += 1
    return int(TRACK), offset


def decode_TRACK_STATUS10(frame, offset):
    TRACK_STATUS10_1 = numpy.array([frame[offset]], dtype=numpy.int8)
    offset += 1
    if TRACK_STATUS10_1 & 1:
        TRACK_STATUS10_2 = numpy.array([frame[offset]], dtype=numpy.int8)
        offset += 1
        if TRACK_STATUS10_2 & 1:
            TRACK_STATUS10_3 = numpy.array([frame[offset]], dtype=numpy.int8)
            offset += 1
    return TRACK_STATUS10_1[0], offset


def decode_ModeA(frame, offset):
    ModeA = numpy.array([frame[offset]], dtype=numpy.uint16)
    offset += 1
    ModeA = ModeA << 8
    ModeA = numpy.array([frame[offset]], dtype=numpy.uint16)
    offset += 1
    ModeA = ModeA & 0x0fff
    return int(ModeA), offset


def decode_TADDR(frame, offset):
    TADDR = numpy.array([frame[offset]], dtype=numpy.uint32)
    offset += 1
    TADDR = TADDR << 8
    TADDR = TADDR + numpy.array([frame[offset]], dtype=numpy.uint32)
    offset += 1
    TADDR = TADDR << 8
    TADDR = TADDR + numpy.array([frame[offset]], dtype=numpy.uint32)
    offset += 1
    return hex(TADDR), offset


def decode_TID(frame, offset):
    offset += 1                     # Caution HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! <-----------------------------------
    TID_ID = numpy.array([frame[offset]], dtype=numpy.uint64)
    offset += 1
    TID_ID = TID_ID << 8
    TID_ID = TID_ID + numpy.array([frame[offset]], dtype=numpy.uint64)
    offset += 1
    TID_ID = TID_ID << 8
    TID_ID = TID_ID + numpy.array([frame[offset]], dtype=numpy.uint64)
    offset += 1
    TID_ID = TID_ID << 8
    TID_ID = TID_ID + numpy.array([frame[offset]], dtype=numpy.uint64)
    offset += 1
    TID_ID = TID_ID << 8
    TID_ID = TID_ID + numpy.array([frame[offset]], dtype=numpy.uint64)
    offset += 1
    TID_ID = TID_ID << 8
    TID_ID = TID_ID + numpy.array([frame[offset]], dtype=numpy.uint64)
    offset += 1
    STR = []
    for i in range(7):
        CH = (TID_ID >> 42 - i * 6) & 0x3f
        STR = STR + [decode_IcaoSixBitsChar(CH)]
    return 0, ''.join(STR), offset

def decode_IcaoSixBitsChar(c):
    if ((c >= 1) & (c <= 26)):
        return chr(ord('A') + c - 1)
    elif c == 32:
        return ' '
    elif ((c >= 40) & (c <= 57)):
        return chr(ord('0') + c - 48)
    else:
        return ''


# Write the following functions:________________________________________________________________________________________

def decode_ModeS(frame, offset):
    ModeS = 0
    offset = offset + 9
    return ModeS, offset


def decode_VFI(frame, offset):
    VFI = 0
    offset = offset + 1
    return VFI, offset


def decode_FL(frame, offset):
    FL = 0
    offset = offset + 2
    return FL, offset

def decode_Meas_H(frame, offset):
    MeasHeight = 0
    offset = offset +2
    return MeasHeight, offset


def decode_TSizeOri(frame, offset):
    TSize, TOri, TWidth = 0,0,0
    TSize = numpy.array([frame[offset]], dtype=numpy.int8)
    offset += 1
    if TSize & 1:
        TOri = numpy.array([frame[offset]], dtype=numpy.int8)
        offset += 1
        if TOri & 1:
            TWidth = numpy.array([frame[offset]], dtype=numpy.int8)
            offset += 1
    return int(TSize), int(TOri*360/128), int(TWidth), offset


def decode_SysStat(frame, offset):
    SysStat = numpy.array([frame[offset]], dtype=numpy.int8)
    offset + 1
    if SysStat & 128:
        NOGO = 'NOGO'
    elif SysStat & 64:
        NOGO = 'Degraded'
    else: NOGO = 'Operational'
    if SysStat & 32:
        OVL = 'Overload'
    else: OVL = 'No overload'
    if SysStat & 16:
        TSV = 'Time source INVALID'
    else: TSV = 'Time source VALID'
    if SysStat & 16:
        DIV = 'Diversity DEGRADED'
    else: DIV = 'Normal Operation'
    if SysStat & 8:
        TTF = 'Test Target Failure'
    else: TTF = 'Test Target Operative'

    return NOGO, offset #At the moment only returns NOGO...



