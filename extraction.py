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

    # przejscie przez wszystkie daty dostepne w input_data_frame
    # for currently_analysed_date in input_data_frame['date']:


    input_data_frame['air_quality'] = ''

    for row_index in range(input_data_frame.shape[0]):
        # if input_data_frame['date'][row_index] == currently_analysed_date:

        # obsluzenie bloku dla pojedynczej daty
        '''
        Ponizszy kod jest zle napisany, ale nie wiem, jak napisac poprawne rozwiazanie.
        
        Taka ponizsza idea kodu przychodzi mi do glowy, ale nie wiem, jak poprawnie ja napisac przy uzyciu biblioteki
        pandas.
        
        Idea rozwiazania wydaje mi sie taka:
        - przejscie przez wszystkie mozliwe daty
        - wyodrebnienie wierszy z danego DataFrame'u spelniajacego koniunkcje warunkow
        - dla wyodrebnionych takich wierszy stworzenie kolumny air_quality i odpowiednie przypisanie wartosci 
        '''

        # idea: wyselekcjonowanie wierszy o okreslonej wartosci w rekordzie date
        # if input_data_frame['date'] == currently_analysed_date:
            # idea: wyselekcjonowanie z wczesniej wyroznionego zbioru wierszy takich wierszy, ktore spelniaja jedna
            # z ponizszych koniunkcji
        if (input_data_frame['param_formula'][row_index] == 'PM10' and 0 <= input_data_frame['value'][row_index] < 20) \
            or (input_data_frame['param_formula'][row_index] == 'PM2.5' and 0 <= input_data_frame['value'][row_index] <= 13) \
            or (input_data_frame['param_formula'][row_index] == '03' and 0 <= input_data_frame['value'][row_index] <= 70) \
            or (input_data_frame['param_formula'][row_index] == 'NO2' and 0 <= input_data_frame['value'][row_index] <= 40) \
            or (input_data_frame['param_formula'][row_index] == 'S02' and 0 <= input_data_frame['value'][row_index] <= 50) \
            or (input_data_frame['param_formula'][row_index] == 'C6H6' and 0 <= input_data_frame['value'][row_index] <= 6) \
            or (input_data_frame['param_formula'][row_index] == 'CO' and 0 <= input_data_frame['value'][row_index] <= 3):
                # idea: dla powyzej wyselekcjonowanych wierszy stworzenie nowej kolumny i nadanie odpowiedniej wartosci
                input_data_frame['air_quality'][row_index] = 'very good'
        elif (input_data_frame['param_formula'][row_index] == 'PM10' and 20.1 <= input_data_frame['value'][row_index] <= 50) \
            or (input_data_frame['param_formula'][row_index] == 'PM2.5' and 13.1 <= input_data_frame['value'][row_index] <= 35) \
            or (input_data_frame['param_formula'][row_index] == '03' and 70.1 <= input_data_frame['value'][row_index] <= 120) \
            or (input_data_frame['param_formula'][row_index] == 'NO2' and 40.1 <= input_data_frame['value'][row_index] <= 100) \
            or (input_data_frame['param_formula'][row_index] == 'S02' and 0 <= input_data_frame['value'][row_index] <= 100) \
            or (input_data_frame['param_formula'][row_index] == 'C6H6' and 6.1 <= input_data_frame['value'][row_index] <= 11) \
            or (input_data_frame['param_formula'][row_index] == 'CO' and 3.1 <= input_data_frame['value'][row_index] <= 7):
                input_data_frame['air_quality'][row_index] = 'good'

        elif (input_data_frame['param_formula'][row_index] == 'PM10' and 50.1 <= input_data_frame['value'][row_index] <= 80) \
            or (input_data_frame['param_formula'][row_index] == 'PM2.5' and 35.1 <= input_data_frame['value'][row_index] <= 55) \
            or (input_data_frame['param_formula'][row_index] == '03' and 120.1 <= input_data_frame['value'][row_index] <= 150) \
            or (input_data_frame['param_formula'][row_index] == 'NO2' and 100.1 <= input_data_frame['value'][row_index] <= 150) \
            or (input_data_frame['param_formula'][row_index] == 'S02' and 100.1 <= input_data_frame['value'][row_index] <= 200) \
            or (input_data_frame['param_formula'][row_index] == 'C6H6' and 11.1 <= input_data_frame['value'][row_index] <= 16) \
            or (input_data_frame['param_formula'][row_index] == 'CO' and 7.1 <= input_data_frame['value'][row_index] <= 11):
                input_data_frame['air_quality'][row_index] = 'moderate'

        elif (input_data_frame['param_formula'][row_index] == 'PM10' and 80.1 <= input_data_frame['value'][row_index] <= 110) \
            or (input_data_frame['param_formula'][row_index] == 'PM2.5' and 55.1 <= input_data_frame['value'][row_index] <= 75) \
            or (input_data_frame['param_formula'][row_index] == '03' and 150.1 <= input_data_frame['value'][row_index] <= 180) \
            or (input_data_frame['param_formula'][row_index] == 'NO2' and 150.1 <= input_data_frame['value'][row_index] <= 200) \
            or (input_data_frame['param_formula'][row_index] == 'S02' and 200.1 <= input_data_frame['value'][row_index] <= 350) \
            or (input_data_frame['param_formula'][row_index] == 'C6H6' and 16.1 <= input_data_frame['value'][row_index] <= 21) \
            or (input_data_frame['param_formula'][row_index] == 'CO' and 11.1 <= input_data_frame['value'][row_index] <= 15):
                input_data_frame['air_quality'][row_index] = 'satisfactory'

        elif (input_data_frame['param_formula'][row_index] == 'PM10' and 110.1 <= input_data_frame['value'][row_index] <= 150) \
            or (input_data_frame['param_formula'][row_index] == 'PM2.5' and 75.1 <= input_data_frame['value'][row_index] <= 110) \
            or (input_data_frame['param_formula'][row_index] == '03' and 180.1 <= input_data_frame['value'][row_index] <= 240) \
            or (input_data_frame['param_formula'][row_index] == 'NO2' and 200.1 <= input_data_frame['value'][row_index] <= 240) \
            or (input_data_frame['param_formula'][row_index] == 'S02' and 350.1 <= input_data_frame['value'][row_index] <= 500) \
            or (input_data_frame['param_formula'][row_index] == 'C6H6' and 21.1 <= input_data_frame['value'][row_index]<= 51) \
            or (input_data_frame['param_formula'][row_index] == 'CO' and 15.1 <= input_data_frame['value'][row_index] <= 21):
                input_data_frame['air_quality'][row_index] = 'bad'

        elif (input_data_frame['param_formula'][row_index] == 'PM10' and input_data_frame['value'][row_index] > 150) \
            or (input_data_frame['param_formula'][row_index] == 'PM2.5' and input_data_frame['value'][row_index] > 110) \
            or (input_data_frame['param_formula'][row_index] == '03' and input_data_frame['value'][row_index] > 240) \
            or (input_data_frame['param_formula'][row_index] == 'NO2' and input_data_frame['value'][row_index] > 240) \
            or (input_data_frame['param_formula'][row_index] == 'S02' and input_data_frame['value'][row_index] > 500) \
            or (input_data_frame['param_formula'][row_index] == 'C6H6' and input_data_frame['value'][row_index] > 51) \
            or (input_data_frame['param_formula'][row_index] == 'CO' and input_data_frame['value'][row_index] > 21):
                input_data_frame['air_quality'][row_index] = 'very bad'

        elif (input_data_frame['param_formula'][row_index] == 'PM10' and input_data_frame['value'][row_index] is None) \
            or (input_data_frame['param_formula'][row_index] == 'PM2.5' and input_data_frame['value'][row_index] is None) \
            or (input_data_frame['param_formula'][row_index] == 'O3' and input_data_frame['value'][row_index] is None) \
            or (input_data_frame['param_formula'][row_index] == 'NO2' and input_data_frame['value'][row_index] is None) \
            or (input_data_frame['param_formula'][row_index] == 'SO2' and input_data_frame['value'][row_index] is None) \
            or (input_data_frame['param_formula'][row_index] == 'C6H6' and input_data_frame['value'][row_index] is None) \
            or (input_data_frame['param_formula'][row_index] == 'CO' and input_data_frame['value'][row_index] is None):
                input_data_frame['air_quality'][row_index] = 'no index'

    return input_data_frame


list_of_objects = data_extraction()

outcome_data_frame = generating_data_frame(list_of_objects)

data_frame = data_transformation(outcome_data_frame)

data_frame = data_air_quality(outcome_data_frame)
data_frame = data_air_quality(outcome_data_frame)

# print(data_frame.to_string())

print(outcome_data_frame.head(5))

# print(list(data_frame.columns.values))
