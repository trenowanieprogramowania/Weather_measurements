from actions_applied_to_data.data_manipulation import data_air_quality_with_loc_method

from primary_operations.extraction import data_extraction, generating_data_frame

# plot_time_performance(number_of_samples=20, size_of_step=1, initial_step=1)

list_of_objects = data_extraction(limited_number_of_samples=1)

outcome_data_frame1 = generating_data_frame(list_of_objects)
# outcome_data_frame2 = generating_data_frame(list_of_objects)

# data_frame = data_transformation(outcome_data_frame)

data_frame1 = data_air_quality_with_loc_method(outcome_data_frame1)
# data_frame2 = data_air_quality_without_loc_method(outcome_data_frame2)

# data_frame1_with_temperature = create_temperature_column(data_frame1)

# data_frame1_with_pressure = create_pressure_column(data_frame1_with_temperature)

# data_frame1_with_humidity = create_humidity_column(data_frame1_with_pressure)


# other_data_frame1 = data_air_quality_without_loc_method(outcome_data_frame1)
# other_data_frame2 = data_air_quality_with_loc_method(data_frame2)

# print(data_frame1.equals(data_frame2))
print(data_frame1.to_string())
# print(data_frame1_with_humidity.to_string())
# print('Other dataFrame-------------------------------------------------------------------------------------')
# print(data_frame2.to_string())

# present_aggregated_data(data_frame1)

# print(data_frame1.tail(5))
# print('-----------------------')
# print(data_frame2.tail(5))
