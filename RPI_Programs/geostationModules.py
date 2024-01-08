#       Bonas HAT Sensor Monitoring Software
#
#       based on Ian Robinson's Seismic Monitoring Software
#       http://schoolphysicsprojects.org
#
#
#        requires
#           python3, python3-obspy, matplotlib
#           sht31
# ---------------------------Notes---------------------------
#
#

from shutil import copyfile
import numpy as np
import os

from matplotlib import pyplot as plt
from globalvariablesModule import *
from obspy import UTCDateTime, Trace, Stream

import matplotlib

matplotlib.use('Agg')  # prevent use of Xwindows


def save_hourly_data_as_mseed(st, channel_no):
    start_date_time = st[0].stats.starttime

    year = str(start_date_time.year)
    month = str(start_date_time.month)
    day = str(start_date_time.day)
    hour = str(start_date_time.hour)

    save_dir = 'Data' + '/' + year + '/' + month + '/' + day
    station_info = station_info_list[channel_no]

    filename = hour + '_' + station_info + '.mseed'

    # create data Directory Structure if not already present
    try:
        os.makedirs('Data/' + year + '/')
    except OSError:
        if not os.path.isdir('Data/' + year + '/'):
            raise

    try:
        os.makedirs('Data/' + year + '/' + month + '/')
    except OSError:
        if not os.path.isdir('Data/' + year + '/' + month + '/'):
            raise

    try:
        os.makedirs('Data/' + year + '/' + month + '/' + day + '/')
    except OSError:
        if not os.path.isdir('Data/' + year + '/' + month + '/' + day + '/'):
            raise

    here = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(here, save_dir, filename)

    datafile = open(filepath, 'wb')
    st.write(datafile, format='MSEED', encoding=4, reclen=4096)
    datafile.close()


def save_weekly_data_as_mseed(st, channel_no):
    weekly_start_time = st[0].stats.starttime
    year = str(weekly_start_time.year)
    month = str(weekly_start_time.month)
    day = str(weekly_start_time.day)
    station_info = station_info_list[channel_no]

    save_dir = 'Data' + '/' + year + '/' + month + '/'

    filename = day + '_' + month + '_' + year + '_weekly_' + station_info + '.mseed'

    # create data Directory Structure if not already present
    try:
        os.makedirs('Data/' + year + '/')
    except OSError:
        if not os.path.isdir('Data/' + year + '/'):
            raise

    try:
        os.makedirs('Data/' + year + '/' + month + '/')
    except OSError:
        if not os.path.isdir('Data/' + year + '/' + month + '/'):
            raise

    here = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(here, save_dir, filename)

    datafile = open(filepath, 'wb')
    st.write(datafile, format='MSEED', encoding=4, reclen=4096)
    datafile.close()


def plot_daily(st, channel_no):
    if st[0].stats.npts > 100:
        try:
            start_time = st[0].stats.starttime
            end_time = st[0].stats.endtime
            year = str(start_time.year)
            month = str(start_time.month)
            day = str(start_time.day)

            date_string = str(year) + '-' + str(month) + '-' + str(day)
            start_hour = start_time.hour
            start_minute = start_time.minute
            time_sampled = end_time - start_time  # length of data in seconds
            graph_start = float(start_hour) + float(start_minute / 60)
            graph_end = graph_start + (time_sampled / 3600.0)
            updated = UTCDateTime().strftime("%A, %d. %B %Y %H:%M%p")
            averaging_length = int(AVERAGINGTIME * st[0].stats.sampling_rate)

            station_info = station_info_list[channel_no]
            datatype = datatype_list[channel_no]
            plot_title = plot_title_list[channel_no]
            plot_ylabel = plot_ylabel_list[channel_no]

            filename1 = ('Plots/today_' + datatype + '.svg')
            filename2 = ('Plots/' + date_string + '_' + station_info + '_' + datatype + '.svg')

            y_values = st[0].data[3:st[0].stats.npts]

            if averaging_length > 0:
                y_values = moving_average(y_values, averaging_length)

            if datatype.lower() == "pressure":
                y_values = y_values / 100.0  # convert to hPa

            x_values = np.linspace(graph_start, graph_end, len(y_values))

            plt.figure(figsize=(12, 4))
            x_axis_text = ('Updated - ' + updated + ' UTC')
            plt.title(plot_title + date_string + ' : ' + station_info)
            plt.xlabel(x_axis_text)
            # zeroLabel=str('%0.5g' % (zeroPoint))
            plt.ylabel(plot_ylabel)

            plt.plot(x_values, y_values, marker='None', color='darkolivegreen')
            plt.xlim(0, 24.01)
            plt.xticks(np.arange(0, 24.01, 2.0))
            plt.grid(True)
            plt.savefig(filename1)

            copyfile(filename1, filename2)
            plt.close('all')

        except (ValueError, IndexError):
            print('an  error on plotting daily')


def plot_weekly(st, channel_no):
    try:
        start_date_time = st[0].stats.starttime
        start_year = start_date_time.year
        start_month = start_date_time.month
        # start_day as day of month i.e  1, 2 ... 31
        start_day = start_date_time.day
        # start day as numerical day of week i.e.  1 (Mon) to 7 (Sun)
        iso_start_day = start_date_time.isoweekday()
        start_hour = start_date_time.hour
        start_minute = start_date_time.minute

        date_string = str(start_year) + '-' + str(start_month) + '-' + str(start_day)

        time_sampled = st[0].stats.npts / st[0].stats.sampling_rate  # length of data in seconds
        graph_start = float(iso_start_day - 1) + float(start_hour / 24) + float(start_minute / 1440)
        graph_end = graph_start + (time_sampled / 86400.0)

        updated = UTCDateTime().strftime("%A, %d. %B %Y %H:%M%p")

        station_info = station_info_list[channel_no]
        datatype = datatype_list[channel_no]
        plot_title = plot_title_list[channel_no]
        plot_ylabel = plot_ylabel_list[channel_no]

        filename1 = ('Plots/weekly_' + datatype + '.svg')
        filename2 = ('Plots/' + date_string + '_weekly_' + station_info + '_' + datatype + '.svg')
        filename3 = ('Plots/' + 'prevWeekly_' + station_info + '_' + datatype + '.svg')

        y_values = st[0].data[0:(st[0].stats.npts - 1)]

        if datatype.lower() == "pressure":
            y_values = y_values / 100.0  # convert to hPa

        x_values = np.linspace(graph_start, graph_end, len(y_values))

        plt.figure(figsize=(12, 4))

        x_axis_text = ("Updated - " + updated + " UTC")
        plt.title(plot_title + date_string + ' : ' + station_info)

        plt.xlabel(x_axis_text)
        plt.ylabel(plot_ylabel)

        plt.plot(x_values, y_values, marker='None', color='darkolivegreen')
        plt.xlim(0.0, 7.01)

        ticks = np.arange(0, 7, 1.0)
        labels = "Mon Tues Weds Thurs Fri Sat Sun".split()
        plt.xticks(ticks, labels)
        plt.grid(True)

        plt.savefig(filename1)
        copyfile(filename1, filename2)
        plt.close('all')

        # midnight sunday-monday  - save previous weekly plot with datestamped name
        time_now = UTCDateTime()

        if time_now.isoweekday() == 1:
            if time_now.hour == 0:
                copyfile(filename1, filename3)
                print('prev week saved')

    except (ValueError, IndexError):
        print('an error on plotting weekly data')


def plotPrev168hrs(tmp_prev_168hr_data, start_time_prev168hrs_data,
                   end_time_prev168hrs_data, ntmp_prev_168hr_data, channel_no):
    try:

        sample_end_minus_168_hrs = end_time_prev168hrs_data - (168 * 3600)

        # our plot area runs from the start of the day, need to determine day of week and
        # time offset from start of day to sample_end_minus_168_hrs

        # start day as numerical day of week i.e.  1 (Mon) to 7 (Sun)
        plot_start_day = sample_end_minus_168_hrs.isoweekday()

        # determine number of seconds since start of day
        offset_from_day_start = (end_time_prev168hrs_data.hour * 3600) + \
                                (end_time_prev168hrs_data.minute * 60) + \
                                end_time_prev168hrs_data.second

        # convert sampleStart Datetime to offset in minutes from **plot** start
        datastart_minute = int(
            (start_time_prev168hrs_data - sample_end_minus_168_hrs + offset_from_day_start) / 60.0)

        datastart_minute = max(datastart_minute, 0)  # if <0 set to 0

        data_end_minute = int(datastart_minute + ntmp_prev_168hr_data)

        # determine date info for graph header
        start_year = start_time_prev168hrs_data.year
        start_month = start_time_prev168hrs_data.month

        # start_day as day of month i.e  1, 2 ... 31
        start_day = start_time_prev168hrs_data.day

        date_string = str(start_year) + '-' + str(start_month) + '-' + str(start_day)

        updated = UTCDateTime().strftime("%A, %d. %B %Y %H:%M%p")

        station_info = station_info_list[channel_no]
        datatype = datatype_list[channel_no]
        plot_title = plot_title_list[channel_no]
        plot_ylabel = plot_ylabel_list[channel_no]

        filename1 = ('Plots/prev168hrs_' + datatype + '.svg')
        y_values = tmp_prev_168hr_data[0:(ntmp_prev_168hr_data - 1), channel_no]

        if datatype.lower() == "pressure":
            y_values = y_values / 100.0  # convert to hPa

        x_values = np.linspace(datastart_minute, data_end_minute, len(y_values))

        plt.figure(figsize=(12, 4))

        x_axis_text = ("Updated - " + updated + " UTC")
        plt.title('prev 168 hrs ' + plot_title + date_string + ' : ' + station_info)
        plt.xlabel(x_axis_text)
        plt.ylabel(plot_ylabel)
        plt.plot(x_values, y_values, marker='None', color='darkolivegreen')

        # xAxis 1 minute per division
        # therefore 8 days = 8*24*60 = 11520 minutes
        plt.xlim(0.0, 11520.0)
        ticks = np.arange(0.0, 11520, 1440.0)  # daily ticks

        # create labels for ticks
        days = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
        labels = []
        for i in range(0, 8):
            j = (plot_start_day - 1 + i) % 7
            labels.append(days[j])

        plt.xticks(ticks, labels)
        plt.grid(True)
        plt.savefig(filename1)
        plt.close('all')

    except (ValueError, IndexError):
        print('an error on plotting prev 168 hrs')


def moving_average(a, n):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def create_mseed(readings, start_time, end_time, n_samples, channel_no):
    station_channel = station_info_list[channel_no]

    true_sample_frequency = float(n_samples) / (end_time - start_time)

    # Fill header attributes
    stats = {'network': STATION_NETWORK, 'station': STATION_ID, 'location': STATION_LOCATION,
             'channel': station_channel, 'npts': n_samples, 'sampling_rate': true_sample_frequency,
             'starttime': start_time, 'endtime': end_time,
             'mseed': {'dataquality': 'D'}}

    trace = Trace(data=readings[0:n_samples, channel_no], header=stats)

    st = Stream(traces=[trace])
    return st
