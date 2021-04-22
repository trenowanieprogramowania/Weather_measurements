from pprint import pprint

import requests

from measurement import Measurement


def generate_data_frame():
    list_of_objects = []
    alternative_list_of_objects = []

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


                # condition for checking existence of 'polluted' (incomplete) data
                if current_measurement['value'] is None or currently_analysed_station['gegrLon'] is None or \
                        currently_analysed_station['gegrLon'] is None:
                    continue

                single_sample = Measurement(
                    date=current_measurement['date'],
                    value=current_measurement['value'],
                    id=currently_analysed_station['id'],
                    stationName=currently_analysed_station['stationName'],
                    latitude=currently_analysed_station['gegrLat'],
                    longitude=currently_analysed_station['gegrLon'],
                    communeName=currently_analysed_station['city']['commune']['communeName'],
                    districtName=currently_analysed_station['city']['commune']['districtName'],
                    provinceName=currently_analysed_station['city']['commune']['provinceName'],
                    addressStreet=currently_analysed_station['addressStreet'],
                    stationId=currently_analysed_sensor['id'],
                    paramName=currently_analysed_sensor['param']['paramName'],
                    paramFomula=currently_analysed_sensor['param']['paramFormula'],
                    idParam=currently_analysed_sensor['param']['idParam']
                )

                list_of_sample = Measurement.serialize(single_sample)
                # list_of_sample = {}
                
                # list_of_sample['date'] = single_sample.date
                # list_of_sample['value'] = single_sample.value
                # list_of_sample['id'] = single_sample.id
                # list_of_sample['stationName'] = single_sample.station_name
                # list_of_sample['gegrLat'] = single_sample.latitude
                # list_of_sample['gegrLon'] = single_sample.longitude
                # list_of_sample['communeName'] = single_sample.location
                # list_of_sample['districtName'] = single_sample.commune_name
                # list_of_sample['provinceName'] = single_sample.district_name
                # list_of_sample['addressStreet'] = single_sample.province_name
                # list_of_sample['stationId'] = single_sample.address_street
                # list_of_sample['paramName'] = single_sample.station_id
                # list_of_sample['paramFormula'] = single_sample.param_name
                # list_of_sample['idParam'] = single_sample.id_param

                print('---------------------------------------------------------------------------------------')
                print(list_of_sample)
                print('---------------------------------------------------------------------------------------')

                list_of_objects.append(list_of_sample)

    return list_of_objects


generate_data_frame()
