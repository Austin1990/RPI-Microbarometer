# these setting are for the Bonas sense HAT BMP-280 & SHT31-DIS based environmental station

home_directory = '/home/ajb/Source/Bonas_HAT'

# below are station parameters for your station. see SEED manual for
# more details http://www.fdsn.org/pdf/SEEDManual_V2.4.pdf  esp. Apprendix A

STATION_ID = 'Home'
STATION_LOCATION = '01'     # 2 digit code to identify specific sensor rig
STATION_NETWORK = 'AJB'

# channel M=mid-period 1-10Hz sampling, D=pressure sensor, I=inside
STATION_CHANNEL_0 = 'MDI'
STATION_INFO_0 = STATION_ID + '-' + STATION_CHANNEL_0 + '-' + STATION_LOCATION
DATATYPE_CHANNEL_0 = 'Pressure'
PLOT_TITLE_CHANNEL_0 = 'Pressure, Callerton, UK '
PLOT_YLABEL_CHANNEL_0 = 'Pressure (hPa)'

# channel M=mid-period 1-10Hz sampling, K=temperature sensor, I=inside
STATION_CHANNEL_1 = 'MKI'
STATION_INFO_1 = STATION_ID + '-' + STATION_CHANNEL_1 + '-' + STATION_LOCATION
DATATYPE_CHANNEL_1 = 'Temperature 1'
PLOT_TITLE_CHANNEL_1 = 'Temperature (BMP-280), Callerton UK '
PLOT_YLABEL_CHANNEL_1 = 'Temperature 1 (°C)'

# channel M=mid-period 1-10Hz sampling, K=temperature sensor, I=inside
STATION_CHANNEL_2 = 'MKI'
STATION_INFO_2 = STATION_ID + '-' + STATION_CHANNEL_2 + '-' + STATION_LOCATION
DATATYPE_CHANNEL_2 = 'Temperature 2'
PLOT_TITLE_CHANNEL_2 = 'Temperature (SHT31), Callerton UK '
PLOT_YLABEL_CHANNEL_2 = 'Temperature 2 (°C)'

# channel M=mid-period 1-10Hz sampling, I=humidity sensor, I=inside
STATION_CHANNEL_3 = 'MII'
STATION_INFO_3 = STATION_ID + '-' + STATION_CHANNEL_3 + '-' + STATION_LOCATION
DATATYPE_CHANNEL_3 = 'Humidity'
PLOT_TITLE_CHANNEL_3 = 'Humidity, Callerton, UK '
PLOT_YLABEL_CHANNEL_3 = 'Humidity (g/m3)'

# channel M=mid-period 1-10Hz sampling, I=CO2 sensor, I=inside
STATION_CHANNEL_4 = 'MYC'
STATION_INFO_4 = STATION_ID + '-' + STATION_CHANNEL_4 + '-' + STATION_LOCATION
DATATYPE_CHANNEL_4 = 'Equivalent CO2'
PLOT_TITLE_CHANNEL_4 = 'Equivalent CO2, Callerton, UK '
PLOT_YLABEL_CHANNEL_4 = 'Equivalent CO2 (ppm)'

# channel M=mid-period 1-10Hz sampling, I=VOC sensor, I=inside
STATION_CHANNEL_5 = 'MYV'
STATION_INFO_5 = STATION_ID + '-' + STATION_CHANNEL_5 + '-' + STATION_LOCATION
DATATYPE_CHANNEL_5 = 'Total VOC'
PLOT_TITLE_CHANNEL_5 = 'Total VOC, Callerton, UK '
PLOT_YLABEL_CHANNEL_5 = 'Total VOC (ppb)'

station_info_list = [STATION_INFO_0, STATION_INFO_1, STATION_INFO_2,
                     STATION_INFO_3, STATION_INFO_4, STATION_INFO_5]
datatype_list = [DATATYPE_CHANNEL_0, DATATYPE_CHANNEL_1, DATATYPE_CHANNEL_2,
                 DATATYPE_CHANNEL_3, DATATYPE_CHANNEL_4, DATATYPE_CHANNEL_5]
plot_title_list = [PLOT_TITLE_CHANNEL_0, PLOT_TITLE_CHANNEL_1, PLOT_TITLE_CHANNEL_2,
                   PLOT_TITLE_CHANNEL_3, PLOT_TITLE_CHANNEL_4, PLOT_TITLE_CHANNEL_5]
plot_ylabel_list = [PLOT_YLABEL_CHANNEL_0, PLOT_YLABEL_CHANNEL_1, PLOT_YLABEL_CHANNEL_2,
                    PLOT_YLABEL_CHANNEL_3, PLOT_YLABEL_CHANNEL_4, PLOT_YLABEL_CHANNEL_5]

channel_list = range(len(station_info_list))
N_CHANNELS = len(channel_list)
active_plot_list = [0, 1, 2, 3, 4, 5]   # change this to control the channels plotted

SAMPLING_FRQ = 5.00
SAMPLING_PERIOD = 1.00 / SAMPLING_FRQ
AVERAGINGTIME = 30  # time interval seconds to calculate running mean

N_TARGET_HOURLY_SAMPLES = int(SAMPLING_FRQ * 3600 * 1.5)
N_TARGET_DAILY_SAMPLES = int(N_TARGET_HOURLY_SAMPLES * 24)
N_TARGET_PREV_MINUTE = int(SAMPLING_FRQ * 60 * 1.3)

# no of weekly samples depends on averaging period e.g. 1 per minute ~10080
N_TARGET_WEEKLY_SAMPLES = 12000

N_HOURS_PER_WEEK = int(24 * 7)
