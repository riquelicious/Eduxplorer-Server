CREATE_DATABASE = """
CREATE DATABASE IF NOT EXISTS {db_name} 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""

# ? Accounts Tables =========================================================================================

CREATE_ACCOUNTS_TABLE = """
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    account_type ENUM('user', 'school') NOT NULL DEFAULT 'user'
);
"""

# ? Location Tables =========================================================================================

CREATE_REGION_TABLE = """
CREATE TABLE IF NOT EXISTS region (
    region_code VARCHAR(10) PRIMARY KEY,
    region_name VARCHAR(255)
);

"""

CREATE_PROVINCE_TABLE = """
CREATE TABLE IF NOT EXISTS province (
    province_code VARCHAR(10) PRIMARY KEY,
    province_name VARCHAR(255),
    region_code VARCHAR(10),
    FOREIGN KEY (region_code) REFERENCES region(region_code)
);
"""

CREATE_CITY_TABLE = """
CREATE TABLE IF NOT EXISTS city (
    city_code VARCHAR(10) PRIMARY KEY,
    city_name VARCHAR(255) NOT NULL,
    province_code VARCHAR(10) NOT NULL,
    FOREIGN KEY (province_code) REFERENCES province(province_code)
);
"""

CREATE_BARANGAY_TABLE = """
CREATE TABLE IF NOT EXISTS barangay (
    brgy_code VARCHAR(10) PRIMARY KEY,
    brgy_name VARCHAR(255) NOT NULL,
    city_code VARCHAR(10) NOT NULL,
    FOREIGN KEY (city_code) REFERENCES city(city_code)
);
"""

# ? Schools Tables =========================================================================================

CREATE_LEVELS_TABLE = """
CREATE TABLE IF NOT EXISTS levels (
    level_id INT(10) AUTO_INCREMENT PRIMARY KEY,
    level_name VARCHAR(50) NOT NULL UNIQUE
);
"""


CREATE_SENIOR_HIGH_SCHOOL_TABLE = """
CREATE TABLE IF NOT EXISTS senior_high_schools (
    school_id INT(10) AUTO_INCREMENT PRIMARY KEY,
    school_name VARCHAR(255),
    location VARCHAR(50)
);
"""

CREATE_COLLEGE_TABLE = """
CREATE TABLE IF NOT EXISTS colleges (
    school_id INT(10) AUTO_INCREMENT PRIMARY KEY,
    school_name VARCHAR(255),
    location VARCHAR(50)
);
"""

CREATE_ELEMENTARY_TABLE = """
CREATE TABLE IF NOT EXISTS elementary (
    school_id INT(10) AUTO_INCREMENT PRIMARY KEY,
    school_name VARCHAR(255),
    location VARCHAR(50)
);
"""

CREATE_KINDER_TABLE = """
CREATE TABLE IF NOT EXISTS kinder (
    school_id INT(10) AUTO_INCREMENT PRIMARY KEY,
    school_name VARCHAR(255),
    location VARCHAR(50)
);
"""

CREATE_HIGHSCHOOL_TABLE = """
CREATE TABLE IF NOT EXISTS junior_high_schools (
    school_id INT(10) AUTO_INCREMENT PRIMARY KEY,
    school_name VARCHAR(255),
    location VARCHAR(50)
);
"""

# ? Tracks and Courses Tables =============================================================================

CREATE_TRACKS_TABLE = """
CREATE TABLE IF NOT EXISTS tracks (
    track_id INT(10) AUTO_INCREMENT PRIMARY KEY,
    track_name VARCHAR(50) NOT NULL
);
"""

CREATE_TABLE_SENIOR_TRACKS = """
CREATE TABLE IF NOT EXISTS connected_tracks (
    school_id INT(10),
    track_id INT(10),
    PRIMARY KEY (school_id, track_id),
    FOREIGN KEY (school_id) REFERENCES senior_high_schools(school_id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE
);
"""

CREATE_COURSE_TABLE = """
CREATE TABLE IF NOT EXISTS courses (
    course_id INT(10) AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL
);
"""

CREATE_TABLE_COLLEGE_COURSES = """
CREATE TABLE IF NOT EXISTS connected_courses (
    school_id INT(10),
    course_id INT(10),
    PRIMARY KEY (school_id, course_id),
    FOREIGN KEY (school_id) REFERENCES colleges(school_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);
"""

# ? Insert Queries =========================================================================================

# ? Locations

INSERT_BARANGAY="INSERT INTO barangay (brgy_code, brgy_name, city_code) VALUES (%s, %s, %s)"

INSERT_PROVINCE="INSERT INTO province (province_code, province_name, region_code) VALUES (%s, %s, %s)"

INSERT_CITY="INSERT INTO city (city_code, city_name, province_code) VALUES (%s, %s, %s)"

INSERT_REGION="INSERT INTO region (region_code, region_name) VALUES (%s, %s)"

# ? Schools

INSERT_LEVELS="INSERT INTO levels (level_name) VALUES (%s)"

INSERT_SENIOR_HIGH_SCHOOL="INSERT INTO senior_high_schools (school_name, location) VALUES (%s, %s)"

INSERT_COLLEGE="INSERT INTO colleges (school_name, location) VALUES (%s, %s)"

INSERT_KINDER="INSERT INTO kinder (school_name, location) VALUES (%s, %s)"

INSERT_ELEMENTARY="INSERT INTO elementary (school_name, location) VALUES (%s, %s)"

INSERT_JUNIOR_HIGH_SCHOOL="INSERT INTO junior_high_schools (school_name, location) VALUES (%s, %s)"

# ? Tracks and Courses

INSERT_TRACK="INSERT INTO tracks (track_name) VALUES (%s)"

INSERT_COURSE ="INSERT INTO courses (course_name) VALUES (%s)"

CONVERT_CONNECTED_COURSES = [
    "SELECT school_id FROM colleges WHERE school_name = %s",
    "SELECT course_id FROM courses WHERE course_name = %s"
]

CONVERT_CONNECTED_TRACKS = [
    "SELECT school_id FROM senior_high_schools WHERE school_name = %s",
    "SELECT track_id FROM tracks WHERE track_name = %s"
]


INSERT_CONNECTED_COURSES="INSERT INTO connected_courses (school_id, course_id) VALUES (%s, %s)"

INSERT_CONNECTED_TRACKS="INSERT INTO connected_tracks (school_id, track_id) VALUES (%s, %s)"

# ? Select Queries =========================================================================================

"""
SELECT co.school_name, cr.course_name 
FROM connected_courses cc
JOIN colleges co ON cc.school_id = co.school_id
JOIN courses cr ON cc.course_id = cr.course_id;
"""

"""
SELECT sh.school_name, tr.track_name 
FROM connected_tracks ct
JOIN senior_high_schools sh ON ct.school_id = sh.school_id
JOIN tracks tr ON ct.track_id = tr.track_id;
"""

"""
SELECT sh.school_name, tr.track_name 
FROM connected_tracks ct
JOIN senior_high_schools sh ON ct.school_id = sh.school_id
JOIN tracks tr ON ct.track_id = tr.track_id
WHERE tr.track_name = 'GAS';
"""

