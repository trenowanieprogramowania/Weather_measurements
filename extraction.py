from pprint import pprint

import requests
import pandas as pd

from measurement import Measurement


def generate_data_frame():
    list_of_objects = []

    url_base = "http://api.gios.gov.pl/pjp-api/rest/"
    url_of_stations = url_base + "station/findAll"
    url_of_single_station_base = url_base + "station/sensors/"
    url_of_single_sensor_base = url_base + "data/getData/"

    json_of_all_stations = requests.get(url_of_stations).json()

    for currently_analysed_station in json_of_all_stations:
        # pprint(currently_analysed_station)

        list_of_sensors_of_station = requests.get(url_of_single_station_base
                                                  + str(currently_analysed_station["id"])).json()

        for currently_analysed_sensor in list_of_sensors_of_station:
            pprint(currently_analysed_sensor)

            list_of_measurements_of_single_sensor = requests.get(url_of_single_sensor_base
                                                                 + str(currently_analysed_sensor["id"])).json()

            for current_measurement in list_of_measurements_of_single_sensor['values']:
                print(f"currently analysed station: {currently_analysed_station}")

                print(f"currently analysed sensor: {currently_analysed_sensor}")

                print(f"current measurement: {current_measurement}")
                print("***********************************************************************")

                single_sample = Measurement(
                    date=current_measurement['date'],
                    value=current_measurement['value'],
                    id=currently_analysed_station['id'],
                    stationName=currently_analysed_station['stationName'],
                    latitude=currently_analysed_station['gegrLat'],
                    longitude=currently_analysed_station['gegrLon'],
                    communeName=currently_analysed_station['city']['name']['communeName'],
                    districtName=currently_analysed_station['city']['name']['districtName'],
                    provinceName=currently_analysed_station['city']['name']['provinceName'],
                    addressStreet=currently_analysed_station['addressStreet'],
                    stationId=currently_analysed_sensor['id'],
                    paramName=currently_analysed_sensor['param']['paramName'],
                    paramFomula=currently_analysed_sensor['param']['paramFormula'],
                    idParam=currently_analysed_sensor['param']['idParam']
                )



generate_data_frame()


""""
parameter = "addressStreet"
other_parameter = "id"

extraction = requests.get(url_address)
# variable given in the form of list of dictionaries
# hence - first index: integer
dictionary_form = extraction.json()

number_of_stations = len(dictionary_form)

id_of_stations = []
id_of_sensors = []
list_of_average_values_from_stations = []

for index in range(number_of_stations):
    id_of_stations.append(dictionary_form[index][other_parameter])

print("Figuring out id of stations")

# acquiring station base parameters
for id_of_station in id_of_stations:
    station_base_url = station_base_url_base + str(id_of_station)

    station_data_first_form = requests.get(station_base_url)
    station_data_extracted_form = station_data_first_form.json()

    for index_of_sensor in range(len(station_data_extracted_form)):
        considered_parameter = "id"
        id_of_sensors.append(station_data_extracted_form[index_of_sensor][considered_parameter])

    station_base_url = station_base_url_base

print(id_of_sensors)
"""

"""
print("completing final part of computations")

print("Figuring out id of sensors")

# acquiring sensor parameters
for index, id_of_sensor in enumerate(id_of_sensors):
    url_of_measured_data = url_of_measured_data_base + str(id_of_sensor)

    acquired_measured_data = requests.get(url_of_measured_data)
    extracted_measured_data = acquired_measured_data.json()

    sum_value = 0
    number_of_measurements = len(extracted_measured_data["values"])

    # avoiding division by 0
    if number_of_measurements == 0:
        number_of_measurements = 1

    for single_measurement in extracted_measured_data["values"]:
        current_data = single_measurement["value"]

        if current_data is not None:
            sum_value += current_data

    average_value = float(sum_value) / float(number_of_measurements)

    list_of_average_values_from_stations.append(average_value)

    url_of_measured_data = url_of_measured_data_base

    print(f"completed computation no. {index}")

print("computations completed")

print(list_of_average_values_from_stations)
"""

"""
acquired_measured_data = requests.get(url_of_measured_data_base + "92").json()['values']

# pprint(acquired_measured_data)

formatted_data = pd.DataFrame(acquired_measured_data)

# pprint(pd.DataFrame(formatted_data['values'][0:3]))

headers_of_column = list(acquired_measured_data[0].keys())
series_of_data = []

for current_dictionary in acquired_measured_data:
    pprint(current_dictionary)
    series_of_data.append(list(current_dictionary.values()))

pprint(headers_of_column)
print('*****************************************************')
pprint(series_of_data)

obtained_data_frame = pd.DataFrame(data=series_of_data, columns=headers_of_column)

obtained_data_frame['measurement'] = obtained_data_frame["value"] > 10

pprint(obtained_data_frame)
"""
