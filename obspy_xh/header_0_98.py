#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Header definitions for XH Version 0.98.

:copyright:
    Lion Krischer (lion.krischer@googlemail.com), 2015
:license:
    The MIT License (MIT)
"""
import numpy as np

# Define headers.
X_VERSION = 0.98

X_HDRSIZE = 1024
I_12345678 = 12345678
F_12345678 = 12345678.0

XH_NPTS = 131072

NPCKS = 20
NOCALPTS = 30
CHARSIZE = 8
COMMENTSIZE = 72
NCMT = 14
NPADS = 34

CHANNEL_MAP = {
    # Not a seismogram.
    0: "",
    1: "Z",
    2: "N",
    3: "E",
    4: "R",
    5: "T"}

LOCATION_MAP = {
    9: "",
    0: "00",
    1: "10",
    2: "20",
    3: "30",
    4: "40",
    5: "50"}


def get_header_dtype(byte_order):
    """
    Specify the byte order and get the dtype suitable for using in a structured
    numpy array.
    """
    dtype = [
        # float   version;      /* format version #             */
        ("version", byte_order + "f4"),

        # int     nhdr;           /* # of bytes in header         */
        ("nhdr", byte_order + "i4"),

        # int     i12345678;      /* byte-order test int          */
        ("i12345678", byte_order + "i4"),

        # float   elat;           /* source latitude (degs)       */
        ("elat", byte_order + "f4"),

        # float   elon;           /* source longitude (degs)      */
        ("elon", byte_order + "f4"),

        # float   edep;           /* source depth                 */
        ("edep", byte_order + "f4"),

        # float   Mb;             /* Mb                           */
        ("Mb", byte_order + "f4"),

        # float   Ms;             /* Ms                           */
        ("Ms", byte_order + "f4"),

        # float   Mw;             /* Mw                           */
        ("Mw", byte_order + "f4"),

        # float   slat;           /* receiver latitude (degs)     */
        ("slat", byte_order + "f4"),

        # float   slon;           /* receiver longitude (degs)    */
        ("slon", byte_order + "f4"),

        # float   elev;           /* receiver elevation           */
        ("elev", byte_order + "f4"),

        # // Typically:
        # // Z: azim=0. inc=-90  N: azim=0 inc=0  E: azim=90 inc=0.
        # float   azim;           /* sensor alignment from north  */
        ("azim", byte_order + "f4"),

        # float   incl;           /* sensor inclination from hori */
        ("incl", byte_order + "f4"),

        # struct  xhtime  ot;     /* ref/origin time (sec)        */
        ("ot_year", byte_order + "i4"),
        ("ot_month", byte_order + "i4"),
        ("ot_day", byte_order + "i4"),
        ("ot_hour", byte_order + "i4"),
        ("ot_minute", byte_order + "i4"),
        ("ot_second", byte_order + "f4"),

        # struct  xhtime  tstart; /* seismogram start time (sec)  */
        ("tstart_year", byte_order + "i4"),
        ("tstart_month", byte_order + "i4"),
        ("tstart_day", byte_order + "i4"),
        ("tstart_hour", byte_order + "i4"),
        ("tstart_minute", byte_order + "i4"),
        ("tstart_second", byte_order + "f4"),

        # int     ndata;          /* number of samples            */
        ("ndata", byte_order + "i4"),

        # float   delta;          /* sample rate: sample/sec      */
        ("delta", byte_order + "f4"),

        # float   tshift;         /* static time shift (sec)      */
        ("tshift", byte_order + "f4"),

        # float   maxamp;         /* maximum amplitude            */
        ("maxamp", byte_order + "f4"),

        # int     qual;           /* waveform quality             */
        ("qual", byte_order + "i4"),

        # int     chid;           /* channel id
        #                         0= NOT A SEISMOGRAM
        #                         1= vertical
        #                         2= north-south
        #                         3= east-west
        #                         4= radial
        #                         5= transverse                    */
        ("chid", byte_order + "i4"),

        # int     locc;           /* location code
        #                         9 =  ""
        #                         0 =  "00"
        #                         1 =  "10"
        #                         2 =  "20"
        #                         3 =  "30"
        #                         4 =  "40"
        #                         5 =  "50"                       */
        ("locc", byte_order + "i4"),

        # complx pole[NOCALPTS];        /* instrument poles     */
        ("pole", byte_order + "c8", NOCALPTS),

        # complx zero[NOCALPTS];        /* instrument zeroes    */
        ("zero", byte_order + "c8", NOCALPTS),

        # float   DS;
        ("DS", byte_order + "f4"),

        # float   A0;
        ("A0", byte_order + "f4"),

        # float   f12345678;            /* byte-order test flt  */
        ("f12345678", byte_order + "f4"),

        # float   tpcks[NPCKS];         /* phase picks  */
        ("tpcks", byte_order + "f4", NPCKS),

        # float   flt[NPCKS];           /* floats               */
        ("flt", byte_order + "f4", NPCKS),

        # int     intg[NPCKS];          /* integers             */
        ("intg", byte_order + "i4", NPCKS),

        # char    cmtcd[NCMT];            /* cmt code             */
        ("cmtcd", np.string_, NCMT),

        # char    evtcd[CHARSIZE];        /* My evt code          */
        ("evtcd", np.string_, CHARSIZE),

        # char    netw[CHARSIZE];         /* network names        */
        ("netw", np.string_, CHARSIZE),

        # char    stnm[CHARSIZE];         /* station name         */
        ("stnm", np.string_, CHARSIZE),

        # char    chan[CHARSIZE];         /* seed channel name    */
        ("chan", np.string_, CHARSIZE),

        # char    rcomment[COMMENTSIZE];  /* record info          */
        ("rcomment", np.string_, COMMENTSIZE),

        # char    wavf[CHARSIZE];         /* waveform type:
        #                                  unprocessed:   "raw"
        #                                  displacement:  "dis"
        #                                  velocity:      "vel"
        #                                  acceleration:  "acc"  */
        ("wavf", np.string_, CHARSIZE),

        # char    padding[NPADS];   /* padding the header up to X_HDRSIZE   */
        ("padding", np.string_, NPADS)
    ]

    return np.dtype(dtype)
