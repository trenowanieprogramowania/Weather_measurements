import matplotlib.pyplot as plt
import numpy as np

import time

from extraction import data_extraction, generating_data_frame

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