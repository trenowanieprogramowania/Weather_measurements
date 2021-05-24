import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import json
import requests
import time

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

    return input_data_frame


def data_air_quality_with_loc_method(input_data_frame: pd.DataFrame):
    with open('air_quality_index.json', 'r') as investigated_source:
        investigated_compounds = json.load(investigated_source)

        given_compounds = set(input_data_frame['param_formula'])

        for currently_investigated_compound in given_compounds:
            # print(input_data_frame['param_formula'])

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


def present_aggregated_data(input_data_frame: pd.DataFrame):
    print('------------------------group_by result - mean concentration of compounds-----------------------------')
    mean_value = input_data_frame.groupby(['commune_name', 'param_formula'], as_index=False)['value'].mean()
    mean_value = data_air_quality_without_loc_method(mean_value)
    print(mean_value.to_string())

    print('------------------------group_by result - pollution level for cities----------------------------------')
    maximum_pollution = input_data_frame.groupby(['commune_name', 'address_street', 'param_formula'],
                                                 as_index=False).agg({'value': ['max', 'min', 'mean']})
    print(maximum_pollution.to_string())

    print('-----------------------group_by result - measurements of compounds per city--------------------------- ')
    measurements_per_city = input_data_frame.groupby(['commune_name', 'param_formula'], as_index=False).size()
    print(measurements_per_city.to_string())

    print('----------------------group_by result - outline of major stations from extracted API----------------------')
    outline_of_stations = input_data_frame.groupby(['commune_name', 'district_name', 'address_street'],
                                                   as_index=False)['location'].first()

    outline_of_stations2 = input_data_frame.groupby(['commune_name', 'district_name', 'address_street'],
                                                    as_index=False)['location'].count()

    outline_of_stations2 = outline_of_stations2.rename(columns={'location': 'number of stations'})

    output = pd.concat([outline_of_stations, outline_of_stations2['number of stations']], axis=1)

    print(output.to_string())

    print('--------------------groupby_result - distribution of amount of compounds per location--------------------')

    location_column = input_data_frame['location']
    location_column = location_column.apply(lambda coordinate: (coordinate['lat'], coordinate['lon']))

    coordinates_table = pd.DataFrame()
    coordinates_table['latitude'] = location_column.apply(lambda component: component[0])
    coordinates_table['longitude'] = location_column.apply(lambda component: component[1])

    combined_location_and_compounds = pd.concat([coordinates_table,
                                                 input_data_frame['param_formula'],
                                                 input_data_frame['value']],
                                                axis=1)

    condensed_form = combined_location_and_compounds.groupby(['latitude', 'longitude', 'param_formula'])['value'].mean()

    print(condensed_form.to_string())

    print('--------------------groupbyresult - cumulative mean for compounds per station--------------------')

    cumulative_table = input_data_frame.groupby(['station_id', 'param_formula'])['value'].expanding().mean()

    print(cumulative_table.to_string())

    print('------------groupby additional result - distribution of average density of compounds------------')

    density_table = input_data_frame.groupby(['param_formula'], as_index=False)['value'].mean()

    print(density_table.to_string())

    print('plotting histogram')
    density_table.plot(x='param_formula', y='value', kind='bar', rot=5, fontsize=4)
    plt.show()
    print('completing plotting histogram')


def plot_time_performance(number_of_samples: int, size_of_step: int, initial_step: int):
    final_step = initial_step + size_of_step * number_of_samples

    list_of_outcomes_loc_method = []
    list_of_outcomes_no_loc_method = []

    for current_step in range(initial_step, final_step , size_of_step):
        list_of_items = data_extraction(current_step)

        outcome_data_frame_no_loc = generating_data_frame(list_of_items)
        outcome_data_frame_loc = generating_data_frame(list_of_items)

        no_loc_starts = time.perf_counter()
        data_frame_no_loc = data_air_quality_without_loc_method(outcome_data_frame_no_loc)
        no_loc_ends = time.perf_counter()
        outcome_no_loc = no_loc_ends - no_loc_starts

        loc_starts = time.perf_counter()
        data_frame_loc = data_air_quality_with_loc_method(outcome_data_frame_loc)
        loc_ends = time.perf_counter()
        outcome_loc = loc_ends - loc_starts

        list_of_outcomes_no_loc_method.append(outcome_no_loc)
        list_of_outcomes_loc_method.append(outcome_loc)

    print(list_of_outcomes_no_loc_method)

    list_of_arguments = np.linspace(0, 1, number_of_samples)

    plt.plot(list_of_arguments, list_of_outcomes_no_loc_method, 'r', label='without loc method')
    plt.plot(list_of_arguments, list_of_outcomes_loc_method, 'b', label='with_loc_method')

    plt.show()

####################################################################################


# plot_time_performance(number_of_samples=20, size_of_step=1, initial_step=1)

list_of_objects = data_extraction(limited_number_of_samples=4)

outcome_data_frame1 = generating_data_frame(list_of_objects)
# outcome_data_frame2 = generating_data_frame(list_of_objects)

# data_frame = data_transformation(outcome_data_frame)

data_frame1 = data_air_quality_without_loc_method(outcome_data_frame1)
# data_frame2 = data_air_quality_with_loc_method(outcome_data_frame2)

# other_data_frame1 = data_air_quality_without_loc_method(outcome_data_frame1)
# other_data_frame2 = data_air_quality_with_loc_method(data_frame2)

# print(data_frame1.equals(data_frame2))
# print(data_frame.to_string())
print(data_frame1.to_string())
# print('Other dataFrame----------------------------------------------------------------------------------------------')
# print(data_frame2.to_string())

present_aggregated_data(data_frame1)

# print(data_frame1.tail(5))
# print('-----------------------')
# print(data_frame2.tail(5))
'''
# print(other_data_frame1.equals(other_data_frame2))

# print(len(data_frame1))
# print(len(data_frame2))

# print(list(data_frame.columns.values))
'''
