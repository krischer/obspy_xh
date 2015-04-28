#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple moduling adding support for the XH format to ObsPy.
"""
from setuptools import setup


setup(
    name="obspy_xh",
    version="0.1",
    author="Lion Krischer",
    author_email="lion.krischer@googlemail.com",
    license="MIT",
    py_modules=["obspy_xh"],
    install_requires=[
        "obspy"
    ],
    # This registers the module with ObsPy.
    entry_points={
        #"obspy.plugin.waveform": [
            #"XH = obspy_xh"],
        #"obspy.plugin.waveform.XH": [
            #"isFormat = obspy_xh.xh:is_xh",
            #"readFormat = obspy_xh.xh:read_xh",
            #"writeFormat = obspy_xh.xh:write_xh",
        #]
    }
)
