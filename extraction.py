import pandas as pd

import requests

from measurement import Measurement


def data_extraction():
    list_of_objects = []

    url_base = "http://api.gios.gov.pl/pjp-api/rest/"
    url_of_stations = url_base + "station/findAll"
    url_of_single_station_base = url_base + "station/sensors/"
    url_of_single_sensor_base = url_base + "data/getData/"

    json_of_all_stations = requests.get(url_of_stations).json()

    for currently_analysed_station in json_of_all_stations:
        list_of_sensors_of_station = requests.get(url_of_single_station_base
                                                  + str(currently_analysed_station["id"])).json()

        for currently_analysed_sensor in list_of_sensors_of_station:
            list_of_measurements_of_single_sensor = requests.get(url_of_single_sensor_base
                                                                 + str(currently_analysed_sensor["id"])).json()

            for current_measurement in list_of_measurements_of_single_sensor['values']:
                print(f"currently analysed station: {currently_analysed_station}")

                print(f"currently analysed sensor: {currently_analysed_sensor}")

                print(f"current measurement: {current_measurement}")
                print("***********************************************************************")

                # condition for checking existence of 'polluted' (incomplete) data
                if current_measurement['value'] is None or currently_analysed_station['gegrLon'] is None or \
                        currently_analysed_station['gegrLon'] is None:
                    continue

                single_sample = Measurement(
                    **current_measurement,
                    **currently_analysed_station,
                    **currently_analysed_station['city']['commune'],
                    **currently_analysed_sensor['param'],
                    stationId=currently_analysed_sensor['id']
                )

                list_of_sample = single_sample.serialize()

                list_of_objects.append(list_of_sample)

    return list_of_objects


def generating_data_frame(list_of_objects):
    headers = Measurement.generating_headers()
    data = Measurement.generating_data()

    # print('111111111111111111111111111111111111111111111111111111111111111111111111111111111111111')
    # print(headers)
    # print('111111111111111111111111111111111111111111111111111111111111111111111111111111111111111')

    # print('222222222222222222222222222222222222222222222222222222222222222222222222222222222222222')
    # print(data)
    # print('222222222222222222222222222222222222222222222222222222222222222222222222222222222222222')

    return pd.DataFrame(data=data, columns=headers)


def data_transformation(input_data_frame: pd.DataFrame):
    input_data_frame['alarm'] = input_data_frame['value'] > 10

    return input_data_frame


def data_air_quality(input_data_frame: pd.DataFrame):
    # compound_name = {'PM10', 'PM2.5', 'O3', 'NO2', 'SO2', 'C6H6', 'CO'}

    for currently_analysed_date in input_data_frame['date']:
        if input_data_frame['date'] == currently_analysed_date:
            if (input_data_frame['param_formula'] == 'PM10' and 0 <= input_data_frame['value'] < 20) \
                    or (input_data_frame['param_formula'] == 'PM2.5' and 0 <= input_data_frame['value'] <= 13) \
                    or (input_data_frame['param_formula'] == '03' and 0 <= input_data_frame['value'] <= 70) \
                    or (input_data_frame['param_formula'] == 'NO2' and 0 <= input_data_frame['value'] <= 40) \
                    or (input_data_frame['param_formula'] == 'S02' and 0 <= input_data_frame['value'] <= 50) \
                    or (input_data_frame['param_formula'] == 'C6H6' and 0 <= input_data_frame['value'] <= 6) \
                    or (input_data_frame['param_formula'] == 'CO' and 0 <= input_data_frame['value'] <= 3):
                input_data_frame['air_quality'] = 'very good'

            elif (input_data_frame['param_formula'] == 'PM10' and 20.1 <= input_data_frame['value'] <= 50) \
                    or (input_data_frame['param_formula'] == 'PM2.5' and 13.1 <= input_data_frame['value'] <= 35) \
                    or (input_data_frame['param_formula'] == '03' and 70.1 <= input_data_frame['value'] <= 120) \
                    or (input_data_frame['param_formula'] == 'NO2' and 40.1 <= input_data_frame['value'] <= 100) \
                    or (input_data_frame['param_formula'] == 'S02' and 0 <= input_data_frame['value'] <= 100) \
                    or (input_data_frame['param_formula'] == 'C6H6' and 6.1 <= input_data_frame['value'] <= 11) \
                    or (input_data_frame['param_formula'] == 'CO' and 3.1 <= input_data_frame['value'] <= 7):
                input_data_frame['air_quality'] = 'good'

            elif (input_data_frame['param_formula'] == 'PM10' and 50.1 <= input_data_frame['value'] <= 80) \
                    or (input_data_frame['param_formula'] == 'PM2.5' and 35.1 <= input_data_frame['value'] <= 55) \
                    or (input_data_frame['param_formula'] == '03' and 120.1 <= input_data_frame['value'] <= 150) \
                    or (input_data_frame['param_formula'] == 'NO2' and 100.1 <= input_data_frame['value'] <= 150) \
                    or (input_data_frame['param_formula'] == 'S02' and 100.1 <= input_data_frame['value'] <= 200) \
                    or (input_data_frame['param_formula'] == 'C6H6' and 11.1 <= input_data_frame['value'] <= 16) \
                    or (input_data_frame['param_formula'] == 'CO' and 7.1 <= input_data_frame['value'] <= 11):
                input_data_frame['air_quality'] = 'moderate'

            elif (input_data_frame['param_formula'] == 'PM10' and 80.1 <= input_data_frame['value'] <= 110) \
                    or (input_data_frame['param_formula'] == 'PM2.5' and 55.1 <= input_data_frame['value'] <= 75) \
                    or (input_data_frame['param_formula'] == '03' and 150.1 <= input_data_frame['value'] <= 180) \
                    or (input_data_frame['param_formula'] == 'NO2' and 150.1 <= input_data_frame['value'] <= 200) \
                    or (input_data_frame['param_formula'] == 'S02' and 200.1 <= input_data_frame['value'] <= 350) \
                    or (input_data_frame['param_formula'] == 'C6H6' and 16.1 <= input_data_frame['value'] <= 21) \
                    or (input_data_frame['param_formula'] == 'CO' and 11.1 <= input_data_frame['value'] <= 15):
                input_data_frame['air_quality'] = 'satisfactory'

            elif (input_data_frame['param_formula'] == 'PM10' and 110.1 <= input_data_frame['value'] <= 150) \
                    or (input_data_frame['param_formula'] == 'PM2.5' and 75.1 <= input_data_frame['value'] <= 110) \
                    or (input_data_frame['param_formula'] == '03' and 180.1 <= input_data_frame['value'] <= 240) \
                    or (input_data_frame['param_formula'] == 'NO2' and 200.1 <= input_data_frame['value'] <= 240) \
                    or (input_data_frame['param_formula'] == 'S02' and 350.1 <= input_data_frame['value'] <= 500) \
                    or (input_data_frame['param_formula'] == 'C6H6' and 21.1 <= input_data_frame['value'] <= 51) \
                    or (input_data_frame['param_formula'] == 'CO' and 15.1 <= input_data_frame['value'] <= 21):
                input_data_frame['air_quality'] = 'bad'

            elif (input_data_frame['param_formula'] == 'PM10' and input_data_frame['value'] > 150) \
                    or (input_data_frame['param_formula'] == 'PM2.5' and input_data_frame['value'] > 110) \
                    or (input_data_frame['param_formula'] == '03' and input_data_frame['value'] > 240) \
                    or (input_data_frame['param_formula'] == 'NO2' and input_data_frame['value'] > 240) \
                    or (input_data_frame['param_formula'] == 'S02' and input_data_frame['value'] > 500) \
                    or (input_data_frame['param_formula'] == 'C6H6' and input_data_frame['value'] > 51) \
                    or (input_data_frame['param_formula'] == 'CO' and input_data_frame['value'] > 21):
                input_data_frame['air_quality'] = 'very bad'

            elif (input_data_frame['param_formula'] == 'PM10' and input_data_frame['value'] is None) \
                    or (input_data_frame['param_formula'] == 'PM2.5' and input_data_frame['value'] is None) \
                    or (input_data_frame['param_formula'] == 'O3' and input_data_frame['value'] is None) \
                    or (input_data_frame['param_formula'] == 'NO2' and input_data_frame['value'] is None) \
                    or (input_data_frame['param_formula'] == 'SO2' and input_data_frame['value'] is None) \
                    or (input_data_frame['param_formula'] == 'C6H6' and input_data_frame['value'] is None) \
                    or (input_data_frame['param_formula'] == 'CO' and input_data_frame['value'] is None):
                input_data_frame['air_quality'] = 'no index'

    return input_data_frame


list_of_objects = data_extraction()

outcome_data_frame = generating_data_frame(list_of_objects)

data_frame = data_transformation(outcome_data_frame)

data_frame = data_air_quality(outcome_data_frame)

# print(data_frame.to_string())

print(outcome_data_frame.head(5))

# print(list(data_frame.columns.values))
