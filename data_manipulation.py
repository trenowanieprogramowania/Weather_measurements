import pandas as pd

import json


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
    # with open('air_quality_index.json', 'r') as investigated_source:
    #    investigated_compounds = json.load(investigated_source)

    data_for_data_frame = {
        "PM10": [
            (150, float('inf')),
            (110, 150),
            (80, 110),
            (50, 80),
            (20, 50),
            (0, 20)
        ],

        "PM2.5": [
            (110, float('inf')),
            (75, 110),
            (55, 75),
            (35, 55),
            (13, 35),
            (0, 13)
        ],

        "O3": [
            (240, float('inf')),
            (180, 240),
            (150, 180),
            (120, 150),
            (70, 120),
            (0, 70)
        ],

        "NO2": [
            (400, float('inf')),
            (200, 400),
            (150, 200),
            (100, 150),
            (40, 100),
            (0, 40)
        ],

        "SO2": [
            (500, float('inf')),
            (350, 500),
            (200, 350),
            (100, 200),
            (50, 100),
            (0, 50)
        ],

        "C6H6": [
            (51, float('inf')),
            (21, 51),
            (16, 21),
            (11, 16),
            (6, 11),
            (0, 6)
        ],

        "CO": [
            (21, float('inf')),
            (15, 21),
            (11, 15),
            (7, 11),
            (3, 7),
            (0, 3)
        ]
    }

    # input_data_frame.loc[
    #                        , 'air_quality']

    pollution_table = pd.DataFrame(data_for_data_frame,
                                   index=['Very bad', 'bad', 'Satisfactory', 'Moderate', 'Good', 'Very good'])

    # print(pollution_table.index)

    input_data_frame.loc[pollution_table[input_data_frame['param_formula']][0]
                         < input_data_frame['value']
                         <= pollution_table[input_data_frame['param_formula']][1],
                         'air_quality'] = 'ok'


    '''
        pollution_table.index[pollution_table[input_data_frame['param_formula']][0]
                                                                < input_data_frame['value']
                                                                <= pollution_table[input_data_frame['param_formula']][1]
                                                                ]
    '''
    return input_data_frame

    '''
        given_compounds = set(input_data_frame['param_formula'])

        for currently_investigated_compound in given_compounds:
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
    '''
