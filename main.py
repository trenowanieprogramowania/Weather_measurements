import os

from dotenv import load_dotenv

from actions_applied_to_data.data_manipulation_iterative_method import data_air_quality_without_loc_method

from primary_operations.extraction import data_extraction, generating_data_frame
load_dotenv()

print(os.environ['app_id'])

list_of_objects = data_extraction(limited_number_of_samples=1)

outcome_data_frame1 = generating_data_frame()

data_frame1 = data_air_quality_without_loc_method(outcome_data_frame1)
