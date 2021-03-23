import requests

url_address = "http://api.gios.gov.pl/pjp-api/rest/station/findAll"
station_base_url_base = "http://api.gios.gov.pl/pjp-api/rest/station/sensors/"
url_of_measured_data_base = "http://api.gios.gov.pl/pjp-api/rest/data/getData/"

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
