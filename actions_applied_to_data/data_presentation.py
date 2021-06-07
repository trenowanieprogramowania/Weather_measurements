import pandas as pd

from actions_applied_to_data.data_manipulation import data_air_quality_without_loc_method


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
    outline_of_stations = input_data_frame.groupby(['location_lat', 'location_lon', 'commune_name',
                                                    'district_name', 'address_street'],
                                                   as_index=False)['value'].mean()

    print(outline_of_stations.to_string())

    print('--------------------group_by result - cumulative mean for compounds per station--------------------')

    cumulative_table = input_data_frame.groupby(['station_id', 'date', 'param_formula'])['value'].expanding().mean()

    print(cumulative_table.to_string())

    print('------------group_by additional result - distribution of average density of compounds------------')

    density_table = input_data_frame.groupby(['param_formula'], as_index=False)['value'].mean()

    print(density_table.to_string())
