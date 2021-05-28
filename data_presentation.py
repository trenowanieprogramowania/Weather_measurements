import pandas as pd

from data_manipulation import data_air_quality_without_loc_method


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
    # outline_of_stations2 = input_data_frame.groupby(['commune_name', 'district_name', 'address_street'],
    #                                                as_index=False)['location'].count()

    # outline_of_stations2 = outline_of_stations2.rename(columns={'location': 'number of stations'})

    # output = pd.concat([outline_of_stations, outline_of_stations2['number of stations']], axis=1)

    # print(output.to_string())

    # print('--------------------groupby_result - distribution of amount of compounds per location--------------------')

    # location_column = input_data_frame['location']
    # location_column = location_column.apply(lambda coordinate: (coordinate['lat'], coordinate['lon']))

    # mean_value = input_data_frame.groupby(['commune_name', 'param_formula'], as_index=False)['value'].mean()
    # attempted_form = input_data_frame.groupby(['location_lat', 'location_lon', 'param_formula'],
    #                                          as_index=False)['value'].mean()
    '''
    print('attempted form')
    print(attempted_form.to_string())


    # coordinates_table = pd.DataFrame()
    # coordinates_table['latitude'] = location_column.apply(lambda component: component[0])
    # coordinates_table['longitude'] = location_column.apply(lambda component: component[1])

    # combined_location_and_compounds = pd.concat([coordinates_table,
    #                                             input_data_frame['param_formula'],
    #                                             input_data_frame['value']],
    #                                            axis=1)
    '''
    # print('-----------------------combined location and compounds dataFrame-----------------------------------')
    # print(f' dimension of input dataFrame: {input_data_frame.shape}')
    # print(f' dimension of output dataFrame: {combined_location_and_compounds.shape}')
    # print(combined_location_and_compounds.to_string())

    # condensed_form = combined_location_and_compounds.groupby(['latitude', 'longitude', 'param_formula'])['value'].mean()

    # print(condensed_form.to_string())

    print('--------------------groupbyresult - cumulative mean for compounds per station--------------------')

    cumulative_table = input_data_frame.groupby(['station_id', 'date', 'param_formula'])['value'].expanding().mean()

    print(cumulative_table.to_string())

    print('------------groupby additional result - distribution of average density of compounds------------')

    density_table = input_data_frame.groupby(['param_formula'], as_index=False)['value'].mean()

    print(density_table.to_string())

    # print('plotting histogram')
    # density_table.plot(x='param_formula', y='value', kind='bar', rot=5, fontsize=4)
    # plt.show()
    # print('completing plotting histogram')

    # pd.crosstab(input_data_frame)