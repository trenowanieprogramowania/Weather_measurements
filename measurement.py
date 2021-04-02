{'date': '2021-03-27 19:00:00', 'value': 9.04482}
{'id': 114, 'stationName': 'Wrocław - Bartnicza', 'gegrLat': '51.115933', 'gegrLon': '17.141125', 'city':
    {'name': 'Wrocław', 'commune':
        {'communeName': 'Wrocław', 'districtName': 'Wrocław', 'provinceName': 'DOLNOŚLĄSKIE'}},
 'addressStreet': 'ul. Bartnicza'}
{'param':
    {'paramName': 'dwutlenek azotu', 'paramFormula': 'NO2'}}


class Measurement:
    def __init__(self, date: str, value: float, id: int, stationName:str, latitude: str, longitude: str,
                 name: str, commune: str, districtName: str, provinceName: str,
                 addressStreet: str, paramName: str, paramFomula: str):
        self.date = date
        self.value = value if value else 0
        self.id = id
        self.station_name = stationName
        self.latitude = latitude
        self.longitude = longitude
        self.location = {'lat': latitude, "lon": longitude}
        self.name = name
        self.city = commune
        self.district_name = districtName
        self.province_name = provinceName
        self.address_street = addressStreet
        self.param_name = paramName
        self.param_formula = paramFomula

    def serialize(self):
        return self.__dict__
