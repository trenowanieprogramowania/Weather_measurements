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

    print('111111111111111111111111111111111111111111111111111111111111111111111111111111111111111')
    print(headers)
    print('111111111111111111111111111111111111111111111111111111111111111111111111111111111111111')

    print('222222222222222222222222222222222222222222222222222222222222222222222222222222222222222')
    print(data)
    print('222222222222222222222222222222222222222222222222222222222222222222222222222222222222222')

    return pd.DataFrame(data=data, columns=headers)


def data_transformation(input_data_frame: pd.DataFrame):
    input_data_frame['alarm'] = input_data_frame['value'] > 10

    return input_data_frame


list_of_objects = data_extraction()

outcome_data_frame = generating_data_frame(list_of_objects)

data_frame = data_transformation(outcome_data_frame)

print(data_frame.to_string())

# print(outcome_data_frame.head(10))
