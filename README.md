# XH Format Plugin for ObsPy

This module provides a plugin to add read support for XH files to [ObsPy](http://www.obspy.org). Writing is currently not supported but is easy enough to do if desired.

### Installation

Assuming ObsPy and everything is installed, grab this repository with git, and install it with `pip`. Make sure to use the `-e` flag for an editable installation.

```bash
$ git clone https://github.com/krischer/obspy_xh.git
$ cd obspy_xh
$ pip install -v -e .
```

If you ever want to update the installation, just run

```python
$ git pull
$ pip install -v -e .
```

within the repository.

### Usage

This should register the plugin with ObsPy and the normal ObsPy functionality should just work.

```python
>>> import obspy
>>> st = obspy.read("obspy_xh/tests/data/dum.xh")
>>> print(st)
6 Trace(s) in Stream:
G.CAN..T | 1994-06-09T00:33:16 - 1994-06-13T04:33:06 | 0.1 Hz, 36000 samples
G.DRV..T | 1994-06-09T00:33:16 - 1994-06-13T04:33:06 | 0.1 Hz, 36000 samples
G.ECH..T | 1994-06-09T00:33:16 - 1994-06-13T04:33:06 | 0.1 Hz, 36000 samples
G.HYB..T | 1994-06-09T00:33:16 - 1994-06-13T04:33:06 | 0.1 Hz, 36000 samples
G.INU..T | 1994-06-09T00:33:16 - 1994-06-13T04:33:06 | 0.1 Hz, 36000 samples
G.KIP..T | 1994-06-09T00:33:16 - 1994-06-13T04:33:06 | 0.1 Hz, 36000 samples
```

The response information is attached to the trace objects and (assuming the information in the XH file is sufficient), instrument response removal works using the normal ObsPy way.

```python
>>> print(st[0].stats.response)
Channel Response
	From M/S (Velocity in Meters Per Second) to COUNTS (Digital Counts)
	Overall Sensitivity: 2.5168e+09 defined at 1.000 Hz
	1 stages:
		Stage 1: PolesZerosResponseStage from M/S to V, gain: 2.5168e+09
        
# Remove response from all traces in the stream object.
>>> st.remove_response()
```

XH specific information is stored in the `stats.xh` attribute.

```python
>>> import pprint
>>> pprint.pprint(st[0].stats.xh.__dict__)
{'cmt_code': '060994A',
 'comment': None,
 'event_code': '060994A',
 'floats': array([ 0., ...], dtype=float32),
 'integers': array([0, ...], dtype=int32),
 'maximum_amplitude': 0.0,
 'phase_picks': array([-12410.68847656, ...], dtype=float32),
 'receiver_elevation_in_m': 650.0,
 'receiver_latitude': -35.32099914550781,
 'receiver_longitude': 148.99899291992188,
 'reference_time': UTCDateTime(1994, 6, 9, 0, 33, 16, 399999),
 'sensor_azimuth': 0.0,
 'sensor_inclination': 90.0,
 'source_body_wave_magnitude': 6.800000190734863,
 'source_depth_in_km': 647.0999755859375,
 'source_latitude': -13.819999694824219,
 'source_longitude': -67.25,
 'source_moment_magnitude': 8.213303565979004,
 'source_surface_wave_magnitude': 0.0,
 'static_time_shift_in_sec': 0.0,
 'waveform_quality': 0,
 'waveform_type': 'vel'}
```