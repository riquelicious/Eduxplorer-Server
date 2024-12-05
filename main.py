from flask import Flask
from flask_cors import CORS
import threading
import time
from Components.AccountManager import AccountManager
from Components.DataBaseManager import DataBaseManager
from Components.LocationManager import LocationManager
from Components.SchoolManager import SchoolManager

app = Flask(__name__) 
CORS(app)

class MainServer:
	def __init__(self):

		self.backup_delay = 24 * 60 * 60 # 24 hours

		#don't touch code past this line
		self.account_manager = AccountManager()
		self.database_manager = DataBaseManager()
		self.location_manager = LocationManager()
		self.school_manager = SchoolManager()

		#start backup thread
		threading.Thread(target=self.backup_thread, daemon=True).start()

		#!routes
		
        #account
		app.add_url_rule('/login', view_func=self.account_manager.login, methods=['POST'])
		app.add_url_rule('/create_account', view_func=self.account_manager.create_account, methods=['POST'])
		app.add_url_rule('/change_password', view_func=self.account_manager.change_password, methods=['POST'])

        #location
		app.add_url_rule('/get_region', view_func=self.location_manager.get_region, methods=['GET'])
		app.add_url_rule('/filter_province', view_func=self.location_manager.filter_province, methods=['POST'])
		app.add_url_rule('/filter_city', view_func=self.location_manager.filter_city, methods=['POST'])
		app.add_url_rule('/filter_barangay', view_func=self.location_manager.filter_barangay, methods=['POST'])

		#schools
		app.add_url_rule('/get_levels', view_func=self.school_manager.get_levels, methods=['GET'])
		app.add_url_rule('/filtered_tracks', view_func=self.school_manager.fetch_filtered_data, methods=['POST'])

		
		


	def backup_thread(self):
		while True:
			time.sleep(self.backup_delay)
			print("Backing up database...")
			self.handler.backup_database()
			print("Database backup completed")

if __name__ == "__main__":
	server = MainServer()
	server.database_manager.create_database()
	app.run(host="0.0.0.0", port=5000)
