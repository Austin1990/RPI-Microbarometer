#       Bonas HAT Sensor Monitoring Software
#
#       based on Ian Robinson's Seismic Monitoring Software
#       http://schoolphysicsprojects.org
#
#       requires
#           python3, python3-obspy, matplotlib
#           sht31, bmp_280
#
# ---------------------------Notes---------------------------
#
#   ## loose weekly readings
#

import os
from bmp_280 import BMP280
from sht31 import SHT31d
from sgp30 import SGP30
from time import sleep
from threading import Thread
from geostationModules import *

device_0 = BMP280()
device_1 = SHT31d()
device_2 = SGP30()

os.chdir(home_directory)

def main():
    # create top level Data and plots directories if not already present
    try:
        os.makedirs('Plots/')
    except OSError:
        if not os.path.isdir('Plots/'):
            raise

    try:
        os.makedirs('Data/')
    except OSError:
        if not os.path.isdir('Data/'):
            raise

    first_week = True  # queue behaviour different when queue not yet fully filled

    # two circular queues are used to store long-term data (>1 day) for plotting
    # queuePrev168hrs stores data points in a numpy array
    #
    # to avoid timing drift q_index_hourly_starttimes stores the start times and pointers to
    # the tail position of each hour's data in queuePrev168hrs

    # create numpy arrays to store the sensor channels data
    tranche_prev_minute = np.zeros([N_TARGET_PREV_MINUTE, N_CHANNELS], dtype=np.float32)
    # implemented as circular queue
    q_prev_168hrs_data = np.zeros([N_TARGET_WEEKLY_SAMPLES, N_CHANNELS], dtype=np.float32)
    daily_readings = np.zeros([N_TARGET_DAILY_SAMPLES, N_CHANNELS], dtype=np.float32)
    hourly_readings = np.zeros([N_TARGET_HOURLY_SAMPLES, N_CHANNELS], dtype=np.float32)
    weekly_readings = np.zeros([N_TARGET_WEEKLY_SAMPLES, N_CHANNELS], dtype=np.float32)

    # create list to hold tail pointers and hourly start times of previous week's data
    q_index_hourly_starttimes = []

    n_prev_minute = 0
    n_daily_readings = 0
    n_hourly_readings = 0
    n_weekly_readings = 0
    hp_prev_168hrs_data = 0
    tp_prev_168hrs_data = 0
    tp_index_hourly_starttimes = 0
    hp_index_hourly_starttimes = 0

    week_start = UTCDateTime()
    day_start = week_start
    hour_start = week_start
    minute_start = week_start
    end_time_prev168hrs_data = week_start

    # Initialise queue for the hourly starttimes and data positions in data queue
    # tmp=[UTCDateTime(), 0]
    # 0 will be replaced by the head pointer, i.e. start position of that hour's readings
    for hour in range(N_HOURS_PER_WEEK):
        tmp = [UTCDateTime(), hour]
        q_index_hourly_starttimes.append(tmp)

    print('Waiting...')
    sleep(30)  # wait 30 sec before starting
    print('Start measurements...')
    try:
        device_2.start_measurement()
    except IOError:
        print('SGP30 error')

    while 1:

        sleep(SAMPLING_PERIOD)

        try:
            sensor_data = read_from_sensors()
            for channel_no in channel_list:
                daily_readings[n_daily_readings, channel_no] = sensor_data[channel_no]
                hourly_readings[n_hourly_readings, channel_no] = sensor_data[channel_no]
                tranche_prev_minute[n_prev_minute, channel_no] = sensor_data[channel_no]

            n_daily_readings = n_daily_readings + 1
            n_hourly_readings = n_hourly_readings + 1
            n_prev_minute = n_prev_minute + 1
            if UTCDateTime().second % 5 == 0:
                print('.', end="")

        except IOError:
            print('read error')
            for channel_no in channel_list:
                daily_readings[n_daily_readings, channel_no] = 0.00
                hourly_readings[n_hourly_readings, channel_no] = 0.00

            n_daily_readings = n_daily_readings + 1
            n_hourly_readings = n_hourly_readings + 1

        # calc average of last minute's values storing in weekly_readings
        if UTCDateTime().minute != minute_start.minute:
            if n_prev_minute > 0:
                print('.', end='\r', flush=True)
                for channel_no in channel_list:
                    mean_data = np.average(tranche_prev_minute[0:n_prev_minute, channel_no])
                    weekly_readings[n_weekly_readings, channel_no] = mean_data
                    q_prev_168hrs_data[hp_prev_168hrs_data, channel_no] = mean_data

                # add 1 to hp wrapping around to 0 if > N_TARGET_WEEKLY_SAMPLES % = 'mod'
                hp_prev_168hrs_data = (hp_prev_168hrs_data + 1) % N_TARGET_WEEKLY_SAMPLES
                # reset tranche to all zeros
                tranche_prev_minute = np.zeros([N_TARGET_PREV_MINUTE, N_CHANNELS], dtype=np.float32)
                n_weekly_readings = n_weekly_readings + 1
                minute_start = UTCDateTime()
                n_prev_minute = 0

        if UTCDateTime().hour != hour_start.hour:
            end_time_prev168hrs_data = UTCDateTime()
            prev_hour_start = hour_start
            hour_start = UTCDateTime()

            if hp_index_hourly_starttimes == N_HOURS_PER_WEEK - 1:  # check whether full week of data has been gathered
                first_week = False

            # wrap around to beginning at 168 hrs
            hp_index_hourly_starttimes = (hp_index_hourly_starttimes + 1) % N_HOURS_PER_WEEK
            # for 1st 168hrs tailpointer=0 .. 1st wrap hp..168->0 and tp -> 1, after that
            # increment tp by 1 each time
            if first_week is False:
                tp_index_hourly_starttimes = (tp_index_hourly_starttimes + 1) % N_HOURS_PER_WEEK

            # write new hour's start position and timestamp to circular queue
            q_index_hourly_starttimes[hp_index_hourly_starttimes][0] = hour_start
            q_index_hourly_starttimes[hp_index_hourly_starttimes][1] = hp_prev_168hrs_data

            tmp_prev_168hr_data = np.zeros([N_TARGET_WEEKLY_SAMPLES, N_CHANNELS], dtype=np.float32)

            # look up pointer to position for first data item
            tp_prev_168hrs_data = q_index_hourly_starttimes[tp_index_hourly_starttimes][1]
            ntmp_prev_168hr_data = 0

            while tp_prev_168hrs_data != hp_prev_168hrs_data:
                for channel_no in channel_list:
                    tmp_prev_168hr_data[ntmp_prev_168hr_data, channel_no] = q_prev_168hrs_data[tp_prev_168hrs_data, channel_no]

                ntmp_prev_168hr_data = ntmp_prev_168hr_data + 1
                tp_prev_168hrs_data = (tp_prev_168hrs_data + 1) % N_TARGET_WEEKLY_SAMPLES  # wrap at end of queue

            # start plotting as thread to hopefully reduce chance of 'glitching' on sensor reads.
            if ntmp_prev_168hr_data > 10:
                thread_plot_and_save = Thread(target=save_and_plot_all, args=((
                    hourly_readings, n_hourly_readings, prev_hour_start,
                    daily_readings, n_daily_readings, day_start,
                    weekly_readings, n_weekly_readings, week_start,
                    tmp_prev_168hr_data, ntmp_prev_168hr_data, end_time_prev168hrs_data,
                    q_index_hourly_starttimes, tp_index_hourly_starttimes)))

                thread_plot_and_save.start()

            # reset data array to zero for new hour
            hourly_readings = np.zeros([N_TARGET_HOURLY_SAMPLES, N_CHANNELS], dtype=np.float32)
            n_hourly_readings = 0

        if day_start.day != UTCDateTime().day:

            # reset data array to zero for new day
            daily_readings = np.zeros([N_TARGET_DAILY_SAMPLES, N_CHANNELS], dtype=np.float32)
            day_start = UTCDateTime()
            n_daily_readings = 0

            if end_time_prev168hrs_data.isoweekday() == 1:  # Monday-- new week starts
                # clear the weekly data array
                weekly_readings = np.zeros([N_TARGET_WEEKLY_SAMPLES, N_CHANNELS], dtype=np.float32)
                week_start = UTCDateTime()
                n_weekly_readings = 0


def read_from_sensors():
    # read data from BMP-280
    bmp_temp = device_0.read_temperature()
    bmp_p = device_0.read_pressure()
    # read data from SHT31
    sht_temp, sht_rh = device_1.read_temperature_humidity()
    air_qual = device_2.get_air_quality()
    readings = (bmp_p, bmp_temp, sht_temp, sht_rh, air_qual.equivalent_co2, air_qual.total_voc)
    return readings


def save_and_plot_all(hourly_readings, n_hourly_readings, prev_hour_start,
                      daily_readings, n_daily_readings, day_start,
                      weekly_readings, n_weekly_readings, week_start,
                      tmp_prev_168hr_data, ntmp_prev_168hr_data, end_time_prev168hrs_data,
                      q_index_hourly_starttimes, tp_index_hourly_starttimes):

    for channel_no in active_plot_list:
        st = create_mseed(weekly_readings, week_start,
                          end_time_prev168hrs_data, n_weekly_readings, channel_no)
        save_weekly_data_as_mseed(st, channel_no)
        plot_weekly(st, channel_no)

        st = create_mseed(hourly_readings, prev_hour_start,
                          end_time_prev168hrs_data, n_hourly_readings, channel_no)
        save_hourly_data_as_mseed(st, channel_no)

        # create daily stream and plot
        st = create_mseed(daily_readings, day_start,
                          end_time_prev168hrs_data, n_daily_readings, channel_no)
        plot_daily(st, channel_no)

        if ntmp_prev_168hr_data > 10:
            start_time_prev168hrs_data = q_index_hourly_starttimes[tp_index_hourly_starttimes][0]
            plotPrev168hrs(tmp_prev_168hr_data, start_time_prev168hrs_data,
                           end_time_prev168hrs_data, ntmp_prev_168hr_data, channel_no)


if __name__ == '__main__':
    main()
