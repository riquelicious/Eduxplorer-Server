from os import listdir
from os.path import join, dirname
import json

class LocationDataParser:
    def __init__(self):
        self.data_dir = join(dirname(__file__), 'philippine-addresses-main')
        self.data_files = listdir(self.data_dir)
        self.barangay = "barangay.json"
        self.city = "city.json"
        self.province = "province.json"
        self.region = "region.json"

    def parse(self, file_name):
        with open(join(self.data_dir, file_name), 'r') as file:
            data = json.load(file)
            
            if isinstance(data, list):
                if file_name == self.barangay:
                    return [(d['brgy_code'], d['brgy_name'], d['city_code']) for d in data]
                elif file_name == self.city:
                    return [(d['city_code'], d['city_name'], d['province_code']) for d in data]
                elif file_name == self.province:
                    return [(d['province_code'], d['province_name'], d['region_code']) for d in data]
                elif file_name == self.region:
                    return [(d['region_code'], d['region_name']) for d in data]
                else:
                    return ValueError(f"Invalid data format in {file_name}")
    
    def parse_barangay(self):  
        return self.parse(self.barangay)

    def parse_city(self):
        return self.parse(self.city)

    def parse_province(self):
        return self.parse(self.province)

    def parse_region(self):
        return self.parse(self.region)
    