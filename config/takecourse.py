from source.interface.takecourse import TakeCourse
from tkinter import *

def take_course():
    take_course = TakeCourse()
    take_course.title("Take Course")
    take_course.resizable(False, False)
    take_course.size(925, 500)
    take_course.configure(bg='white')
    take_course.center_window()
    take_course.background('images\\education.png')
    take_course.create_frame()