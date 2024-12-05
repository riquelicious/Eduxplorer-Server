import mariadb
from colorama import Fore, Style
import os
import datetime
import inspect
from .ContextManager import CreationContextManager, RequestContextManager
from .LocationDataParser import LocationDataParser
from .SchoolDataParser import SchoolDataParser
from .DataBaseQueries import *


print( Fore.GREEN + "mariadb version: ",mariadb.__version__ + Style.RESET_ALL)


class DataBaseManager:
	def __init__(self):
		self.database = "eduxplorer_db"
		self.password = os.getenv('db_password')
		self.LocationParser = LocationDataParser()
		self.SchoolParser = SchoolDataParser()

	def backup_database(self):
		backup_file = f"{self.database}_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
		command = Fore.GREEN +  f"mysqldump -u root -p{self.password} {self.database} > ./Backups/{backup_file} " + Style.RESET_ALL
		os.system(command)
		print( Fore.GREEN + f"Backup created: {backup_file}" + Style.RESET_ALL)

	def create_database(self):
		# ? database
		self.create_db_if_not_exists()
		
		# ? accounts
		self.create_accounts_table()
		
		# ? locations
		self.create_region_table()
		self.create_province_table()
		self.create_city_table()
		self.create_barangay_table()

		# ? schools
		self.create_levels_table()
		self.create_kinder_table()
		self.create_elementary_table()
		self.create_highschool_table()
		self.create_seniorhighschool_table()
		self.create_college_table()

		# ? schools tracks and courses
		self.create_track_table()
		self.create_course_table()
		self.create_connected_tracks_table()
		self.create_connected_courses_table()


	def create_db_if_not_exists(self):
		try:
			with CreationContextManager() as cursor:
				cursor.execute(CREATE_DATABASE.format(db_name=self.database))
				print( Fore.GREEN + f"Database {self.database} created" + Style.RESET_ALL)
		except mariadb.Error as err:
			print( Fore.RED + "Database creation failed" + Style.RESET_ALL)
			print( Fore.RED + f"Error: {err}" + Style.RESET_ALL)

	def execute_query(self, query, query_name):
		try:
			with RequestContextManager() as cursor:
				cursor.execute(query)
				print( Fore.GREEN + f"Function: {inspect.currentframe().f_code.co_name} - {query_name} Table Created" + Style.RESET_ALL)
		except mariadb.Error as err:
			if hasattr(err, 'errno') and hasattr(err, 'msg'):
				print( Fore.RED + f"Error Code: {err.errno}, Message: {err.msg}" + Style.RESET_ALL)
			else:
				print( Fore.RED + f"Error: {err}" + Style.RESET_ALL)

	def populate_if_empty(self, table_name, insert_query,  function : callable = None, data = []):
		try:
			with RequestContextManager() as cursor:
				check_empty = f"SELECT COUNT(*) FROM {table_name}"
				cursor.execute(check_empty)
				(count,) = cursor.fetchone()
				if count == 0:
					if data == []:
						data = function()
					cursor.executemany(insert_query, data)
					print( Fore.GREEN + f"Function: {inspect.currentframe().f_code.co_name} - {table_name} Table Populated" + Style.RESET_ALL)
				else:
					print( Fore.YELLOW + f"Table {table_name} is not empty" + Style.RESET_ALL)
		except mariadb.Error as err:
			if hasattr(err, 'errno') and hasattr(err, 'msg'):
				print( Fore.RED + f"Function: {inspect.currentframe().f_code.co_name} - {table_name} Table population failed  || Error Code: {err.errno}, Message: {err.msg}" + Style.RESET_ALL)
				print(Fore.BLUE + f"Executing query: {insert_query}" + Style.RESET_ALL)
			else:
				print( Fore.RED + f"Function: {inspect.currentframe().f_code.co_name} - {table_name} Table population failed  || Error: {err}" + Style.RESET_ALL)
				print(Fore.BLUE + f"Executing query: {insert_query}" + Style.RESET_ALL)

	def data_to_id(self, function : callable, insert_query):
		school_course_pairs = []
		data = function()
		
		with RequestContextManager() as cursor:
			for item in data:
				school_name = item[0]
				course_name = item[1]
				# print(school_name, course_name, insert_query)
				cursor.execute( insert_query[0], (school_name,) )
				school_id = cursor.fetchone()
				cursor.execute( insert_query[1], (course_name,) )
				course_id = cursor.fetchone()
				if course_id == None or school_id == None:
					print(f"Course {course_name} not found")
					continue
				course_id = course_id[0]
				school_id = school_id[0]
				# print(school_id, course_id)
				if not (school_id, course_id) in school_course_pairs:
					school_course_pairs.append((school_id, course_id))
		return school_course_pairs

	# ? CREATE TABLES

	# ? Accounts Tables =========================================================================================

	def create_accounts_table(self):
		self.execute_query(CREATE_ACCOUNTS_TABLE, "Accounts")

	# ? Location Tables =========================================================================================	
	
	def create_region_table(self):
		self.execute_query(CREATE_REGION_TABLE, "Region")
		self.populate_if_empty("region", INSERT_REGION, self.LocationParser.parse_region)

	def create_province_table(self):
		self.execute_query(CREATE_PROVINCE_TABLE, "Province")
		self.populate_if_empty("province", INSERT_PROVINCE, self.LocationParser.parse_province)

	def create_city_table(self):
		self.execute_query(CREATE_CITY_TABLE, "City")
		self.populate_if_empty("city", INSERT_CITY, self.LocationParser.parse_city)

	def create_barangay_table(self):
		self.execute_query(CREATE_BARANGAY_TABLE, "Barangay")
		self.populate_if_empty("barangay", INSERT_BARANGAY, self.LocationParser.parse_barangay)

	# ? Schools Tables =========================================================================================
	
	def create_levels_table(self):
		self.execute_query(CREATE_LEVELS_TABLE, "Levels")
		self.populate_if_empty("levels", INSERT_LEVELS, self.SchoolParser.parse_level)

	def create_kinder_table(self):
		self.execute_query(CREATE_KINDER_TABLE, "Kinder")
		self.populate_if_empty("kinder", INSERT_KINDER, self.SchoolParser.parse_kindergarten)

	def create_elementary_table(self):
		self.execute_query(CREATE_ELEMENTARY_TABLE, "Elementary")
		self.populate_if_empty("elementary", INSERT_ELEMENTARY, self.SchoolParser.parse_elementary)

	def create_highschool_table(self):
		self.execute_query(CREATE_HIGHSCHOOL_TABLE, "HighSchool")
		self.populate_if_empty("junior_high_schools", INSERT_JUNIOR_HIGH_SCHOOL, self.SchoolParser.parse_highschool)

	def create_seniorhighschool_table(self):
		self.execute_query(CREATE_SENIOR_HIGH_SCHOOL_TABLE, "SeniorHighSchool")
		self.populate_if_empty("senior_high_schools", INSERT_SENIOR_HIGH_SCHOOL, self.SchoolParser.parse_seniorhighschool)

	def create_college_table(self):
		self.execute_query(CREATE_COLLEGE_TABLE, "College")
		self.populate_if_empty("colleges", INSERT_COLLEGE, self.SchoolParser.parse_college)

	# ? Schools Tracks and Courses Tables =========================================================================================

	def create_track_table(self):
		self.execute_query(CREATE_TRACKS_TABLE, "Track")
		self.populate_if_empty("tracks", INSERT_TRACK, self.SchoolParser.parse_track)

	def create_course_table(self):
		self.execute_query(CREATE_COURSE_TABLE, "Course")
		self.populate_if_empty("courses", INSERT_COURSE, self.SchoolParser.parse_course)

	def create_connected_courses_table(self):
		self.execute_query(CREATE_TABLE_COLLEGE_COURSES, "Connected Courses")
		data = self.data_to_id(self.SchoolParser.parse_connected_courses, CONVERT_CONNECTED_COURSES)
		self.populate_if_empty("connected_courses", INSERT_CONNECTED_COURSES, data = data)

	def create_connected_tracks_table(self):
		self.execute_query(CREATE_TABLE_SENIOR_TRACKS, "Connected Tracks")
		data = self.data_to_id(self.SchoolParser.parse_connected_tracks, CONVERT_CONNECTED_TRACKS)
		self.populate_if_empty("connected_tracks", INSERT_CONNECTED_TRACKS, data = data)
