from pprint import pprint

import requests


def flatten_dictionary(input_dictionary: dict, applied_dictionary: dict, set_of_headers: set, set_of_values: set):
    for current_key, current_value in input_dictionary.items():
        if isinstance(current_value, dict):
            flatten_dictionary(current_value, applied_dictionary, set_of_headers, set_of_values)
        else:
            if current_key in set_of_headers or current_value in set_of_values:
                continue
            else:
                applied_dictionary[current_key] = current_value

                set_of_headers.add(current_key)
                set_of_values.add(current_value)

    return applied_dictionary, set_of_headers, set_of_values


def generate_data_frame():
    alternative_list_of_objects = []

    url_base = "http://api.gios.gov.pl/pjp-api/rest/"
    url_of_stations = url_base + "station/findAll"
    url_of_single_station_base = url_base + "station/sensors/"
    url_of_single_sensor_base = url_base + "data/getData/"

    json_of_all_stations = requests.get(url_of_stations).json()

    for currently_analysed_station in json_of_all_stations:
        # pprint(currently_analysed_station)

        list_of_sensors_of_station = requests.get(url_of_single_station_base
                                                  + str(currently_analysed_station["id"])).json()

        for currently_analysed_sensor in list_of_sensors_of_station:
            pprint(currently_analysed_sensor)

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

                # alternative form of generating structure of data
                alternative_sample = {}
                set_of_headers = set()
                set_of_values = set()

                alternative_sample, set_of_headers, set_of_values = flatten_dictionary(current_measurement,
                                                                                       alternative_sample,
                                                                                       set_of_headers,
                                                                                       set_of_values)

                alternative_sample, set_of_headers, set_of_values = flatten_dictionary(currently_analysed_sensor,
                                                                                       alternative_sample,
                                                                                       set_of_headers,
                                                                                       set_of_values)

                alternative_sample, set_of_headers, set_of_values = flatten_dictionary(currently_analysed_station,
                                                                                       alternative_sample,
                                                                                       set_of_headers,
                                                                                       set_of_values)

                alternative_list_of_objects.append(alternative_sample)

    return alternative_list_of_objects


# generate_data_frame()
