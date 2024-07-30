from tkinter import *
import sqlite3
from PIL import Image, ImageTk
from config import dashboard
from tkinter import messagebox
import json

with open("data\\variables.json", "r") as f:
    var = json.load(f)

class TakeCourse(Toplevel):
    def __init__(self, database="data\\university.db"):
        super().__init__()
        self.database = database
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        print('TakeCourse is created')

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
        
    def background(self, source):
        self.img = ImageTk.PhotoImage(Image.open(source))
        Label(self, image=self.img, border=0, bg='white').place(x=50, y=60)
        
    def clear_course_id(self, event):
        if self.course_id.get() == 'Course Code':
            self.course_id.delete(0, END)
            
    def fill_course_id(self, event):
        if self.course_id.get() == '':
            self.course_id.insert(0, 'Course Code')
        
    def courseId(self):
        self.course_id = Entry(self.frame, width=25, fg='black', border=0, bg='white', font=('Arial', 11))
        self.course_id.place(x=50, y=80)
        self.course_id.insert(0, 'Course Code')
        Frame(self.frame, width=150, height=2, bg='black').place(x=25, y=107)
        self.course_id.bind('<FocusIn>', self.clear_course_id)
        self.course_id.bind('<FocusOut>', self.fill_course_id)
        
    def clear_course_name(self, event):
        if self.course_name.get() == 'Course Name':
            self.course_name.delete(0, END)
            
    def fill_course_name(self, event):
        if self.course_name.get() == '':
            self.course_name.insert(0, 'Course Name')
        
    def courseName(self):
        self.course_name = Entry(self.frame, width=25, fg='black', border=0, bg='white', font=('Arial', 11))
        self.course_name.place(x=50, y=150)
        self.course_name.insert(0, 'Course Name')
        Frame(self.frame, width=150, height=2, bg='black').place(x=25, y=177)
        self.course_name.bind('<FocusIn>', self.clear_course_name)
        self.course_name.bind('<FocusOut>', self.fill_course_name)
        
    def clear_units(self, event):
        if self.units.get() == 'Units':
            self.units.delete(0, END)
            
    def fill_units(self, event):
        if self.units.get() == '':
            self.units.insert(0, 'Units')
        
    def units(self):
        self.units = Entry(self.frame, width=25, fg='black', border=0, bg='white', font=('Arial', 11))
        self.units.place(x=255, y=115)
        self.units.insert(0, 'Units')
        Frame(self.frame, width=150, height=2, bg='black').place(x=215, y=142)
        self.units.bind('<FocusIn>', self.clear_units)
        self.units.bind('<FocusOut>', self.fill_units)

    def add(self):
        self.course_id_get = self.course_id.get()
        self.course_name_get = self.course_name.get()
        self.units_get = self.units.get()
        with self.conn:
            self.cur.execute("SELECT student_id FROM Students WHERE username =?", (var['username'],))
            result = self.cur.fetchone()
            self.id = int(result[0])
            
            self.cur.execute("SELECT course_id, course_name, numbers FROM Courses WHERE course_id=?", (self.course_id_get,))
            self.result = self.cur.fetchone()
            
            self.cur.execute("SELECT units_needed from Students WHERE student_id=?", (self.id,))
            units_needed = self.cur.fetchone()[0]
            
        if self.result != None:
            if self.result[1] == self.course_name_get:
                try:
                    self.units_get = int(self.units_get)
                    if self.units_get > 0:
                        if self.units_get <= self.result[2]:
                            if units_needed >= self.units_get:
                                try:
                                    with self.conn:
                                        self.cur.execute("INSERT INTO CurriculumVitaa (student_id, course_id, course_name, units) VALUES (?,?,?,?)", (self.id, self.course_id_get, self.course_name_get, self.units_get))
                                        self.conn.commit()
                                        
                                        new_course_numbers = self.result[2] - self.units_get
                                        self.cur.execute("UPDATE Courses SET numbers=? WHERE course_id=?", (new_course_numbers, self.course_id_get))
                                        self.conn.commit()
                                        
                                        new_student_units = units_needed - self.units_get   
                                        self.cur.execute("UPDATE Students SET units_needed=? WHERE student_id=?", (new_student_units, self.id))
                                        self.conn.commit()
                                        
                                        messagebox.showinfo('Success', 'Course Added Successfully')
                                        self.course_id.delete(0, END)
                                        self.course_name.delete(0, END)
                                        self.units.delete(0, END)
                                        self.course_id.insert(0, 'Course Code')
                                        self.course_name.insert(0, 'Course Name')
                                        self.units.insert(0, 'Units')
                                        self.course_id.focus()
                                        
                                except sqlite3.IntegrityError:
                                    new_course_numbers = self.result[2] - self.units_get
                                    self.cur.execute("UPDATE Courses SET numbers=? WHERE course_id=?", (new_course_numbers, self.course_id_get))
                                    self.conn.commit()
                                    messagebox.showinfo('Success', 'Course Added Successfully')
                                    self.course_id.delete(0, END)
                                    self.course_name.delete(0, END)
                                    self.units.delete(0, END)
                                    self.course_id.insert(0, 'Course Code')
                                    self.course_name.insert(0, 'Course Name')
                                    self.units.insert(0, 'Units')
                                    self.course_id.focus()
                            else:
                                messagebox.showerror("Error", "Units are enough")
                                
                        else:
                            messagebox.showinfo('Error', 'Units Exceeded')
                            
                    else:
                        messagebox.showinfo('Error', 'Units Must Be Positive')
        
                except ValueError:
                    messagebox.showinfo('Error', 'Units Must Be Number')
                    
            else:
                messagebox.showerror('Error', 'Course Name Does Not Match')
                
        else:
            messagebox.showerror('Error', 'Course Not Found')
      
    def add_button(self):
        self.add_btn = Button(self.frame, text='Add', width=15, height=1, bg='green',cursor='hand2', fg='white', border=0, pady=7, font=('Arial' , 11, 'bold'), command=self.add)
        self.add_btn.place(x=30, y=234)
        
    def destroy(self):
        self.conn.close()
        super().destroy()
        dashboard.close()
        
    def exit_button(self):
        self.exit_btn = Button(self.frame, text='Exit', width=11, height=1, bg='red', cursor='hand2', fg='white', pady=7, border=0, font=('Arial' , 11, 'bold'), command=self.destroy)
        self.exit_btn.place(x=235, y=234)
        
    def heading(self):
        self.head = Label(self.frame, text='Take Course', fg="blue", font=('Arial', 23, 'bold'), bg='white')
        self.head.place(x=90, y=5)
    
    def create_frame(self):
        self.frame = Frame(self, width=350, height=350, bg='white')
        self.frame.place(x=480, y=70)
        # Add login form elements to the frame
        self.heading()
        self.courseId()
        self.courseName()
        self.units()
        self.add_button()
        self.exit_button()
        
    