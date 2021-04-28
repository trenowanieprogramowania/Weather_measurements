class Measurement:
    registry_list = []

    def __init__(
                 self,
                 date: str,
                 value: float,
                 id: int,
                 stationName: str,
                 communeName: str,
                 districtName: str,
                 provinceName: str,
                 addressStreet: str,
                 stationId: int,
                 paramName: str,
                 paramFormula: str,
                 idParam: int,
                 **kwargs
                ):
        self.date = date if date else ''
        self.value = value if value else 0
        self.id = id if id else 0
        self.station_name = stationName if stationName else ''
        self.location = {'lat': kwargs['gegrLat'], 'lon': kwargs['gegrLon']} \
            if 'gegrLat' and 'gegrLon' in kwargs.keys() else {'lat': '', 'lon': ''}
        self.commune_name = communeName if communeName else ''
        self.district_name = districtName if districtName else ''
        self.province_name = provinceName if provinceName else ''
        self.address_street = addressStreet if addressStreet else ''
        self.station_id = stationId if stationId else 0
        self.param_name = paramName if paramName else ''
        self.param_formula = paramFormula if paramFormula else ''
        self.id_param = idParam if idParam else ''

        Measurement.registry_list.append(self)

    def serialize(self):
        return self.__dict__
    """
    TODO
    - convert to class method
    - consider putting and extracting from list (details to be completed)
    """
    def determine_headers(self):
        return list(self.serialize().keys())

    @classmethod
    def generate_data(cls):
        generated_grid = []

        for index in range(len(cls.registry_list)):
            empty_entry = []

            generated_grid.append(empty_entry)

        for current_entry, constructed_object_in_class in zip(generated_grid, cls.registry_list):
            current_entry.append(constructed_object_in_class)

        return generated_grid


def generate_data1(list_of_objects: list):
    outcome_list = []

    for current_object in list_of_objects:
        outcome_list.append(list(current_object.__dict__.values()))

    return outcome_list
