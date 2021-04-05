"""
{'date': '2021-03-27 19:00:00', 'value': 9.04482}
{'id': 114, 'stationName': 'Wrocław - Bartnicza', 'gegrLat': '51.115933', 'gegrLon': '17.141125', 'city':
    {'name': 'Wrocław', 'commune':
        {'communeName': 'Wrocław', 'districtName': 'Wrocław', 'provinceName': 'DOLNOŚLĄSKIE'}},
 'addressStreet': 'ul. Bartnicza'}
{'param':
    {'paramName': 'dwutlenek azotu', 'paramFormula': 'NO2'}}
"""

"""
{'id': 14397,
 'param': {'idParam': 3,
           'paramCode': 'PM10',
           'paramFormula': 'PM10',
           'paramName': 'pył zawieszony PM10'},
 'stationId': 52}
"""

"""
{
    "key": "PM10",
    "values": [
    {
        "date": "2017-03-28 11:00:00",
        "value": 30.3018
    },
    {
        "date": "2017-03-28 12:00:00",
        "value": 27.5946
    }]
}
"""

"""
{
    "key": "PM10",
    "values": [
    {
        "date": "2017-03-28 11:00:00",
        "value": 30.3018
    },
    {
        "date": "2017-03-28 12:00:00",
        "value": 27.5946
    }]
}
"""


class Measurement:
    def __init__(
                 self,
                 date: str,
                 value: float,
                 id: int,
                 stationName: str,
                 latitude: str,
                 longitude: str,
                 communeName: str,
                 districtName: str,
                 provinceName: str,
                 addressStreet: str,
                 stationId: int,
                 paramName: str,
                 paramFomula: str,
                 idParam: int
                ):
        self.date = date if date else ''
        self.value = value if value else 0
        self.id = id if id else 0
        self.station_name = stationName if stationName else ''
        self.latitude = latitude if latitude else ''
        self.longitude = longitude if longitude else ''
        self.location = {'lat': latitude, 'lon': longitude}
        self.commune_name = communeName if communeName else ''
        self.district_name = districtName if districtName else ''
        self.province_name = provinceName if provinceName else ''
        self.address_street = addressStreet if addressStreet else ''
        self.station_id = stationId if stationId else 0
        self.param_name = paramName if paramName else ''
        self.param_formula = paramFomula if paramFomula else ''
        self.id_param = idParam if idParam else ''

    def serialize(self):
        return self.__dict__
