import pandas as pd

import json
import requests

from measurement import Measurement


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


def investigate_air_quality(input_data_frame: pd.DataFrame):
    with open('air_quality_index.json', 'r') as investigated_source:
        investigated_compounds = json.load(investigated_source)

        if input_data_frame['param_formula'] in investigated_compounds["Compound"].keys():
            investigated_param_formula = input_data_frame['param_formula']

            if input_data_frame['value'] \
                    > investigated_compounds['Compound'][investigated_param_formula]['Very bad']:
                return 'Very bad'
            elif investigated_compounds['Compound'][investigated_param_formula]['Very bad'] \
                    >= input_data_frame['value'] \
                    > investigated_compounds['Compound'][investigated_param_formula]['Bad']:
                return 'Bad'
            elif investigated_compounds['Compound'][investigated_param_formula]['Bad'] \
                    >= input_data_frame['value'] \
                    > investigated_compounds['Compound'][investigated_param_formula]['Satisfactory']:
                return 'Satisfactory'
            elif investigated_compounds['Compound'][investigated_param_formula]['Satisfactory'] \
                    >= input_data_frame['value'] \
                    > investigated_compounds['Compound'][investigated_param_formula]['Moderate']:
                return 'Moderate'
            elif investigated_compounds['Compound'][investigated_param_formula]['Moderate'] \
                    >= input_data_frame['value'] \
                    > investigated_compounds['Compound'][investigated_param_formula]['Good']:
                return 'Good'
            elif investigated_compounds['Compound'][investigated_param_formula]['Good'] \
                    >= input_data_frame['value'] \
                    > investigated_compounds['Compound'][investigated_param_formula]['Very good']:
                return 'Very good'


def data_air_quality_without_loc_method(input_data_frame: pd.DataFrame):
    input_data_frame['air_quality'] = input_data_frame.apply(investigate_air_quality, axis=1)

    # print('------------------------Generating group_by result---------------------------------------')
    # mean_value = input_data_frame.groupby(['param_formula'], as_index=False)['value'].mean()
    # print(mean_value.to_string())

    return input_data_frame


def data_air_quality_with_loc_method(input_data_frame: pd.DataFrame):
    with open('air_quality_index.json', 'r') as investigated_source:
        investigated_compounds = json.load(investigated_source)

        given_compounds = set(input_data_frame['param_formula'])

        for currently_investigated_compound in given_compounds:

            if currently_investigated_compound in investigated_compounds["Compound"].keys():
                investigated_param_formula = currently_investigated_compound

                input_data_frame.loc[input_data_frame['value']
                                     > investigated_compounds['Compound'][investigated_param_formula]['Very bad'], \
                                     'air_quality'] \
                    = 'Very bad'

                input_data_frame.loc[((input_data_frame['value']
                                       > investigated_compounds['Compound'][investigated_param_formula]['Bad'])
                                      &
                                      (input_data_frame['value']
                                       <=
                                       investigated_compounds['Compound'][investigated_param_formula]['Very bad'])), \
                                     'air_quality'] \
                    = 'Bad'

                input_data_frame.loc[((input_data_frame['value']
                                       > investigated_compounds['Compound'][investigated_param_formula]['Satisfactory'])
                                      &
                                      (input_data_frame['value']
                                       <=
                                       investigated_compounds['Compound'][investigated_param_formula]['Bad'])), \
                                     'air_quality'] \
                    = 'Satisfactory'

                input_data_frame.loc[((input_data_frame['value']
                                       > investigated_compounds['Compound'][investigated_param_formula]['Moderate'])
                                      &
                                      (input_data_frame['value']
                                       <=
                                       investigated_compounds['Compound'][investigated_param_formula]['Satisfactory'])), \
                                     'air_quality'] \
                    = 'Moderate'

                input_data_frame.loc[((input_data_frame['value']
                                       > investigated_compounds['Compound'][investigated_param_formula]['Good'])
                                      &
                                      (input_data_frame['value']
                                       <=
                                       investigated_compounds['Compound'][investigated_param_formula]['Moderate'])), \
                                     'air_quality'] \
                    = 'Good'

                input_data_frame.loc[((input_data_frame['value']
                                       > investigated_compounds['Compound'][investigated_param_formula]['Very good'])
                                      &
                                      (input_data_frame['value']
                                       <=
                                       investigated_compounds['Compound'][investigated_param_formula]['Good'])), \
                                     'air_quality'] \
                    = 'Very good'

    return input_data_frame


####################################################################################


list_of_objects = data_extraction(1)

outcome_data_frame1 = generating_data_frame(list_of_objects)
outcome_data_frame2 = generating_data_frame(list_of_objects)

# data_frame = data_transformation(outcome_data_frame)

data_frame1 = data_air_quality_without_loc_method(outcome_data_frame1)
data_frame2 = data_air_quality_with_loc_method(outcome_data_frame2)

other_data_frame1 = data_air_quality_without_loc_method(outcome_data_frame1)
other_data_frame2 = data_air_quality_with_loc_method(data_frame2)

# print(other_data_frame1.equals(other_data_frame2))
# print(data_frame.to_string())
#print(other_data_frame1.to_string())
#print('Other dataFrame------------------------------------------------------------------------------------------------------------')
#print(other_data_frame2.to_string())

print(other_data_frame1.tail(5))
print('-----------------------')
print(other_data_frame2.tail(5))

print(other_data_frame1.equals(other_data_frame2))

# print(len(data_frame1))
# print(len(data_frame2))

# print(list(data_frame.columns.values))
