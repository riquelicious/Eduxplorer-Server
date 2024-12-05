from os.path import join, dirname
import json
from enum import Enum

class SchoolDataParser:
    class JSON_PATH(Enum):
        COURSE = 'edu_course.json'
        TRACK = 'edu_track.json'
        LEVELS = 'school_levels.json'
        KINDER = 'school_kindergarten.json'
        ELEMENTARY = 'school_elementary.json'
        HIGH = 'school_highschool.json'
        SENIOR = 'school_seniorhighschool.json'
        COLLEGE = 'school_college.json'

    def __init__(self):
        self.data_dir = join(dirname(__file__), 'SchoolData')

    
    def parse(self, file_name):
        with open(join(self.data_dir, file_name), 'r') as file:
            data = json.load(file)
            assert isinstance(data, list), f"Invalid data format in {file_name}"
            return data

    # ? Format functions ================================================================================

    def format_schools(self, data):
        return [(d['School'], d['Location']) for d in data]
    
    def format_tracks(self, data):
        return [(track,) for track in data]

    def format_connected_courses(self, data):
        return [(d['School'], t) for d in data for t in d['Tracks']]

    def format_levels(self, data):
        return [(level,) for level in data]


    # ? School Data ====================================================================================

    def parse_level(self):
        data = self.parse(self.JSON_PATH.LEVELS.value)
        return self.format_levels(data)

    def parse_seniorhighschool(self):
        data = self.parse(self.JSON_PATH.SENIOR.value)
        return self.format_schools(data)

    def parse_kindergarten(self):
        data = self.parse(self.JSON_PATH.KINDER.value)
        return self.format_schools(data)
        
    def parse_elementary(self):
        data = self.parse(self.JSON_PATH.ELEMENTARY.value)
        return self.format_schools(data)
    
    def parse_highschool(self):
        data = self.parse(self.JSON_PATH.HIGH.value)
        return self.format_schools(data)        
    
    def parse_college(self):
        data = self.parse(self.JSON_PATH.COLLEGE.value)
        return self.format_schools(data)
    
    # ? Track and Course Data  =====================================================================================

    def parse_track(self):
        data = self.parse(self.JSON_PATH.TRACK.value)
        return self.format_tracks(data)
        
    def parse_course(self):
        data = self.parse(self.JSON_PATH.COURSE.value)
        return self.format_tracks(data)
    
    def parse_connected_courses(self):
        data = self.parse(self.JSON_PATH.COLLEGE.value)
        return self.format_connected_courses(data)
    
    def parse_connected_tracks(self):
        data = self.parse(self.JSON_PATH.SENIOR.value)
        return self.format_connected_courses(data)
