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
