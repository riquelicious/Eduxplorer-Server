import mariadb
from .ContextManager import  RequestContextManager , CreationContextManager

class RequestHandler:
	def insert_account(self, account):
		print("account")
		try:
			with RequestContextManager() as cursor:
				cursor.execute("SELECT * FROM accounts WHERE username = %s", (account['username'],))
				if cursor.fetchone():
					print("Username is already in use.")
					return {"success": False, "error": "Username is already in use."}
				cursor.execute("SELECT * FROM accounts WHERE email = %s", (account['email'],))
				if cursor.fetchone():
					print("Email is already in use.")
					return {"success": False, "error": "Email is already in use."}
				sql = """
					INSERT INTO accounts (username, password, email, account_type)
					VALUES (%s, %s, %s, %s)
				"""
				cursor.execute(sql, (account['username'], account['password'], account['email'], account['account_type']))
				print("Account created successfully.")
				return {"success": True, "message": "Account created successfully."}
		except mariadb.Error as err:
			return {"success": False, "message": f"Error: {err}"}

	def login(self, email, password):
		try:
			with RequestContextManager() as cursor:
				cursor.execute("SELECT * FROM accounts WHERE email = %s AND password = %s", (email, password))
				result = cursor.fetchone()
				if result:
					return {"success": True, "message": "Login successful."}
				else:
					return {"success": False, "error": "Invalid email or password."}
		except mariadb.Error as err:
			return {"success": False, "message": f"Error: {err}"}

	def get_region(self):
		try:
			with RequestContextManager() as cursor:
				cursor.execute("SELECT * FROM region")
				result = cursor.fetchall()
				
				regions = { 
					"regions": []}
				for row in result:
					region = {
						"region_code": row[0],
						"region_name": row[1]
					}

					regions["regions"].append(region)

				return regions
		except mariadb.Error as err:
			return {"success": False, "message": f"Error: {err}"}

	def filter_province(self, region_code):
		try:
			with RequestContextManager() as cursor:
				cursor.execute("SELECT * FROM province WHERE region_code = %s", (region_code,))
				result = cursor.fetchall()
			
				provinces = {
					"provinces": []
				}
				for row in result:
					province = {
						"province_code": row[0],
						"province_name": row[1],
						"region_code": row[2]
					}

					provinces["provinces"].append(province)

				return provinces
		except mariadb.Error as err:
			return {"success": False, "message": f"Error: {err}"}

	def filter_city(self, province_code):
		try:
			with RequestContextManager() as cursor:
				cursor.execute("SELECT * FROM city WHERE province_code = %s", (province_code,))
				result = cursor.fetchall()
				
				cities = {
					"cities": []
				}
				for row in result:
					city = {
						"city_code": row[0],
						"city_name": row[1],
						"province_code": row[2]
					}

					cities["cities"].append(city)

				return cities
		except mariadb.Error as err:
			return {"success": False, "message": f"Error: {err}"}

	def filter_barangay(self, city_code):
		try:
			with RequestContextManager() as cursor:
				cursor.execute("SELECT * FROM barangay WHERE city_code = %s", (city_code,))
				result = cursor.fetchall()

				barangays = {
					"barangays": []
				}
				for row in result:
					barangay = {
						"brgy_code": row[0],
						"brgy_name": row[1],
						"city_code": row[2]
					}

					barangays["barangays"].append(barangay)
				return barangays
		except mariadb.Error as err:
			return {"success": False, "message": f"Error: {err}"}


	def get_levels(self):
		try:
			with RequestContextManager() as cursor:
				cursor.execute("SELECT * FROM levels ORDER BY level_id ASC")
				result = cursor.fetchall()
				
				levels = {
					"levels": []
				}
				for row in result:
					level = {
						"level_id": row[0],
						"level_name": row[1]
					}

					levels["levels"].append(level)
					
				return levels
		except mariadb.Error as err:
			return {"success": False, "message": f"Error: {err}"}
		
	def fetch_filtered_tracks(self, query):
		try:
			with RequestContextManager() as cursor:
				if query == "":
					cursor.execute("SELECT * FROM tracks")
				else:
					cursor.execute("SELECT * FROM tracks WHERE track_name LIKE %s", ('%' + query + '%',))
				result = cursor.fetchall()
				
				tracks = {
					"tracks": []
				}
				for row in result:
					track = {
						"track_id": row[0],
						"track_name": row[1]
					}

					tracks["tracks"].append(track)

				return tracks
		except mariadb.Error as err:
			return {"success": False, "message": f"Error: {err}"}
		
	def fetch_filtered_courses(self, query):
		try:
			with RequestContextManager() as cursor:
				if query == "":
					cursor.execute("SELECT * FROM courses")
				else:
					cursor.execute("SELECT * FROM courses WHERE course_name LIKE %s", ('%' + query + '%',))
				result = cursor.fetchall()
					
				tracks = {
					"tracks": []
				}
				for row in result:
					track = {
						"track_id": row[0],
						"track_name": row[1]
					}

					tracks["tracks"].append(track)

				return tracks
		except mariadb.Error as err:
			return {"success": False, "message": f"Error: {err}"}