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
    data_for_data_frame = {
        "param_formula": [
            "PM10",
            "PM2.5",
            "O3",
            "NO2",
            "SO2",
            "C6H6",
            "CO"
        ],

        "Very bad": [
            float('inf'),
            float('inf'),
            float('inf'),
            float('inf'),
            float('inf'),
            float('inf'),
            float('inf')
        ],

        "Bad": [
            150,
            110,
            240,
            400,
            500,
            51,
            21
        ],

        "Satisfactory": [
                    110,
                    75,
                    180,
                    200,
                    350,
                    21,
                    15
        ],

        "Moderate": [
                        80,
                        55,
                        150,
                        150,
                        200,
                        16,
                        11
        ],

        "Good": [
                50,
                35,
                120,
                100,
                100,
                11,
                7
        ],

        "Very good": [
                    20,
                    13,
                    70,
                    40,
                    50,
                    6,
                    3
        ]
        #
        # "PM10": [
        #     (150, float('inf')),
        #     (110, 150),
        #     (80, 110),
        #     (50, 80),
        #     (20, 50),
        #     (0, 20)
        # ],
        #
        # "PM2.5": [
        #     (110, float('inf')),
        #     (75, 110),
        #     (55, 75),
        #     (35, 55),
        #     (13, 35),
        #     (0, 13)
        # ],
        #
        # "O3": [
        #     (240, float('inf')),
        #     (180, 240),
        #     (150, 180),
        #     (120, 150),
        #     (70, 120),
        #     (0, 70)
        # ],
        #
        # "NO2": [
        #     (400, float('inf')),
        #     (200, 400),
        #     (150, 200),
        #     (100, 150),
        #     (40, 100),
        #     (0, 40)
        # ],
        #
        # "SO2": [
        #     (500, float('inf')),
        #     (350, 500),
        #     (200, 350),
        #     (100, 200),
        #     (50, 100),
        #     (0, 50)
        # ],
        #
        # "C6H6": [
        #     (51, float('inf')),
        #     (21, 51),
        #     (16, 21),
        #     (11, 16),
        #     (6, 11),
        #     (0, 6)
        # ],
        #
        # "CO": [
        #     (21, float('inf')),
        #     (15, 21),
        #     (11, 15),
        #     (7, 11),
        #     (3, 7),
        #     (0, 3)
        # ]
    }

    pollution_table = pd.DataFrame(data_for_data_frame) #,
                                   # index=['Very bad', 'bad', 'Satisfactory', 'Moderate', 'Good', 'Very good'])

    #result = input_data_frame.merge(pollution_table, how='left')

    print(pollution_table.to_string())

    merged_table = pd.merge(input_data_frame, pollution_table)

    # print(merged_table.to_string())

    merged_table.loc[merged_table['value'] <= merged_table["Very good"]
                    ,'air_quality_index'] = "very good"

    merged_table.loc[(merged_table["Very good"] < merged_table['value'])
                     &
                     (merged_table['value'] <= merged_table["Good"])
                    ,'air_quality_index'] = "good"

    merged_table.loc[(merged_table["Good"] < merged_table['value'])
                     &
                     (merged_table['value'] <= merged_table["Moderate"])
    , 'air_quality_index'] = "moderate"

    merged_table.loc[(merged_table["Moderate"] < merged_table['value'])
                     &
                     (merged_table['value'] <= merged_table["Satisfactory"])
    , 'air_quality_index'] = "satisfactory"

    merged_table.loc[(merged_table["Satisfactory"] < merged_table['value'])
                     &
                     (merged_table['value'] <= merged_table["Bad"])
    , 'air_quality_index'] = "bad"

    merged_table.loc[merged_table['value'] > merged_table["Bad"]
    , 'air_quality_index'] = "very bad"

    print('-------------------------------------------------------------------------------------------')

    # No common columns to perform merge on.
    # print(pollution_table['PM10'].loc[(pollution_table['PM10'].str[0] > input_data_frame['value']) &
    #                                  (input_data_frame['param_formula'] == 'PM10') ])

    
    '''
    input_data_frame.where((pollution_table[input_data_frame['param_formula']][0]
                           < input_data_frame['value']
                           <= pollution_table[input_data_frame['param_formula']][1],
                           )
    '''

    '''
    input_data_frame.loc[pollution_table.loc[pollution_table[input_data_frame['param_formula']]]
                         < input_data_frame['value'], 'air_quality'] = 'ok'

    '''

    '''
    print('-----------------pollution table-------------------------------')
    print(pollution_table[input_data_frame['param_formula']].to_string())

    input_data_frame.loc[
                            pollution_table[input_data_frame['param_formula']][0]
                            < input_data_frame['value']
                            <= pollution_table[input_data_frame['param_formula']][1],
                            'air_quality'
                        ] = 'ok'

    '''

    '''
    pollution_table.index[pollution_table[input_data_frame['param_formula']][0]
                                                                < input_data_frame['value']
                                                                <= pollution_table[input_data_frame['param_formula']][1]
                                                                ]
    '''
    
    # return input_data_frame


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
    '''
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
    '''

    # del merged_table['Very good']
    # del merged_table['Very bad': 'Very good']

    merged_table = pd.concat(merged_table['date':'latest'], merged_table['air_quality_index'])

    return merged_table
