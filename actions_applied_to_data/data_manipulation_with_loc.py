import pandas as pd


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
    }

    pollution_table = pd.DataFrame(data_for_data_frame)

    print(pollution_table.to_string())

    merged_table = pd.merge(input_data_frame, pollution_table)

    merged_table.loc[merged_table['value'] <= merged_table["Very good"]
    , 'air_quality_index'] = "very good"

    merged_table.loc[(merged_table["Very good"] < merged_table['value'])
                     &
                     (merged_table['value'] <= merged_table["Good"])
    , 'air_quality_index'] = "good"

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

    name_of_columns_for_elimination = ['Very bad', 'Bad', 'Satisfactory', 'Moderate', 'Good', 'Very good']

    for name_of_current_column in name_of_columns_for_elimination:
        del merged_table[name_of_current_column]

    return merged_table
