import json
import time
import sqlite3
import PIL.Image as Imageee
from datetime import date, datetime
from khayyam import JalaliDate, JalaliDatetime, TehranTimezone
from tkinter import *
from config import takecourse

# from config.database import University
# from tkinter.ttk import *

with open("data\\variables.json", "r") as f:
    var = json.load(f)

class Dashboard(Tk):
    def __init__(self, database="data\\university.db"):
        super().__init__()
        self.database = database
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        print('Dashboard is created')
        
    def size(self, width, height):
        self.width = width
        self.height = height
        self.geometry(f"{self.width}x{self.height}")
        
    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
    def hide_window(self):
        self.withdraw()
        print('Dashboard is hidden now')
        
    def show_window(self):
        self.deiconify()
        print("Dashboard is shpwn now")
        
    def display_time(self):
        lbl = Label(self.heading, font=('Arial', 20), background='#f0f0f0', foreground='black')
        lbl.place(x=0, y=0)
        
        local_time_list = list(time.localtime())
        self.local_time_list_key = ['year', 'month', 'day', 'hour', 'min', 'sec']
        localtime_dic = dict(zip(self.local_time_list_key, local_time_list))
        self.localtime = JalaliDatetime(datetime(localtime_dic['year'], localtime_dic['month'], localtime_dic['day'], localtime_dic['hour'], localtime_dic['min'], localtime_dic['sec']), TehranTimezone).strftime('%Y/%m/%d  %H:%M:%S')
        lbl.config(text=self.localtime)
        lbl.after(1000, self.display_time)
    
    def display_university_name(self, university_name):
        lbl = Label(self.heading, text=university_name, font=('Arial', 20, 'bold'), background='#f0f0f0', foreground='black')
        lbl.place(x=720, y=0)
        
    def header(self):
        self.heading = Frame(self, width=1000, height=39, bg='#f0f0f0')
        self.heading.place(x=0, y=0)
        
        self.display_time()
        self.display_university_name("سامانه دانشگاهی")
        
    def profile(self):
        img = Imageee.open('images\\profile.png')
        profile_resized = img.resize((200, 200))
        profile_resized.save('images\\profile_resized.png')
        self.profile = PhotoImage(file='images\\profile_resized.png')
        Label(self.information, image=self.profile, border=0, bg='white').place(x=110, y=80)
        
    def name(self):
        with self.conn:
            self.cur.execute("SELECT first_name, last_name FROM Students WHERE username =?", (var['username'],))
            result = self.cur.fetchone()
            self.name = Label(self.information, text=f'{result[0]} {result[1]}', font=('Arial', 20, 'bold'), background='#f0f0f0', foreground='red')
            self.name.place(x=600, y=80)
        
    def student_id(self):
        with self.conn:
            self.cur.execute("SELECT student_id FROM Students WHERE username =?", (var['username'],))
            result = self.cur.fetchone()
            self.id = result
            self.student_id = Label(self.information, text=f'شماره دانشجویی :    {result[0]}', font=('Arial', 20, 'bold'), background='#f0f0f0', foreground='black')
            self.student_id.place(x=575, y=130)
        
    def avrage(self):
        with self.conn:
            self.cur.execute("SELECT avrage FROM Students WHERE username =?", (var['username'],))
            result = self.cur.fetchone()
            self.average = Label(self.information, text=f'معدل :    {result[0]}', font=('Arial', 20, 'bold'), background='#f0f0f0', foreground='black')
            self.average.place(x=575, y=180)
        
    def units(self):
        with self.conn:
            self.cur.execute("SELECT units_needed FROM Students WHERE username =?", (var['username'],))
            result = self.cur.fetchone()
            self.units = Label(self.information, text=f'تعداد واحد مجاز :    {result[0]}', font=('Arial', 20, 'bold'), background='#f0f0f0', foreground='black')
            self.units.place(x=575, y=230)
            
        # self.units = Label(self.information, text=f'تعداد واحد مجاز :    18', font=('Arial', 20, 'bold'), background='#f0f0f0', foreground='black')
        # self.units.place(x=575, y=230)
        
    def take_course_window(self):
        self.hide_window()
        takecourse.take_course()
        # self.take_course_window = Toplevel(self)
        # self.take_course_window.title('انتخاب واحد')
        # self.take_course_window.geometry('300x300')
        # self.take_course_window.resizable(False, False)
        # self.take_course_window.iconbitmap('images\\icon.ico')
        # self.take_course_window.config(bg='#f0f0f0')
        # self.take_course_window.protocol("WM_DELETE_WINDOW", self.take_course_window.withdraw)

        # self.take_course_window_label = Label(self.take_course_window, text='انتخاب واحد', font=('Arial', 15, 'bold'), background='#f0f0f0', foreground='black')
        # self.take_course_window_label.place(x=100, y=20)

        # self.take_course_window_listbox = Listbox(self.take_course_window, selectmode='single', font=('Arial', 15, 'bold'), bg='#f0f0f0', fg='black')
        
    def take_course_button(self):
        with self.conn:
            result = self.cur.execute("SELECT date FROM TakeCourses WHERE student_id =?", (self.id[0],))
            result = self.cur.fetchone()
            take_course_date = result[0]
            
        date_time = datetime.strptime(self.localtime, "%Y/%m/%d  %H:%M:%S")
        take_course_date_time= datetime.strptime(take_course_date, "%Y-%m-%d %H:%M:%S")

        if date_time > take_course_date_time:
            self.take_course = Button(self.information, text='انتخاب واحد', width=30, font=('Arial', 13, 'bold'), height=2, bg='green',cursor='hand2', fg='white', border=0, pady=2, command=self.take_course_window)
            self.take_course.place(x=300, y=320)

        else:
            self.take_course = Button(self.information, text='انتخاب واحد', width=30, font=('Arial', 13, 'bold'), height=2, bg='#57a1f8',cursor='hand2', fg='white', border=0, pady=2, state='disabled')
            self.take_course.place(x=300, y=320)
        
    def information(self):
        self.information = Frame(self, width=1000, height=500, bg='#f0f0f0')
        self.information.place(x=0, y=39)
        
        self.name()
        self.profile()
        self.student_id()
        self.avrage()
        self.units()
        self.take_course_button()