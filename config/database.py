from source.database.database import University
import json

with open("data\\variables.json", "r") as f:
    var = json.load(f)
    
def university():
    # pass
    global university
    university = University() # db creation
    university.create_table("Login", "username TEXT PRIMARY KEY", "password TEXT") # login table creation
    university.create_table("Students", "student_id INTEGER PRIMARY KEY","username TEXT", "first_name TEXT", "last_name TEXT", "father_name TEXT", "avrage FLOAT", "nation_code CHAR(10)", "field TEXT", "units_needed INTEGER") # Student table creation
    university.create_table("Courses", "student_id", "course_id INTEGER PRIMARY KEY", "course_name TEXT", "numbers INTEGER", "type TEXT") # Course table creation
    university.create_table("Schedule", "course_id INTEGER PRIMARY KEY", "teacher_id INTEGER", "capacity INTEGER") # Schedule table creation
    university.create_table("CurriculumVitaa", "student_id INTEGER", "course_id INTEGER PRIMARY KEY", "course_name TEXT", "units INTEGER") # CurriculumVitae table creation
    university.create_table("TakeCourses", "student_id INTEGER PRIMARY KEY", "entered_time DATETIME", "date DATETIME") # TakeCourses table creation
    university.close_connection() # db closing
    
    # complete database
    university.open_connection()
    university.insert_into_table("Login", 'admin', '12345678')
    university.insert_into_table("Students", 101, "admin", "علی", "قاسمی", "مجید", 3.5, "1131239825", "math", 10)
    university.insert_into_table('Courses', 101, 1, "math", 3, "main")
    university.insert_into_table('Courses', 101, 2, "physics", 2, "main")
    university.insert_into_table('Courses', 101, 3, "sport", 1, "valentiary")
    university.insert_into_table('Schedule', 1, 5, 30)
    university.insert_into_table('Schedule', 2, 6, 22)
    university.insert_into_table('Schedule', 3, 3, 10)
    university.insert_into_table('TakeCourses', 101, "1400-07-01", "1403-5-6 20:00:00")
    
def connect():
    university.open_connection()
    