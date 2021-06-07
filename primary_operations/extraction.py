import pandas as pd

import requests

from core_for_data.measurement import Measurement


def data_extraction(limited_number_of_samples=False):
    list_of_data = []

    url_base = "http://api.gios.gov.pl/pjp-api/rest/"
    url_of_stations = url_base + "station/findAll"
    url_of_single_station_base = url_base + "station/sensors/"
    url_of_single_sensor_base = url_base + "data/getData/"

    json_of_all_stations = requests.get(url_of_stations).json()

    if limited_number_of_samples:
        json_of_all_stations = json_of_all_stations[:limited_number_of_samples]

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
                print("***********************************************************************************************")

                try:
                    single_sample = Measurement(
                        **current_measurement,
                        **currently_analysed_station,
                        **currently_analysed_station['city']['commune'],
                        **currently_analysed_sensor['param'],
                        stationId=currently_analysed_sensor['id']
                    )

                    list_of_sample = single_sample.serialize()

                    list_of_data.append(list_of_sample)
                except TypeError as e:
                    print('missing parameters in object construction:', e)

                    continue

    return list_of_data


def generating_data_frame(list_of_objects):
    headers = Measurement.generating_headers()
    data = Measurement.generating_data()

    return pd.DataFrame(data=data, columns=headers)


# exemplary usage
# def data_transformation(input_data_frame: pd.DataFrame):
#    input_data_frame['alarm'] = input_data_frame['value'] > 10
#
#    return input_data_frame
