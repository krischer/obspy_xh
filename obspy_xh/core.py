#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
XH file support for ObsPy.

:copyright:
    Lion Krischer (lion.krischer@googlemail.com), 2015
:license:
    MIT
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import io
import struct

import obspy
from obspy.core import AttribDict
from obspy.core.util.obspy_types import CustomComplex
from obspy.station.response import (InstrumentSensitivity, Response,
                                    PolesZerosResponseStage)
import numpy as np


from . import header_0_98


def detect_format_version_and_endianness(filename):
    """
    Detects the format version and byte order. Will return False if the file
    is not an XH file.

    :param filename: The file to check.
    :type filename: str
    """
    with io.open(filename, "rb") as fh:
        version = fh.read(4)
        fh.seek(4, 1)
        byte_order_test_int = fh.read(4)

    if len(version) != 4 or len(byte_order_test_int) != 4:
        return False

    # Detect byte order.
    if struct.unpack("<i", byte_order_test_int)[0] == 12345678:
        # Little endian.
        bo = "<"
    elif struct.unpack(">i", byte_order_test_int)[0] == 12345678:
        # Big endian.
        bo = ">"
    else:
        # Not an XH file.
        return False

    version = str(struct.unpack(bo + "f", version)[0])[:4]
    # Only version 0.98 is currently supported.
    if version != "0.98":
        return False
    return {"byte_order": bo, "format_version": version}


def is_xh(filename):
    """
    Detects if the given file is an XH file.

    :param filename: The file to check.
    :type filename: str
    """
    info = detect_format_version_and_endianness(filename)
    if info is False:
        return False
    return True


def read_xh(filename):
    """
    Reads the given file to an ObsPy Stream object.

    :param filename: The file to read.
    :type filename: str
    """
    info = detect_format_version_and_endianness(filename)

    # Dispatch based on the XH format version.
    if info["format_version"] == "0.98":
        return read_xh_0_98(filename, info["byte_order"])
    else:
        raise NotImplementedError


def read_xh_0_98(filename, byte_order):
    """
    Reads the given file to an ObsPy Stream object for the XH format version
    0.98.

    :param filename: The file to read.
    :type filename: str
    """
    st = obspy.Stream()

    with io.open(filename, "rb") as fh:
        while True:
            header = fh.read(1024)
            if len(header) < 1024:
                break
            header = np.frombuffer(
                header, dtype=header_0_98.get_header_dtype(byte_order))
            header = _record_array_to_dict(header)

            # Convert both times.
            ref_origin_time = obspy.UTCDateTime(
                header["ot_year"],
                header["ot_month"],
                header["ot_day"],
                header["ot_hour"],
                header["ot_minute"],
                header["ot_second"])
            starttime = obspy.UTCDateTime(
                header["tstart_year"],
                header["tstart_month"],
                header["tstart_day"],
                header["tstart_hour"],
                header["tstart_minute"],
                header["tstart_second"])

            data = np.frombuffer(fh.read(header["ndata"] * 4),
                                 dtype=byte_order + "f4")

            tr = obspy.Trace(data=data)
            tr.stats.network = header["netw"]
            tr.stats.station = header["stnm"]
            tr.stats.channel = header_0_98.CHANNEL_MAP[header["chid"]]
            tr.stats.location = header_0_98.LOCATION_MAP[header["locc"]]
            # The name 'delta' for the sampling rate is a bit odd but it
            # appears to be interpreted correctly here.
            tr.stats.sampling_rate = header["delta"]
            tr.stats.starttime = starttime

            # Build the instrument response.
            # XXX: The instrument response definition in XH is very basic and
            # so the definition is not complete and might not work with ObsPy.
            response = Response()
            sensitivity = InstrumentSensitivity(
                # Random choice, but not really used by anything so it should
                # be ok.
                frequency=1.0,
                # Assume the DS field is the total sensitivity.
                value=header["DS"],
                # This is true for most commonly used instruments.
                input_units="M/S",
                output_units="COUNTS")
            paz = PolesZerosResponseStage(
                stage_sequence_number=1,
                # We assume DS is somehow the total sensitivity. As we have
                # only one stage we also make it he gain of this stage.
                stage_gain_frequency=1.0,
                stage_gain=header["DS"],
                input_units="M/S",
                output_units="V",
                pz_transfer_function_type="LAPLACE (RADIANS/SECOND)",
                # Arbitrary frequency. Usually 1 for most instruments. Must be
                # correct to assure everything works as expected!
                normalization_frequency=1.0,
                normalization_factor=header["A0"],
                zeros=[CustomComplex(_i) for _i in header["zero"]],
                poles=[CustomComplex(_i) for _i in header["pole"]])
            response.instrument_sensitivity = sensitivity
            response.response_stages.append(paz)
            # Attach to trace object.
            tr.stats.response = response

            # Assemble XH specific header.
            xh_header = AttribDict()
            xh_header.reference_time = ref_origin_time
            xh_header.source_latitude = header["elat"]
            xh_header.source_longitude = header["elon"]
            xh_header.source_depth_in_km = header["edep"]
            xh_header.source_body_wave_magnitude = header["Mb"]
            xh_header.source_surface_wave_magnitude = header["Ms"]
            xh_header.source_moment_magnitude = header["Mw"]
            xh_header.receiver_latitude = header["slat"]
            xh_header.receiver_longitude = header["slon"]
            xh_header.receiver_elevation_in_m = header["elev"]
            xh_header.sensor_azimuth = header["azim"]
            xh_header.sensor_inclination = header["incl"]
            xh_header.maximum_amplitude = header["maxamp"]
            xh_header.waveform_quality = header["qual"]
            # XXX: Should this be applied to the seismogram start time?
            xh_header.static_time_shift_in_sec = header["tshift"]
            xh_header.comment = header["rcomment"]
            xh_header.event_code = header["evtcd"]
            xh_header.cmt_code = header["cmtcd"]
            xh_header.phase_picks = header["tpcks"]
            xh_header.floats = header["flt"]
            xh_header.integers = header["intg"]
            xh_header.waveform_type = header["wavf"]

            tr.stats.xh = xh_header

            st.traces.append(tr)

    return st


def _record_array_to_dict(rec_array):
    """
    Helper function converting a record array to a simple to use dictionary.
    """
    ret_val = {}
    for name in rec_array.dtype.names:
        if name == "padding":
            continue
        value = rec_array[name][0]

        # A bit of a hack to convert to native Python types. There is probably
        # a better way.
        if value.shape:
            ret_val[name] = value
        elif str(value.dtype).startswith("float"):
            ret_val[name] = float(value)
        elif str(value.dtype).startswith("int"):
            ret_val[name] = int(value)
        elif value.dtype.kind == "S":
            value = value.split(b"\x00")[0].decode()
            if value == 'null':
                value = None
            ret_val[name] = value
        else:
            raise NotImplementedError
    return ret_val


def write_xh(st, filename):
    pass
