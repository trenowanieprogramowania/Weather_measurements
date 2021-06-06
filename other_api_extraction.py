import requests

import pandas as pd


def get_temperature_for_given_city(input_data_frame: pd.DataFrame):
    if input_data_frame['latest']:
        api_url_base = 'http://api.openweathermap.org/data/2.5/weather?'
        api_id = 'a7d2731f602a8409c162c49eef541af8'

        latitude_of_city = input_data_frame['location_lat']
        longitude_of_city = input_data_frame['location_lon']

        # name_of_city = input_data_frame['commune_name']

        # url_of_city = api_url_base + 'q=' + name_of_city + '&appid=' + api_id

        url_of_city = api_url_base + "lat=" + latitude_of_city + "&" + "lon=" + longitude_of_city + "&" + "appid=" + api_id

        json_from_api = requests.get(url_of_city).json()

        temperature_of_city_in_kelvin = float(json_from_api['main']['temp'])
        temperature_of_city_in_celsius = temperature_of_city_in_kelvin - 273.13

        return temperature_of_city_in_celsius


def get_pressure_for_given_city(input_data_frame: pd.DataFrame):
    if input_data_frame['latest']:
        api_url_base = 'http://api.openweathermap.org/data/2.5/weather?'
        api_id = 'a7d2731f602a8409c162c49eef541af8'

        latitude_of_city = input_data_frame['location_lat']
        longitude_of_city = input_data_frame['location_lon']

        # name_of_city = input_data_frame['commune_name']

        # url_of_city = api_url_base + 'q=' + name_of_city + '&appid=' + api_id

        url_of_city = api_url_base + "lat=" + latitude_of_city + "&" + "lon=" + longitude_of_city + "&" + "appid=" + api_id

        json_from_api = requests.get(url_of_city).json()

        pressure_in_city = float(json_from_api['main']['pressure'])

        return pressure_in_city


def get_humidity_for_given_city(input_data_frame: pd.DataFrame):
    if input_data_frame['latest']:
        api_url_base = 'http://api.openweathermap.org/data/2.5/weather?'
        api_id = 'a7d2731f602a8409c162c49eef541af8'

        latitude_of_city = input_data_frame['location_lat']
        longitude_of_city = input_data_frame['location_lon']

        # name_of_city = input_data_frame['commune_name']

        # url_of_city = api_url_base + 'q=' + name_of_city + '&appid=' + api_id

        url_of_city = api_url_base + "lat=" + latitude_of_city + "&" + "lon=" + longitude_of_city + "&" + "appid=" + api_id

        json_from_api = requests.get(url_of_city).json()

        humidity_in_city = float(json_from_api['main']['humidity'])

        return humidity_in_city


def create_temperature_column(input_data_frame: pd.DataFrame):
    input_data_frame['temperature'] = input_data_frame.apply(get_temperature_for_given_city, axis=1)

    return input_data_frame


def create_pressure_column(input_data_frame: pd.DataFrame):
    input_data_frame['pressure'] = input_data_frame.apply(get_pressure_for_given_city, axis=1)

    return input_data_frame


def create_humidity_column(input_data_frame: pd.DataFrame):
    input_data_frame['humidity'] = input_data_frame.apply(get_humidity_for_given_city, axis=1)

    return input_data_frame
