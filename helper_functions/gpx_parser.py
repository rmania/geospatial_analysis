# credits https://github.com/tkrajina/gpxpy/blob/master/gpxinfo
#!/usr/bin/env python

import sys 
import logging 
import math 
import argparse

def format_time(time_s):
    if not time_s:
        return 'n/a'
    else:
        minutes = math.floor(time_s / 60.)
        hours = math.floor(minutes / 60.)
        return '%s:%s:%s' % (str(int(hours)).zfill(2), str(int(minutes % 60)).zfill(2), str(int(time_s % 60)).zfill(2))


def format_long_length(length):
    return '{:.3f}km'.format(length / 1000.)


def format_short_length(length):
    return '{:.2f}m'.format(length)


def format_speed(speed):
    if not speed:
        speed = 0
    else:
        return '{:.2f}m/s = {:.2f}km/h'.format(speed, speed * 3600. / 1000.)


def print_gpx_part_info(gpx_part, indentation='    '):
    """
    gpx_part may be a track or segment.
    """
    length_2d = gpx_part.length_2d()
    length_3d = gpx_part.length_3d()
    print('%sLength 2D: %s' % (indentation, format_long_length(length_2d)))
    print('%sLength 3D: %s' % (indentation, format_long_length(length_3d)))

    moving_time, stopped_time, moving_distance, stopped_distance, max_speed = gpx_part.get_moving_data()
    avg_speed = moving_distance / moving_time
    print('%sMoving time: %s' % (indentation, format_time(moving_time)))
    print('%sStopped time: %s' % (indentation, format_time(stopped_time)))
    print('%sMax speed: %s' % (indentation, format_speed(max_speed)))
    print('%sAvg speed: %s' % (indentation, format_speed(avg_speed)))

    uphill, downhill = gpx_part.get_uphill_downhill()
    print('%sTotal uphill: %s' % (indentation, format_short_length(uphill)))
    print('%sTotal downhill: %s' % (indentation, format_short_length(downhill)))

    start_time, end_time = gpx_part.get_time_bounds()
    print('%sStarted: %s' % (indentation, start_time))
    print('%sEnded: %s' % (indentation, end_time))

    points_no = len(list(gpx_part.walk(only_points=True)))
    print('%sPoints: %s' % (indentation, points_no))

    if points_no > 0:
        distances = []
        previous_point = None
        for point in gpx_part.walk(only_points=True):
            if previous_point:
                distance = point.distance_2d(previous_point)
                distances.append(distance)
            previous_point = point
        print('%sAvg distance between points: %s' % (indentation, format_short_length(sum(distances) / len(list(gpx_part.walk())))))

    print('')


def print_gpx_info(gpx, gpx_file):
    print('File: %s' % gpx_file)

    if gpx.name:
        print('  GPX name: %s' % gpx.name)
    if gpx.description:
        print('  GPX description: %s' % gpx.description)
    if gpx.author_name:
        print('  Author: %s' % gpx.author_name)
    if gpx.author_email:
        print('  Email: %s' % gpx.author_email)

    print_gpx_part_info(gpx)

    for track_no, track in enumerate(gpx.tracks):
        for segment_no, segment in enumerate(track.segments):
            print('    Track #%s, Segment #%s' % (track_no, segment_no))
            print_gpx_part_info(segment, indentation='        ')


def run(gpx_files):
    if not gpx_files:
        print('No GPX files given')
        sys.exit(1)

    for gpx_file in gpx_files:
        try:
            gpx = mod_gpxpy.parse(open(gpx_file))
            print_gpx_info(gpx, gpx_file)
        except Exception as e:
            logging.exception(e)
            print('Error processing %s' % gpx_file)
            sys.exit(1)


def make_parser():
    parser = argparse.ArgumentParser(usage='%(prog)s [-s] [-m] [-d] [file ...]',
        description='Command line utility to extract basic statistics from gpx file(s)')
    parser.add_argument('-s', '--seconds', action='store_true',
                        help='print times as N seconds, rather than HH:MM:SS')
    parser.add_argument('-m', '--miles', action='store_true',
                        help='print distances and speeds using miles and feet')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='show detailed logging')
    return parser