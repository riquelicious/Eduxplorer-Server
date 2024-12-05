from flask import  request, jsonify


from .RequestManager import RequestHandler

class SchoolManager:
    def __init__(self):
        self.requester = RequestHandler()
   
    def get_levels(self):
        return jsonify(self.requester.get_levels()), 200

    def fetch_filtered_data(self):
        data = request.get_json()
        print(data)
        level = data["level"]
        query = data["query"]
        if level == '4':
            return jsonify(self.requester.fetch_filtered_tracks(query)), 200
        elif level == '5':
            return jsonify(self.requester.fetch_filtered_courses(query)), 200
        return jsonify({"success": False, "message": "Invalid level"}), 400