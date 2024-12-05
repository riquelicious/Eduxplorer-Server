from flask import  request, jsonify


from .RequestManager import RequestHandler

class LocationManager:
    def __init__(self):
        self.requester = RequestHandler()
   
    def get_region(self):
        return jsonify(self.requester.get_region()), 200

    def filter_province(self):        
        data = request.get_json()
        region = data["code"]
        return jsonify(self.requester.filter_province(region)), 200

    def filter_city(self):
        data = request.get_json()
        province = data["code"]
        return jsonify(self.requester.filter_city(province)), 200

    def filter_barangay(self):
        data = request.get_json()
        city = data["code"]
        return jsonify(self.requester.filter_barangay(city)), 200